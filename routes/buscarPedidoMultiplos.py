import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def buscar_pedido(page: ft.Page, navigate_to, header):
    print("Entrou na tela de buscar pedido")
    matricula = user_info.get("matricula")
    codfilial = user_info.get("codfilial")

    def dialog_em_aberto():
        print("Entrou em abrir dialog")
        dialog_aberto = ft.AlertDialog(
            title=ft.Text("Você assim possui pedidos em aberto"),
            
        )
        page.open(dialog_aberto)
        # page.update() 

    # 1) Lista que vai acumulando todos os números de pedido
    pedidos: list[str] = []

    # 2) Componentes de UI
    input_numped = ft.TextField(
        label="Número do pedido",
        # prefix_icon=ft.icons.INSERT_DRIVE_FILE,
        border_radius=ft.border_radius.all(10),
        border_color=colorVariaveis['bordarInput'],
        border_width=2,
        width=300,
        keyboard_type=ft.KeyboardType.NUMBER,
        autofocus=True,
        on_submit=lambda e: abrir_dialog_manual(e),
    )
    button_buscar_manual = ft.ElevatedButton(
        text="Buscar Pedido Manual",
        bgcolor=colorVariaveis['botaoAcao'],
        color=colorVariaveis['texto'],
        width=600,
        # on_click=lambda e: print("Botão Buscar Pedido Manual clicado"),
        on_click=lambda e: abrir_dialog_manual(e),
    )
    button_buscar_automatico = ft.ElevatedButton(
        text="Buscar Pedido Automático",
        bgcolor=colorVariaveis['botaoAcao'],
        color=colorVariaveis['texto'],
        width=600,
        on_click=lambda e: pedido_automatico(),
    )

    # 3) Função auxiliar para snackbars
    def show_snack(message: str, error: bool = False):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=colorVariaveis['erro'] if error else colorVariaveis['sucesso'],
        )
        page.open(page.snack_bar)
        # page.snack_bar.open = True
        # page.update()

    def em_aberto(matricula, codfilial):
        try:
            resp = requests.post(
                f"{base_url}/buscarPedidoMultiplos",
                json={
                    "action": "aberto",
                    "matricula": matricula,
                    "codfilial": codfilial
                }
            )
            if resp.status_code == 201:
                print("Pedidos em aberto encontrados")
                dialog_em_aberto()
                show_snack("Pedidos em aberto encontrados")
            # elif resp.status_code == 200:
            #     show_snack("Pedidos em aberto processados")
            else:
                pass
                # show_snack("Nenhum pedido em aberto encontrado", error=True)
        except Exception as exc:
            print("Erro na requisição em aberto:", exc)
            show_snack("Erro na requisição em aberto", error=True)

    # 4) Requisição manual: envia lista de pedidos
    def pedido_manual(lista_de_pedidos: list[str]):
        try:
            resp = requests.post(
                f"{base_url}/buscarPedidoMultiplos",
                json={
                    "action": "manual",
                    "numped": lista_de_pedidos,
                    "matricula": matricula
                }
            )
            if resp.status_code == 200:
                show_snack("Pedidos manuais encontrados")
                navigate_to("/atribuir_etiqueta")
            elif resp.status_code == 201:
                show_snack("Pedidos manuais processados")
                navigate_to("/atribuir_etiqueta")
            else:
                show_snack("Nenhum pedido manual encontrado", error=True)
        except Exception as exc:
            print("Erro na requisição manual:", exc)
            show_snack("Erro na requisição manual", error=True)

    # 5) Requisição automática
    def pedido_automatico():
        try:
            resp = requests.post(
                f"{base_url}/buscarPedidoMultiplos",
                json={
                    "action": "automatico",
                    "matricula": matricula
                }
            )
            if resp.status_code == 200:
                show_snack("Pedido automático encontrado")
                navigate_to("/atribuir_etiqueta")
            elif resp.status_code == 201:
                show_snack("Pedido automático processado")
                navigate_to("/atribuir_etiqueta")
            else:
                show_snack("Nenhum pedido automático encontrado", error=True)
        except Exception as exc:
            print("Erro na requisição automática:", exc)
            show_snack("Erro na requisição automática", error=True)

    # 6) Dialog para pergunta “Mais algum pedido?”
    def abrir_dialog_manual(e):
        numped = input_numped.value.strip()
        if not numped:
            show_snack("Digite um número de pedido antes", error=True)
            return

        dialog = ft.AlertDialog(
            title=ft.Text("Mais pedidos?"),
            content=ft.Text("Deseja consultar outro pedido manualmente?"),
            actions=[
                ft.TextButton(
                    "Sim",
                    on_click=lambda ev: (
                        pedidos.append(numped),               # guarda o pedido atual
                        setattr(input_numped, "value", ""),   # limpa o campo
                        setattr(dialog, "open", False),       # fecha o dialog
                        page.update()
                    )
                ),
                ft.TextButton(
                    "Não",
                    on_click=lambda ev: (
                        pedidos.append(numped),               # guarda o último pedido
                        setattr(dialog, "open", False),
                        page.update(),
                        pedido_manual(pedidos)                # chama a requisição com toda a lista
                    )
                ),
            ]
        )
        page.open(dialog)
        # page.update()

    

    em_aberto(matricula, codfilial)

    # 7) Montagem da View
    return ft.View(
        route="/buscar_pedido",
        controls=[
            header,
            ft.Text("Buscar Pedido", size=24, weight="bold", color=colorVariaveis['titulo']),
            ft.Container(height=20),
            ft.Text("Busca Manual", size=18, weight="bold"),
            input_numped,
            button_buscar_manual,
            ft.Container(height=40),
            ft.Text("Busca Automática", size=18, weight="bold"),
            button_buscar_automatico,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
    )
