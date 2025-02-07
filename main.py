import flet as ft
import requests
from routes.config.config import base_url
from routes.menu import menu_page
from routes.armazenarEtiqueta import buscar_etiqueta
from routes.enderecarProduto import enderecar_produto
from routes.consultarProdutoEndereco import consultar_produto_endereco
from routes.transferirProduto import transferir_produto

def main(page: ft.Page):
    page.title = "Login"
    page.window_width = 450
    page.window_height = 700
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    # Cabeçalho que usa as variáveis globais definidas após o login
    def create_header():
        # Importa o módulo config para acessar as informações atualizadas
        import routes.config.config as config
        return ft.AppBar(
            title=ft.Text(f"{config.user_info.get('matricula', '')} - {config.user_info.get('usuario', '')}"),
            bgcolor="blue",
            actions=[
                ft.PopupMenuButton(
                    icon=ft.icons.MENU,
                    icon_size=40,
                    icon_color="#0000ff",
                    items=[
                        ft.ElevatedButton(
                            icon=ft.icons.HOME,
                            text="Menu",
                            on_click=lambda e: navigate_to("/menu"),
                        ),
                        ft.ElevatedButton(
                            icon=ft.icons.LOGOUT,
                            text="Sair",
                            on_click=lambda e: navigate_to("/login"),
                        ),
                    ]
                ),
            ]
        )

    # Função de navegação entre rotas
    def navigate_to(route, arguments=None):
        page.views.clear()
        if route == "/login":
            page.views.append(create_login_view())
        elif route == "/menu":
            page.views.append(menu_page(page, navigate_to, create_header()))
        elif route == "/armazenar_bonus":
            page.views.append(buscar_etiqueta(navigate_to, create_header(),))
        elif route == "/enderecarProduto":
            page.views.append(enderecar_produto(page, navigate_to, create_header(), arguments))
        elif route == "/consultarProdutoEndereco":
            page.views.append(consultar_produto_endereco(navigate_to, create_header()))
        elif route == "/transferirProduto":
            page.views.append(transferir_produto(page, navigate_to, create_header()))
        page.update()

    # Tela de login
    def create_login_view():
        def login(e):
            username.value = username.value.upper()
            password.value = password.value.upper()
            page.update()

            try:
                response = requests.post(
                    base_url + "/login",
                    json={"username": username.value, "password": password.value},
                )
                print(f"Status code: {response.status_code}")
                print(f"Response: {response.json()}")

                if response.status_code == 200:
                    response_data = response.json()
                    global usuario, matricula, codfilial, nomeCompleto
                    usuario = response_data.get('usuario')
                    matricula = response_data.get('matricula')
                    codfilial = response_data.get('codfilial')
                    nomeCompleto = response_data.get('nomeCompleto')

                    # Atualiza o dicionário global de usuário no módulo config
                    import routes.config.config as config
                    config.user_info.update({
                        'matricula': matricula,
                        'usuario': usuario,
                        'codfilial': codfilial,
                        'nomeCompleto': nomeCompleto,
                    })

                    print(matricula, usuario, codfilial)
                    print(f"UserConfig: {config.user_info}")

                    snackbar_sucess = ft.SnackBar(
                        content=ft.Text("Login com sucesso"),
                        bgcolor=ft.colors.GREEN,
                        show_close_icon=True,
                        duration=1000,
                    )
                    page.overlay.append(snackbar_sucess)
                    snackbar_sucess.open = True
                    page.update()
                    navigate_to("/menu", arguments={
                        'matricula': matricula,
                        'usuario': usuario,
                        'codfilial': codfilial,
                        'nomeCompleto': nomeCompleto
                    })
                elif response.status_code == 404:
                    snackbar_error = ft.SnackBar(
                        content=ft.Text(
                            f"Usuário não encontrado {response.json()}",
                            color=ft.colors.WHITE,
                            size=20,
                        ),
                        bgcolor=ft.colors.RED,
                        show_close_icon=True,
                    )
                    page.overlay.append(snackbar_error)
                    snackbar_error.open = True
                else:
                    snackbar_error = ft.SnackBar(
                        content=ft.Text("Login incorreto", color=ft.colors.WHITE, size=20),
                        bgcolor=ft.colors.RED,
                        show_close_icon=True,
                    )
                    page.overlay.append(snackbar_error)
                    snackbar_error.open = True
            except requests.RequestException as exc:
                snackbar_error = ft.SnackBar(
                    content=ft.Text(f"Erro na conexão: {str(exc)}", color=ft.colors.WHITE, size=20),
                    bgcolor=ft.colors.RED,
                    show_close_icon=True,
                )
                page.overlay.append(snackbar_error)
                snackbar_error.open = True
            page.update()

        username = ft.TextField(
            label="Usuário",
            prefix_icon=ft.icons.PERSON,
            border_radius=ft.border_radius.all(10),
            border_color=ft.colors.BLACK,
            border_width=2,
            width=300,
        )
        password = ft.TextField(
            label="Senha",
            prefix_icon=ft.icons.PASSWORD,
            border_radius=ft.border_radius.all(10),
            border_color=ft.colors.BLACK,
            border_width=2,
            password=True,
            can_reveal_password=True,
            width=300,
        )
        button_login = ft.ElevatedButton(
            text="Login",
            bgcolor="#0000ff",
            color="#ffffff",
            width=300,
            on_click=login,
        )

        return ft.View(
            route="/login",
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[username, password, button_login],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    alignment=ft.alignment.center,
                    expand=True,
                )
            ],
        )

    # Inicializa a navegação na tela de login
    navigate_to("/login")

# Inicializa o aplicativo
ft.app(target=main)
