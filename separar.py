import flet as ft

def create_separar_pedido_page(navigate_to):
    """
    Função para criar a tela de Separar Pedido como uma View.
    """
    header = ft.Text("Separar Pedido", size=24, weight="bold", color="blue")

    voltar_button = ft.ElevatedButton(
        text="Voltar", 
        bgcolor="red", 
        color="white", 
        on_click=lambda e: navigate_to("/menu")  # Implementar lógica de navegação
    )

    # Retorna a view configurada para a página de separar pedido
    return ft.View(
        route="/separar",  # Definindo a rota para acessar esta página
        controls=[
            ft.Container(height=20),  # Espaçamento
            ft.Column(
                controls=[header, voltar_button],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        ],
    )
