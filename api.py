from fastapi import FastAPI

from database import DataBase

from config import config
import models
import routers

app = FastAPI()

database = DataBase()

app.include_router(routers.UsersRouter(config, database).router)


@app.get('/', response_model=models.ApiInfo)
async def get_index():
    return {'host': config["HOST"], 'port': config["PORT"]}
