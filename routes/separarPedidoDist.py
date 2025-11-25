import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def separar_pedido_dist(page: ft.Page, navigate_to, header, arguments=None):
    matricula = user_info.get("matricula")
    codfilial = user_info.get("codfilial")
    pedido = arguments.get("numped")
    print(f"User config na tela Separar Pedido Dist: {matricula}, pedido: {pedido}")

    def buscar_itens_pedido(numped, codfilial):
        print(f"Buscando itens do pedido {numped} na filial {codfilial}")
        response = requests.get(
            f"{base_url}/separarPedidoDist/{numped}",
            params={
                "codfilial": codfilial,
                "numped": numped
            }
        )
        resposta = response.json()

        if response.status_code == 200:
            itens = resposta.get("itens", [])
            print(f"Itens do pedido {numped}: {itens}")
            return itens
        else:
            mensagem = resposta.get("message")
            print(f"Erro ao buscar itens do pedido {numped}: {mensagem}")
            return []

    itens = buscar_itens_pedido(pedido, codfilial)
    print(f"Itens para separar do pedido {itens}")

    titulo = ft.Text(
        f"Pedido: {pedido}",
        size=24, weight="bold",
        color=colorVariaveis['titulo']
    )
    aba_separar = ft.Tab(
        text="Separar",
        content=ft.Column(
            spacing=10,
            controls=[
                ft.Text("Endereço do produto", weight="bold", size=16),

                # Linha 1: módulo / rua
                ft.Row(
                    controls=[
                        ft.Text(f"Módulo: {1}", weight="bold"),
                        ft.Text(f"Rua: {1}", weight="bold"),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),

                # Linha 2: edi / nível / apto
                ft.Row(
                    controls=[
                        ft.Text(f"Edi: {2}", weight="bold"),
                        ft.Text(f"Nível: {3}", weight="bold"),
                        ft.Text(f"Apto: {304}", weight="bold"),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Divider(),
                ft.TextField(
                    label = "Código do endereço",
                    expand=True,
                    autofocus=True,
                    keyboard_type=ft.KeyboardType.TEXT,
                ),
                ft.ElevatedButton(
                    "Validar endereço",
                    expand=True,
                    bgcolor=colorVariaveis['botaoAcao'],
                    color=colorVariaveis['texto'],
                )
            ],
        ),
    )
    abas = ft.Tabs(
        tabs=[
            aba_separar,
            ft.Tab(text="Conferir Itens", content=ft.Column(controls=[
                ft.Text("Conteúdo da aba Conferir Itens")
            ])),
            ft.Tab(text="Separar Abastecimento", content=ft.Column(controls=[
                ft.Text("Conteúdo da aba Separar Abastecimento")
            ]))
        ]
    )
    
    return ft.View(
        route="/separar_pedido_dist",
        controls=[
            header,
            titulo,
            abas
        ]
    )