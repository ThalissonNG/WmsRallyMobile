import flet as ft

def menu_page(page: ft.Page, navigate_to, header, arguments):
    welcome_text = ft.Text("Menu Principal", size=24, weight="bold", color="blue")
    # matricula = arguments.get("matricula", "N/A")
    # print(matricula)

    # Retorna a view configurada
    return ft.View(
        route="/menu",  # Define a rota da página
        controls=[header,
                welcome_text,
                ft.Container(height=20),
                ft.Column(
                    controls=[ 
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    "Separar Pedido",
                                    expand=True
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
                                    expand=True,
                                    on_click=lambda e: navigate_to("/armazenar_bonus", arguments),
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
                                    "Consultar Produto ou Endereço",
                                    expand=True,
                                    on_click=lambda e: navigate_to("/consultarProdutoEndereco", arguments),
                                ),
                            ],
                            spacing=10,
                        ),
                    ],
                    spacing=10,
                ),
            ],
    )
