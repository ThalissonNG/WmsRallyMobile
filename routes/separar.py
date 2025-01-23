import flet as ft

def separar_page(navigate_to, header):
    title = ft.Text(
        "Separar Pedido",
        size=24,
        weight="bold",
        color="blue"
    )
    busca_manual = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "Busca Manual",
                    size=20,
                    weight=600
                ),
                ft.TextField(
                    label="Digite o número do pedido...",
                    prefix_icon=ft.icons.SEARCH,
                    border_radius=ft.border_radius.all(10),
                    border_color=ft.colors.BLACK,
                    border_width=2,
                    width=300,
                ),
                ft.ElevatedButton(
                    text="Buscar",
                    width=600,
                    on_click=lambda e: print("Clicou pra buscar manual"),
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        border=ft.border.all(
            color="black",
            width=2,
        ),
        border_radius=ft.border_radius.all(10),
        padding=10,
    )
    busca_automatica =ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "Busca Automática",
                    size=20,
                    weight=600,
                ),
                ft.ElevatedButton(
                    text="Busca Automática",
                    width=600,
                    height=50,
                    on_click=lambda e: print("Clicou pra buscar automatica"),
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        border=ft.border.all(
            color="black",
            width=2,
        ),
        border_radius=ft.border_radius.all(10),
        padding=10,
    )
    return ft.View(
        route="/separar",  # Definindo a rota para acessar esta página
        controls=[
            header,
            title,
            ft.Container(height=10),  # Espaçamento
            ft.Container(
                content=ft.Column(
                    controls=[
                        busca_manual,
                        busca_automatica,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=60
                ),
                alignment=ft.alignment.center,
                expand=True,
            ),
        ],
)

