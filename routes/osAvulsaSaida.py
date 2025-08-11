import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def os_avulsa_saida(page, navigate_to, header):
    # Usuário e filial
    matricula = user_info['matricula']
    codfilial = user_info['codfilial']

    # 1) Chama a API para buscar endereço e produto
    try:
        response = requests.post(
            f"{base_url}/os_avulsa_saida",
            json={
                "matricula": matricula,
                "codfilial": codfilial,
                "action": "buscar_dados"
            }
        )
        response.raise_for_status()
        dados_endereco = response.json().get("endereco")  # ex: (codend, MOD, RUA, EDI, NIV, APT, codprod, qt, numos)
        print(f"Dados do endereço: {dados_endereco}")
    except Exception:
        page.snack_bar = ft.SnackBar(
            ft.Text("Erro ao buscar dados"),
            bgcolor=colorVariaveis['erro']
        )
        page.snack_bar.open = True
        page.update()
        dados_endereco = None

    # 2) Cabeçalho da tela
    titulo = ft.Text(
        "OS Avulsa - Saída",
        size=24, weight="bold", color=colorVariaveis['titulo']
    )

    # 3) Seção dinâmica que vai crescendo conforme o fluxo
    dynamic_section = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        spacing=12
    )

    # 4) Controles fixos no topo
    controls = [
        header,
        titulo,
        ft.Divider(),
    ]

    # 5) Se recebi dados do endpoint, monto o primeiro bloco
    if dados_endereco:
        # Exibe MOD, RUA, EDI, NIV, APT e Código do Produto (índice 6)
        endereco_info = ft.Container(
            padding=10,
            # border=ft.border.all(1, ft.Colors.WHITE),
            # border_radius=5,
            content=ft.Column(
                spacing=4,
                controls=[
                    ft.Text(f"Numos: {dados_endereco[10]}", weight="bold"),
                    ft.Row(
                        controls=[
                            ft.Text(f"MOD: {dados_endereco[1]}"),
                            ft.Text(f"RUA: {dados_endereco[2]}"),
                            ft.Text(f"EDI: {dados_endereco[3]}"),
                            ft.Text(f"NIV: {dados_endereco[4]}"),
                            ft.Text(f"APT: {dados_endereco[5]}"),
                        ],
                        # spacing=8,
                        ),
                        ft.Row(
                            controls=[
                                ft.Text(f"Códprod: {dados_endereco[6]}"),
                                ft.Text(f"Códfab: {dados_endereco[7]}"),
                            ]
                        ),
                        ft.Text(f"Descrição: {dados_endereco[8]}"),
                ]
            )
        )

        # Campo para digitar o código do endereço
        input_cod_end = ft.TextField(
            autofocus=True,
            label="Código do Endereço",
            hint_text="Escaneie ou digite aqui",
            keyboard_type=ft.KeyboardType.TEXT,
            expand=True,
            border_radius=5,
            border_color=colorVariaveis['bordarInput'],
        )
        input_cod_end.on_submit = lambda e, campo=input_cod_end: validar_endereco(
            e, page, navigate_to, dados_endereco, campo, dynamic_section
        )
        btn_confirmar = ft.ElevatedButton(
            text="Confirmar Código",
            on_click=lambda e, campo=input_cod_end: validar_endereco(
                e, page, navigate_to, dados_endereco, campo, dynamic_section
            )
        )

        dynamic_section.controls.extend([
            endereco_info,
            ft.Row(spacing=8, controls=[input_cod_end, btn_confirmar])
        ])
    else:
        dynamic_section.controls.append(
            ft.Text("Não foi possível carregar o endereço.", color=colorVariaveis['erro'])
        )

    # 6) Retorna a View com todo o conteúdo
    return ft.View(
        route="/os_avulsa_saida",
        controls=[*controls, dynamic_section]
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

def validar_endereco(e, page, navigate_to, dados_endereco, campo, dynamic_section):
    entrada = campo.value.strip()
    codigo_correto = str(dados_endereco[0])  # codendereço
    if entrada != codigo_correto:
        campo.error_text = "Endereço incorreto!"
        snack_bar(
            "Endereço incorreto!",
            colorVariaveis['texto'],
            colorVariaveis['erro'],
            page
        )
        page.update()
        return

    # Limpa erros visuais
    campo.error_text = None
    snack_bar(
        "Endereço correto!",
        colorVariaveis['textoPreto'],
        colorVariaveis['sucesso'],
        page
    )
    page.update()

    # Próxima etapa: inserir código de barras do produto (índice 6)
    codprod = dados_endereco[6]

    input_cod_bar = ft.TextField(
        autofocus=True,
        label=f"Código de Barras do Produto",
        hint_text="Escaneie aqui",
        keyboard_type=ft.KeyboardType.TEXT,
        expand=True,
        border_radius=5,
        border_color=colorVariaveis['bordarInput']
    )
    input_cod_bar.on_submit = lambda ev, tb=input_cod_bar: validar_codbarra_produto(
        ev, page, navigate_to, dados_endereco, dynamic_section, codprod, tb
    )
    btn_cod_bar = ft.ElevatedButton(
        text="Confirmar Barras",
        on_click=lambda ev, tb=input_cod_bar: validar_codbarra_produto(
            ev, page, navigate_to, dados_endereco, dynamic_section, codprod, tb
        )
    )

    dynamic_section.controls.append(
        ft.Column(
            spacing=8,
            controls=[
                ft.Divider(),
                ft.Text("Agora digite o código de barras do produto:", weight="bold"),
                ft.Row(spacing=8, controls=[input_cod_bar, btn_cod_bar])
            ]
        )
    )
    page.update()


def validar_codbarra_produto(e, page, navigate_to, dados_endereco, dynamic_section, codprod, campo):
    entrada = campo.value.strip()
    if not entrada:
        campo.error_text = "Informe o código de barras"
        page.update()
        return

    btn = e.control
    btn.disabled = True
    page.update()

    try:
        response = requests.post(
            f"{base_url}/os_avulsa_saida",
            json={
                "codprod": codprod,
                "codbarra": entrada,
                "action": "validar_codbarra"
            }
        )
        response.raise_for_status()

        # Sucesso: limpa seção e monta etapa de quantidade (índice 7)
        dynamic_section.controls.clear()
        qt_necessaria = dados_endereco[9]

        dynamic_section.controls.extend([
            ft.Text(f"Código do Produto: {codprod}", weight="bold"),
            ft.Text(f"Descrição: {dados_endereco[8]}", weight="bold"),
            ft.Text(f"Quantidade a buscar: {qt_necessaria}", weight="bold"),
        ])

        campo_qt = ft.TextField(
            label="Quantidade a Inserir",
            keyboard_type=ft.KeyboardType.NUMBER,
            expand=True,
            border_radius=5,
            border_color=colorVariaveis['bordarInput'],
        )
        campo_qt.on_submit = lambda ev, cq=campo_qt: validar_quantidade(
            ev, page, navigate_to, dados_endereco, dynamic_section, codprod, cq
        )
        btn_qt = ft.ElevatedButton(
            text="Confirmar Quantidade",
            on_click=lambda ev, cq=campo_qt: validar_quantidade(
                ev, page, navigate_to, dados_endereco, dynamic_section, codprod, cq
            )
        )

        dynamic_section.controls.append(
            ft.Row(spacing=8, controls=[campo_qt, btn_qt])
        )
        page.update()

    except Exception as exc:
        msg = ""
        try:
            msg = response.json().get("mensagem", str(exc))
        except:
            msg = str(exc)
        page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=colorVariaveis['erro'])
        page.snack_bar.open = True

    finally:
        btn.disabled = False
        page.update()


