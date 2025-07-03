import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def buscar_bonus(page: ft.Page, navigate_to, header):
    matricula = user_info.get("matricula")
    codfilial = user_info.get("codfilial")
    print(f"User config na tela conferir bonus: {matricula}")

    def snackbar(mensagem, bgcolor, page):
        snack = ft.SnackBar(
            content=ft.Text(
                mensagem,
                color="white"
            ),
            bgcolor=bgcolor)
        page.open(snack)

    def consultar_bonus(numbonus, codfilial, matricula):
        response = requests.post(
            base_url + "/buscar_bonus",
            json={
                "numbonus": numbonus,
                "codfilial": codfilial,
                "matricula": matricula
            },
        )
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.json()}")

        resposta = response.json()
        mensagem = resposta.get("message")
        print(mensagem)
        if response.status_code == 200:
            snackbar(mensagem, colorVariaveis['sucesso'], page)
        elif response.status_code == 201:
            snackbar(mensagem, colorVariaveis['restante'], page)
        elif response.status_code == 400:
            snackbar(mensagem, colorVariaveis['erro'], page)

    titulo = ft.Text(
        "Conferir Bonus",
        size=24, weight="bold",
        color=colorVariaveis['titulo']
    )
    numbonus_campo = ft.TextField(
        label="Numero do Bonus",
    )
    buscar_numbonus = ft.ElevatedButton(
        "Buscar",
        bgcolor=colorVariaveis['botaoAcao'],
        color=colorVariaveis['texto'],
        on_click=lambda e: consultar_bonus(
            numbonus_campo.value,
            codfilial,
            matricula
        ),
    )

    return ft.View(
        route="/buscar_bonus",
        controls=[
            header,
            titulo,
            ft.Container(height=20),
            numbonus_campo,
            ft.Container(height=20),
            buscar_numbonus
        ]
    )