from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import StreamingResponse
from app.functions.generate_qr_code import generate_qr_code, generate_custom_qr_code
from io import BytesIO

router = APIRouter()


@router.get("/")
def say_hello():
    print("hello")
    return {"hello": "world"}


@router.get("/generate-qr")
def generate_qr(text: str = Query(..., min_length=1)):
    try:
        img_bytes = generate_qr_code(text)
        return StreamingResponse(BytesIO(img_bytes), media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/generate-custom-qr")
def generate_custom_qr(
        text: str = Query(..., min_length=1),
        logo: str = None,
        qr_color: str = Query('black', regex=r'^[a-zA-Z]+$'),
        bg_color: str = Query('white', regex=r'^[a-zA-Z]+$'),
        logo_size: int = Query(50, ge=10, le=200),
        version: int = Query(1, ge=1, le=40),  # Tamanho de 1 a 40
        error_correction: str = Query('L', regex=r'^[LMQH]$')
):
    try:
        img_bytes = generate_custom_qr_code(
            text=text,
            logo_path=logo,
            qr_color=qr_color,
            bg_color=bg_color,
            logo_size=logo_size,
            version=version,
            error_correction=error_correction
        )
        return StreamingResponse(BytesIO(img_bytes), media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

