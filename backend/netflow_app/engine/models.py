from pydantic import BaseModel
from typing import List, Optional

class Node(BaseModel):
    id: str
    type: Optional[str] = None

class Arc(BaseModel):
    id: str
    source: str
    target: str

class Network(BaseModel):
    nodes: List[Node]
    arcs: List[Arc]
