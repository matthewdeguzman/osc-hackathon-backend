from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import uvicorn

from dotenv import load_dotenv

import os

from routes import login, clubs, events, posts

load_dotenv()

origins = ['http://localhost:3000', 'https://sp2ruehlafolifav2halxigicm0dajqn.lambda-url.us-east-1.on.aws']

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(login.router)
app.include_router(clubs.router)
app.include_router(events.router)
app.include_router(posts.router)

lambda_handler = Mangum(app)

if __name__ == '__main__':
    if os.getenv('RUN_LAMBDA', False) is False:
        uvicorn.run(app, host='0.0.0.0', port=8000)
