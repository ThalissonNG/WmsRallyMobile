import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def ajustar_endereco(page: ft.Page, navigate_to, header):
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

    def validar_endereco(codendereco, codfilial):
        response = requests.post(
            base_url + "/ajustar_endereco",
            json={
                "codendereco": codendereco,
                "matricula": matricula,
                "codfilial": codfilial
            }
        )
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.json()}")

        if response.status_code == 201:
            dados_endereco = response.json().get("dados_endereco", [])
            container_principal.content = construir_container(dados_endereco)
            page.update()

            snack_bar("Endereço ajustado com sucesso!", colorVariaveis['sucesso'], colorVariaveis['textoPreto'], page)
        else:
            mensagem = response.json().get("message")
            snack_bar(mensagem, colorVariaveis['erro'], colorVariaveis['texto'], page)

    def construir_container(lista_enderecos):
        cards = []

        for linha in lista_enderecos:
            codprod, codfab, descricao, qt, tipoendereco, capacidade, reposicao, validade = linha
            
            card = ft.Container(
                padding=10,
                border=ft.border.all(1, ft.Colors.GREY_400),
                border_radius=8,
                margin=ft.margin.symmetric(vertical=4, horizontal=6),
                content=ft.Column(
                    spacing=4,
                    controls=[
                        ft.Text(descricao, weight="bold", size=14),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(f"Codprod: {codprod}", size=12),
                                ft.Text(f"Codfab: {codfab}", size=12),
                            ]
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(f"Qt: {qt}", size=12, weight="bold"),
                                ft.Text(f"Validade: {validade}", size=12),
                            ]
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(f"Capacidade: {capacidade}", size=12),
                                ft.Text(f"Reposição: {reposicao}", size=12,),
                            ]
                        ),
                        ft.Button(
                            text="Ajustar Endereço",
                            bgcolor=colorVariaveis['botaoAcao'],
                            color=colorVariaveis['texto'],
                        )
                    ]
                )
            )
            cards.append(card)

        return ft.Column(controls=cards, spacing=10, expand=True, scroll=ft.ScrollMode.AUTO)

    titulo = ft.Text(
        "Ajustar Endereço",
        size=24,
        weight="bold",
        color=colorVariaveis['titulo']
    )
    input_codendereco = ft.TextField(
        label="Código Endereço",
        autofocus=True,
        keyboard_type=ft.KeyboardType.NUMBER,
        on_submit=lambda e: validar_endereco(input_codendereco.value, codfilial)
    )
    buscar_endereco = ft.ElevatedButton(
        "Buscar Endereço",
        bgcolor=colorVariaveis['botaoAcao'],
        color=colorVariaveis['texto'],
        on_click=lambda e: validar_endereco(input_codendereco.value, codfilial)
    )
    container_principal = ft.Container(
        expand=True,
        margin=ft.margin.symmetric(vertical=4, horizontal=6),
        content=ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO
        )
    )
    return ft.View(
        route="/ajustar_endereco",
        controls=[
            header,
            ft.Column(
                expand=True,
                controls=[
                    titulo,
                    ft.Container(height=20),
                    input_codendereco,
                    buscar_endereco,
                    ft.Divider(),
                    container_principal
                ]
            )
        ]
    )