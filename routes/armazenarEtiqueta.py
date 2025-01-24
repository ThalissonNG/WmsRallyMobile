import flet as ft
import requests
from routes.config.config import base_url

def buscar_etiqueta(navigate_to, header):

    def consultarEtiqueta(codetiqueta):
        try:
            response = requests.post(
                f"{base_url}/consultarEtiqueta",
                json={"codetiqueta": codetiqueta},
            )
            if response.status_code == 200:
                resposta = response.json()
                codproduto = resposta.get("codprod")
                qt = resposta.get("qt")
                numbonus = resposta.get("numbonus")
                print(f"Produto: {codproduto} - Qt: {qt} - Bônus: {numbonus}")
            else:
                print("Erro ao consultar bônus")
        except Exception as e:
            print(e)
    
    title = ft.Text(
        "Armazenar Produto(s)",
        size=24,
        weight="bold",
        color="blue"
    )
    inputEtiqueta = ft.TextField(
        label="Número Etiqueta",
        prefix_icon=ft.icons.STICKY_NOTE_2,
        border_radius=ft.border_radius.all(10),
        border_color=ft.colors.BLACK,
        border_width=2,
        width=300,
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    divEtiqueta = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "Bipar Etiqueta",
                    size=20,
                    weight=600,
                ),
                inputEtiqueta,
                ft.ElevatedButton(
                    text="Buscar",
                    width=600,
                    on_click=lambda e: consultarEtiqueta(inputEtiqueta.value),
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=10,
    )
    return ft.View(
        route="/separar",
        controls=[
            header,
            title,
            ft.Container(height=20),
            divEtiqueta,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

