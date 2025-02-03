import flet as ft
import requests
from routes.config.config import base_url

def transferir_produto(navigate, header, arguments):
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
    quantidade = ft.TextField(
        label="QUANTIDADE",
        prefix_icon=ft.icons.BARCODE_READER,
        border_radius=ft.border_radius.all(10),
        border_color=ft.colors.BLACK,
        border_width=2,
    )
    coecodenderecoNovo = ft.TextField(
        label="CODENDERECO",
        prefix_icon=ft.icons.BARCODE_READER,
        border_radius=ft.border_radius.all(10),
        border_color=ft.colors.BLACK,
        border_width=2,
    )
    buttonTransferir = ft.ElevatedButton(
        text="Transferir",
        on_click=lambda e: print(f"Tranferir o produto: {codbarra.value}, do endereço: {codenderecoAtual.value} para o endereço: {coecodenderecoNovo.value}")
    )
    return ft.View(
        route="/transferirProduto",
        controls=[
            header,
            title,
            codenderecoAtual,
            codbarra,
            quantidade,
            coecodenderecoNovo,
            buttonTransferir,
        ]
    )