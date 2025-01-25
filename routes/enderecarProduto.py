import flet as ft
import requests
from routes.config.config import base_url

def enderecar_produto(navigate_to, header, arguments):
    codprod = arguments.get("codprod", "N/A")
    qt = arguments.get("qt", "N/A")
    numbonus = arguments.get("numbonus", "N/A")

    print(f"Bônus: {numbonus} - Produto: {codprod} - Quantidade: {qt}")

    numbonus = ft.Container(
        content=ft.Text(
            f"Número do bônus: {numbonus}",
            size=16,
            color=ft.colors.BLACK,
            text_align="left",
        ),
        bgcolor=ft.colors.WHITE,
        padding=10,
        border_radius=ft.border_radius.all(10),
        alignment=ft.alignment.center_left,
    )
    tableCodprod = ft.Container(
        content=ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("CODPROD")),
                ft.DataColumn(ft.Text("QT")),
                ft.DataColumn(ft.Text("ENDEREÇO")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(codprod)),
                        ft.DataCell(ft.Text(qt)),
                        ft.DataCell(ft.Text("Endereço")),
                    ]
                )
            ]
        ),
        expand=True,
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
                    ],
                    spacing=20
                ),
                alignment=ft.alignment.center,
                expand=True,
            ),
        ],
    )