import uvicorn
from fastapi import FastAPI

from users.infra_structure.container import Container

import users.external_interface.routers
import users


router_modules = [users.external_interface.routers]
container = Container()
container.wire(modules=router_modules)

app = FastAPI()
app.container = container
for router_module in router_modules:
    app.include_router(router_module.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
