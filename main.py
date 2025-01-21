import flet as ft
import requests

def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER


    def login(e):
        username.value = username.value.upper()
        password.value = password.value.upper()
        page.update()

        try:
            response = requests.post("http://192.168.1.244:5000/wmsMobile/login", json={
                "username": username.value,
                "password": password.value
            })
            print(f"Status code: {response.status_code}")
            print(f"Response: {response.json()}")

            if response.status_code == 200:
                snackbar_sucess = ft.SnackBar(
                    content=ft.Text('Login com sucesso'),
                    bgcolor=ft.colors.GREEN,
                    show_close_icon=True,
                )
                page.overlay.append(snackbar_sucess)
                snackbar_sucess.open = True
            elif response.status_code == 404:
                snackbar_error = ft.SnackBar(
                    content=ft.Text(f'Usário não encontrado {response.json()}', color=ft.colors.WHITE, size=20),
                    bgcolor=ft.colors.RED,
                    show_close_icon=True,
                )
                page.overlay.append(snackbar_error)
                snackbar_error.open = True
            else:
                snackbar_error = ft.SnackBar(
                    content=ft.Text('Login incorreto', color=ft.colors.WHITE, size=20),
                    bgcolor=ft.colors.RED,
                    show_close_icon=True,
                )
                page.overlay.append(snackbar_error)
                snackbar_error.open = True

        except requests.RequestException as e:
            snackbar_error = ft.SnackBar(
                content=ft.Text(f"Erro na conexão: {str(e)}", color=ft.colors.WHITE, size=20),
                bgcolor=ft.colors.RED,
                show_close_icon=True,
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
        text="login",
        bgcolor='#0000ff',
        color='#ffffff',
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
