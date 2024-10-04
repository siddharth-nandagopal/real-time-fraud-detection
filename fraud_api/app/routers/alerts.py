from fastapi import APIRouter
from starlette.requests import Request

from app.controllers.AlertController import AlertController as controller

router = APIRouter()


@router.get("", tags=["alerts"])
async def action(request: Request):
    return await controller.index(request)
