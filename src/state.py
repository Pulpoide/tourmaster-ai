from typing import TypedDict, Annotated, List, Union
import operator

class AgentState(TypedDict):
    messages: Annotated[List[dict], operator.add]
    next_node: str
    query: str
    answer: str
    expert_used: str