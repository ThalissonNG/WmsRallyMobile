import flet as ft
from routes.config.config import colorVariaveis

def separar_multiplos_pedidos(page: ft.Page, navigate_to, header, arguments=None):
    print(arguments)
    titulo = ft.Text(
        "Separar Múltiplos Pedidos",
        size=24, weight="bold",
        color=colorVariaveis['titulo']
    )

    # Abas placeholder
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Separar",
                content=ft.Container(
                    content=ft.Text("Conteúdo da aba Separar", size=16),
                    padding=20
                ),
            ),
            ft.Tab(
                text="Resumo",
                content=ft.Container(
                    content=ft.Text("Conteúdo da aba Resumo", size=16),
                    padding=20
                ),
            ),
            ft.Tab(
                text="Finalizar",
                content=ft.Container(
                    content=ft.Text("Conteúdo da aba Finalizar", size=16),
                    padding=20
                ),
            ),
        ],
        expand=1,
    )

    return ft.View(
        route="/separar_multiplos_pedidos",
        controls=[
            header,
            titulo,
            ft.Container(height=10),
            tabs
        ]
    )
