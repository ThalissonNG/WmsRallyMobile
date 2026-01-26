import flet as ft
from routes.config.config import user_info, colorVariaveis

def menu_page(page: ft.Page, navigate_to, header):
    
    matricula = user_info.get("matricula")
    print(f"User config na tela Menu: {matricula}")

    titulo = ft.Text(
        "Menu Principal",
        size=24, weight="bold",
        color=colorVariaveis['titulo']
    )
    # Retorna a view configurada
    return ft.View(
        route="/menu",  # Define a rota da página
        controls=[header,
                titulo,
                ft.Container(height=20),
                ft.Column(
                    controls=[ 
                        ft.Row(
                            controls=[
                                
                                ft.ElevatedButton(
                                    "Separar Pedido Dist",
                                    expand=True,
                                    on_click=lambda e: navigate_to("/buscar_pedido_dist")
                                ),
                                ft.ElevatedButton(
                                    "Transferência",
                                    expand=True,
                                    on_click=lambda e: navigate_to("/buscar_transferencia_devolucao")
                                    ),
                            ],
                            spacing=10,
                        ),
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    "Inventário",
                                    expand=True,
                                    on_click=lambda e: navigate_to("/contagem_inventario")
                                    ),
                                ft.ElevatedButton(
                                    "Armazenar Bônus", 
                                    expand=True,
                                    on_click=lambda e: navigate_to("/buscar_etiqueta_v2"),
                                ),
                            ],
                            spacing=10,
                        ),
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    "Cadastrar codbarra",
                                    expand=True,
                                    on_click=lambda e: navigate_to("/cadastrar_codbarra")
                                    ),
                                ft.ElevatedButton(
                                    "Transferir Produto",
                                    expand=True,
                                    on_click=lambda e: navigate_to("/transferirProduto")
                                    ),
                            ],
                            spacing=10,
                        ),
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    "Inventario Rotativo",
                                    expand=True,
                                    on_click=lambda e: navigate_to("/contagem_inventario_rotativo")
                                ),
                                ft.ElevatedButton(
                                    "Consultar Produto ou Endereço",
                                    expand=True,
                                    on_click=lambda e: navigate_to("/consultarProdutoEndereco"),
                                ),
                            ],
                            spacing=10,
                        ),
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    "Os Avulsa",
                                    expand=True,
                                    on_click=lambda e: navigate_to("/os_avulsa")
                                ),
                                ft.ElevatedButton(
                                    "Conferir Bonus",
                                    expand=True,
                                    on_click=lambda e: navigate_to("/buscar_bonus")
                                ),
                            ],
                            spacing=10,
                        ),
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    "Separar Pedido - Var",
                                    expand=True,
                                    on_click=lambda e: navigate_to("/buscar_pedido_varejo")
                                ),
                                ft.ElevatedButton(
                                    "Abastecimento V2",
                                    expand=True,
                                    on_click=lambda e: navigate_to("/abastecimentoV2")
                                ),
                            ],
                            spacing=10,
                        ),
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    "Devolução",
                                    expand=True,
                                    on_click=lambda e: navigate_to("/buscar_devolucao")
                                ),
                                ft.ElevatedButton(
                                    "Ajustar Endereço",
                                    expand=True,
                                    on_click=lambda e: navigate_to("/ajustar_endereco")
                                ),
                            ],
                            spacing=10,
                        ),
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    "--------",
                                    expand=True,
                                    # on_click=lambda e: navigate_to("/buscar_pedido_varejo")
                                ),
                                ft.ElevatedButton(
                                    "--------",
                                    expand=True,
                                    # on_click=lambda e: navigate_to("/buscar_etiqueta_v2")
                                ),
                            ],
                            spacing=10,
                        ),
                    ],
                    spacing=10,
                    scroll=ft.ScrollMode.AUTO,
                    expand=True
                ),
            ],
    )
