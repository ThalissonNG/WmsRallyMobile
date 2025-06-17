import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def os_avulsa_saida(e, navigate_to, header):
    titulo = ft.Text(
        "OS Avulsa - Saida",
        size=24,
        weight="bold",
        color=colorVariaveis['titulo']
    )

    return ft.View(
        route="/cadastrar_codbarra",
        controls=[
            header,
            titulo,
            ft.Divider(),
        ]
    )