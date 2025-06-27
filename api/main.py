from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite acesso de qualquer origem (ideal para Streamlit Cloud)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Candle(BaseModel):
    id: int
    value: float

@app.get("/velas", response_model=List[Candle])
def get_velas():
    candles = [{"id": i + 1, "value": round(1 + (i % 5) * 0.5, 2)} for i in range(20)]
    return candles
