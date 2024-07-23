from fastapi import FastAPI

from router import router

from database import engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(router)

@app.get('/')
def root():
    return {'message': 'Hello, world!'}