from typing import TypedDict, Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    # annotating the messages with `operator.add`,
    # e.g. "we can only append messages to the state"
    messages: Annotated[Sequence[BaseMessage], operator.add]
