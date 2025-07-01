import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def separar_pedido_dist(page: ft.Page, navigate_to, header):
    matricula = user_info.get("matricula")
    print(f"User config na tela Separar Pedido Dist: {matricula}")

    titulo = ft.Text(
        "Separar Pedido de Distribuição",
        size=24, weight="bold",
        color=colorVariaveis['titulo']
    )
    tag = ft.Text(
        "Atenção: Esta funcionalidade está em desenvolvimento e não está disponível no momento.",
        size=16, weight="bold",
        color=colorVariaveis['erro']
    )

    return ft.View(
        route="/separar_pedido_dist",
        controls=[
            header,
            titulo,
            tag,
            ft.Container(height=20),
            ft.ElevatedButton(
                "Buscar Pedido",
                # expand=True,
                bgcolor=colorVariaveis['botaoAcao'],
                color=colorVariaveis['texto']
            )
        ]
    )