import flet as ft
import requests
import datetime
from routes.config.config import base_url, colorVariaveis, user_info

def contagem_inventario_rotativo(e, navigate_to, header):
    titulo = ft.Text(
        "Inventario Rotativo",
        size=24,
        weight="bold",
        color=colorVariaveis['titulo']
    )

    return ft.View(
        route="/contagem_inventario_rotativo",
        scroll= True,
        controls=[
            header,
            titulo
        ]
    )