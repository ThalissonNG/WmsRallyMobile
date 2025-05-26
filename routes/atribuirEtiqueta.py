import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

# Variáveis globais para gerenciar etiquetas de cada pedido
digit_index = 0
numped_lista_global = []
etiquetas = []


def atribuir_etiqueta_pedido(page: ft.Page, navigate_to, header):
    global digit_index, numped_lista_global, etiquetas

    # Recupera a matrícula do usuário logado
    matricula = user_info.get('matricula')

    # Função para exibir mensagens de feedback (snackbar)
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

    # Função para enviar as etiquetas atribuídas ao backend
    def atribuir_etiqueta():
        try:
            response = requests.post(
                f"{base_url}/separarPedido",
                json={
                    "action": "atribuir_etiqueta",
                    "matricula": matricula,
                    "numped": numped_lista_global,
                    "etiquetas": etiquetas
                }
            )
            if response.status_code == 201:
                show_snack("Etiquetas atribuídas com sucesso!")
                navigate_to("/separar_pedido")
            else:
                show_snack("Erro ao atribuir etiquetas!", error=True)
        except Exception:
            show_snack("Erro ao atribuir etiquetas!", error=True)

    # 1) Buscar lista de pedidos via API
    try:
        resp = requests.post(
            f"{base_url}/separarPedido",
            json={"action": "buscar_pedidos", "matricula": matricula}
        )
        dados = resp.json() if resp.status_code == 200 else {}
        numped_lista = dados.get("numped_lista", [])
    except Exception:
        numped_lista = []

    # 2) Inicializar variáveis globais na primeira execução
    if not numped_lista_global:
        numped_lista_global = numped_lista
        etiquetas = [None] * len(numped_lista_global)
        digit_index = 0

    # 3) Título da tela
    title = ft.Text(
        "Separar Pedido - Atribuir Etiquetas",
        size=24,
        weight="bold",
        color=colorVariaveis['titulo'],
        text_align="center"
    )

    # 4) Container dinâmico para exibir cada pedido e campo de entrada
    container_dinamico = ft.Column(expand=True, alignment=ft.MainAxisAlignment.CENTER)

    # 5) Função para exibir próximo pedido
    def mostrar_proximo():
        container_dinamico.controls.clear()
        if digit_index < len(numped_lista_global):
            numped = numped_lista_global[digit_index]
            texto_pedido = ft.Text(f"Pedido: {numped}", size=18)
            campo_etiqueta = ft.TextField(label="Etiqueta", width=300)
            botao_salvar = ft.ElevatedButton(
                text="Salvar",
                on_click=lambda e: salvar_etiqueta(e, campo_etiqueta.value)
            )
            container_dinamico.controls.extend([texto_pedido, campo_etiqueta, botao_salvar])
        else:
            atribuir_etiqueta()
        page.update()

    # 6) Salvar etiqueta e avançar
    def salvar_etiqueta(e, valor: str):
        global etiquetas, digit_index
        etiquetas[digit_index] = valor
        digit_index += 1
        mostrar_proximo()

    # 7) Carregar o primeiro pedido ao iniciar
    mostrar_proximo()

    # 8) Retornar a view
    return ft.View(
        route="/atribuir_etiqueta",
        controls=[
            header,
            title,
            ft.Divider(),
            container_dinamico
        ],
        scroll=ft.ScrollMode.AUTO
    )


# Execução standalone
if __name__ == "__main__":
    ft.app(target=atribuir_etiqueta_pedido)
