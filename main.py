from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html

from src.api.routers.hotels import router as hotel_router
from src.api.routers.rooms import router as room_router
from src.api.routers.auth import router as auth_router

from src.core.exception.base import AppError
from src.api.erors_heandler import app_exception_handler

app = FastAPI(docs_url=None)

app.add_exception_handler(AppError, app_exception_handler)

app.include_router(hotel_router)
app.include_router(room_router)
app.include_router(auth_router)


@app.get("/docs", include_in_schema=False)
async def custom_swagger():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Swagger UI",
        swagger_js_url=("https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"),
        swagger_css_url=("https://unpkg.com/swagger-ui-dist@5/swagger-ui.css"),
    )
