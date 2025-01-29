import flet as ft
import requests
from routes.config.config import base_url

def enderecar_produto(page: ft.Page, navigate_to, header, arguments):
    codprod = arguments.get("codprod", "N/A")
    codfab = arguments.get("codfab", "N/A")
    descricao = arguments.get("descricao", "N/A")
    qt = int(arguments.get("qt", 0))
    numbonus = arguments.get("numbonus", "N/A")
    matricula = arguments.get("matricula", "N/A")
    codfilial = arguments.get("codfilial", "N/A")

    print(f"Bônus: {numbonus} - Produto: {codprod} - Codfab: {codfab} - Descricao: {descricao} - Quantidade: {qt}")
    print(f"Matricula: {matricula} - codfilial: {codfilial}")

    def guardar_produto(page, codbarra, codendereco, qtGuardar, numbonus):
        try:
            response = requests.post(
                f"{base_url}/guardarProduto",
                json={"codbarra": codbarra,
                        "codendereco": codendereco,
                        "qt": qtGuardar,
                        "matricula": matricula,
                        "codfilial": codfilial,
                        "numbonus": numbonus,
                    }
            )
            if response.status_code == 400 or response.status_code == 500:
                resposta = response.json()
                print(resposta)
                snackbar_sucess = ft.SnackBar(
                    content=ft.Text("Informação incompleta", color="white"),
                    bgcolor=ft.colors.RED,
                    show_close_icon=True,
                    duration=1000,
                )
                page.overlay.append(snackbar_sucess)
                snackbar_sucess.open = True
                page.update()
            elif response.status_code == 200:
                print("Produto guardado com sucesso")
                snackbar_sucess = ft.SnackBar(
                    content=ft.Text("Produto guardado com sucesso"),
                    bgcolor=ft.colors.GREEN,
                    show_close_icon=True,
                    duration=1000,
                )
                page.overlay.append(snackbar_sucess)
                snackbar_sucess.open = True
                
                nonlocal qt  # Permite modificar a variável `qt` definida fora do escopo da função
                qt -= int(qtGuardar)  # Atualiza a quantidade

                # Atualiza o texto da tabela na tela
                infosProduto.controls[0].rows[0].cells[1].content.value = str(qt)
                infosProduto.update()

                page.update()
        except Exception as e:
            print(e)

    codbarra = ft.TextField(
        label="CODBARRA",
        prefix_icon=ft.icons.BARCODE_READER,
        border_radius=ft.border_radius.all(10),
        border_color=ft.colors.BLACK,
        border_width=2,
    )
    codendereco = ft.TextField(
        label="CODENDERECO",
        prefix_icon=ft.icons.STORAGE,
        border_radius=ft.border_radius.all(10),
        border_color=ft.colors.BLACK,
        border_width=2,
    )
    qtEndereco = ft.TextField(
        label="QUANTIDADE",
        prefix_icon=ft.icons.STORAGE,
        border_radius=ft.border_radius.all(10),
        border_color=ft.colors.BLACK,
        border_width=2,
    )
    numbonus_container = ft.Container(
        content=ft.Text(
            f"Número do bônus: {numbonus}",
            size=16,
            text_align="left",
        ),
        padding=10,
        border_radius=ft.border_radius.all(10),
        alignment=ft.alignment.center_left,
    )
    infosProduto = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text(
                                    "CODPROD:",
                                    weight="bold",
                                ),
                                ft.Text(codprod),
                            ],
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(
                                    "CODFAB:",
                                    weight="bold",
                                ),
                                ft.Text(codfab),
                            ],
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(
                                    "QT:",
                                    weight="bold",
                                ),
                                ft.Text(qt),
                            ],
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_AROUND
                ),
                ft.Divider(),
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text(
                                    "DESCRIÇÃO:",
                                    weight="bold",
                                ),
                                ft.Text(descricao),
                            ],
                            expand=True,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Divider(),
            ],
        ),
        padding=10,
        expand=True,
    )
    buttonGuardar = ft.ElevatedButton(
        text="Guardar",
        on_click=lambda e: guardar_produto(
            e.page,
            codbarra.value,
            codendereco.value,
            qtEndereco.value,
            numbonus,
            ) 
    )

    return ft.View(
        route="/enderecarBonus",
        controls=[
            header,
            ft.Container(height=10),
            ft.Container(
                content=ft.Column(
                    controls=[
                        numbonus_container,
                        infosProduto,
                        codbarra,
                        codendereco,
                        qtEndereco,
                        buttonGuardar,
                    ],
                )
            ),
        ],
        scroll="always",
    )