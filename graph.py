from langgraph.prebuilt import ToolInvocation
import json
from langchain_core.messages import FunctionMessage
from langgraph.graph import StateGraph, END

from state import AgentState
from tools import model_with_tools, tool_executor


def call_model(state: AgentState):
    messages = state["messages"]
    response = model_with_tools.invoke(messages)
    # because we've annotated the messages with `operator.add`,
    # the response will be appended to the messages (our state object)
    return {"messages": [response]}


def call_tool(state):
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


# this basically says that if we don't need to call a tool, we should end the conversation and output the response
def should_continue(state):
    last_message = state["messages"][-1]

    if "function_call" not in last_message.additional_kwargs:
        return "end"

    return "continue"


# let's start building our graph
workflow = StateGraph(AgentState)

workflow.add_node("agent", call_model)
workflow.add_node("tool", call_tool)
workflow.set_entry_point("agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "tool",
        "end": END
    }
)
# we always want our tool to return to the agent
workflow.add_edge("tool", "agent")
graph_app = workflow.compile()
