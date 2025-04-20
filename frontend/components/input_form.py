from reactpy import component, html

@component
def InputForm(props):
    return html.div(
        {"class": "control-panel"},
        html.h2("Configuração do Caminho"),
        html.form(
            {"onSubmit": props["onSubmit"]},
            html.div(
                {"class": "form-group"},
                html.label({"for": "inicio"}, "Ponto Inicial (linha coluna):"),
                html.input({
                    "type": "text",
                    "id": "inicio",
                    "placeholder": "Ex: 0 0",
                    "pattern": r"\d+ \d+",
                    "required": True,
                    "title": "Digite duas coordenadas separadas por espaço"
                })
            ),
            html.div(
                {"class": "form-group"},
                html.label({"for": "final"}, "Ponto Final (linha coluna):"),
                html.input({
                    "type": "text",
                    "id": "final",
                    "placeholder": "Ex: 9 9",
                    "pattern": r"\d+ \d+",
                    "required": True,
                    "title": "Digite duas coordenadas separadas por espaço"
                })
            ),
            html.button(
                {"type": "submit", "class": "submit-button"},
                "Calcular Caminho"
            ),
            html.p(
                {"class": "map-info"},
                f"Tamanho do Mapa: {props['dimensoes']['linhas']} linhas × {props['dimensoes']['colunas']} colunas"
            )
        )
    )