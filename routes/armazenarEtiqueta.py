import flet as ft
import requests
from routes.config.config import base_url

def buscar_etiqueta(navigate_to, header):

    def consultarEtiqueta(page, codetiqueta):
        try:
            response = requests.post(
                f"{base_url}/consultarEtiqueta",
                json={"codetiqueta": codetiqueta},
            )
            if response.status_code == 200:
                resposta = response.json()
                data = resposta.get("data", {})
                codprod = data.get("codprod")
                descricao = data.get("descricao")
                qt = data.get("qt")
                numbonus = data.get("numbonus")

                navigate_to("/enderecarProduto",
                            arguments={
                                "codprod": codprod,
                                "descricao": descricao,
                                "qt": qt,
                                "numbonus": numbonus
                            })
            else:
                print("Erro ao consultar o código de barras")
                snackbar_error = ft.SnackBar(
                        content=ft.Text(
                            f"Erro ao consultar o código de barras",
                            color=ft.colors.WHITE,
                            size=20,
                        ),
                        bgcolor=ft.colors.RED,
                        show_close_icon=True,
                    )
                page.snack_bar = snackbar_error
                snackbar_error.open = True
                page.update()
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
                    on_click=lambda e: consultarEtiqueta(e.page, inputEtiqueta.value),
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

