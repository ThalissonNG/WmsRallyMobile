import flet as ft
import cx_Oracle
from database import get_db_connection

def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def login(e):
        username.value = username.value.upper()
        password.value = password.value.upper()
        dados_usuario = {}

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            query_login = """
                        select
                            r.matricula,
                            r.nome_guerra,
                            decrypt(senhabd, nome_guerra) as senha,
                            r.codfilial,
                            r.nome
                        from pcempr r
                        where r.nome_guerra = :nome_guerra
                        """
            cursor.execute(query_login, {'nome_guerra': username.value})
            result_login = cursor.fetchone()
            if result_login:
                dados_usuario[result_login[1]] = {
                    "matricula": result_login[0],
                    "usuario": result_login[1],
                    "senha": result_login[2],
                    "filial": result_login[3],
                    "nome": result_login[4]
                }
                print(dados_usuario[result_login[1]])
            else:
                print(f"Usuário {username.value} não encontrada")
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            print(f"Ocorreu um erro ao executar a consulta: {error.message}")
        finally:
            cursor.close()
            conn.close()
        
        if username.value in dados_usuario and password.value == dados_usuario[username.value]['senha']:
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