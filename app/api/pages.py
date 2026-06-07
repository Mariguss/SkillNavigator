from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

router = APIRouter(tags=["pages"])


@router.get("/", response_class=HTMLResponse)
async def page_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/login", response_class=HTMLResponse)
async def page_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/register", response_class=HTMLResponse)
async def page_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.get("/profile", response_class=HTMLResponse)
async def page_profile(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})


@router.get("/applications", response_class=HTMLResponse)
async def page_applications(request: Request):
    return templates.TemplateResponse("applications.html", {"request": request})


@router.get("/analytics", response_class=HTMLResponse)
async def page_analytics(request: Request):
    return templates.TemplateResponse("analytics.html", {"request": request})


@router.get("/admin", response_class=HTMLResponse)
async def page_admin(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})


@router.get("/matches", response_class=HTMLResponse)
async def page_matches(request: Request):
    return templates.TemplateResponse("matches.html", {"request": request})
