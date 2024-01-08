from typing import Optional
from fastapi import FastAPI, Request, Header
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# set fastapi route
@app.get('/index/', response_class=HTMLResponse)
def index(request: Request, hx_request: Optional[str] = Header(None)):
    animes = [{'name': 'Jujutsu kaisen', 'studio': 'MAPPA', 'writer': 'Gege Akutami'},
              {'name': 'Demon slayer', 'studio': 'Ufotable', 'writer': 'Koyoharu Gotōge'},
              {'name': 'Attack on Titan', 'studio': 'Wit Studio', 'writer': 'Hiroyuki Sawano'},
              {'name': 'Solo leveling', 'studio': 'A-1 Pictures', 'writer': 'Chugong'}, 
         
    ]
    context = {'request': request, 'animes': animes}
    if hx_request:
        return templates.TemplateResponse("table.html", context)
    return templates.TemplateResponse("index.html", context)


