import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def separar_transferencia_devolucao(e, navigate_to, header):
    matricula = user_info.get('matricula')
    codfilial = user_info.get('codfilial')

    try:
        response = requests.post(
            f"{base_url}/buscar_dados_transferencia_devolucao",
            json={
                "matricula": matricula,
                "codfilial": codfilial
            }
        )
        if response.status_code == 200:
            dados = response.json()
            dados_itens = dados.get("dados_itens", [])
            dados_codbarras = dados.get("dados_codbarras", [])
            dados_resumo = dados.get("dados_resumo", [])
        else:
            print("Erro ao buscar dados")
            dados_itens, dados_codbarras, dados_resumo = [], [], []
    except Exception as exc:
        print(exc)
        dados_itens, dados_codbarras, dados_resumo = [], [], []

    title = ft.Text(
        "Separar Transferência/Devolução",
        size=24,
        weight="bold",
        color=colorVariaveis['titulo']
    )
    return ft.View(
        route="/separar_pedido",
        controls=[
            header,
            title,
        ]
    )