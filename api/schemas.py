from pydantic import BaseModel
from typing import List, Optional

class ClientBase(BaseModel):
    name: str
    server_id: Optional[int] = None

class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    id: int

    class Config:
        from_attributes = True

class ServerBase(BaseModel):
    url: str
    ip: Optional[str] = None
    user: Optional[str] = None

class ServerCreate(ServerBase):
    pass

class Server(ServerBase):
    id: int
    clients: List[Client] = []

    class Config:
        from_attributes = True