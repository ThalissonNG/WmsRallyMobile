import flet as ft
import requests

from routes.config.config import base_url, colorVariaveis, user_info


def os_avulsa_entrada(page, navigate_to, header):
    """Fluxo de entrada de OS avulsa.

    1. Busca os dados da OS de entrada (produto e OS).
    2. Solicita a leitura do código de barras do produto.
    3. Solicita o endereço onde o produto será armazenado.

    A cada etapa uma requisição é feita. Somente em caso de
    ``status_code`` 200 o fluxo avança; qualquer outro código exibe um erro
    e permanece na etapa atual.
    """

    matricula = user_info["matricula"]
    codfilial = user_info["codfilial"]

    # Seção dinâmica que será atualizada de acordo com o fluxo
    dynamic_section = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        spacing=12,
    )

    # ------------------------------------------------------------------
    # 1) Buscar dados da OS de entrada
    # ------------------------------------------------------------------
    try:
        response = requests.post(
            f"{base_url}/os_avulsa_entrada",
            json={
                "matricula": matricula,
                "codfilial": codfilial,
                "action": "buscar_dados",
            },
        )
        response.raise_for_status()
        dados_os = response.json().get("dados_os")
    except Exception:
        page.snack_bar = ft.SnackBar(
            ft.Text("Erro ao buscar dados"),
            bgcolor=colorVariaveis["erro"],
        )
        page.snack_bar.open = True
        page.update()
        dados_os = None

    # ------------------------------------------------------------------
    # Cabeçalho fixo da tela
    # ------------------------------------------------------------------
    titulo = ft.Text(
        "OS Avulsa - Entrada",
        size=24,
        weight="bold",
        color=colorVariaveis["titulo"],
    )

    controls = [header, titulo, ft.Divider()]

    # ------------------------------------------------------------------
    # Primeira etapa: validar código de barras do produto
    # ------------------------------------------------------------------
    if dados_os:
        numos, codprod = dados_os[0][0], dados_os[0][1]

        dynamic_section.controls.extend(
            [
                ft.Text(f"OS: {numos}", color=ft.Colors.WHITE),
                ft.Text(f"Cód. Produto: {codprod}", color=ft.Colors.WHITE),
            ]
        )

        campo_cod_bar = ft.TextField(
            label="Código de Barras do Produto",
            hint_text="Escaneie ou digite aqui",
            keyboard_type=ft.KeyboardType.TEXT,
            expand=True,
            border_radius=5,
            border_color=colorVariaveis["bordarInput"],
        )

        campo_cod_bar.on_submit = lambda e, tb=campo_cod_bar: _validar_codbarra(
            e,
            page,
            navigate_to,
            tb,
            dynamic_section,
            codprod,
            numos,
        )

        btn_cod_bar = ft.ElevatedButton(
            text="Confirmar Barras",
            on_click=lambda e, tb=campo_cod_bar: _validar_codbarra(
                e,
                page,
                navigate_to,
                tb,
                dynamic_section,
                codprod,
                numos,
            ),
        )

        dynamic_section.controls.append(
            ft.Row(spacing=8, controls=[campo_cod_bar, btn_cod_bar])
        )
    else:
        dynamic_section.controls.append(
            ft.Text("Nenhuma OS disponível.", color=colorVariaveis["erro"])
        )

    return ft.View(
        route="/os_avulsa_entrada",
        controls=[*controls, dynamic_section],
    )


# ======================================================================
# Funções auxiliares
# ======================================================================
def _validar_codbarra(
    e,
    page,
    navigate_to,
    campo,
    dynamic_section,
    codprod,
    numos,
):
    """Valida o código de barras do produto."""

    entrada = campo.value.strip()
    if not entrada:
        campo.error_text = "Informe o código de barras"
        page.update()
        return

    btn = e.control
    btn.disabled = True
    page.update()

    try:
        resp = requests.post(
            f"{base_url}/os_avulsa_entrada",
            json={
                "codprod": codprod,
                "codbarra": entrada,
                "numos": numos,
                "matricula": user_info["matricula"],
                "codfilial": user_info["codfilial"],
                "action": "validar_codbarra",
            },
        )
        resp.raise_for_status()

        # Sucesso: próxima etapa (informar endereço)
        dynamic_section.controls.clear()
        dynamic_section.controls.append(
            ft.Text(f"Cód. Produto: {codprod}", weight="bold")
        )

        campo_end = ft.TextField(
            label="Endereço de Armazenagem",
            hint_text="Escaneie ou digite aqui",
            keyboard_type=ft.KeyboardType.TEXT,
            expand=True,
            border_radius=5,
            border_color=colorVariaveis["bordarInput"],
        )

        campo_end.on_submit = lambda ev, ce=campo_end: _validar_endereco(
            ev,
            page,
            navigate_to,
            ce,
            dynamic_section,
            codprod,
            numos,
        )

        btn_end = ft.ElevatedButton(
            text="Confirmar Endereço",
            on_click=lambda ev, ce=campo_end: _validar_endereco(
                ev,
                page,
                navigate_to,
                ce,
                dynamic_section,
                codprod,
                numos,
            ),
        )

        dynamic_section.controls.append(
            ft.Row(spacing=8, controls=[campo_end, btn_end])
        )
        page.update()

    except Exception as exc:  # status != 200
        msg = ""
        try:
            msg = resp.json().get("mensagem", str(exc))
        except Exception:
            msg = str(exc)

        page.snack_bar = ft.SnackBar(
            ft.Text(msg),
            bgcolor=colorVariaveis["erro"],
        )
        page.snack_bar.open = True
    finally:
        btn.disabled = False
        page.update()


def _validar_endereco(
    e,
    page,
    navigate_to,
    campo,
    dynamic_section,
    codprod,
    numos,
):
    """Valida o endereço e finaliza a OS avulsa de entrada."""

    endereco = campo.value.strip()
    if not endereco:
        campo.error_text = "Informe o endereço"
        page.update()
        return

    btn = e.control
    btn.disabled = True
    page.update()

    payload = {
        "codprod": codprod,
        "codendereco": endereco,
        "numos": numos,
        "matricula": user_info["matricula"],
        "codfilial": user_info["codfilial"],
        "action": "validar_endereco",
    }
    print(payload)

    try:
        resp = requests.post(f"{base_url}/os_avulsa_entrada", json=payload)
        resp.raise_for_status()

        # Sucesso: retorna para tela principal de OS avulsa
        navigate_to("/os_avulsa")
    except Exception as exc:
        msg = ""
        try:
            msg = resp.json().get("mensagem", str(exc))
        except Exception:
            msg = str(exc)
        page.snack_bar = ft.SnackBar(
            ft.Text(msg),
            bgcolor=colorVariaveis["erro"],
        )
        page.snack_bar.open = True
        page.update()
    finally:
        btn.disabled = False
        page.update()

