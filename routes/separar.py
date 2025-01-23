import flet as ft

def separar_page(navigate_to, header):
    """
    Função para criar a tela de Separar Pedido como uma View.
    """
    title = ft.Text("Separar Pedido", size=24, weight="bold", color="blue")

    # Retorna a view configurada para a página de separar pedido
    return ft.View(
        route="/separar",  # Definindo a rota para acessar esta página
        controls=[
            header,
            ft.Container(height=20),  # Espaçamento
            ft.Column(
                controls=[
                    title,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        ],
    )
