import flet as ft
import requests
from routes.config.config import base_url

def transferir_produto(page, navigate, header, arguments):
    # 1) Crie o Column de produtos normalmente:
    lista_produtos = ft.Column(scroll=ft.ScrollMode.AUTO)

    title = ft.Text(
        "Transferir Produto",
        size=24,
        weight="bold",
        color="blue"
    )
    codenderecoAtual = ft.TextField(
        label="CODENDERECO",
        prefix_icon=ft.icons.BARCODE_READER,
        border_radius=ft.border_radius.all(10),
        border_color=ft.colors.BLACK,
        border_width=2,
    )
    buttonCodendereco = ft.ElevatedButton(
        text="Consultar",
        on_click=lambda e: consultar_endereco(codenderecoAtual.value, e),
    )
    codbarra = ft.TextField(
        label="CODBARRA",
        prefix_icon=ft.icons.BARCODE_READER,
        border_radius=ft.border_radius.all(10),
        border_color=ft.colors.BLACK,
        border_width=2,
    )
    buttonCodbarra = ft.ElevatedButton(
        text="Transferir",
        on_click=lambda e: consultar_codbarra(codbarra.value, codenderecoAtual.value, e)
    )

    # 2) Crie o AlertDialog já referenciando esse Column no 'content'
    dialog = ft.AlertDialog(
        title=ft.Text(f"Itens do endereço"),
        content=lista_produtos,    # <-- Aqui colocamos o Column como 'content'
        actions=[
            codbarra,
            buttonCodbarra,
            ft.ElevatedButton("Fechar", on_click=lambda e: fechar_dialog(page)),
        ],
    )

    def abrir_dialog():
        page.dialog = dialog
        dialog.open = True
        page.update()

    def fechar_dialog(e):
        dialog.open = False
        new_lista_produtos = ft.Column(scroll=ft.ScrollMode.AUTO)
        dialog.content = new_lista_produtos
        nonlocal lista_produtos  # Use nonlocal para modificar a variável do escopo da função transferir_produto
        lista_produtos = new_lista_produtos
        page.update()


    def criar_container_endereco(row):
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

    def consultar_endereco(codenderecoAtual, e):
        lista_produtos.controls.clear()
        try:
            response = requests.post(
                f"{base_url}/transferirProduto",
                json={"codenderecoAtual":codenderecoAtual}
            )
            if response.status_code == 200:
                dados = response.json()
                dados_endereco = dados.get("dados_endereco", [])
                lista_produtos.controls.clear()
                # Preenche o Column com os dados
                for row in dados_endereco:
                    container_end = criar_container_endereco(row)
                    lista_produtos.controls.append(container_end)

                # Após adicionar todos os produtos, abra o diálogo
                abrir_dialog()
            elif response.status_code == 402:
                snackbar_error = ft.SnackBar(
                    content=ft.Text(
                        f"Endereço: {codenderecoAtual} não encontrado",
                        color=ft.colors.WHITE,
                        size=20,
                    ),
                    bgcolor=ft.colors.RED,
                    show_close_icon=True,
                )
                page.overlay.append(snackbar_error)
                snackbar_error.open = True
            e.page.update()
        except Exception as exc:
            print("Erro na requisição (endereco):", exc)
        e.page.update()

    def consultar_codbarra(codbarra, codenderecoAtual, e):
        try:
            response = requests.post(
                f"{base_url}/transferirProduto",
                json={"codbarra": codbarra,
                        "codenderecoAtual": codenderecoAtual
                }
            )
            if response.status_code == 200:
                print("Tem codbarra")
            else:
                print("Não tem codbarra")
        except Exception as exc:
            print("Erro na requisição (endereco):", exc)
        e.page.update()
    return ft.View(
        route="/transferirProduto",
        controls=[
            header,
            title,
            codenderecoAtual,
            buttonCodendereco,
        ]
    )
