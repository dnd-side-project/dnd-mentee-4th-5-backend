import uvicorn
from fastapi import FastAPI

import auth.external_interface.routers
import drinks.external_interface.routers
import health.external_interface.routers
import reviews.external_interface.routers
import users.external_interface.routers
import wishes.external_interface.routers
from container import Container
from settings import Settings


def create_app() -> FastAPI:
    router_modules = [
        auth.external_interface.routers,
        health.external_interface.routers,
        users.external_interface.routers,
        reviews.external_interface.routers,
        wishes.external_interface.routers,
        drinks.external_interface.routers,
    ]

    container = Container()
    container.wire(modules=router_modules)
    container.settings.from_pydantic(Settings())

    db = container.db()
    db.create_database()

    app = FastAPI()
    app.container = container
    for router_module in router_modules:
        app.include_router(router_module.router)
    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
