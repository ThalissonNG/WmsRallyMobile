import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def separar_pedido(e, navigate_to, header):
    
    title = ft.Text(
        "Separar Pedido - Atribuir Etiquetas",
        size=24,
        weight="bold",
        color=colorVariaveis['titulo'],
        text_align="center"
    )

    return ft.View(
        route="/separar_pedido",
        controls=[
            header,
            title,
        ],
        scroll=ft.ScrollMode.AUTO
    )