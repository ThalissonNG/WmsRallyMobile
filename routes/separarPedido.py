import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info


def separar_pedido(page: ft.Page, navigate_to, header):
    # Matrícula do usuário logado
    matricula = user_info.get("matricula")

    # Função para exibir snackbars de feedback
    def show_snack(message: str, error: bool = False):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=colorVariaveis['erro'] if error else colorVariaveis['sucesso'],
            action=ft.IconButton(
                icon=ft.icons.CLOSE,
                on_click=lambda ev: setattr(page.snack_bar, "open", False) or page.update()
            )
        )
        page.snack_bar.open = True
        page.update()

    # Requisição para buscar dados da separação
    def buscar_itens():
        try:
            response = requests.post(
                f"{base_url}/separarPedido",
                json={"action": "buscar_dados", "matricula": matricula}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            show_snack(f"Erro ao buscar itens: {e}", error=True)
            return {}

    dados = buscar_itens()
    dados_resumo = dados.get("dados_resumo", [])

    # Título da página
    title = ft.Text(
        "Separar Pedido",
        size=24,
        weight="bold",
        color=colorVariaveis['titulo'],
        text_align="center"
    )

    # Aba "Separar"
    separar_tab = ft.Tab(
        text="Separar",
        content=ft.Column(
            controls=[
                ft.Text("Implementar fluxo de escaneamento aqui."),
            ],
            expand=True
        )
    )

    # Montar lista de itens do resumo em layout responsivo (3 linhas por item)
    resumo_items = []
    for grupo in dados_resumo:
        for item in grupo:
            resumo_items.append(
                ft.Container(
                    padding=ft.padding.all(8),
                    content=ft.Column(
                        spacing=4,
                        controls=[
                            # Linha 1: codprod, codfab, origem
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text(f"CODPROD: {str(item[0])}", width=80),  # codprod
                                    ft.Text(f"CODFAV: {str(item[1])}", width=60),                 # codfab
                                    ft.Text(f"ORIGEM: {str(item[3])}", width=60),  # origem
                                ]
                            ),
                            # Linha 2: descricao (auto-wrap)
                            ft.Text(f"DESCRICAO: {item[2]}"),
                            # Linha 3: ped, sep, rest
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text(f"P:{item[4]}", width=50, weight="bold"),
                                    ft.Text(f"S:{item[5]}", width=50, weight="bold"),
                                    ft.Text(f"R:{item[6]}", width=50, weight="bold"),
                                ]
                            ),
                        ]
                    )
                )
            )
            # Adiciona divisor entre itens
            resumo_items.append(ft.Divider())

    # Aba "Resumo"
    resumo_tab = ft.Tab(
        text="Resumo",
        content=ft.Column(
            expand=True,
            controls=[
                ft.Text("Resumo do pedido:"),
                ft.ListView(
                    expand=True,
                    spacing=4,
                    padding=ft.padding.symmetric(vertical=8),
                    controls=resumo_items
                )
            ]
        )
    )

    # Aba "Finalizar"
    finalizar_tab = ft.Tab(
        text="Finalizar",
        content=ft.Column(
            controls=[
                ft.Text("Tela de finalização: implementar resumo e botão concluir."),
            ],
            expand=True
        )
    )

    # Componente de abas
    tabs = ft.Tabs(
        selected_index=1,
        tabs=[separar_tab, resumo_tab, finalizar_tab],
        expand=True
    )

    # Retorna a View com abas
    return ft.View(
        route="/separar_pedido",
        controls=[
            header,
            title,
            tabs
        ],
        scroll=ft.ScrollMode.AUTO
    )
