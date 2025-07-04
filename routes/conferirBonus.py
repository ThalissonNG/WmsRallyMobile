import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def conferir_bonus(page, navigate_to, header, arguments):
    matricula = user_info.get("matricula")
    codfilial = user_info.get("codfilial")
    numbonus = arguments.get("numbonus", "N/A")
    print(f"Tela de conferir bonusMatricula: {matricula} - Codfilial: {codfilial} - Numbonus: {numbonus}")
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