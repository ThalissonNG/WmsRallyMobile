import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def conferir_bonus(page: ft.Page, navigate_to, header):
    matricula = user_info.get("matricula")
    print(f"User config na tela conferir bonus: {matricula}")

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