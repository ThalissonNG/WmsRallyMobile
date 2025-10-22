import flet as ft
import requests
import os
import re
from urllib.parse import urlparse
from routes.config.config import base_url, colorVariaveis, user_info


def configuracoes_page(page: ft.Page, navigate_to, header):

    # Extract current host from base_url to show as default
    try:
        parsed = urlparse(base_url)
        current_host = parsed.hostname or ""
    except Exception:
        current_host = base_url.replace("http://", "").split(":")[0]

    input_ip = ft.TextField(
        label="Endereco IP do Servidor",
        value=current_host,
        autofocus=True,
        on_submit=lambda e: confirmar_ip(input_ip.value)
    )
    salvar_ip_button = ft.ElevatedButton(
        text="Salvar",
        on_click=lambda e: confirmar_ip(input_ip.value)
    )
    login_button = ft.IconButton(
        icon=ft.Icons.HOME,
        tooltip="Voltar",
        on_click=lambda e: navigate_to("/login")
    )
    app_bar_config = ft.AppBar(
        title=ft.Text("Configuracoes"),
        center_title=True,
        bgcolor=colorVariaveis['botaoAcao'],
        leading=login_button
    )

    def confirmar_ip(ip):
        new_ip = (ip or "").strip()
        if not new_ip:
            snackbar_error = ft.SnackBar(
                content=ft.Text("Informe um IP valido"),
                bgcolor=colorVariaveis['erro'],
                show_close_icon=True,
            )
            page.overlay.append(snackbar_error)
            snackbar_error.open = True
            page.update()
            return

        # Keep scheme, port and path from existing base_url
        try:
            p = urlparse(base_url)
            scheme = p.scheme or "http"
            port = f":{p.port}" if p.port else ""
            path = p.path or ""
            new_base_url = f"{scheme}://{new_ip}{port}{path}"
        except Exception:
            # Fallback simple if parsing fails
            new_base_url = f"http://{new_ip}"

        # Path to config.py (based on this file location in routes/)
        routes_dir = os.path.dirname(__file__)
        config_path = os.path.join(routes_dir, 'config', 'config.py')

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Replace the base_url line preserving double quotes
            pattern = r'^(\s*base_url\s*=\s*")[^"]*("\s*)$'
            replacement = rf'\1{new_base_url}\2'
            new_content, n = re.subn(pattern, replacement, content, flags=re.MULTILINE)

            if n == 0:
                # If not found in expected format, try a broader replacement
                pattern_alt = r'base_url\s*=\s*\".*?\"'
                new_content, n = re.subn(pattern_alt, f'base_url = "{new_base_url}"', content, flags=re.DOTALL)

            if n == 0:
                raise ValueError("Nao foi possivel localizar base_url em config.py")

            with open(config_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            snackbar_sucess = ft.SnackBar(
                content=ft.Text(f"IP salvo: {new_base_url}. Reinicie o app para aplicar."),
                bgcolor=colorVariaveis['sucesso'],
                show_close_icon=True,
                duration=2000,
            )
            page.overlay.append(snackbar_sucess)
            snackbar_sucess.open = True
        except Exception as exc:
            snackbar_error = ft.SnackBar(
                content=ft.Text(f"Falha ao salvar: {exc}"),
                bgcolor=colorVariaveis['erro'],
                show_close_icon=True,
            )
            page.overlay.append(snackbar_error)
            snackbar_error.open = True
        finally:
            page.update()

    return ft.View(
        "/configuracoes",
        controls=[
            app_bar_config,
            ft.Container(height=20),
            input_ip,
            salvar_ip_button
        ]
    )

