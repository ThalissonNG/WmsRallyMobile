import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def separar_pedido(e, navigate_to, header):
    matricula = user_info.get('matricula')
    print(f"Matricual tela de separar pedidod {matricula}")
    title = ft.Text(
        "Separar pedido",
        size=24,
        weight="bold",
        color=colorVariaveis['titulo']
    )
    return ft.View(
        route="/separar_pedido",
        controls=[
            header,
            title,
        ]
    )