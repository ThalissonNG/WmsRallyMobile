import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def buscar_pedido(e, navigate_to, header):
    matricula = user_info.get('matricula')
    print(matricula)

    def pedidoManual(numped):
        try:
            response = requests.post(
                f"{base_url}/buscarPedido",
                json={"numped": numped,
                        "matricula": matricula}
            )
            if response.status_code == 200:
                print("Tem pedido manual")
                navigate_to("/separar_pedido")
            elif response.status_code == 201:
                navigate_to("/separar_pedido")
            else:
                print("Não tem pedido")
        except Exception as exc:
            print(exc)

    def pedidoAutomatico():
        try:
            response = requests.post(
                f"{base_url}/buscarPedido",
                json={"numped": None,
                        "matricula": matricula}
            )
            if response.status_code == 200:
                print("Tem pedido automatico")
                navigate_to("/separar_pedido")
            elif response.status_code == 201:
                navigate_to("/separar_pedido")
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
        "Busca Automatica",
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
        route="/buscar_pedido",
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
