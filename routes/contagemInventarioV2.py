import datetime

import flet as ft
import requests

from routes.config.config import base_url, colorVariaveis, snack_bar, user_info


def contagem_inventario_v2(page, navigate_to, header):
    matricula = user_info.get("matricula")
    codfilial = user_info.get("codfilial")

    state = {
        "dados_os": None,
        "resumo": [],
        "produto_atual": None,
        "etapa": "inicial",
        "editando_codprod": None,
        "mostrar_cadastro_codbarra": False,
    }

    tabs = None
    card_bg = "#1F2532"
    section_bg = "#151A24"

    def validade_padrao():
        return (datetime.date.today() + datetime.timedelta(days=365)).strftime("%d%m%Y")

    def apenas_numeros(valor):
        return "".join(filter(str.isdigit, valor))[:8]

    def atualizar_campo_data(control):
        control.value = apenas_numeros(control.value)
        if control.value and len(control.value) < 8:
            control.error_text = "Digite 8 dígitos (DDMMYYYY)"
        else:
            control.error_text = None
        control.update()

    def focar(control):
        try:
            control.focus()
        except Exception as exc:
            print("Erro ao focar campo V2:", exc)

    def limpar_campos_produto():
        state["produto_atual"] = None
        state["mostrar_cadastro_codbarra"] = False
        codbarra_field.value = ""
        quantidade_field.value = ""
        validade_field.value = validade_padrao()
        validade_field.error_text = None

    def limpar_estado():
        state["dados_os"] = None
        state["resumo"] = []
        state["produto_atual"] = None
        state["etapa"] = "inicial"
        state["editando_codprod"] = None
        state["mostrar_cadastro_codbarra"] = False
        endereco_field.value = ""
        edit_quantidade_field.value = ""
        edit_validade_field.value = validade_padrao()
        edit_validade_field.error_text = None
        limpar_campos_produto()
        if tabs is not None:
            tabs.selected_index = 0

    def carregar_resumo(silencioso=False):
        if not state["dados_os"]:
            state["resumo"] = []
            return True

        try:
            response = requests.post(
                f"{base_url}/resumo_contagem",
                json={"dados_os": state["dados_os"]},
            )
            if response.status_code == 200:
                state["resumo"] = response.json().get("resumo", [])
                if state["editando_codprod"] is not None:
                    existe_item = any(item[0] == state["editando_codprod"] for item in state["resumo"])
                    if not existe_item:
                        state["editando_codprod"] = None
                return True

            if not silencioso:
                snack_bar("Erro ao buscar resumo", colorVariaveis["erro"], colorVariaveis["texto"], page)
            return False
        except Exception as exc:
            print("Erro ao atualizar resumo V2:", exc)
            if not silencioso:
                snack_bar("Erro ao atualizar resumo", colorVariaveis["erro"], colorVariaveis["texto"], page)
            return False

    def render_info_os():
        if not state["dados_os"]:
            return None

        dados = state["dados_os"][0]
        return ft.Container(
            padding=12,
            border_radius=12,
            bgcolor=card_bg,
            content=ft.Column(
                spacing=6,
                controls=[
                    ft.Text("Endereço Atual", size=18, weight="bold", color=colorVariaveis["titulo"]),
                    ft.Text(f"Nº Inventário: {dados[0]}"),
                    ft.Text(f"Nº OS: {dados[1]}"),
                    # ft.Text(f"Endereço esperado: {dados[2]}", weight="bold"),
                    ft.Text(
                        f"MOD: {dados[3]}, RUA: {dados[4]}, EDI: {dados[5]}, NIV: {dados[6]}, APT: {dados[7]}"
                    ),
                ],
            ),
        )

    def render_separar():
        etapa_label = {
            "inicial": "Inicie o inventário para carregar o próximo endereço.",
            "endereco": "Etapa 1: valide o endereço do inventário.",
            "codbarra": "Etapa 2: valide o código de barras do produto.",
            "quantidade": "Etapa 3: informe quantidade e validade.",
        }

        controls = [
            ft.Text("Fluxo de Separação", size=18, weight="bold", color=colorVariaveis["titulo"]),
            ft.Text(etapa_label[state["etapa"]]),
        ]

        if not state["dados_os"]:
            controls.append(start_button)
            separar_body.controls = controls
            return

        info_os = render_info_os()
        if info_os is not None:
            controls.append(info_os)

        endereco_controls = [
            ft.Text("Validar Endereço", weight="bold"),
            endereco_field,
        ]
        if state["etapa"] == "endereco":
            endereco_controls.append(validar_endereco_btn)
        else:
            endereco_controls.append(
                ft.Text(
                    "Endereço validado com sucesso.",
                    color=colorVariaveis["sucesso"],
                    weight="bold",
                )
            )
        controls.append(ft.Container(padding=12, border_radius=12, bgcolor=section_bg, content=ft.Column(controls=endereco_controls)))

        if state["etapa"] in ("codbarra", "quantidade"):
            barcode_controls = [
                ft.Text("Validar Código de Barras", weight="bold"),
                codbarra_field,
                validar_codbarra_btn,
            ]
            if state["mostrar_cadastro_codbarra"]:
                barcode_controls.extend(
                    [
                        ft.Text("Código de barras não cadastrado.", color=colorVariaveis["erro"], weight="bold"),
                        cadastrar_codbarra_btn,
                    ]
                )
            controls.append(
                ft.Container(
                    padding=12,
                    border_radius=12,
                    bgcolor=section_bg,
                    content=ft.Column(controls=barcode_controls),
                )
            )

        if state["produto_atual"]:
            produto = state["produto_atual"]
            controls.append(
                ft.Container(
                    padding=12,
                    border_radius=12,
                    bgcolor=section_bg,
                    content=ft.Column(
                        spacing=8,
                        controls=[
                            ft.Text("Produto Validado", weight="bold"),
                            ft.Text(f"CODPROD: {produto[0]}"),
                            ft.Text(f"DESCRIÇÃO: {produto[1]}"),
                            ft.Text(f"CODFAB: {produto[2]}"),
                            quantidade_field,
                            validade_field,
                            confirmar_quantidade_btn,
                        ],
                    ),
                )
            )

        if state["resumo"]:
            controls.append(
                ft.Container(
                    padding=12,
                    border_radius=12,
                    bgcolor=section_bg,
                    content=ft.Column(
                        spacing=8,
                        controls=[
                            ft.Text(f"Itens no resumo: {len(state['resumo'])}", weight="bold"),
                            ft.ElevatedButton(
                                "Encerrar leitura e ir para Finalizar",
                                bgcolor=colorVariaveis["botaoAcao"],
                                color=colorVariaveis["texto"],
                                on_click=ir_para_finalizar,
                            ),
                        ],
                    ),
                )
            )

        separar_body.controls = controls

    def render_resumo():
        controls = [ft.Text("Resumo da Contagem", size=18, weight="bold", color=colorVariaveis["titulo"])]

        if not state["dados_os"]:
            controls.append(ft.Text("Inicie o inventário para carregar o resumo."))
            resumo_body.controls = controls
            return

        if not state["resumo"]:
            controls.append(ft.Text("Nenhum item confirmado ainda."))
            resumo_body.controls = controls
            return

        for item in state["resumo"]:
            item_controls = [
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Column(
                            spacing=2,
                            controls=[
                                ft.Text(f"Codprod: {item[0]}", weight="bold"),
                                ft.Text(f"Descrição: {item[1]}"),
                                ft.Text(f"CodFab: {item[2]}"),
                                ft.Text(f"Quantidade: {item[3]}", weight="bold"),
                            ],
                        ),
                        ft.TextButton(
                            text="Editar",
                            icon=ft.Icons.EDIT,
                            on_click=lambda e, item=item: iniciar_edicao(item),
                        ),
                    ],
                )
            ]

            if state["editando_codprod"] == item[0]:
                item_controls.extend(
                    [
                        edit_quantidade_field,
                        edit_validade_field,
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    "Salvar",
                                    bgcolor=colorVariaveis["botaoAcao"],
                                    color=colorVariaveis["texto"],
                                    on_click=lambda e, item=item: salvar_edicao(item),
                                ),
                                ft.TextButton("Cancelar", on_click=cancelar_edicao),
                            ]
                        ),
                    ]
                )

            item_controls.append(ft.Divider())
            controls.append(ft.Container(padding=8, content=ft.Column(controls=item_controls)))

        resumo_body.controls = controls

    def render_finalizar():
        controls = [ft.Text("Finalizar Endereço", size=18, weight="bold", color=colorVariaveis["titulo"])]

        if not state["dados_os"]:
            controls.append(ft.Text("Inicie o inventário para preparar a finalização."))
            finalizar_body.controls = controls
            return

        dados = state["dados_os"][0]
        controls.append(
            ft.Container(
                padding=12,
                border_radius=12,
                bgcolor=section_bg,
                content=ft.Column(
                    spacing=6,
                    controls=[
                        ft.Text(f"Inventário: {dados[0]}", weight="bold"),
                        ft.Text(f"OS: {dados[1]}"),
                        # ft.Text(f"Endereço: {dados[2]}"),
                        ft.Text(f"Itens no resumo: {len(state['resumo'])}"),
                    ],
                ),
            )
        )

        if state["resumo"]:
            controls.append(
                ft.Text(
                    "Confirme a finalização quando terminar a leitura dos produtos deste endereço."
                )
            )
        else:
            controls.append(
                ft.Text(
                    "Nenhum produto foi confirmado. Ao finalizar, a API receberá este endereço como sem produtos."
                )
            )

        controls.append(
            ft.ElevatedButton(
                "Finalizar",
                bgcolor=colorVariaveis["botaoAcao"],
                color=colorVariaveis["texto"],
                on_click=abrir_confirmacao_finalizacao,
            )
        )
        controls.append(ft.TextButton("Voltar para Separar", on_click=voltar_para_separar))

        finalizar_body.controls = controls

    def render_all():
        render_separar()
        render_resumo()
        render_finalizar()
        page.update()

    def iniciar_inventario(e):
        try:
            response = requests.post(
                f"{base_url}/contagem_inventario",
                json={"codfilial": codfilial, "matricula": matricula},
            )
            if response.status_code in [200, 202]:
                dados_os = response.json().get("dados_os", [])
                print("Dados OS recebidos:", dados_os)
                if not dados_os:
                    snack_bar("Nenhum inventário disponível.", colorVariaveis["erro"], colorVariaveis["texto"], page)
                    return

                limpar_estado()
                state["dados_os"] = dados_os
                state["etapa"] = "endereco"
                carregar_resumo(silencioso=True)
                render_all()
                focar(endereco_field)
            else:
                snack_bar("Erro ao buscar inventário.", colorVariaveis["erro"], colorVariaveis["texto"], page)
        except Exception as exc:
            print("Erro ao buscar inventário V2:", exc)
            snack_bar("Erro ao buscar inventário.", colorVariaveis["erro"], colorVariaveis["texto"], page)

    def validar_endereco(e):
        if not state["dados_os"]:
            return

        if endereco_field.value.strip() == str(state["dados_os"][0][2]):
            state["etapa"] = "codbarra"
            snack_bar("Endereço validado!", colorVariaveis["sucesso"], colorVariaveis["textoPreto"], page)
            render_all()
            focar(codbarra_field)
        else:
            snack_bar("Endereço incorreto", colorVariaveis["erro"], colorVariaveis["texto"], page)
            render_all()

    def validar_codbarra(e):
        if not state["dados_os"]:
            return

        try:
            response = requests.post(
                f"{base_url}/contagem_inventario",
                json={
                    "codbarra": codbarra_field.value,
                    "matricula": matricula,
                    "codfilial": codfilial,
                    "dados_os": state["dados_os"],
                    "action": "validar_codbarra",
                },
            )
            if response.status_code == 200:
                produto = response.json().get("produto", [])
                state["produto_atual"] = produto[0] if produto else None
                state["mostrar_cadastro_codbarra"] = False
                state["etapa"] = "quantidade"
                quantidade_field.value = ""
                validade_field.value = validade_padrao()
                validade_field.error_text = None
                render_all()
                focar(quantidade_field)
            elif response.status_code == 500:
                state["produto_atual"] = None
                state["mostrar_cadastro_codbarra"] = True
                snack_bar("Código de barras não cadastrado", colorVariaveis["erro"], colorVariaveis["texto"], page)
                render_all()
                focar(codbarra_field)
            else:
                snack_bar("Resposta inesperada ao validar código de barras.", colorVariaveis["erro"], colorVariaveis["texto"], page)
                focar(codbarra_field)
        except Exception as exc:
            print("Erro ao validar código de barras V2:", exc)
            snack_bar("Erro ao validar código de barras.", colorVariaveis["erro"], colorVariaveis["texto"], page)
            focar(codbarra_field)

    def confirmar_quantidade(e):
        if not state["produto_atual"]:
            return

        validade = apenas_numeros(validade_field.value)
        if len(validade) < 8:
            validade_field.error_text = "Digite 8 dígitos (DDMMYYYY)"
            validade_field.update()
            return

        try:
            response = requests.post(
                f"{base_url}/contagem_inventario",
                json={
                    "codbarra": codbarra_field.value,
                    "quantidade": quantidade_field.value,
                    "dados_os": state["dados_os"],
                    "validade": validade,
                    "action": "confirmar_quantidade",
                },
            )
            dados = response.json()
            mensagem = dados.get("mensagem")
            if response.status_code == 200:
                snack_bar(mensagem, colorVariaveis["sucesso"], colorVariaveis["textoPreto"], page)
                carregar_resumo(silencioso=True)
                limpar_campos_produto()
                state["etapa"] = "codbarra"
                render_all()
                focar(codbarra_field)
            else:
                snack_bar(mensagem, colorVariaveis["erro"], colorVariaveis["texto"], page)
                focar(quantidade_field)
        except Exception as exc:
            print("Erro ao confirmar quantidade V2:", exc)
            snack_bar("Erro ao confirmar quantidade.", colorVariaveis["erro"], colorVariaveis["texto"], page)
            focar(quantidade_field)

    def iniciar_edicao(item):
        state["editando_codprod"] = item[0]
        edit_quantidade_field.value = str(item[3])
        edit_validade_field.value = validade_padrao()
        edit_validade_field.error_text = None
        if tabs is not None:
            tabs.selected_index = 1
        render_all()

    def cancelar_edicao(e):
        state["editando_codprod"] = None
        edit_quantidade_field.value = ""
        edit_validade_field.value = validade_padrao()
        edit_validade_field.error_text = None
        render_all()

    def salvar_edicao(item):
        validade = apenas_numeros(edit_validade_field.value)
        if len(validade) < 8:
            edit_validade_field.error_text = "Digite 8 dígitos (DDMMYYYY)"
            edit_validade_field.update()
            return

        try:
            response = requests.post(
                f"{base_url}/contagem_inventario",
                json={
                    "codprod": item[0],
                    "nova_quantidade": edit_quantidade_field.value,
                    "dados_os": state["dados_os"],
                    "validade": validade,
                    "action": "editar_contagem",
                },
            )
            if response.status_code == 200:
                snack_bar("Quantidade atualizada!", colorVariaveis["sucesso"], colorVariaveis["textoPreto"], page)
                state["editando_codprod"] = None
                carregar_resumo(silencioso=True)
                render_all()
            else:
                snack_bar("Erro ao atualizar quantidade", colorVariaveis["erro"], colorVariaveis["texto"], page)
        except Exception as exc:
            print("Erro ao editar item V2:", exc)
            snack_bar("Erro ao atualizar quantidade", colorVariaveis["erro"], colorVariaveis["texto"], page)

    def ir_para_finalizar(e):
        if tabs is not None:
            tabs.selected_index = 2
            page.update()

    def voltar_para_separar(e):
        if tabs is not None:
            tabs.selected_index = 0
            page.update()

    def confirmar_finalizacao(dialog, btn_confirmar):
        btn_confirmar.disabled = True
        page.update()
        try:
            response = requests.post(
                f"{base_url}/contagem_inventario",
                json={
                    "dados_os": state["dados_os"],
                    "matricula": matricula,
                    "codfilial": codfilial,
                    "action": "finalizar_contagem",
                },
            )
            dados = response.json()
            mensagem = dados.get("mensagem")
            if response.status_code == 200:
                page.close(dialog)
                if dialog in page.overlay:
                    page.overlay.remove(dialog)
                limpar_estado()
                navigate_to("/menu")
                snack_bar(mensagem, colorVariaveis["sucesso"], colorVariaveis["textoPreto"], page)
            else:
                btn_confirmar.disabled = False
                snack_bar(mensagem, colorVariaveis["erro"], colorVariaveis["texto"], page)
                page.update()
        except Exception as exc:
            print("Erro ao finalizar inventário V2:", exc)
            btn_confirmar.disabled = False
            snack_bar("Erro ao finalizar contagem.", colorVariaveis["erro"], colorVariaveis["texto"], page)
            page.update()

    def abrir_confirmacao_finalizacao(e):
        btn_confirmar = ft.ElevatedButton(
            "Finalizar",
            bgcolor=colorVariaveis["botaoAcao"],
            color=colorVariaveis["texto"],
        )
        dialog = ft.AlertDialog(
            title=ft.Text("Finalizar a contagem desse endereço?"),
            content=ft.Text("Essa ação encerra o endereço atual e retorna ao menu."),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda evt: page.close(dialog)),
                btn_confirmar,
            ],
        )
        btn_confirmar.on_click = lambda evt: confirmar_finalizacao(dialog, btn_confirmar)
        page.open(dialog)

    title = ft.Text("Inventário V2", size=24, weight="bold", color=colorVariaveis["titulo"])

    start_button = ft.ElevatedButton(
        "Iniciar Inventário V2",
        bgcolor=colorVariaveis["botaoAcao"],
        color=colorVariaveis["texto"],
        on_click=iniciar_inventario,
    )

    endereco_field = ft.TextField(
        label="Endereço",
        autofocus=True,
        on_submit=validar_endereco,
    )
    codbarra_field = ft.TextField(
        label="Código de Barras",
        on_submit=validar_codbarra,
    )
    quantidade_field = ft.TextField(label="Quantidade")
    validade_field = ft.TextField(
        label="Data de Validade (DDMMYYYY)",
        value=validade_padrao(),
        max_length=8,
        hint_text="Ex: 25062025",
        on_change=lambda e: atualizar_campo_data(e.control),
        on_blur=lambda e: atualizar_campo_data(e.control),
    )

    edit_quantidade_field = ft.TextField(label="Nova Quantidade")
    edit_validade_field = ft.TextField(
        label="Data de Validade (DDMMYYYY)",
        value=validade_padrao(),
        max_length=8,
        hint_text="Ex: 25062025",
        on_change=lambda e: atualizar_campo_data(e.control),
        on_blur=lambda e: atualizar_campo_data(e.control),
    )

    validar_endereco_btn = ft.ElevatedButton(
        "Validar Endereço",
        bgcolor=colorVariaveis["botaoAcao"],
        color=colorVariaveis["texto"],
        on_click=validar_endereco,
    )
    validar_codbarra_btn = ft.ElevatedButton(
        "Validar Código de Barras",
        bgcolor=colorVariaveis["botaoAcao"],
        color=colorVariaveis["texto"],
        on_click=validar_codbarra,
    )
    confirmar_quantidade_btn = ft.ElevatedButton(
        "Confirmar Quantidade",
        bgcolor=colorVariaveis["botaoAcao"],
        color=colorVariaveis["texto"],
        on_click=confirmar_quantidade,
    )
    cadastrar_codbarra_btn = ft.TextButton(
        "Cadastrar código de barras",
        on_click=lambda e: navigate_to("/cadastrar_codbarra"),
    )

    separar_body = ft.Column(spacing=12, expand=True, scroll=ft.ScrollMode.AUTO)
    resumo_body = ft.Column(spacing=8, expand=True, scroll=ft.ScrollMode.AUTO)
    finalizar_body = ft.Column(spacing=12, expand=True, scroll=ft.ScrollMode.AUTO)

    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=200,
        expand=True,
        tabs=[
            ft.Tab(text="Separar", content=ft.Container(padding=10, content=separar_body)),
            ft.Tab(text="Resumo", content=ft.Container(padding=10, content=resumo_body)),
            ft.Tab(text="Finalizar", content=ft.Container(padding=10, content=finalizar_body)),
        ],
    )

    render_all()

    return ft.View(
        route="/contagem_inventario_v2",
        controls=[
            header,
            title,
            tabs,
        ],
    )
