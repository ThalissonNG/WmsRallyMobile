import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def armazenar_bonus_v2(page: ft.Page, navigate_to, header):

    return ft.View(
        route="/armazenar_bonus_v2",
        controls=[
            header
        ]
    )
