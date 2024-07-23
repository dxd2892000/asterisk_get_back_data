from sqlalchemy.orm import Session
from sqlalchemy import or_

import models as md
import schemas as sch

# Tạo một client mới
def create_client(db: Session, client: sch.ClientCreate): 
    # Tạo một client mới
    new_client = md.Client(
        name=client.name,
        server_id=client.server_id
    )
    
    # Thêm client mới vào session
    db.add(new_client)
    
    # Cập nhật server liên quan
    if client.server_id:
        server = db.query(md.Server).filter(md.Server.id == client.server_id).first()
        if server:
            server.clients.append(new_client)
        else:
            raise ValueError(f"Server with id {client.server_id} is not found")

    # Commit và refresh session
    db.commit()
    db.refresh(new_client)
    
    return new_client

def update_client(db: Session, client_id: int, client_data: sch.ClientCreate):
    # Tìm client dựa trên ID
    db_client = db.query(md.Client).filter(md.Client.id == client_id).first()
    
    if not db_client:
        raise ValueError("The client is not found")
    
    # Cập nhật thông tin client
    db_client.name = client_data.name
    
    # Kiểm tra và cập nhật server_id
    if client_data.server_id and db_client.server_id != client_data.server_id:
        # Xóa client khỏi danh sách clients của server cũ
        if db_client.server_id:
            old_server = db.query(md.Server).filter(md.Server.id == db_client.server_id).first()
            if old_server and db_client in old_server.clients:
                old_server.clients.remove(db_client)
        
        # Cập nhật server_id cho client
        db_client.server_id = client_data.server_id
        
        # Thêm client vào danh sách clients của server mới
        new_server = db.query(md.Server).filter(md.Server.id == client_data.server_id).first()
        if new_server:
            if db_client not in new_server.clients:
                new_server.clients.append(db_client)
        else:
            raise ValueError(f"Server with id {client_data.server_id} not found")
    
    # Commit và refresh session
    db.commit()
    db.refresh(db_client)
    
    return db_client

def get_client(db: Session, name: str):
    return db.query(md.Client).filter(md.Client.name == name).first()

def get_client_by_id(db: Session, id: int):
    return db.query(md.Client).filter(md.Client.id == id).first()

def create_server(db: Session, server: sch.ServerCreate):
    # Tạo một server mới
    db_server = md.Server(
        url=server.url,
        ip=server.ip,
        user=server.user
    )
    
    # Thêm server mới vào session
    db.add(db_server)
    
    # Commit và refresh session
    db.commit()
    db.refresh(db_server)
    
    return db_server
def update_server(db: Session, server_id: int, server_data: sch.ServerCreate):
    # Find server by ID
    db_server = db.query(md.Server).filter(md.Server.id == server_id).first()
    
    if not db_server:
        raise ValueError("The server is not found")
    
    # Update server info
    db_server.url = server_data.url
    db_server.ip = server_data.ip
    db_server.user = server_data.user

    # Commit and refresh session
    db.commit()
    db.refresh(db_server)
    
    return db_server

def get_server_all(db: Session):
    return db.query(md.Server).all()

def get_server_by_id(db: Session, id: int):
    return db.query(md.Server).filter(md.Server.id == id).first()

def get_server_from_client_by_name(db: Session, name: str):
    client = db.query(md.Client).filter(md.Client.name == name).first()
    if not client:
        raise ValueError("The client is not found")
    return client.server