import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def buscar_pedido_dist(page: ft.Page, navigate_to, header):
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
        print(f"Buscando pedido: {numped} para matricula: {matricula} na filial: {codfilial}")
        input_codetiqueta = ft.TextField(
            label="Código da Etiqueta",
            expand=True,
            autofocus=True,
            keyboard_type=ft.KeyboardType.NUMBER,
            on_submit=lambda e: atribuir_etiqueta(numped, input_codetiqueta.value, codfilial, matricula)
        )
        button_atribuir = ft.ElevatedButton(
            "Atribuir Etiqueta",
            expand=True,
            bgcolor=colorVariaveis['botaoAcao'],
            color=colorVariaveis['texto'],
            on_click=lambda e: atribuir_etiqueta(numped, input_codetiqueta.value, codfilial, matricula)
        )
        response = requests.get(
            f"{base_url}/buscarPedidoDist",
            params={
                "codfilial": codfilial,
                "matricula": matricula,
                "numped": numped
            }
        )
        resposta = response.json()

        if response.status_code == 200:
            numped = resposta.get("numped")
            snack_bar(f"Pedido {numped} encontrado com sucesso!", colorVariaveis['sucesso'], colorVariaveis['textoPreto'], page)
            Container.content.controls.clear()
            Container.content.controls.append(
                ft.Text(f"Atribuir Etiqueta ao pedido {numped}:", size=16)
            )
            Container.content.controls.append(input_codetiqueta)
            Container.content.controls.append(button_atribuir)
            Container.update()
        else:
            mensagem = resposta.get("message")
            snack_bar(mensagem, colorVariaveis['erro'], colorVariaveis['texto'], page)

    def atribuir_etiqueta(numped, codetiqueta, codfilial, matricula):
        if not codetiqueta:
            snack_bar("Por favor, insira o código da etiqueta.", colorVariaveis['erro'], colorVariaveis['texto'], page)
            return
        
        print(f"Atribuindo etiqueta {codetiqueta} ao pedido {numped} para matricula: {matricula} na filial: {codfilial}")
        response = requests.put(
            f"{base_url}/buscarPedidoDist",
            json={
                "numped": numped,
                "codetiqueta": codetiqueta,
                "codfilial": codfilial,
                "matricula": matricula
            }
        )
        resposta = response.json()

        if response.status_code == 200:
            snack_bar(f"Etiqueta {codetiqueta} atribuída ao pedido {numped} com sucesso!", colorVariaveis['sucesso'], colorVariaveis['textoPreto'], page)
            navigate_to("/separar_pedido_dist", arguments={"numped": numped})
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
                ft.Divider(height=50),
                ft.ElevatedButton(
                    "Busca automática",
                    expand=True,
                    bgcolor=colorVariaveis['botaoAcao'],
                    color=colorVariaveis['texto'],
                    on_click=lambda e: buscar_pedido(codfilial, matricula)
                )
            ]
        )
    )
    titulo = ft.Text(
        "Buscar Pedido V2",
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