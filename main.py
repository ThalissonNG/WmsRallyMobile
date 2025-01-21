import flet as ft

def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def login(e):
        if username.value == 'thalisson' and password.value == 'Tha2809_':
            snackbar_sucess = ft.SnackBar(
                content=ft.Text('Login com sucesso'),
                bgcolor=ft.colors.GREEN,
                show_close_icon=True,
            )
            page.overlay.append(snackbar_sucess)
            snackbar_sucess.open = True
        else:
            snackbar_error = ft.SnackBar(
                content=ft.Text('Login incorreto', color=ft.colors.WHITE, size=20),
                bgcolor=ft.colors.RED,
                show_close_icon=True
            )
            page.overlay.append(snackbar_error)
            snackbar_error.open = True
        page.update()

    username = ft.TextField(
        label='Usuário',
        prefix_icon=ft.icons.PERSON,
        bgcolor=ft.colors.BLACK,
        border_radius=ft.border_radius.all(10),
        border_color=ft.colors.WHITE,
        border_width=2,
        width=300,
    )
    password = ft.TextField(
        label='Senha',
        prefix_icon=ft.icons.PERSON,
        bgcolor=ft.colors.BLACK,
        border_radius=ft.border_radius.all(10),
        border_color=ft.colors.WHITE,
        border_width=2,
        password=True,
        can_reveal_password=True,
        width=300,
    )
    button_login = ft.ElevatedButton(
        text='Login',
        bgcolor=ft.colors.BLUE,
        color=ft.colors.WHITE,
        width=300,
        on_click=login,
    )
    page.add(
        ft.Container(
            content=ft.Column(
                controls=[username, password, button_login],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
    )
    page.update()

ft.app(main)