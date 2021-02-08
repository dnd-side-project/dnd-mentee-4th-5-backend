import auth.external_interface.routers
import health.external_interface.routers
import users.external_interface.routers
import uvicorn
from container import Container
from fastapi import FastAPI


def create_app():
    router_modules = [
        users.external_interface.routers,
        health.external_interface.routers,
        auth.external_interface.routers,
    ]
    container = Container()
    container.wire(modules=router_modules)

    app = FastAPI()
    app.container = container
    for router_module in router_modules:
        app.include_router(router_module.router)
    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
