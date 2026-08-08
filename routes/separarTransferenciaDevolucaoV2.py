import uuid

import flet as ft
import requests

from routes.config.config import base_url, colorVariaveis, user_info


def separar_transferencia_devolucao_v2(
    page: ft.Page, navigate_to, header, arguments=None
):
    arguments = arguments or {}
    numnota = arguments.get("numnota")
    matricula = user_info.get("matricula")
    codfilial = user_info.get("codfilial")
    estado_atual = {"valor": None}

    aba_separar = ft.Tab(
        text="Separar",
        content=ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True),
    )
    aba_resumo = ft.Tab(
        text="Resumo",
        content=ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True),
    )
    aba_finalizar = ft.Tab(
        text="Finalizar",
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
        ),
    )

    def mostrar_mensagem(mensagem, sucesso=False):
        page.open(
            ft.SnackBar(
                content=ft.Text(mensagem, color="white"),
                bgcolor=(
                    colorVariaveis["sucesso"]
                    if sucesso
                    else colorVariaveis["erro"]
                ),
            )
        )

    def ler_resposta(response):
        try:
            return response.json()
        except ValueError:
            return {
                "success": False,
                "message": f"A API retornou uma resposta inválida ({response.status_code}).",
            }

    def consultar_estado(mostrar_erro=True):
        try:
            response = requests.get(
                f"{base_url}/transferenciaDevolucaoV2/{numnota}",
                params={"codfilial": codfilial, "matricula": matricula},
                timeout=30,
            )
            resposta = ler_resposta(response)
            if response.status_code == 200 and resposta.get("success") is True:
                aplicar_estado(resposta.get("data", {}).get("estado", {}))
                return True
            if mostrar_erro:
                mostrar_mensagem(
                    resposta.get("message", "Não foi possível consultar a separação.")
                )
        except requests.RequestException as exc:
            if mostrar_erro:
                mostrar_mensagem(f"Erro de comunicação com a API: {exc}")
        return False

    def aplicar_estado(estado):
        estado_atual["valor"] = estado
        montar_aba_separar(estado.get("proximo_item"))
        montar_aba_resumo(estado.get("resumo", []), estado.get("progresso", {}))
        montar_aba_finalizar(estado.get("progresso", {}))
        page.update()

    def montar_aba_separar(item):
        aba_separar.content.controls.clear()
        if not item:
            aba_separar.content.controls.extend(
                [
                    ft.Container(height=10),
                    ft.Text(
                        "Todos os produtos disponíveis foram separados.",
                        size=16,
                        weight="bold",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "Confira o resumo e finalize a separação.",
                        text_align=ft.TextAlign.CENTER,
                    ),
                ]
            )
            return

        endereco = item.get("endereco", {})
        input_endereco = ft.TextField(
            label="Código do Endereço",
            autofocus=True,
            keyboard_type=ft.KeyboardType.NUMBER,
        )

        def validar_endereco(e):
            try:
                digitado = int((input_endereco.value or "").strip())
            except ValueError:
                mostrar_mensagem("Informe um endereço válido.")
                return

            if digitado != endereco.get("codendereco"):
                mostrar_mensagem("Endereço incorreto. Tente novamente.")
                input_endereco.value = ""
                input_endereco.focus()
                page.update()
                return

            mostrar_mensagem("Endereço validado com sucesso!", sucesso=True)
            montar_produto(item)
            page.update()

        input_endereco.on_submit = validar_endereco
        aba_separar.content.controls.extend(
            [
                ft.Text("Endereço do produto", weight="bold", size=16),
                ft.Row(
                    controls=[
                        ft.Text(
                            f"Qt Separada: {item.get('qt_separada', 0)}",
                            weight="bold",
                        ),
                        ft.Text(f"Módulo: {endereco.get('modulo', '-')}", weight="bold"),
                        ft.Text(f"Rua: {endereco.get('rua', '-')}", weight="bold"),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    wrap=True,
                ),
                ft.Row(
                    controls=[
                        ft.Text(f"Edi: {endereco.get('edificio', '-')}", weight="bold"),
                        ft.Text(f"Nível: {endereco.get('nivel', '-')}", weight="bold"),
                        ft.Text(f"Apto: {endereco.get('apto', '-')}", weight="bold"),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    wrap=True,
                ),
                ft.Text(
                    f"Disponível no endereço: {endereco.get('qt_disponivel', 0)}",
                    weight="bold",
                ),
                ft.Divider(),
                input_endereco,
                ft.ElevatedButton(
                    "Validar endereço",
                    expand=True,
                    bgcolor=colorVariaveis["botaoAcao"],
                    color=colorVariaveis["texto"],
                    on_click=validar_endereco,
                ),
            ]
        )

    def montar_produto(item):
        aba_separar.content.controls.clear()
        endereco = item.get("endereco", {})
        id_operacao = str(uuid.uuid4())
        input_codbarras = ft.TextField(label="Código de Barras", autofocus=True)
        input_quantidade = ft.TextField(
            label="Quantidade",
            keyboard_type=ft.KeyboardType.NUMBER,
        )

        def confirmar_produto(e):
            codbarra = (input_codbarras.value or "").strip()
            try:
                quantidade = int((input_quantidade.value or "").strip())
            except ValueError:
                mostrar_mensagem("Informe uma quantidade inteira válida.")
                return

            if not codbarra:
                mostrar_mensagem("Informe o código de barras.")
                return
            if quantidade <= 0:
                mostrar_mensagem("A quantidade deve ser maior que zero.")
                return

            botao_confirmar.disabled = True
            botao_pular.disabled = True
            page.update()
            try:
                response = requests.post(
                    f"{base_url}/transferenciaDevolucaoV2/{numnota}/separar",
                    json={
                        "id_operacao": id_operacao,
                        "item_id": item.get("item_id"),
                        "matricula": matricula,
                        "codfilial": codfilial,
                        "codprod": item.get("codprod"),
                        "codbarra": codbarra,
                        "codendereco": endereco.get("codendereco"),
                        "quantidade": quantidade,
                    },
                    timeout=30,
                )
                resposta = ler_resposta(response)
                if response.status_code in (200, 201) and resposta.get("success") is True:
                    novo_estado = resposta.get("data", {}).get("estado")
                    if novo_estado:
                        aplicar_estado(novo_estado)
                    else:
                        consultar_estado()
                    mostrar_mensagem(
                        resposta.get("message", "Quantidade separada com sucesso."),
                        sucesso=True,
                    )
                    return

                mostrar_mensagem(
                    resposta.get("message", "Não foi possível confirmar o produto.")
                )
                if resposta.get("code") == "ESTADO_DA_SEPARACAO_ALTERADO":
                    consultar_estado(mostrar_erro=False)
            except requests.RequestException as exc:
                mostrar_mensagem(
                    f"Erro de comunicação com a API: {exc}. Tente novamente sem sair desta tela."
                )
            finally:
                botao_confirmar.disabled = False
                botao_pular.disabled = False
                if botao_confirmar.page:
                    page.update()

        def pular_produto(e):
            botao_confirmar.disabled = True
            botao_pular.disabled = True
            page.update()
            try:
                response = requests.patch(
                    f"{base_url}/transferenciaDevolucaoV2/{numnota}/pular",
                    json={
                        "item_id": item.get("item_id"),
                        "codprod": item.get("codprod"),
                        "codfilial": codfilial,
                        "matricula": matricula,
                    },
                    timeout=30,
                )
                resposta = ler_resposta(response)
                if response.status_code == 200 and resposta.get("success") is True:
                    novo_estado = resposta.get("data", {}).get("estado")
                    if novo_estado:
                        aplicar_estado(novo_estado)
                    else:
                        consultar_estado()
                    mostrar_mensagem(resposta.get("message", "Produto pulado."), sucesso=True)
                    return
                mostrar_mensagem(resposta.get("message", "Não foi possível pular o produto."))
            except requests.RequestException as exc:
                mostrar_mensagem(f"Erro de comunicação com a API: {exc}")
            finally:
                botao_confirmar.disabled = False
                botao_pular.disabled = False
                if botao_confirmar.page:
                    page.update()

        input_codbarras.on_submit = lambda e: input_quantidade.focus()
        input_quantidade.on_submit = confirmar_produto
        botao_confirmar = ft.ElevatedButton(
            "Confirmar Produto",
            expand=True,
            bgcolor=colorVariaveis["botaoAcao"],
            color=colorVariaveis["texto"],
            on_click=confirmar_produto,
        )
        botao_pular = ft.ElevatedButton(
            "Pular Produto",
            expand=True,
            bgcolor=colorVariaveis["erro"],
            color=colorVariaveis["texto"],
            on_click=pular_produto,
        )
        aba_separar.content.controls.extend(
            [
                ft.Text(f"Codprod: {item.get('codprod', '-')}", weight="bold"),
                ft.Text(f"Codfab: {item.get('codfab', '-')}", weight="bold"),
                ft.Text(f"Descrição: {item.get('descricao', '-')}", weight="bold"),
                ft.Row(
                    controls=[
                        ft.Text(f"Qt Pedida: {item.get('qt_pedida', 0)}"),
                        ft.Text(f"Qt Separada: {item.get('qt_separada', 0)}"),
                        ft.Text(f"Qt Restante: {item.get('qt_restante', 0)}"),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    wrap=True,
                ),
                ft.Text(
                    f"Qt Endereço: {endereco.get('qt_disponivel', 0)}",
                    weight="bold",
                ),
                ft.Divider(),
                input_codbarras,
                input_quantidade,
                ft.Row(controls=[botao_confirmar]),
                ft.Container(height=10),
                ft.Row(controls=[botao_pular]),
            ]
        )

    def montar_aba_resumo(resumo, progresso):
        aba_resumo.content.controls.clear()
        aba_resumo.content.controls.append(
            ft.Text(
                "Itens completos: "
                f"{progresso.get('itens_completos', 0)}/{progresso.get('total_itens', 0)}",
                weight="bold",
            )
        )
        cores = {
            "PARCIAL": colorVariaveis["restante"],
            "COMPLETO": colorVariaveis["sucesso"],
            "EXCESSO": colorVariaveis["erro"],
        }
        for item in resumo:
            situacao = item.get("situacao", "NAO_INICIADO")
            cor_fundo = cores.get(situacao)
            cor_texto = (
                colorVariaveis["texto"]
                if situacao == "EXCESSO"
                else colorVariaveis["textoPreto"]
            )
            aba_resumo.content.controls.append(
                ft.Container(
                    padding=10,
                    bgcolor=cor_fundo,
                    border_radius=8,
                    border=ft.border.all(1, colorVariaveis["bordarInput"]),
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Text(f"Codprod: {item.get('codprod', '-')}", color=cor_texto),
                                    ft.Text(f"Codfab: {item.get('codfab', '-')}", color=cor_texto),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                wrap=True,
                            ),
                            ft.Text(f"Descrição: {item.get('descricao', '-')}", color=cor_texto),
                            ft.Row(
                                controls=[
                                    ft.Text(f"Pedida: {item.get('qt_pedida', 0)}", color=cor_texto),
                                    ft.Text(f"Separada: {item.get('qt_separada', 0)}", color=cor_texto),
                                    ft.Text(f"Restante: {item.get('qt_restante', 0)}", color=cor_texto),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                wrap=True,
                            ),
                            ft.Text(
                                f"Situação: {situacao.replace('_', ' ').title()}",
                                color=cor_texto,
                                weight="bold",
                            ),
                        ]
                    ),
                )
            )

    def montar_aba_finalizar(progresso):
        aba_finalizar.content.controls.clear()
        aba_finalizar.content.controls.extend(
            [
                ft.Container(height=20),
                ft.Text(
                    f"Itens completos: {progresso.get('itens_completos', 0)} de "
                    f"{progresso.get('total_itens', 0)}",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.ElevatedButton(
                    "Finalizar Separação da Transferência",
                    bgcolor=colorVariaveis["botaoAcao"],
                    color=colorVariaveis["texto"],
                    disabled=not progresso.get("pode_finalizar", False),
                    on_click=lambda e: finalizar_separacao(False),
                ),
            ]
        )

    def finalizar_separacao(confirmar_divergencias):
        try:
            response = requests.post(
                f"{base_url}/transferenciaDevolucaoV2/{numnota}/finalizar",
                json={
                    "codfilial": codfilial,
                    "matricula": matricula,
                    "confirmar_divergencias": confirmar_divergencias,
                },
                timeout=30,
            )
            resposta = ler_resposta(response)
            if response.status_code == 200 and resposta.get("success") is True:
                mostrar_mensagem(
                    resposta.get("message", "Separação finalizada com sucesso."),
                    sucesso=True,
                )
                navigate_to("/buscar_transferencia_devolucao_v2")
                return

            if (
                response.status_code == 409
                and resposta.get("code") == "DIVERGENCIAS_NAO_CONFIRMADAS"
            ):
                abrir_dialogo_divergencias(
                    resposta.get("details", {}).get("divergencias", [])
                )
                return

            mostrar_mensagem(
                resposta.get("message", "Não foi possível finalizar a separação.")
            )
        except requests.RequestException as exc:
            mostrar_mensagem(f"Erro de comunicação com a API: {exc}")

    def abrir_dialogo_divergencias(divergencias):
        controles = [
            ft.Text("Os produtos abaixo ainda possuem quantidade pendente:"),
            ft.Divider(),
        ]
        for item in divergencias:
            controles.append(
                ft.Text(
                    f"Produto {item.get('codprod', '-')}: pedida "
                    f"{item.get('qt_pedida', 0)}, separada "
                    f"{item.get('qt_separada', 0)}, restante "
                    f"{item.get('qt_restante', 0)}"
                )
            )

        def confirmar(e):
            page.close(dialogo)
            finalizar_separacao(True)

        dialogo = ft.AlertDialog(
            title=ft.Text("Divergências encontradas"),
            content=ft.Column(controls=controles, scroll=ft.ScrollMode.AUTO),
            actions=[
                ft.TextButton("Finalizar assim mesmo", on_click=confirmar),
                ft.TextButton("Cancelar", on_click=lambda e: page.close(dialogo)),
            ],
        )
        page.open(dialogo)

    tabs = ft.Tabs(
        tabs=[aba_separar, aba_resumo, aba_finalizar],
        scrollable=True,
        selected_index=0,
        expand=1,
    )
    view = ft.View(
        route="/separar_transferencia_devolucao_v2",
        controls=[
            header,
            ft.Text(
                f"Transferência V2 — Nota {numnota}",
                size=22,
                weight="bold",
                color=colorVariaveis["titulo"],
            ),
            tabs,
        ],
    )

    if numnota is None:
        aba_separar.content.controls.append(
            ft.Text("Número da nota não informado.", color=colorVariaveis["erro"])
        )
    else:
        consultar_estado()

    return view
