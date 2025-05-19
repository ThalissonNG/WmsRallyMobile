import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

# Variáveis globais para gerenciar etiquetas de cada pedido
current_tag_index = 0
numped_lista_global = []
etiquetas = []


def separar_pedido(page: ft.Page, navigate_to, header):
    global current_tag_index, numped_lista_global, etiquetas

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
            if response.status_code == 200:
                show_snack("Etiquetas atribuídas com sucesso!")
            else:
                show_snack("Erro ao atribuir etiquetas!", error=True)
        except Exception as e:
            print(f"Erro ao atribuir etiquetas: {e}")
            show_snack("Erro ao atribuir etiquetas!", error=True)

    # 1) Buscar lista de pedidos via API
    try:
        response = requests.post(
            f"{base_url}/separarPedido",
            json={
                "action": "buscar_pedidos",
                "matricula": matricula,
            }
        )
        if response.status_code == 200:
            dados = response.json()
            numped_lista = dados.get("numped_lista", [])
        else:
            numped_lista = []
    except Exception as e:
        print(f"Erro ao buscar pedidos: {e}")
        numped_lista = []

    # 2) Inicializar variáveis globais na primeira execução
    if not numped_lista_global:
        numped_lista_global = numped_lista
        etiquetas = [None] * len(numped_lista_global)
        current_tag_index = 0

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

    # 5) Exibir próximo pedido e campo para inserir etiqueta
    def mostrar_proximo():
        container_dinamico.controls.clear()
        if current_tag_index < len(numped_lista_global):
            numped = numped_lista_global[current_tag_index]
            texto_pedido = ft.Text(f"Pedido: {numped}", size=18)
            campo_etiqueta = ft.TextField(label="Etiqueta", width=300)
            botao_salvar = ft.ElevatedButton(
                text="Salvar",
                on_click=lambda e: salvar_etiqueta(e, campo_etiqueta.value)
            )
            container_dinamico.controls.extend([texto_pedido, campo_etiqueta, botao_salvar])
        else:
            finalizar_etiquetas()
        page.update()

    # 6) Salvar etiqueta e avançar para o próximo pedido
    def salvar_etiqueta(e, valor: str):
        global etiquetas, current_tag_index
        etiquetas[current_tag_index] = valor
        current_tag_index += 1
        mostrar_proximo()

    # 7) Quando todas as etiquetas forem atribuídas
    def finalizar_etiquetas():
        # TODO: Chamar atribuir_etiqueta() para enviar ao backend
        print("Etiquetas atribuídas:", etiquetas)
        print("Lista de pedidos:", numped_lista_global)
        atribuir_etiqueta()
        container_dinamico.controls.clear()
        mensagem_final = ft.Text("Todas as etiquetas foram atribuídas!", size=18, weight="bold")
        container_dinamico.controls.append(mensagem_final)
        # show_snack("Processo concluído com sucesso")
        page.update()

    # 8) Carregar o primeiro pedido ao iniciar
    mostrar_proximo()

    # 9) Montar e retornar a View
    return ft.View(
        route="/separar_pedido",
        controls=[
            header,
            title,
            ft.Divider(),
            container_dinamico
        ],
        scroll=ft.ScrollMode.AUTO
    )
