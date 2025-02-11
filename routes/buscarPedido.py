import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis

def buscar_pedido(e, navigate_to, header):
    # Funções de overlay
    def show_overlay(e):
        inputCodetiqueta = ft.TextField(
            label="Etiqueta",
            prefix_icon=ft.icons.INSERT_DRIVE_FILE,
            border_radius=ft.border_radius.all(10),
            border_color=colorVariaveis['bordarInput'],
            border_width=2,
            width=300,
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        overlay = ft.Container(
            width=e.width,
            height=e.height,
            bgcolor=ft.colors.BLACK,
            alignment=ft.alignment.center,
            content=ft.Column(
                controls=[
                    ft.Text("Pedido encontrado!", size=30, weight="bold"),
                    ft.Text("Bipe um etiqueta e coloque na caixa onde irá os produtos"),
                    inputCodetiqueta,
                    ft.ElevatedButton(
                        text="Fechar",
                        on_click=lambda e: close_overlay(e.page)
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )
        e.overlay.append(overlay)
        e.update()

    def close_overlay(page):
        page.overlay.clear()
        page.update()

    def pedidoManual(numped):
        try:
            response = requests.post(
                f"{base_url}/separarPedido",
                json={"numped": numped}
            )
            if response.status_code == 200:
                print("tem pedido")
                show_overlay(e)
            else:
                print("Não tem pedido")
        except Exception as exc:
            print(exc)

    def pedidoAutomatico():
        try:
            response = requests.post(
                f"{base_url}/separarPedido"
            )
            if response.status_code == 201:
                print("Tem pedido automatico")
                show_overlay(e)
            else:
                print("Não tem pedido")
        except Exception as exc:
            print(exc)
    title = ft.Text(
        "Buscar Pedido",
        size=24,
        weight="bold",
        color=colorVariaveis['titulo']
    )
    buscaManual = ft.Text(
        "Busca Manual",
        size=18,
        weight="bold",
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
        on_click=lambda e: pedidoManual(inputNumped.value)
    )
    buscaAutomatica = ft.Text(
        "Busca Manual",
        size=18,
        weight="bold",
    )
    buttonBuscarAutomatico = ft.ElevatedButton(
        text="Buscar",
        bgcolor=colorVariaveis['botaoAcao'],
        color=colorVariaveis['texto'],
        width=600,
        height=70,
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(size=20)
        ),
        on_click=lambda e: pedidoAutomatico()
    )
    return ft.View(
        route="/separar_pedido",
        controls=[
            header,
            title,
            ft.Container(height=20),
            buscaManual,
            inputNumped,
            buttonBuscarPedido,
            ft.Container(height=20),
            buscaAutomatica,
            buttonBuscarAutomatico
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
