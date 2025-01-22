import flet as ft

def menuPage(page: ft.Page, go_back):
    page.controls.clear()
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    welcome_text = ft.Text("Menu", size=24, weight="bold")
    logout_button = ft.ElevatedButton(
        text="Logout",
        on_click=lambda e: go_back(page),  
    )

    page.add(
        ft.Container(
            content=ft.Column(
                controls=[welcome_text, logout_button],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
    )
    page.update()
