import sys
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Adiciona o diretório do backend ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importações locais
from algoritmo import main as algoritmo_main
from utils import valida_coordenadas
from algoritmo import (  # Importe todas as variáveis globais que você usa
    mapa, 
    inicio, 
    final, 
    dicPosicoesCalculadas, 
    listaAberta, 
    listaFechada
)

app = FastAPI()

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CoordenadasRequest(BaseModel):
    inicio: tuple[int, int]
    final: tuple[int, int]

@app.post("/executar")
async def executar_algoritmo(request: CoordenadasRequest):
    try:
        # Valida as coordenadas
        if not valida_coordenadas(request.inicio, request.final, mapa):
            raise HTTPException(status_code=400, detail="Coordenadas inválidas")
        
        # Limpa variáveis globais para nova execução
        global inicio, final, dicPosicoesCalculadas, listaAberta, listaFechada
        inicio = request.inicio
        final = request.final
        dicPosicoesCalculadas = {}
        listaAberta = []
        listaFechada = []
        
        # Executa o algoritmo
        resultado = algoritmo_main()
        
        return {
            "mapa": mapa,
            "caminho": resultado,
            "inicio": inicio,
            "final": final
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/mapa")
async def obter_mapa():
    return {
        "mapa": mapa,
        "dimensoes": {
            "linhas": len(mapa),
            "colunas": len(mapa[0]) if mapa else 0
        }
    }