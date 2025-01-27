import flet as ft
import requests
from routes.config.config import base_url

def enderecar_produto(navigate_to, header, arguments):
    codprod = arguments.get("codprod", "N/A")
    descricao = arguments.get("descricao", "N/A")
    qt = arguments.get("qt", "N/A")
    numbonus = arguments.get("numbonus", "N/A")

    print(f"Bônus: {numbonus} - Produto: {codprod} - Descrica0: {descricao} - Quantidade: {qt}")

    def guardar_produto(codetiquetaGuardar, enderecoGuardar, qtGuardar):
        try:
            response = requests.post(
                f"{base_url}/guardarProduto",
                json={"codetiqueta": codetiquetaGuardar,
                        "codendereco": enderecoGuardar,
                        "qt": qtGuardar,
                    }
            )
        except Exception as e:
            print(e)

    codetiquetaEndereco = ft.TextField(expand=True)
    enderecoDestino = ft.TextField(expand=True)
    qtEndereco = ft.TextField(expand=True)
    numbonus = ft.Container(
        content=ft.Text(
            f"Número do bônus: {numbonus}",
            size=16,
            color=ft.colors.BLACK,
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
                            ft.DataCell(ft.Text(qt)),
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
                        ft.DataCell(codetiquetaEndereco),
                        ft.DataCell(enderecoDestino),
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
            codetiquetaEndereco.value,
            enderecoDestino.value,
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
    )