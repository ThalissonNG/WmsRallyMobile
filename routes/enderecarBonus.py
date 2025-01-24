import flet as ft

def enderecar_bonus_page(navigate_to, header):
    return ft.View(
        route="/enderecarBonus",
        controls=[
            header,
            ft.Container(height=10),  # Espaçamento
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "Endereçar Bônus",
                            size=20,
                            weight=600
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=60
                ),
                alignment=ft.alignment.center,
                expand=True,
            ),
        ],
    )