import flet as ft
import requests
from routes.config.config import colorVariaveis, base_url, user_info

def separar_multiplos_pedidos(page: ft.Page, navigate_to, header, arguments=None):
    print(f"Arguments recebidos: {arguments}")
    
    codfilial = user_info.get("codfilial")
    matricula = user_info.get("matricula")
    
    # Extrair os números dos pedidos de 'arguments' e formatar como string separada por vírgula
    numpeds_list = [str(arg.get("numped")) for arg in arguments] if arguments else []
    numpeds_str = ", ".join(numpeds_list)

    def buscar_itens_pedido(numpeds, codfilial):
        try:
            response = requests.get(
                f"{base_url}/separar_multiplos_pedido",
                params={
                    "numped": numpeds,
                    "codfilial": codfilial,
                    "matricula": matricula
                }
            )
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Erro ao buscar itens: {response.status_code}")
                return None
        except Exception as e:
            print(f"Exceção ao buscar itens: {e}")
            return None

    # Chamada inicial para buscar os itens
    dados_itens = buscar_itens_pedido(numpeds_str, codfilial)
    print(f"Itens recuperados: {dados_itens}")

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
