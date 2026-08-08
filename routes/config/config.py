import flet as ft
app_version = '1.10.0'
user_info = {}
colorVariaveis = {
    'botaoAcao': "#0366FF",
    'texto': "#ffffff",
    'textoPreto': "#000000",
    'bordarInput': "#0a0a0a",
    'icones': "#ffffff",
    'titulo': "#4f4ce5",
    'sucesso': "#10b650",
    'erro': "#ff0000",
    'restante': "#ffb300"
}

def snack_bar(mensagem, bgcolor, color, page):
    snack = ft.SnackBar(
        content=ft.Text(
            mensagem,
            color="white"
        ),
        bgcolor=bgcolor
    )
    page.open(snack)
