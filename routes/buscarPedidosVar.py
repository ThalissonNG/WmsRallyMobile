import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def buscar_pedido_var(page: ft.Page, navigate_to, header):
    matricula = user_info.get("matricula")
    codfilial = user_info.get("codfilial")

    def snack_bar(mensagem, bgcolor, color, page):
        snack = ft.SnackBar(
            content=ft.Text(
                mensagem,
                color="white"
            ),
            bgcolor=bgcolor
        )
        page.open(snack)

    def buscar_pedido(codfilial, matricula, numped=None):
        if not numped:
            snack_bar("Por favor, insira o número do pedido.", colorVariaveis['erro'], colorVariaveis['texto'], page)
            return
        
        print(f"Buscando pedido: {numped} para matricula: {matricula} na filial: {codfilial}")
        response = requests.post(
            f"{base_url}/buscarPedidoVar",
            json={
                "codfilial": codfilial,
                "matricula": matricula,
                "numped": numped
            }
        )
        resposta = response.json()

        if response.status_code == 200:
            mensagem = resposta.get("message")
            snack_bar(mensagem, colorVariaveis['sucesso'], colorVariaveis['textoPreto'], page)
            navigate_to("/separar_pedido_varejo", arguments={"numped": numped})
        elif response.status_code == 202:
            mensagem = resposta.get("message")
            snack_bar(mensagem, colorVariaveis['sucesso'], colorVariaveis['textoPreto'], page)
            navigate_to("/separar_pedido_varejo", arguments={"numped": numped})
        else:
            mensagem = resposta.get("message")
            snack_bar(mensagem, colorVariaveis['erro'], colorVariaveis['texto'], page)

    input_numped = ft.TextField(
        label="Número do Pedido",
        expand=True,
        autofocus=True,
        keyboard_type=ft.KeyboardType.NUMBER,
        on_submit=lambda e: buscar_pedido(codfilial, matricula, input_numped.value)
    )
    Container = ft.Container(
        content=ft.Column(
            controls=[
                input_numped,
                ft.ElevatedButton(
                    "Buscar Pedido",
                    expand=True,
                    bgcolor=colorVariaveis['botaoAcao'],
                    color=colorVariaveis['texto'],
                    on_click=lambda e: buscar_pedido(codfilial, matricula, input_numped.value)
                ),
            ]
        )
    )
    titulo = ft.Text(
        "Buscar Pedido Varejo",
        size=24, weight="bold",
        color=colorVariaveis['titulo']
    )

    return ft.View(
        route="/buscar_pedido_V2",
        controls=[
            header,
            titulo,
            ft.Container(height=20),
            Container
        ]
    )