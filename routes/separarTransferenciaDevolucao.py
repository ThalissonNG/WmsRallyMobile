import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def separar_transferencia_devolucao(e, navigate_to, header):
    title = ft.Text(
        "Separar Transferência/Devolução",
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