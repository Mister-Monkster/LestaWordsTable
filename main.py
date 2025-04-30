import uvicorn
from fastapi import FastAPI
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from routers.router import router as file

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(file)


@app.get("/")
async def redirect():
    return RedirectResponse(url="/file/download")


if __name__ == '__main__':
    uvicorn.run(app,
                host="127.0.0.1",
                port=8000)