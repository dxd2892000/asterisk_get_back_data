from fastapi import Depends, HTTPException, APIRouter, Form

from sqlalchemy.orm import Session

from database import SessionLocal

from cdr import Cdr

from typing import Any

import crud as crud
import schemas as sch


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/server/create', response_model=sch.Server)
def createServer(
    url: str = Form(...),
    ip: str = Form(...),
    user: str = Form(...),
    db: Session = Depends(get_db)
):
    server_create = sch.ServerCreate(url=url, ip=ip, user=user)
    db_server = crud.get_server_by_ip(db, ip=server_create.ip)
    if db_server:
        raise HTTPException(status_code=400, detail="Server already registered")
    return crud.create_server(db=db, server=server_create)

@router.put("/server/update", response_model=sch.Server)
def updateServer(
    id: int = Form(...), 
    url: str = Form(...),
    ip: str = Form(...),
    user: str = Form(...),
    db: Session = Depends(get_db)
):
    server_update = sch.ServerCreate(url=url, ip=ip, user=user)
    db_server = crud.get_server_by_id(db, id)
    if not db_server:
        raise HTTPException(status_code=400, detail="Server is not found")
    else:
        try:
            return crud.update_server(db, id, server_update)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

@router.get('/server/servers', response_model=list[sch.Server])
def getServerAll(db: Session = Depends(get_db)):
    return crud.get_server_all(db)

@router.post('/client/create', response_model=sch.Client)
def createClient(
    name: str = Form(...),
    server_id: str = Form(None),
    db: Session = Depends(get_db)
):
    client_create = sch.ClientCreate(name=name, server_id=server_id)
    db_client = crud.get_client(db, name=name)
    if db_client:
        raise HTTPException(status_code=400, detail="Client already registered")
    return crud.create_client(db=db, client=client_create)

@router.put('/client/update')
def updateClient(
    id: int = Form(...),
    name: str = Form(...),
    server_id = Form(...),
    db: Session = Depends(get_db)
):
    client_update = sch.ClientCreate(name=name, server_id=server_id)
    db_client = crud.get_client_by_id(db, id)
    if db_client:
        try:
            return crud.update_client(db, id, client_update)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
    else:
        raise HTTPException(status_code=400, detail="Client not found")

@router.post('/cdr/backup')
def getBackCdr(name: str = Form(...), startTime: Any = Form(...), endTime: Any = Form(...), db: Session = Depends(get_db)):
    server = crud.get_server_from_client_by_name(db, name)
    getCdr = Cdr(host=server.ip, user=server.user, password="1qazxsw2!@", dbname="asteriskcdrdb", name=name, url=server.url)

    return getCdr.process_call(startTime, endTime)