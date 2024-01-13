from typing import Optional
from fastapi import FastAPI, Request, Header, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from . import models
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="sql_app/templates")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup_populate_db():
    db = SessionLocal()
    num_animes = db.query(models.Anime).count()
    if num_animes == 0:
        animes = [{'name': 'Jujutsu kaisen', 'studio': 'MAPPA', 'writer': 'Gege Akutami'},
              {'name': 'Demon slayer', 'studio': 'Ufotable', 'writer': 'Koyoharu Gotōge'},
              {'name': 'Attack on Titan', 'studio': 'Wit Studio', 'writer': 'Hiroyuki Sawano'},
              {'name': 'Solo leveling', 'studio': 'A-1 Pictures', 'writer': 'Chugong'},
                 ]
        for anime in animes:
            db.add(models.Anime(**anime))
        db.commit()
    else:
        print(f"number of animes is {num_animes}")



# set fastapi route
@app.get('/index/', response_class=HTMLResponse)
async def movieList(
    request: Request,
    hx_request: Optional[str] = Header(None),
    db: Session = Depends(get_db)):
    
    
    animes = db.query(models.Anime).all()
    context = {'request': request, 'animes': animes}
    if hx_request:
        return templates.TemplateResponse("partials/table.html", context)
    return templates.TemplateResponse("index.html", context)


