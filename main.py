from fastapi import FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    print("Request for index page received")
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/favicon.ico")
async def favicon():
    file_path = "./static/favicon.ico"
    return FileResponse(
        path=file_path,
        headers={"mimetype": "image/vnd.microsoft.icon"},
    )


@app.post("/hello", response_class=HTMLResponse)
async def hello(request: Request, name: str = Form(...)):
    if name:
        print(f"Request for hello page received with name={name}")
        return templates.TemplateResponse(
            "hello.html",
            {"request": request, "name": name},
        )
    else:
        print("No name received — redirecting")
        return RedirectResponse(
            request.url_for("index"),
            status_code=status.HTTP_302_FOUND,
        )
