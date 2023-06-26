from fastapi import FastAPI

from api import car_router, reservation_router

app = FastAPI()

app.include_router(car_router)
app.include_router(reservation_router)
