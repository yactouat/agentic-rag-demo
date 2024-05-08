import json
from langchain.output_parsers.openai_tools import PydanticToolsParser
from langchain_core.messages import FunctionMessage
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.utils.function_calling import convert_to_openai_tool
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolInvocation
from langchain.prompts import PromptTemplate

from chains import rag_chain
from state import AgentState
from tools import model_with_tools, tool_executor


def call_model(state: AgentState):
    messages = state["messages"]
    response = model_with_tools.invoke(messages)
    # because we've annotated the messages with `operator.add`,
    # the response will be appended to the messages (our state object)
    return {"messages": [response]}


def call_initial_rag_chain(state: AgentState):
    q = {"question": state["messages"][-1].content}
    res = rag_chain.invoke(q)
    return {"messages": [res["response"]]}


def call_tool(state: AgentState):
    last_message = state["messages"][-1]

    action = ToolInvocation(
        tool=last_message.additional_kwargs["function_call"]["name"],
        tool_input=json.loads(
            last_message.additional_kwargs["function_call"]["arguments"]
        )
    )

    response = tool_executor.invoke(action)

    function_message = FunctionMessage(content=str(response), name=action.tool)

    return {"messages": [function_message]}


def fully_answers_question(state: AgentState):
    initial_question = state["messages"][0].content
    initial_answer = state["messages"][1].content

    class Answered(BaseModel):
        binary_score: str = Field(description="Fully answered: 'yes' or 'no'")

    # create a tool out of the `Answered` class
    answered_tool = convert_to_openai_tool(Answered)
    # using a more powerful model to ensure that the question is answered properly
    verifier_model = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0)
    verifier_model = verifier_model.bind(
        tools=[answered_tool],
        tool_choice={
            "type": "function",
            "function": {
                "name": "Answered",
            }
        }
    )
    # parser to extract the binary score into a usable format
    fully_answered_parser = PydanticToolsParser(tools=[Answered])

    fully_answered_prompt = PromptTemplate(
        template="""You will determine if the provided question is fully answered by the provided answer.\n
Question:
{question}

Answer:
{answer}

You will respond with exactly either 'yes' or 'no'.""",
        input_variables=["question", "answer"]
    )

    fully_answered_chain = fully_answered_prompt | verifier_model | fully_answered_parser

    fully_answered_res = fully_answered_chain.invoke(
        {"question": initial_question, "answer": initial_answer}
    )

    if fully_answered_res[0].binary_score == "yes":
        return "end"

    return "continue"


# this basically says that if we don't need to call a tool, we should end the conversation and output the response
def should_continue(state):
    last_message = state["messages"][-1]

    if "function_call" not in last_message.additional_kwargs:
        return "end"

    return "continue"


# let's start building our graph
workflow = StateGraph(AgentState)

# the initial RAG fetch checks if in the current data, we have something that answers the user's question
workflow.add_node("initial_rag_call", call_initial_rag_chain)
workflow.add_node("agent", call_model)
workflow.add_node("tool", call_tool)
# final edge to end the conversation
workflow.add_edge("tool", "agent")
# check if the question is fully answered on initial interaction
workflow.add_conditional_edges(
    "initial_rag_call",
    fully_answers_question,
    {
        "continue": "agent",
        "end": END
    }
)
# decide to call an external tool or output an answer with a conditional edge
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "tool",
        "end": END
    }
)
workflow.set_entry_point("initial_rag_call")

graph_app = workflow.compile()
