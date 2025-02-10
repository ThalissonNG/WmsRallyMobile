import flet as ft
import requests
from routes.config.config import base_url, user_info, colorVariaveis

def buscar_pedido(e, navigate_to, header):
    print(f"User infos tela buscar pedidos: {user_info}")
    title = ft.Text(
        "Buscar Pedido",
        size=24,
        weight="bold",
        color=colorVariaveis['titulo']
    )
    return ft.View(
        route="/separar_pedido",
        controls=[
            header,
            title,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )