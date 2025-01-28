import flet as ft
import requests
from routes.config.config import base_url

def enderecar_produto(navigate_to, header, arguments):
    codprod = arguments.get("codprod", "N/A")
    descricao = arguments.get("descricao", "N/A")
    qt = int(arguments.get("qt", 0))
    numbonus = arguments.get("numbonus", "N/A")

    print(f"Bônus: {numbonus} - Produto: {codprod} - Descricao: {descricao} - Quantidade: {qt}")

    def guardar_produto(page, codbarra, codendereco, qtGuardar):
        try:
            response = requests.post(
                f"{base_url}/guardarProduto",
                json={"codbarra": codbarra,
                        "codendereco": codendereco,
                        "qt": qtGuardar,
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
                tableCodprod.controls[0].rows[0].cells[1].content.value = str(qt)
                tableCodprod.update()

                page.update()
        except Exception as e:
            print(e)

    codbarra = ft.TextField(expand=True)
    codendereco = ft.TextField(expand=True)
    qtEndereco = ft.TextField(expand=True)
    numbonus = ft.Container(
        content=ft.Text(
            f"Número do bônus: {numbonus}",
            size=16,
            text_align="left",
        ),
        padding=10,
        border_radius=ft.border_radius.all(10),
        alignment=ft.alignment.center_left,
    )
    tableCodprod = ft.Row(
        controls=[
            ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("CODPROD")),
                    ft.DataColumn(ft.Text("QT")),
                    ft.DataColumn(ft.Text("DESCRICAO")),
                ],
                rows=[
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(codprod)),
                            ft.DataCell(ft.Text(str(qt))),
                            ft.DataCell(ft.Text(descricao)),
                        ]
                    )
                ],
            )
        ],
        scroll="always",
        width=400,
    )
    tableEndereco = ft.Container(
        content=ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("CODPROD")),
                ft.DataColumn(ft.Text("DESTINO")),
                ft.DataColumn(ft.Text("QUANTIDADE")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(codbarra),
                        ft.DataCell(codendereco),
                        ft.DataCell(qtEndereco),
                    ]
                )
            ]
        ),
        expand=True,
    )
    buttonGuardar = ft.ElevatedButton(
        text="Guardar",
        on_click=lambda e: guardar_produto(
            e.page,
            codbarra.value,
            codendereco.value,
            qtEndereco.value
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
                        numbonus,
                        tableCodprod,
                        tableEndereco,
                        buttonGuardar,
                    ],
                ),
                # alignment=ft.alignment.center,
                # expand=True,
            ),
        ],
        scroll="always",
    )