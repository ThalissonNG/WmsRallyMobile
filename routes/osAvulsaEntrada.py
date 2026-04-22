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

    # Cabeçalho fixo da tela
    titulo = ft.Text(
        "OS Avulsa - Entrada",
        size=24,
        weight="bold",
        color=colorVariaveis["titulo"],
    )

    # Seção dinâmica que será atualizada de acordo com o fluxo
    dynamic_section = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        spacing=12,
    )

    def renderizar_dados_os(dados_os):
        dynamic_section.controls.clear()

        if not dados_os:
            dynamic_section.controls.append(
                ft.Text("Nenhuma OS disponível.", color=colorVariaveis["erro"])
            )
            page.update()
            return

        numos, codprod, codfab, descricao, qtpedida = (
            dados_os[0][0],
            dados_os[0][1],
            dados_os[0][2],
            dados_os[0][3],
            dados_os[0][4],
        )

        dynamic_section.controls.extend(
            [
                ft.Text(f"OS: {numos}", weight="bold"),
                ft.Row(
                    controls=[
                        ft.Text(f"Códprod: {codprod}"),
                        ft.Text(f"Códfab: {codfab}"),
                    ]
                ),
                ft.Text(f"Descrição: {descricao}"),
                ft.Text(f"Quantidade: {qtpedida}"),
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
            descricao,
            qtpedida,
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
                descricao,
                qtpedida,
                numos,
            ),
        )

        dynamic_section.controls.append(
            ft.Row(spacing=8, controls=[campo_cod_bar, btn_cod_bar])
        )
        page.update()

    def buscar_dados_os(action, numos=None):
        payload = {
            "matricula": matricula,
            "codfilial": codfilial,
            "action": action,
        }

        if action == "buscar_dados_manual":
            if not numos:
                input_numos.error_text = "Informe o número da OS"
                snack_bar(
                    "Digite o número da OS para busca manual.",
                    colorVariaveis["texto"],
                    colorVariaveis["erro"],
                    page,
                )
                page.update()
                return

            input_numos.error_text = None
            payload["numos"] = numos

        dynamic_section.controls.clear()
        dynamic_section.controls.append(
            ft.Text("Buscando dados da OS...", color=colorVariaveis["titulo"])
        )
        page.update()

        try:
            response = requests.post(f"{base_url}/os_avulsa_entrada", json=payload)
            response.raise_for_status()
            dados_os = response.json().get("dados_os")
            renderizar_dados_os(dados_os)
        except Exception:
            dynamic_section.controls.clear()
            dynamic_section.controls.append(
                ft.Text("Nenhuma OS disponível.", color=colorVariaveis["erro"])
            )
            page.snack_bar = ft.SnackBar(
                ft.Text("Erro ao buscar dados"),
                bgcolor=colorVariaveis["erro"],
            )
            page.snack_bar.open = True
            page.update()

    input_numos = ft.TextField(
        label="Número da OS",
        hint_text="Digite o número da OS",
        keyboard_type=ft.KeyboardType.NUMBER,
        autofocus=True,
        expand=True,
        border_radius=5,
        border_color=colorVariaveis["bordarInput"],
        on_submit=lambda e: buscar_dados_os(
            "buscar_dados_manual", e.control.value.strip()
        ),
    )

    btn_busca_manual = ft.ElevatedButton(
        text="Buscar OS Manual",
        bgcolor=colorVariaveis["botaoAcao"],
        color=colorVariaveis["texto"],
        on_click=lambda e: buscar_dados_os(
            "buscar_dados_manual", input_numos.value.strip()
        ),
    )

    btn_busca_automatica = ft.ElevatedButton(
        text="Buscar OS Automática",
        bgcolor=colorVariaveis["botaoAcao"],
        color=colorVariaveis["texto"],
        on_click=lambda e: buscar_dados_os("buscar_dados"),
    )

    controls = [
        header,
        titulo,
        ft.Divider(),
        ft.Row(spacing=8, controls=[input_numos, btn_busca_manual]),
        ft.Container(height=12),
        btn_busca_automatica,
        ft.Divider(),
    ]

    return ft.View(
        route="/os_avulsa_entrada",
        controls=[*controls, dynamic_section],
    )

def snack_bar(message, cor_texto, color, page):
        page.snack_bar = ft.SnackBar(
            ft.Text(
                message,
                color=cor_texto
                ),
            bgcolor=color,
            duration=1000
        )
        page.open(page.snack_bar)
        # page.snack_bar.open = True
        # page.update()

# ======================================================================
# Funções auxiliares
# ======================================================================
def _validar_codbarra(e, page, navigate_to, campo, dynamic_section, codprod, descricao, qtpedida, numos,):
    """Valida o código de barras do produto."""

    entrada = campo.value.strip()
    if not entrada:
        campo.error_text = "Informe o código de barras"
        snack_bar(
            "Codigo de barras incorreto!",
            colorVariaveis['texto'],
            colorVariaveis['erro'],
            page
        )
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
        print(resp.status_code)

        if resp.status_code == 400:
            snack_bar(
                "Codigo de barras incorreto!",
                colorVariaveis['texto'],
                colorVariaveis['erro'],
                page
            )
            page.update()
            return

        # Sucesso: próxima etapa (informar endereço)
        dynamic_section.controls.clear()
        dynamic_section.controls.append(
            ft.Text(f"OS: {numos}", weight="bold"),
        )
        dynamic_section.controls.append(
            ft.Text(f"Cód. Produto: {codprod}", weight="bold"),
        )
        dynamic_section.controls.append(
            ft.Text(f"Descrição: {descricao}")
        )
        dynamic_section.controls.append(
            ft.Text(f"Quantidade: {qtpedida}")
        )
        snack_bar(
            "Código de barras validado com sucesso!",
            colorVariaveis['textoPreto'],
            colorVariaveis['sucesso'],
            page
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
        snack_bar(
            "Erro ao validar código de barras!",
            colorVariaveis['texto'],
            colorVariaveis['erro'],
            page
        )
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


def _validar_endereco( e, page, navigate_to, campo, dynamic_section, codprod, numos,):
    """Valida o endereço e finaliza a OS avulsa de entrada."""

    endereco = campo.value.strip()
    if not endereco:
        campo.error_text = "Informe o endereço"
        snack_bar(
            "Endereço incorreto!",
            colorVariaveis['texto'],
            colorVariaveis['erro'],
            page
        )
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
        snack_bar(
            "Produto guardado com sucesso!",
            colorVariaveis['textoPreto'],
            colorVariaveis['sucesso'],
            page
        )

        # Sucesso: retorna para tela principal de OS avulsa
        navigate_to("/os_avulsa")
    except Exception as exc:
        msg = ""
        snack_bar(
            "Erro ao validar endereço!",
            colorVariaveis['texto'],
            colorVariaveis['erro'],
            page
        )
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
