from fastapi import FastAPI
import uvicorn

import models
from routes import login

app = FastAPI()

app.include_router(login.router)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
