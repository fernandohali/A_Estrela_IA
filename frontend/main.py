from reactpy import component, html, hooks, run
import aiohttp
from reactpy.backend.fastapi import configure
from fastapi import FastAPI

from components.input_form import InputForm
from components.mapa_display import MapaDisplay

frontend_app = FastAPI()

@component
def App():
    mapa, set_mapa = hooks.use_state([])
    resultado, set_resultado = hooks.use_state(None)
    loading, set_loading = hooks.use_state(False)
    error, set_error = hooks.use_state(None)
    dimensoes, set_dimensoes = hooks.use_state({"linhas": 0, "colunas": 0})

    async def carregar_mapa():
        try:
            set_loading(True)
            async with aiohttp.ClientSession() as session:
                async with session.get("http://localhost:8000/mapa") as response:
                    if response.status == 200:
                        data = await response.json()
                        set_mapa(data["mapa"])
                        set_dimensoes(data["dimensoes"])
                    else:
                        set_error("Erro ao carregar o mapa")
        except Exception as e:
            set_error(f"Erro de conexão: {str(e)}")
        finally:
            set_loading(False)

    hooks.use_effect(carregar_mapa, [])

    async def executar_algoritmo(inicio, final):
        try:
            set_loading(True)
            set_error(None)
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "http://localhost:8000/executar",
                    json={"inicio": [int(x) for x in inicio.split()], 
                         "final": [int(x) for x in final.split()]}
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        set_resultado(data)
                    else:
                        error_data = await response.json()
                        set_error(error_data.get("detail", "Erro ao executar o algoritmo"))
        except Exception as e:
            set_error(f"Erro de conexão: {str(e)}")
        finally:
            set_loading(False)

    if loading:
        return html.div({"class": "loading"}, "Processando...")
    
    if error:
        return html.div({"class": "error"}, f"Erro: {error}")

    return html.div(
        {"class": "container"},
        html.div(
            {"class": "header"},
            html.h1("Algoritmo A* - Visualização de Caminho")
        ),
        html.div(
            {"class": "content"},
            InputForm({
                "onSubmit": lambda e: (
                    e.preventDefault(),
                    executar_algoritmo(
                        e["target"]["elements"]["inicio"]["value"],
                        e["target"]["elements"]["final"]["value"]
                    )
                ),
                "dimensoes": dimensoes
            }),
            MapaDisplay({
                "mapa": mapa,
                "resultado": resultado,
                "dimensoes": dimensoes
            })
        )
    )

configure(frontend_app, App)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(frontend_app, host="0.0.0.0", port=3000)