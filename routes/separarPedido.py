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
    inputNumped = ft.TextField(
        label="Número do pedido",
        prefix_icon=ft.icons.INSERT_DRIVE_FILE,
        border_radius=ft.border_radius.all(10),
        border_color=colorVariaveis['bordarInput'],
        border_width=2,
        width=300,
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    buttonBuscarPedido = ft.ElevatedButton(
        text="Buscar",
        bgcolor=colorVariaveis['botaoAcao'],
        color=colorVariaveis['texto'],
        width=600,
        on_click=lambda e: print(f"Número do pedido: {inputNumped.value}")
    )
    return ft.View(
        route="/separar_pedido",
        controls=[
            header,
            title,
            ft.Container(height=20),
            inputNumped,
            buttonBuscarPedido
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )