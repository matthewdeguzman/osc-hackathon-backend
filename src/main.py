from fastapi import FastAPI
import uvicorn

from routes import login, clubs, events

app = FastAPI()

app.include_router(login.router)
app.include_router(clubs.router)
app.include_router(events.router)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
