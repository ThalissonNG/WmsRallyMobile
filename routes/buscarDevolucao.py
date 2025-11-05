import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def buscar_devolucao(e, navigate_to, header):
    matricula = user_info.get('matricula')
    codfilial = user_info.get('codfilial')
    print(matricula)

    def transferencia_devolucao(codfornec, numnota, codfilial):
        try:
            response = requests.post(
                f"{base_url}/consultar_devolucao",
                json={
                    "numnota": numnota,
                    "codfornec": codfornec,
                    "codfilial": codfilial,
                    "matricula": matricula
                }
            )
            if response.status_code == 200:
                dados = response.json()
                numnota_separar = dados.get("numnota")
                print(f"numnota: {numnota_separar}")
                print("Iniciada separação")
                navigate_to("/separar_devolucao",
                    arguments={
                        "numnota": numnota
                    }
                )
            elif response.status_code == 202:
                dados = response.json()
                numnota_separar = dados.get("numnota")
                print(f"numnota: {numnota_separar}")
                print("Iniciada separação")
                print("Separação em andamento")
                navigate_to("/separar_devolucao",
                    arguments={
                        "numnota": numnota
                    }
                )
            elif response.status_code == 404:
                print("Não tem pedido")
        except Exception as exc:
            print(exc)

    title = ft.Text(
        "Buscar Devolução",
        size=24,
        weight="bold",
        color=colorVariaveis['titulo']
    )
    buscar = ft.Text(
        "Buscar",
        size=18,
        weight="bold",
    )
    Numnota = ft.TextField(
        label="Número da Nota",
        # prefix_icon=ft.icons.INSERT_DRIVE_FILE,
        border_radius=ft.border_radius.all(10),
        border_color=colorVariaveis['bordarInput'],
        border_width=2,
        width=300,
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    codfornec = ft.TextField(
        label="Código fornecedor",
        # prefix_icon=ft.icons.INSERT_DRIVE_FILE,
        border_radius=ft.border_radius.all(10),
        border_color=colorVariaveis['bordarInput'],
        border_width=2,
        width=300,
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    buttonBuscarPedido = ft.ElevatedButton(
        text="Buscar",
        bgcolor=colorVariaveis['botaoAcao'],
        color=colorVariaveis['texto'],
        width=600,
        on_click=lambda e: transferencia_devolucao(codfornec.value, Numnota.value, codfilial)
    )
    return ft.View(
        route="/buscar_devolucao",
        controls=[
            header,
            title,
            ft.Container(height=20),
            buscar,
            Numnota,
            codfornec,
            buttonBuscarPedido,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