def validar_quantidade(e, page, navigate_to, dados_endereco, dynamic_section, codprod, campo_qt):
    entrada = campo_qt.value.strip()
    if not entrada:
        campo_qt.error_text = "Informe a quantidade"
        page.update()
        return
    try:
        qt_digitada = int(entrada)
    except ValueError:
        campo_qt.error_text = "Valor inválido"
        page.update()
        return

    qt_necessaria = dados_endereco[9]
    if qt_digitada != qt_necessaria:
        campo_qt.error_text = f"Quantidade incorreta, esperada {qt_necessaria}"
        snack_bar(
            f"Quantidade incorreta!",
            colorVariaveis['texto'],
            colorVariaveis['erro'],
            page
        )
        page.update()
        return

    # Tudo certo: limpa erro e envia requisição
    campo_qt.error_text = None
    page.update()

    codendereco = dados_endereco[0]
    matricula   = user_info['matricula']
    codfilial   = user_info['codfilial']
    payload = {
        "codendereco": codendereco,
        "codprod":     codprod,
        "quantidade":  qt_digitada,
        "matricula":   matricula,
        "codfilial":   codfilial,
        "numos":       dados_endereco[10],
        "action":      "validar_quantidade"
    }

    try:
        resp = requests.post(f"{base_url}/os_avulsa_saida", json=payload)
        resp.raise_for_status()
        snack_bar(
            "Separação concluída com sucesso!",
            colorVariaveis['textoPreto'],
            colorVariaveis['sucesso'],
            page
        )
        # Navega para a tela principal de OS Avulsa
        navigate_to("/os_avulsa")
    except Exception as exc:
        err = ""
        try:
            err = resp.json().get("mensagem", str(exc))
        except:
            err = str(exc)
        page.snack_bar = ft.SnackBar(ft.Text(err), bgcolor=colorVariaveis['erro'])
        page.snack_bar.open = True
        page.update()
