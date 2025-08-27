import flet as ft
import requests
from routes.config.config import base_url, user_info, colorVariaveis

def consultar_produto_endereco(navigate_to, header):
    matricula = user_info.get("matricula")
    codfilial = user_info.get("codfilial")
    print(f"User info tela de consultarProduto: {matricula}")

    lista_produtos_col = ft.Column(scroll=ft.ScrollMode.AUTO)

    def snackbar(mensagem, bgcolor, e):
        snack = ft.SnackBar(
            content=ft.Text(
                mensagem,
                color="white"
            ),
            bgcolor=bgcolor)
        e.page.open(snack)

    def criar_container_total(row):
        codprod, codfab, qt, descricao, modulo, rua, edificio, nivel, apto, tipoendereco, total, validade = row

        return ft.Container(
            padding=10,
            expand=True,
            content=ft.Column(
                controls=[
                    ft.Text("TOTAL", weight="BOLD"),
                    ft.Text(str(total)),
                ]
            ),
            border=ft.border.all(1,),
        )

    def criar_container_produto(row):
        codprod, codfab, descricao = row

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
                ]
            ),
            border=ft.border.all(1,),
        )
    
    def criar_container_produto_filial(row):
        codprod, codfab, qt, descricao, modulo, rua, edificio, nivel, apto, tipoendereco, total, validade = row

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
                                    ft.Text("QT", weight="BOLD"),
                                    ft.Text(str(qt)),
                                ]
                            ),
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
                        ],
                    ),
                    ft.Divider(),
                    ft.Row(
                        expand=True,
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        controls=[
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
                            ft.Column(
                                controls=[
                                    ft.Text("VAL", weight="BOLD"),
                                    ft.Text(str(validade)),
                                ]
                            ),
                        ]
                    )
                ]
            ),
            border=ft.border.all(1),
        )

    def consultar_produto(codbarra, e):
        try:
            response = requests.post(
                f"{base_url}/consultarProdutoEndereco",
                json={"codbarra": codbarra,
                    "codfilial": codfilial},
            )
            if response.status_code == 200:
                dados = response.json()
                dados_produto = dados.get("dados_produto", [])
                dados_produto_filial = dados.get("dados_produto_filial", [])

                # print("Dados do produto na filial:", dados_produto_filial)
                # print("Dados do produto", dados_produto)

                lista_produtos_col.controls.clear()

                if dados_produto_filial:
                    linha1 = dados_produto_filial[0]
                    # print(f"Linha 1{linha1}")
                    container_total = criar_container_total(linha1)
                    lista_produtos_col.controls.append(container_total)

                for row in dados_produto:
                    container_prod = criar_container_produto(row)
                    lista_produtos_col.controls.append(container_prod)

                for row in dados_produto_filial:
                    container_prod = criar_container_produto_filial(row)
                    lista_produtos_col.controls.append(container_prod)

                e.page.update()

            elif response.status_code == 400:
                resposta = response.json()
                mensagem = resposta.get("message")
                snackbar(mensagem, colorVariaveis['erro'], e)

            else:
                print("Erro no backend:", response.status_code, response.text)
        except Exception as exc:
            print("Erro na requisição consultar produto:", exc)

    def criar_container_endereco(row):
        """row deve ser algo como [codprod, codfab, qt, descricao]."""
        codprod, codfab, qt, descricao, validade = row

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
                            ft.Column(
                                controls=[
                                    ft.Text("VAL", weight="BOLD"),
                                    ft.Text(str(validade)),
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
            border=ft.border.all(1,),
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

                #print("Recebido do backend (endereços):", dados_endereco)

                # Preenche com containers de endereço
                for row in dados_endereco:
                    container_end = criar_container_endereco(row)
                    lista_produtos_col.controls.append(container_end)

                e.page.update()
            elif response.status_code == 400:
                resposta = response.json()
                mensagem = resposta.get("message")
                snackbar(mensagem, colorVariaveis['erro'], e)
            else:
                print("Erro no backend (endereco):", response.status_code, response.text)
        except Exception as exc:
            print("Erro na requisição (endereco):", exc)

    title = ft.Text(
        "Consultar Produto ou Endereço",
        size=24,
        weight="bold",
        color=colorVariaveis['titulo']
    )
    codbarra = ft.TextField(
        label="Código de Barras",
        width=300,
        border_radius=ft.border_radius.all(10),
        border_color=colorVariaveis['bordarInput'],
        on_submit=lambda e: consultar_produto(codbarra.value, e),
    )
    codendereco = ft.TextField(
        label="Endereço",
        width=300,
        border_radius=ft.border_radius.all(10),
        border_color=colorVariaveis['bordarInput'],
        on_submit=lambda e: consultar_endereco(codendereco.value, e),
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
                            color=colorVariaveis['texto'],
                            bgcolor=colorVariaveis['botaoAcao'],
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
                            color=colorVariaveis['texto'],
                            bgcolor=colorVariaveis['botaoAcao'],
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
            ft.Container(
                
                content=lista_produtos_col,
                expand=True,
            ),
        ],
    )
