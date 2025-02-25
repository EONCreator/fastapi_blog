import uvicorn
from fastapi import FastAPI
import typer
import asyncio

from fastapi.openapi.utils import get_openapi

from database.database import init_models, create_database_if_not_exists
from api.routers.routers import all_routers

app = FastAPI(
    swagger_ui_parameters={"syntaxHighlight": False},
    title="Blog API"
)

for router in all_routers:
    app.include_router(router)


@app.on_event("startup")
async def startup_event():
    print("Initializing database...")
    await create_database_if_not_exists()
    await init_models()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Blog API",
        version="0.0.1",
        description="API for Blog",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
