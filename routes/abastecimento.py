import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def abastecimento(page: ft.Page, navigate_to, header):
    matricula = user_info.get("matricula")
    codfilial = user_info.get("codfilial")
    print(f"User config na tela Abastecimento: {matricula}")

    def buscar_os(numos):
        print(f"Buscar OS: {numos}")

    titulo = ft.Text(
        "Abastecimento",
        size=24, weight="bold",
        color=colorVariaveis['titulo']
    )
    input_numos = ft.TextField(
        label="Número OS",
        width=300,
        on_submit=lambda e: buscar_os(e.control.value)
    )
    button_buscar = ft.ElevatedButton(
        "Buscar OS",
        on_click=lambda e: buscar_os(input_numos.value)
    )
    button_buscar_automatixa = ft.ElevatedButton(
        "Buscar OS (Automático)",
        on_click=lambda e: buscar_os(input_numos.value)
    )
    # Retorna a view configurada
    return ft.View(
        route="/abastecimento",  # Define a rota da página
        controls=[header,
                titulo,
                input_numos,
                button_buscar,
                ft.Divider(),
                button_buscar_automatixa
        ]
    )