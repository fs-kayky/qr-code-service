from fastapi import FastAPI, APIRouter
from qr_generator.router import router as qr_generator_router
app = FastAPI()
router = APIRouter()

app.include_router(qr_generator_router)