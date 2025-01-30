import flet as ft
import requests
from routes.config.config import base_url

def consultar_produto_endereco(navigate_to, header, arguments):

    codprod = 22719
    codfab = 6
    qt = 30
    descricao = "CAPA BANCO PERSONALIZADA TODOS OS MODELOS EXCETO POP (LOGO HONDA) PRETA - JC MAXI BR"
    modulo = 1
    rua = 1
    edificio = 1
    nivel = 1
    apto = 2
    tipoendereco = "PIKING"

    codprod2 = 32545
    codfab2 = 65410
    qt2 = 154

    title = ft.Text(
        "Consultar Produto ou Endereço",
        size=24,
        weight="bold",
        color="blue",
    )
    codbarra = ft.TextField(
        label="Código de Barras",
        width=300,
    )
    codendereco = ft.TextField(
    label="Endereço",
    width=300,
    )
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Produto",
                content=ft.Column(
                    [
                        ft.Text(
                            "Informe o código de barras do produto",
                            size=16,
                        ),
                        codbarra,
                        ft.ElevatedButton(
                            text="Consultar",
                            on_click=lambda e: print(f"Consultar Produto: {codbarra.value}"),
                        ),
                    ]
                ),
            ),
            ft.Tab(
                text="Endereço",
                content=ft.Column(
                    [
                        ft.Text(
                            "Informe o código de barras do endereço",
                            size=16,
                        ),
                        codendereco,
                        ft.ElevatedButton(
                            text="Consultar",
                            on_click=lambda e: print(f"Consultar Endereço: {codendereco.value}"),
                        ),
                    ],
                ),
            ),
        ],
        height=200,
    )
    resultadoProduto = ft.Container(
    content=ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text("CODPROD", weight="BOLD"),
                            ft.Text(str(codprod)),
                        ]
                    ),
                    ft.Column(
                        controls=[
                            ft.Text("CODFAB", weight="BOLD"),
                            ft.Text(str(codfab)),
                        ]
                    ),
                    ft.Column(
                        controls=[
                            ft.Text("QT", weight="BOLD"),
                            ft.Text(str(qt)),
                        ]
                    ),
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.SPACE_AROUND
            ),
            ft.Divider(),
            ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text("Descrição", weight="BOLD"),
                            ft.Text(descricao),
                        ],
                        expand=True
                    )
                ],
            ),
            ft.Divider(),
            ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text("MODULO", weight="BOLD"),
                            ft.Text(str(modulo)),
                        ]
                    ),
                    ft.Column(
                        controls=[
                            ft.Text("RUA", weight="BOLD"),
                            ft.Text(str(rua)),
                        ]
                    ),
                    ft.Column(
                        controls=[
                            ft.Text("EDIFICIO", weight="BOLD"),
                            ft.Text(str(edificio)),
                        ]
                    ),
                    ft.Column(
                        controls=[
                            ft.Text("NIVEL", weight="BOLD"),
                            ft.Text(str(nivel)),
                        ]
                    ),
                    ft.Column(
                        controls=[
                            ft.Text("APTO", weight="BOLD"),
                            ft.Text(str(apto)),
                        ]
                    ),
                    ft.Column(
                        controls=[
                            ft.Text("TIPOENDERECO", weight="BOLD"),
                            ft.Text(tipoendereco),
                        ]
                    ),
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.SPACE_AROUND
            ),
        ],
        # Se quiser rolagem vertical, você pode usar:
        scroll=ft.ScrollMode.AUTO,
    ),
)

    return ft.View(
        route="/consultarProdutoEndereco",
        controls=[
            header,
            title,
            tabs,
            resultadoProduto,
        ],
        scroll=ft.ScrollMode.AUTO,
    )