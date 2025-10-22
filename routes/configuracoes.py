import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def configuracoes_page(page: ft.Page, navigate_to, header):

    input_ip = ft.TextField(
        label="Endereço IP do Servidor",
        value=base_url.replace("http://", "").split(":")[0],
        autofocus=True,
        on_submit=lambda e: confirmar_ip(input_ip.value)
    )
    salvar_ip_button = ft.ElevatedButton(
        text="Salvar",
        on_click=lambda e: confirmar_ip(input_ip.value)
    )

    def confirmar_ip(ip):
        print("Endereço IP:", ip)
    
    return ft.View(
        "/configuracoes",
        controls=[
            header,
            ft.Container(height=20),
            input_ip,
            salvar_ip_button
        ]
    )