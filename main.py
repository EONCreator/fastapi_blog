import uvicorn
from fastapi import FastAPI
import typer
import asyncio

from database.database import init_models
from api.routers.routers import all_routers

cli = typer.Typer()

@cli.command()
def db_init_models():
    asyncio.run(init_models())
    print("Done")
    

app = FastAPI(
    title="API Блога"
)

for router in all_routers:
    app.include_router(router)

if __name__ == "__main__":
    cli()
    uvicorn.run(app, host="0.0.0.0", port=8000)
