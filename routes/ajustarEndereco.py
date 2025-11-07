import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def ajustar_endereco(page: ft.Page, navigate_to, header):

    return ft.View(
        route="/ajustar_endereco",
        controls=[
            header
        ]
    )