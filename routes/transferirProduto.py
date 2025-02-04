import flet as ft
import requests
from routes.config.config import base_url

def transferir_produto(page, navigate, header, arguments):
    lista_produtos = ft.Column(scroll=ft.ScrollMode.AUTO)
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
    def consultar_endereco(codenderecoAtual, e):
        lista_produtos.controls.clear()

        try:
            response = requests.post(
                f"{base_url}/transferirProduto",
                json={"codenderecoAtual":codenderecoAtual}
            )
            if response.status_code == 200:
                print("Retornou 200")
                dados = response.json()
                dados_endereco = dados.get("dados_endereco",[])
                for row in dados_endereco:
                    container_end = criar_container_endereco(row)
                    lista_produtos.controls.append(container_end)
                    e.page.update()
                abrir_dialog(page)

            elif response.status_code == 402:
                print("Endereço não encontrado")
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
        except Exception as exc:
            print("Erro na requisição (endereco):", exc)
        page.update()

    def abrir_dialog(e):
        page.dialog = dialog
        dialog.open = True
        page.update()

    def fechar_dialog(e):
        dialog.open = False
        page.update()
    
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
    codbarra = ft.TextField(
        label="CODBARRA",
        prefix_icon=ft.icons.BARCODE_READER,
        border_radius=ft.border_radius.all(10),
        border_color=ft.colors.BLACK,
        border_width=2,
    )
    buttonTransferir = ft.ElevatedButton(
        text="Transferir",
        on_click=lambda e: consultar_endereco(codenderecoAtual.value, e),
    )

    dialog = ft.AlertDialog(
        title=ft.Text("Itens do endereço CODENDERECO"),
        actions=[
            codbarra,
            ft.ElevatedButton("Fechar", on_click=fechar_dialog),
        ],
    )
    return ft.View(
        route="/transferirProduto",
        controls=[
            header,
            title,
            codenderecoAtual,
            buttonTransferir,
        ]
    )