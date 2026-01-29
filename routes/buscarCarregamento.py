import flet as ft
import requests
from routes.config.config import colorVariaveis, user_info, base_url, snack_bar


def buscar_carregamento(page: ft.Page, navigate_to, header):
    codfilial = user_info['codfilial']
    matricula = user_info['matricula']

    def atribuir_carregamento(numcar):
        if not numcar:
            snack_bar("Digite o número do carregamento", colorVariaveis['erro'], colorVariaveis['texto'], page)
            return False
        try:
            url = f"{base_url}/buscar_carregamento/{numcar}"
            payload = {
                "codfilial": codfilial,
                "matricula": matricula,
            }
            response = requests.post(url, json=payload)
            # print(response.json())
            mensagem = response.json()['message']
            if response.status_code == 200:
                snack_bar(mensagem, colorVariaveis['sucesso'], colorVariaveis['texto'], page)
                navigate_to("/separar_carregamento", arguments={"numcar": numcar})
                return True
            else:
                snack_bar(mensagem, colorVariaveis['erro'], colorVariaveis['texto'], page)
                return False
        except Exception as e:
            print(e)
            return False

    titulo = ft.Text(
        "Buscar Carregamento",
        size=24,
        weight="bold",
        color=colorVariaveis['titulo']
    )

    num_carregamento = ft.TextField(
        label="Carregamento",
        border_radius=ft.border_radius.all(10),
        border_color=colorVariaveis['bordarInput'],
        border_width=2,
        width=300,
        autofocus=True,
        on_submit=lambda e: atribuir_carregamento(num_carregamento.value)
    )

    btn_buscar = ft.ElevatedButton(
        text="Buscar",
        bgcolor=colorVariaveis['botaoAcao'],
        color=colorVariaveis['texto'],
        width=300,
        on_click=lambda e: atribuir_carregamento(num_carregamento.value)
    )

    return ft.View(
        route="/buscar_carregamento",
        controls=[
            header,
            titulo,
            ft.Container(height=20),
            ft.Column(
                controls=[
                    num_carregamento,
                    btn_buscar,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        ]
    )
