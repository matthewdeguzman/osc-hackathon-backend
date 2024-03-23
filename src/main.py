from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from routes import login, clubs, events, posts
origins = [
        "http://localhost:3000",
        ]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login.router)
app.include_router(clubs.router)
app.include_router(events.router)
app.include_router(posts.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
