import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def os_avulsa(e, navigate_to, header):
    titulo = ft.Text(
        "OS Avulsa",
        size=24,
        weight="bold",
        color=colorVariaveis['titulo']
    )

    saida_avulsa = ft.ElevatedButton(
        text="Saida Avulsa",
        bgcolor=colorVariaveis['botaoAcao'],
        color=colorVariaveis['texto'],
        # on_click=lambda e: print("Saida Avulsa")
        on_click=lambda e: navigate_to("/os_avulsa_saida")
    )

    entrada_avulsa = ft.ElevatedButton(
        text="Entrada Avulsa",
        bgcolor=colorVariaveis['botaoAcao'],
        color=colorVariaveis['texto'],
        # on_click=lambda e: print("Entrada Avulsa"),
        on_click=lambda e: navigate_to("/os_avulsa_entrada")
    )

    return ft.View(
        route="/cadastrar_codbarra",
        controls=[
            header,
            titulo,
            ft.Divider(),
            ft.Row(
                controls=[
                    saida_avulsa,
                    entrada_avulsa
                ]
            )
        ]
    )