import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def cadastrar_codbarra(e, navigate_to, header):
    matricula = user_info['matricula']
    codfilial = user_info['codfilial']

    def cadastrar_produto(e, codbarra, codprod, qt):
        try:
            response = requests.post(
                f"{base_url}/cadastrar_codbarra",
                json={
                    "codbarra":codbarra,
                    "codprod":codprod,
                    "qt":qt
                }
            )
            if response.status_code == 200:
                dados = response.json()
                mensagem = dados.get("mensagem")
                print(f"Mensagem: {mensagem}")
                e.page.snack_bar = ft.SnackBar(
                content=ft.Text(mensagem),
                bgcolor=colorVariaveis['sucesso'],
                )
                e.page.snack_bar.open = True
                e.page.update()
                navigate_to("/cadastrar_codbarra")
            else:
                dados = response.json()
                mensagem = dados.get("mensagem")
                print(f"Mensagem: {mensagem}")
                e.page.snack_bar = ft.SnackBar(
                content=ft.Text(mensagem, color=colorVariaveis['texto']),
                bgcolor=colorVariaveis['erro'],
                )
                e.page.snack_bar.open = True
                e.page.update()
            
        except Exception as exc:
            print(exc)
            mensagem = f"Erro: {exc}"
            e.page.snack_bar = ft.SnackBar(
                content=ft.Text(mensagem, color=colorVariaveis['texto']),
                bgcolor=colorVariaveis['erro'],
                )
            e.page.snack_bar.open = True
            e.page.update()

    titulo = ft.Text(
        "Cadastrar Codbarras",
        size=24,
        weight="bold",
        color=colorVariaveis['titulo']
    )
    codbarra = ft.TextField(
        label="codbarra"
    )
    codprod = ft.TextField(
        label="codprod"
    )
    quantidade = ft.TextField(
        label="quantidade"
    )
    cadastrar = ft.ElevatedButton(
        text="cadastar",
        bgcolor=colorVariaveis['botaoAcao'],
        color=colorVariaveis['texto'],
        on_click=lambda e: cadastrar_produto(e, codbarra.value, codprod.value, quantidade.value)
    )

    return ft.View(
        route="/cadastrar_codbarra",
        controls=[
            header,
            titulo,
            ft.Divider(),
            codbarra,
            codprod,
            quantidade,
            cadastrar
        ]
    )