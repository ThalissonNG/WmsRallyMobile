import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def os_avulsa_entrada(e, navigate_to, header):
    matricula = user_info['matricula']
    codfilial = user_info['codfilial']

    resultado_container = ft.Container()

    def consultar_os_avulsa_entrada(codfilial, matricula):
        try:
            response = requests.post(
                f"{base_url}/os_avulsa_entrada",
                json={
                    "matricula": matricula,
                    "codfilial": codfilial,
                    "action": "consultar"
                }
            )
            if response. status_code == 200 or response. status_code == 201:
                dados = response.json()
                dados_os = dados.get("dados_os", [])
                print(f"dados recebidos: {dados_os}")
                mostrar_campo_codbarra(e, dados_os)
            else:
                print("Erro ao buscar OS Avulsa - entrada")
                print(response.status_code, response.text)
        except Exception as exc:
            print(exc)
    
    def confirmar_codbarra(dados_os, codbarra, numos):
        response = requests.post(
            f"{base_url}/os_avulsa_entrada",
            json={
                "codbarra": codbarra,
                "numos": numos,
                "matricula": matricula,
                "codfilial": codfilial,
                "action": "validar_codbarra"
            }
        )
        if response. status_code == 200:
            print("Código de barras válido")
            dados = response.json()
            codprod = dados.get("codprod")
            print(f"codprod: {codprod}")
        else:
            print("Erro ao buscar OS Avulsa - entrada")
            print(response.status_code, response.text)

    def mostrar_campo_codbarra(e, dados_os):
        campo = ft.TextField(label="Código de Barras")
        btn = ft.ElevatedButton(
            text="Validar Código de Barras",
            on_click=lambda e: confirmar_codbarra(dados_os, campo.value, dados_os[0][0])
        )
        # atualiza o container placeholder
        resultado_container.content = ft.Column(
            controls=[
                ft.Text(f"numos: {dados_os[0][0]}"),
                ft.Text(f"codprod: {dados_os[0][1]}"),
                campo,
                btn
            ]
        )
        e.page.update()

    consultar_os_avulsa_entrada(codfilial, matricula)

    titulo = ft.Text(
        "OS Avulsa - Entrada",
        size=24,
        weight="bold",
        color=colorVariaveis['titulo']
    )
    codbarra = ft.TextField(
        label="Código de Barras"
    )
    validar_codbarra = ft.ElevatedButton(
        text="Validar Código de Barras",
        on_click=lambda e: confirmar_codbarra(e, codbarra.value)
    )

    return ft.View(
        route="/cadastrar_codbarra",
        controls=[
            header,
            titulo,
            ft.Divider(),
            resultado_container
        ]
    )