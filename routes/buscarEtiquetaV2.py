import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def buscar_etiqueta_v2(page: ft.Page, navigate_to, header):
    codfilial = user_info.get("codfilial")
    matricula = user_info.get("matricula")

    titulo = ft.Text(
        "Buscar Etiqueta",
        size=24, weight="bold",
        color=colorVariaveis['titulo']
    )
    etiqueta_input = ft.TextField(
        label="Código da Etiqueta",
        border_radius=ft.border_radius.all(10),
        border_color=colorVariaveis['bordarInput'],
        border_width=2,
        on_submit=lambda e: buscar_etiqueta(etiqueta_input.value),
        autofocus=True
    )
    confirm_button = ft.ElevatedButton(
        text="Confirmar",
        bgcolor=colorVariaveis['botaoAcao'],
        color=colorVariaveis['texto'],
        width=300,
        on_click=lambda e: buscar_etiqueta(etiqueta_input.value)
    )

    def snack_bar(mensagem, bgcolor, color, page):
        snack = ft.SnackBar(
            content=ft.Text(
                mensagem,
                color="white"
            ),
            bgcolor=bgcolor
        )
        page.open(snack)
    
    def buscar_etiqueta(codetiqueta):
        if not codetiqueta:
            snack_bar("Código da etiqueta não informado", colorVariaveis['erro'], "white", page)
            return None

        try:
            response = requests.post(
                f"{base_url}/buscar_etiqueta/{codetiqueta}",
                json={
                    "matricula": matricula
                }
            )
            resposta = response.json()

            if response.status_code == 200:
                mensagem = resposta.get("message")
                snack_bar(mensagem, colorVariaveis['sucesso'], colorVariaveis['textoPreto'], page)
                
                navigate_to("/armazenar_etiqueta_v2", arguments={
                    "codetiqueta": codetiqueta
                })
            else:
                mensagem = resposta.get("message")
                snack_bar(mensagem, colorVariaveis['erro'], "white", page)
        except Exception as e:
            print(f"Erro ao buscar etiqueta: {str(e)}")
            return None

    return ft.View(
        route="/armazenar_etiqueta_v2",
        controls=[
            header,
            titulo,
            etiqueta_input,
            confirm_button
        ]
    )