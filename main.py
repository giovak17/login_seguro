import hashlib
from typing import Annotated
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import starlette.status as status

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# CREDENCIALES
usuarioSecreto = "admin"
# El hash es "mypass" en MD5
hashSecreto = "a029d0df84eb5549c641e04a9ef389e5"

@app.post("/login/")
async def login(request: Request, usuario: Annotated[str, Form()], contrasena: Annotated[str, Form()]):
    contrasenaHash = hashlib.md5(contrasena.encode()).hexdigest()

    if (contrasenaHash == hashSecreto) and (usuario == usuarioSecreto):
        return templates.TemplateResponse(request=request, name="paginaSecreta.html", context={"usuario": usuario, "contrasena": contrasena, "hash": contrasenaHash})

    return RedirectResponse("/?error=Credenciales incorrectas", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/")
async def root(request: Request, error: str =""):
    return templates.TemplateResponse(request=request, name="index.html", context={"error":error})