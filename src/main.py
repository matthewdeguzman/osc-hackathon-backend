from fastapi import FastAPI
import uvicorn

from routes import login, clubs, events, posts

app = FastAPI()

app.include_router(login.router)
app.include_router(clubs.router)
app.include_router(events.router)
app.include_router(posts.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
