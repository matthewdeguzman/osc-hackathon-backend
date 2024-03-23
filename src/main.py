from fastapi import FastAPI
import uvicorn

import models
from routes import login, club, post

app = FastAPI()

app.include_router(login.router)
app.include_router(club.router)
app.include_router(post.router)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
