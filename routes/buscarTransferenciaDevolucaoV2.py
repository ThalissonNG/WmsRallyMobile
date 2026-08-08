import flet as ft
import requests

from routes.config.config import base_url, colorVariaveis, user_info


def buscar_transferencia_devolucao_v2(page: ft.Page, navigate_to, header):
    matricula = user_info.get("matricula")
    codfilial = user_info.get("codfilial")

    def mostrar_mensagem(mensagem, sucesso=False):
        page.open(
            ft.SnackBar(
                content=ft.Text(mensagem, color="white"),
                bgcolor=(
                    colorVariaveis["sucesso"]
                    if sucesso
                    else colorVariaveis["erro"]
                ),
            )
        )

    def iniciar_separacao(e):
        numnota = input_numnota.value.strip()
        codfornec = input_codfornec.value.strip()

        if not numnota or not codfornec:
            mostrar_mensagem("Informe o número da nota e o código do fornecedor.")
            return

        try:
            numnota = int(numnota)
            codfornec = int(codfornec)
        except ValueError:
            mostrar_mensagem("Nota e fornecedor devem ser números válidos.")
            return

        botao_iniciar.disabled = True
        page.update()

        try:
            response = requests.post(
                f"{base_url}/transferenciaDevolucaoV2/iniciar",
                json={
                    "numnota": numnota,
                    "codfornec": codfornec,
                    "codfilial": codfilial,
                    "matricula": matricula,
                },
                timeout=30,
            )
            try:
                resposta = response.json()
            except ValueError:
                resposta = {}

            if response.status_code == 200 and resposta.get("success") is True:
                navigate_to(
                    "/separar_transferencia_devolucao_v2",
                    arguments={"numnota": numnota},
                )
                return

            mostrar_mensagem(
                resposta.get("message", "Não foi possível iniciar a separação.")
            )
        except requests.RequestException as exc:
            mostrar_mensagem(f"Erro de comunicação com a API: {exc}")
        finally:
            botao_iniciar.disabled = False
            if botao_iniciar.page:
                page.update()

    input_numnota = ft.TextField(
        label="Número da Nota",
        autofocus=True,
        keyboard_type=ft.KeyboardType.NUMBER,
        on_submit=iniciar_separacao,
    )
    input_codfornec = ft.TextField(
        label="Código do Fornecedor",
        keyboard_type=ft.KeyboardType.NUMBER,
        on_submit=iniciar_separacao,
    )
    botao_iniciar = ft.ElevatedButton(
        "Buscar e iniciar separação",
        expand=True,
        bgcolor=colorVariaveis["botaoAcao"],
        color=colorVariaveis["texto"],
        on_click=iniciar_separacao,
    )

    return ft.View(
        route="/buscar_transferencia_devolucao_v2",
        controls=[
            header,
            ft.Text(
                "Transferência V2",
                size=24,
                weight="bold",
                color=colorVariaveis["titulo"],
            ),
            ft.Container(height=10),
            ft.Text("Informe a nota e o fornecedor para iniciar ou retomar."),
            input_numnota,
            input_codfornec,
            ft.Row(controls=[botao_iniciar]),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
    )
