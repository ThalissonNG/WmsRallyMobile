import flet as ft

def menuPage(page: ft.Page, navigate_to):
    """
    Função para criar a tela de menu como uma View.
    """
    # Elementos do menu
    welcome_text = ft.Text("Menu Principal", size=24, weight="bold", color="blue")
    logout_button = ft.ElevatedButton(
        text="Logout", 
        bgcolor="red", 
        color="white",
        on_click=lambda e: page.go("/login"),  # Voltar para a tela de login
    )

    # Retorna a view configurada
    return ft.View(
        route="/menu",  # Define a rota da página
        controls=[
                ft.Container(height=20),  # Espaçamento
                ft.Column(
                    controls=[ 
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    "Separa Pedido",
                                    expand=True,
                                    on_click=lambda e: navigate_to("/separar"),  # Navegação para a nova página
                                ),
                                ft.ElevatedButton(
                                    "Conferir Bônus",
                                    expand=True
                                    ),
                            ],
                            spacing=10,
                        ),
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    "O.S Abastecimento",
                                    expand=True
                                    ),
                                ft.ElevatedButton(
                                    "Armazenar Bônus", 
                                    expand=True
                                    ),
                            ],
                            spacing=10,
                        ),
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    "O.S Avulsa",
                                    expand=True
                                    ),
                                ft.ElevatedButton(
                                    "Transferir Produto",
                                    expand=True
                                    ),
                            ],
                            spacing=10,
                        ),
                        ft.Row(
                            controls=[
                                ft.ElevatedButton("Carregar carro", expand=True),
                                ft.ElevatedButton(
                                    "Consultar Produto ou Endereço", expand=True
                                ),
                            ],
                            spacing=10,
                        ),
                    ],
                    spacing=10,
                ),
            ],
    )
