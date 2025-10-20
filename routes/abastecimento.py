import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def abastecimento(page: ft.Page, navigate_to, header):
    matricula = user_info.get("matricula")
    codfilial = user_info.get("codfilial")
    print(f"User config na tela Abastecimento: {matricula}")

    def snackbar(mensagem, bgcolor, page):
        snack = ft.SnackBar(
            content=ft.Text(
                mensagem,
                color="white"
            ),
            bgcolor=bgcolor)
        page.open(snack)
    def buscar_os(numos):
        if not numos:
            snackbar("Digite o numero da OS", colorVariaveis['erro'], page)
            return

        print(f"Buscar OS: {numos}")

        response = requests.post(
            base_url + "/abastecimento",
            json={
                "numos": numos,
                "matricula": matricula,
                "codfilial": codfilial,
                "action": "atribuir_os"
            },
        )
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.json()}")
        resposta = response.json()
        mensagem = resposta.get("message")
        print(mensagem)
        
        if response.status_code == 200:
            snackbar(mensagem, colorVariaveis['sucesso'], page)
            navigate_to("/separar_abastecimento", arguments={
                "num_os": numos,
            })
        elif response.status_code == 400:
            snackbar(mensagem, colorVariaveis['erro'], page)


    titulo = ft.Text(
        "Abastecimento",
        size=24, weight="bold",
        color=colorVariaveis['titulo']
    )
    input_numos = ft.TextField(
        label="Número OS",
        width=300,
        on_submit=lambda e: buscar_os(e.control.value)
    )
    button_buscar = ft.ElevatedButton(
        "Buscar OS",
        on_click=lambda e: buscar_os(input_numos.value)
    )
    button_buscar_automatixa = ft.ElevatedButton(
        "Buscar OS (Automático)",
        on_click=lambda e: buscar_os(input_numos.value)
    )
    # Retorna a view configurada
    return ft.View(
        route="/abastecimento",  # Define a rota da página
        controls=[header,
                titulo,
                input_numos,
                button_buscar,
                ft.Divider(),
                button_buscar_automatixa
        ]
    )