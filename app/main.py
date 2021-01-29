import uvicorn
from fastapi import FastAPI
from health.external_interface.routers import router as health_routers

app = FastAPI()
app.include_router(health_routers)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
