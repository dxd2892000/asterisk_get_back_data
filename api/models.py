from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Server(Base):
    __tablename__ = 'servers'

    id = Column(Integer, autoincrement=True, primary_key=True)
    url = Column(String(100), unique=True)
    ip = Column(String(100), unique=True)
    user = Column(String(100))

    # Thiết lập mối quan hệ với Client
    clients = relationship("Client", back_populates="server")

class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(100), unique=True)
    server_id = Column(Integer, ForeignKey('servers.id'), nullable=True)

    # Thiết lập mối quan hệ với Server
    server = relationship("Server", back_populates="clients")