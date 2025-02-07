import flet as ft
import requests
from routes.config.config import base_url
from routes.config.config import user_info

def consultar_produto_endereco(navigate_to, header):
    matricula = user_info.get("matricula")
    print(f"User info tela de consultarProduto: {matricula}")

    lista_produtos_col = ft.Column(scroll=ft.ScrollMode.AUTO)

    def criar_container_produto(row):
        codprod, codfab, qt, descricao, modulo, rua, edificio, nivel, apto, tipoendereco = row

        return ft.Container(
            padding=10,
            content=ft.Column(
                controls=[
                    ft.Row(
                        expand=True,
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
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
                    ),
                    ft.Divider(),
                    ft.Row(
                        controls=[
                            ft.Column(
                                expand=True,
                                controls=[
                                    ft.Text("PRODUTO", weight="BOLD"),
                                    ft.Text(descricao),
                                ]
                            )
                        ],
                    ),
                    ft.Divider(),
                    ft.Row(
                        expand=True,
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text("MOD", weight="BOLD"),
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
                                    ft.Text("EDI", weight="BOLD"),
                                    ft.Text(str(edificio)),
                                ]
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text("NIV", weight="BOLD"),
                                    ft.Text(str(nivel)),
                                ]
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text("APT", weight="BOLD"),
                                    ft.Text(str(apto)),
                                ]
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text("TIPEND", weight="BOLD"),
                                    ft.Text(str(tipoendereco)),
                                ]
                            ),
                        ],
                    ),
                ]
            ),
            border=ft.border.all(1, 'black'),
        )

    def consultar_produto(codbarra, e):
        try:
            response = requests.post(
                f"{base_url}/consultarProdutoEndereco",
                json={"codbarra": codbarra},
            )
            if response.status_code == 200:
                dados = response.json()
                dados_produto = dados.get("dados_produto", [])

                print("Recebido do backend:", dados_produto)

                lista_produtos_col.controls.clear()

                for row in dados_produto:
                    container_prod = criar_container_produto(row)
                    lista_produtos_col.controls.append(container_prod)

                e.page.update()

            else:
                print("Erro no backend:", response.status_code, response.text)
        except Exception as exc:
            print("Erro na requisição:", exc)

    def criar_container_endereco(row):
        """row deve ser algo como [codprod, codfab, qt, descricao]."""
        codprod, codfab, qt, descricao = row

        return ft.Container(
            padding=10,
            content=ft.Column(
                controls=[
                    ft.Row(
                        expand=True,
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
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
                    ),
                    ft.Divider(),
                    ft.Row(
                        controls=[
                            ft.Column(
                                expand=True,
                                controls=[
                                    ft.Text("PRODUTO", weight="BOLD"),
                                    ft.Text(descricao),
                                ]
                            )
                        ],
                    ),
                ]
            ),
            border=ft.border.all(1, 'black'),
        )
    
    def consultar_endereco(codendereco_valor, e):
        # Limpa a lista de produtos do column
        lista_produtos_col.controls.clear()
        e.page.update()

        try:
            response = requests.post(
                f"{base_url}/consultarProdutoEndereco",
                json={"codendereco": codendereco_valor},
            )
            if response.status_code == 200:
                dados = response.json()
                dados_endereco = dados.get("dados_endereco", [])

                print("Recebido do backend (endereços):", dados_endereco)

                # Preenche com containers de endereço
                for row in dados_endereco:
                    container_end = criar_container_endereco(row)
                    lista_produtos_col.controls.append(container_end)

                e.page.update()
            else:
                print("Erro no backend (endereco):", response.status_code, response.text)
        except Exception as exc:
            print("Erro na requisição (endereco):", exc)

    title = ft.Text(
        "Consultar Produto ou Endereço",
        size=24,
        weight="bold",
        color="blue"
    )
    codbarra = ft.TextField(
        label="Código de Barras",
        width=300
    )
    codendereco = ft.TextField(
        label="Endereço",
        width=300
    )

    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        height=200,
        tabs=[
            ft.Tab(
                text="Produto",
                content=ft.Column(
                    [
                        ft.Text("Informe o código de barras do produto", size=16),
                        codbarra,
                        ft.ElevatedButton(
                            text="Consultar",
                            on_click=lambda e: consultar_produto(codbarra.value, e),
                        ),
                    ]
                ),
            ),
            ft.Tab(
                text="Endereço",
                content=ft.Column(
                    [
                        ft.Text("Informe o código de barras do endereço", size=16),
                        codendereco,
                        ft.ElevatedButton(
                            text="Consultar",
                            on_click=lambda e: consultar_endereco(codendereco.value, e),
                        ),
                    ],
                ),
            ),
        ],
    )

    return ft.View(
        route="/consultarProdutoEndereco",
        scroll=ft.ScrollMode.AUTO,
        controls=[
            header,
            title,
            tabs,
            lista_produtos_col,
        ],
    )
