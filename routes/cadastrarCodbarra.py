import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def cadastrar_codbarra(e, navigate_to, header):
    matricula = user_info['matricula']
    codfilial = user_info['codfilial']

    titulo = ft.Text(
        "Cadastrar Codbarras",
        size=24,
        weight="bold",
        color=colorVariaveis['titulo']
    )

    return ft.View(
        route="/cadastrar_codbarra",
        controls=[
            header,
            titulo
        ]
    )