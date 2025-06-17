import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def os_avulsa_saida(e, navigate_to, header):
    matricula = user_info['matricula']
    codfilial = user_info['codfilial']

    def consultar_os_avulsa_saida(codfilial, matricula):
        try:
            response = requests.post(
                f"{base_url}/os_avulsa_saida",
                json={
                    "matricula": matricula,
                    "codfilial": codfilial
                }
            )
            if response. status_code == 200:
                print("OS Avulsa - Saida")
            else:
                print("Erro ao buscar OS Avulsa - Saida")
                print(response.status_code, response.text)
        except Exception as exc:
            print(exc)
    
    consultar_os_avulsa_saida(codfilial, matricula)

    titulo = ft.Text(
        "OS Avulsa - Saida",
        size=24,
        weight="bold",
        color=colorVariaveis['titulo']
    )

    return ft.View(
        route="/cadastrar_codbarra",
        controls=[
            header,
            titulo,
            ft.Divider(),
        ]
    )