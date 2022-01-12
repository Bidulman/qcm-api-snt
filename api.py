from fastapi import FastAPI

import config
import models

app = FastAPI()


@app.get('/', response_model=models.ApiInfo)
async def get_index():
    return {'host': config.HOST, 'port': config.PORT}
