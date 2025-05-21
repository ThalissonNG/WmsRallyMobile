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
            controls=[ft.Text("Implementar fluxo de escaneamento aqui.")],
            expand=True
        )
    )

    # Montar lista de itens do resumo em layout responsivo (3 linhas por item)
    resumo_items = []
    for grupo in dados_resumo:
        for item in grupo:
            # Se não iniciou (restante == 0), não aplica cor; caso contrário, define conforme status
            if item[6] == 0:
                linha_cor = None
                text_color = None
            elif item[5] == item[4]:
                linha_cor = colorVariaveis['sucesso']
                text_color = ft.colors.BLACK
            elif item[5] > item[4]:
                linha_cor = colorVariaveis['erro']
                text_color = ft.colors.WHITE
            else:
                linha_cor = colorVariaveis.get('restante', None)
                text_color = ft.colors.WHITE

            # Define cor do texto: branco em caso de erro, preto caso contrário
            # text_color = ft.colors.WHITE if linha_cor == colorVariaveis['erro'] else ft.colors.BLACK

            resumo_items.append(
                ft.Container(
                    padding=ft.padding.all(8),
                    bgcolor=linha_cor,
                    content=ft.Column(
                        spacing=4,
                        controls=[
                            # Linha 0: numpedido
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text(
                                        f"PEDIDO: {item[7]}",
                                        width=80,
                                        color=text_color,
                                        weight="bold"
                                    ),
                                ]
                            ),
                            # Linha 1: codprod, codfab, origem
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text(f"CODPROD: {item[0]}", width=80, color=text_color),
                                    ft.Text(f"CODFAB: {item[1]}", width=60, color=text_color),
                                    ft.Text(
                                        f"ORIGEM: {item[3]}" if item[3] is not None else "ORIGEM:",
                                        width=60,
                                        color=text_color
                                    ),
                                ]
                            ),
                            # Linha 2: descricao
                            ft.Text(f"DESCRICAO: {item[2]}", color=text_color),
                            # Linha 3: ped, sep, rest
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text(f"P:{item[4]}", width=50, weight="bold", color=text_color),
                                    ft.Text(f"S:{item[5]}", width=50, weight="bold", color=text_color),
                                    ft.Text(f"R:{item[6]}", width=50, weight="bold", color=text_color),
                                ]
                            ),
                        ]
                    )
                )
            )
            resumo_items.append(ft.Divider())

    # Aba "Resumo"
    resumo_tab = ft.Tab(
        text="Resumo",
        content=ft.Column(
            expand=True,
            controls=[
                ft.Text("Resumo do pedido:", color=colorVariaveis['titulo']),
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
            controls=[ft.Text("Tela de finalização: implementar resumo e botão concluir.", color=colorVariaveis['titulo'])],
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
        controls=[header, title, tabs],
        scroll=ft.ScrollMode.AUTO
    )