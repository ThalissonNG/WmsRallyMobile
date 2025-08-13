import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info


def buscar_pedido_unico(page: ft.Page, navigate_to, header):
    matricula = user_info.get("matricula")
    codfilial = user_info.get("codfilial")
    print(f"User config na tela Buscar Pedido Único: {matricula}, Filial: {codfilial}")

    def snack_bar(message, cor_texto, color, page):
        page.snack_bar = ft.SnackBar(
            ft.Text(
                message,
                color=cor_texto
                ),
            bgcolor=color,
            duration=1000
        )
        page.open(page.snack_bar)
    
    def dialog_pedido_aberto(page, mensagem: str, numped: int | None):
        info_pedido = f"Pedido em aberto: {numped[0][0]}" if numped is not None else "Há um pedido em aberto."

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Atenção"),
            content=ft.Column(
                tight=True,
                spacing=8,
                controls=[
                    ft.Text(mensagem),
                    ft.Text(info_pedido, weight="bold"),
                ],
            ),
            actions_alignment=ft.MainAxisAlignment.START,
            actions=[
                ft.Column(
                    width="100%",
                    spacing=10,
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        ft.ElevatedButton(
                            "OK",
                            bgcolor=colorVariaveis['botaoAcao'],
                            color=colorVariaveis['texto'],
                            on_click=lambda e, d=None: (e.page.close(dlg), e.page.update())
                        ),
                        ft.Container(height=30),
                        ft.ElevatedButton(
                            "Finalizar Pedido",
                            bgcolor=ft.Colors.RED,
                            color=colorVariaveis['texto'],
                            on_click=lambda e, d=None: (
                                finalizar_pedido(numped[0][0]),
                                e.page.close(dlg), e.page.update()
                                )
                        )
                    ]
                ),
            ],
        )
        page.open(dlg)
        page.update()

    def verificar_pedido_aberto(matricula, codfilial):
        try:
            response = requests.post(
                f"{base_url}/buscarPedidoUnico",
                json={
                    "matricula": matricula,
                    "codfilial": codfilial,
                    "action": "verificar_pedido_aberto"
                }
            )
            print(f"Status code verificar pedido aberto: {response.status_code}")
            print(f"Response verificar pedido aberto: {response.json()}")
            if response.status_code == 202:
                print("Pedido já aberto.")
                mensagem = response.json().get("message")
                numped = response.json().get("numped_aberto")
                dialog_pedido_aberto(page, mensagem, numped)
                return True
            else:
                return False
        except requests.exceptions.RequestException as e:
            print(f"Erro ao fazer a requisição: {e}")
            return False

    def buscar_pedido(numped, matricula, codfilial):
        print(f"Entrou em buscar pedido: {numped}, {matricula}, {codfilial}")
        if not numped:
            snack_bar(
                "Número do pedido não pode ser vazio!",
                colorVariaveis['texto'],
                colorVariaveis['erro'],
                page)
            page.update()
            return
        
        try:
            response = requests.post(
                f"{base_url}/buscarPedidoUnico",
                json={
                    "numped": numped,
                    "matricula": matricula,
                    "codfilial": codfilial,
                    "action": "buscar_pedido"
                }
            )
            # response.raise_for_status()
            print(f"Status code: {response.status_code}")
            print(f"Response: {response.json()}")

            if response.status_code == 200:
                print("Pedido encontrado com sucesso!")
                # navigate_to("/atribuir_etiqueta")
            elif response.status_code == 500:
                mensagem = response.json().get("message")
                snack_bar(
                    f"Erro: {mensagem}",
                    colorVariaveis['texto'],
                    colorVariaveis['erro'],
                    page
                )
                # navigate_to("/atribuir_etiqueta")
            elif response.status_code == 202:
                print("Pedido já separado.")
                # navigate_to("/atribuir_etiqueta")
            else:
                snack_bar(
                    "Erro ao buscar pedido. Verifique o número do pedido.",
                    colorVariaveis['texto'],
                    colorVariaveis['erro'],
                    page)
                page.update()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao fazer a requisição: {e}")
            snack_bar(
                "Erro ao buscar pedido. Tente novamente mais tarde.",
                colorVariaveis['texto'],
                colorVariaveis['erro'],
                page)
            page.update()

    def finalizar_pedido(numped):
        print(f"Finalizando pedido: {numped}")
        try:
            response = requests.post(
                f"{base_url}/buscarPedidoUnico",
                json={
                    "numped": numped,
                    "matricula": matricula,
                    "codfilial": codfilial,
                    "action": "finalizar_pedido"
                }
            )
            if response.status_code == 200:
                snack_bar(
                    "Pedido finalizado com sucesso!",
                    colorVariaveis['textoPreto'],
                    colorVariaveis['sucesso'],
                    page)
            else:
                snack_bar(
                    "Erro ao finalizar pedido.",
                    colorVariaveis['texto'],
                    colorVariaveis['erro'],
                    page)
        except requests.exceptions.RequestException as e:
            print(f"Erro ao fazer a requisição: {e}")
            snack_bar(
                "Erro ao finalizar pedido. Tente novamente mais tarde.",
                colorVariaveis['texto'],
                colorVariaveis['erro'],
                page)

    verificar_pedido_aberto(matricula, codfilial)

    title = ft.Text(
        "Separar Pedido",
        size=24,
        weight="bold",
        color=colorVariaveis['titulo'],
        text_align="center"
    )
    input_numped = ft.TextField(
        label="Número do pedido",
        border_radius=ft.border_radius.all(10),
        # border_color=colorVariaveis['bordarInput'],
        border_width=2,
        keyboard_type=ft.KeyboardType.NUMBER,
        autofocus=True,
        on_submit=lambda e: buscar_pedido(input_numped.value, matricula, codfilial),
    )
    btn_buscarPedido = ft.ElevatedButton(
        text="Buscar Pedido",
        bgcolor=colorVariaveis['botaoAcao'],
        color=colorVariaveis['texto'],
        width=600,
        on_click=lambda e: buscar_pedido(input_numped.value, matricula, codfilial),
    )

    return ft.View(
        route="/buscar_pedido_unico",
        controls=[
            header,
            title,
            input_numped,
            btn_buscarPedido,
        ]
    )