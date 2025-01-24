import flet as ft
import requests
from routes.config.config import base_url

def buscar_etiqueta(navigate_to, header):

    def consultarEtiqueta(numetiqueta):
        try:
            response = requests.post(
                f"{base_url}/bonusConsultar",
                json={"numbonus": numetiqueta},
            )
            if response.status_code == 200:
                bonus = response.json()
                print(bonus)
                navigate_to("/enderecarBonus")
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
    numetiqueta = ft.TextField(
        label="Digite o número do bônus...",
        prefix_icon=ft.icons.SEARCH,
        border_radius=ft.border_radius.all(10),
        border_color=ft.colors.BLACK,
        border_width=2,
        width=300,
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    busca_manual = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "Busca Manual",
                    size=20,
                    weight=600
                ),
                numetiqueta,
                ft.ElevatedButton(
                    text="Buscar",
                    width=600,
                    on_click=lambda e: consultarEtiqueta(numetiqueta.value),
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        border=ft.border.all(
            color="black",
            width=2,
        ),
        border_radius=ft.border_radius.all(10),
        padding=10,
    )
    return ft.View(
        route="/separar",
        controls=[
            header,
            title,
            busca_manual,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.alignment.center,
        expand=True,
    )

