import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def conferir_conbus(page, navigate_to, header):
    titulo = ft.Text(
        "Conferir Bonus",
        size=24, weight="bold",
        color=colorVariaveis['titulo']
    )

    return ft.View(
        route="/conferir_bonus",
        controls=[
            header,
            titulo,
        ]
    )