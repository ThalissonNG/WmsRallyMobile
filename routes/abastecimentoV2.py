import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def abastecimentoV2(page: ft.Page, navigate_to, header):
    matricula = user_info.get("matricula")
    codfilial = user_info.get("codfilial")
    def snackbar(mensagem, bgcolor, page):
        snack = ft.SnackBar(
            content=ft.Text(
                mensagem,
                color="white"
            ),
            bgcolor=bgcolor)
        page.open(snack)
    
    def buscar_os(numos=None):
        # if not numos:
        #     snackbar("Digite o numero da OS", colorVariaveis['erro'], page)
        #     return

        print(f"Buscar OS: {numos}")

        response = requests.post(
            base_url + "/abastecimentoV2",
            json={
                "numos": numos,
                "matricula": matricula,
                "codfilial": codfilial,
            },
        )
        # print(f"Status code: {response.status_code}")
        # print(f"Response: {response.json()}")
        
        resposta = response.json()
        mensagem = resposta.get("message")
        numos_atribuida = resposta.get("numos")
        # print(mensagem, numos_atribuida)
        
        if response.status_code == 200:
            snackbar(mensagem, colorVariaveis['sucesso'], page)
            navigate_to("/separar_abastecimentoV2", arguments={
                "num_os": numos_atribuida,
            })
        else:   
            snackbar(mensagem, colorVariaveis['erro'], page)
    
    titulo = ft.Text(
        "Abastecimento V2",
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
        on_click=lambda e: buscar_os()
    )
    return ft.View(
        route="/abastecimento",  # Define a rota da página
        controls=[
            header,
            titulo,
            input_numos,
            button_buscar,
            ft.Divider(),
            button_buscar_automatixa
        ]
    )