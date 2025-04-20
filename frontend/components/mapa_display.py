from reactpy import component, html

@component
def MapaDisplay(props):
    mapa = props["mapa"]
    resultado = props.get("resultado", None)
    dimensoes = props["dimensoes"]
    
    dados = resultado["caminho"] if resultado else mapa
    
    simbolos = {
        0: "",
        1: "■",
        "A": "A",
        "B": "B",
        "^": "↑",
        "v": "↓",
        "<": "←",
        ">": "→"
    }

    def get_cell_style(value):
        base_style = {
            "display": "flex",
            "alignItems": "center",
            "justifyContent": "center",
            "fontWeight": "bold",
            "fontSize": "14px",
            "border": "1px solid #eee",
            "boxSizing": "border-box",
            "width": "100%",
            "height": "100%",
        }
        
        if value == 1:
            base_style.update({
                "backgroundColor": "#34495e",
                "color": "white"
            })
        elif value == "A":
            base_style.update({
                "backgroundColor": "#2ecc71",
                "color": "white",
                "borderRadius": "50%"
            })
        elif value == "B":
            base_style.update({
                "backgroundColor": "#e74c3c",
                "color": "white",
                "borderRadius": "50%"
            })
        elif value in ["^", "v", "<", ">"]:
            base_style.update({
                "backgroundColor": "#3498db",
                "color": "white",
                "borderRadius": "4px"
            })
        else:
            base_style["backgroundColor"] = "#ecf0f1"
        
        return base_style

    grid_style = {
        "display": "grid",
        "gridTemplateRows": f"repeat({dimensoes['linhas']}, 1fr)",
        "gridTemplateColumns": f"repeat({dimensoes['colunas']}, 1fr)",
        "aspectRatio": "1 / 1",
        "maxWidth": "80vmin",
        "maxHeight": "80vmin",
        "width": "100%",
        "backgroundColor": "white",
        "border": "2px solid #ddd",
        "boxShadow": "0 2px 10px rgba(0,0,0,0.1)",
    }

    return html.div(
        {"class": "map-container"},
        html.h2("Visualização do Mapa"),
        html.div(
            {"class": "map-grid", "style": grid_style},
            [
                html.div(
                    {
                        "key": f"cell-{i}-{j}",
                        "style": get_cell_style(cell),
                        "class": "map-cell"
                    },
                    simbolos.get(cell, cell)
                )
                for i, row in enumerate(dados)
                for j, cell in enumerate(row)
            ]
        ),
        html.div(
            {"class": "legend"},
            html.h3("Legenda:"),
            html.div(
                {"class": "legend-item"},
                html.span({
                    "class": "legend-color",
                    "style": get_cell_style("A")
                }, "A"),
                html.span(" - Ponto Inicial")
            ),
            html.div(
                {"class": "legend-item"},
                html.span({
                    "class": "legend-color",
                    "style": get_cell_style("B")
                }, "B"),
                html.span(" - Ponto Final")
            ),
            html.div(
                {"class": "legend-item"},
                html.span({
                    "class": "legend-color",
                    "style": get_cell_style(1)
                }, "■"),
                html.span(" - Obstáculo")
            ),
            html.div(
                {"class": "legend-item"},
                html.span({
                    "class": "legend-color",
                    "style": get_cell_style("^")
                }, "↑"),
                html.span(" - Caminho percorrido")
            )
        )
    )
