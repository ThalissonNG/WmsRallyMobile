import asyncio
import json

import flet as ft
import requests

from routes.config.config import base_url, colorVariaveis, snack_bar, user_info


def ajustar_contagem_end(page, navigate_to, header):
    matricula = user_info.get("matricula")
    codfilial = user_info.get("codfilial")
    print(f"Ajustar Contagem End - Matricula: {matricula}, Codfilial: {codfilial}")
    
    titulo = ft.Text(
        "Ajustar Contagem End",
        size=24,
        weight="bold",
        color=colorVariaveis["titulo"],
    )

    state = {
        "codendereco_atual": "",
        "endereco_confirmado": False,
        "produto_encontrado": None,
        "itens_resumo": [],
    }

    async def focar_async(control):
        try:
            await asyncio.sleep(0.08)
            if getattr(control, "page", None) is not None:
                control.focus()
        except Exception as exc:
            print(f"Erro ao focar controle: {exc}")

    def focar(control):
        try:
            if getattr(control, "page", None) is not None:
                page.run_task(focar_async, control)
        except Exception as exc:
            print(f"Erro ao focar controle: {exc}")

    def atualizar_controle(control):
        if getattr(control, "page", None) is not None:
            control.update()

    def atualizar_estado_codbarra():
        habilitado = state["endereco_confirmado"]
        codbarra_field.disabled = not habilitado
        buscar_codbarra_btn.disabled = not habilitado
        codbarra_field.hint_text = (
            "Digite ou bipar o código de barras"
            if habilitado
            else "Disponível após validar o endereço"
        )
        atualizar_controle(codbarra_field)
        atualizar_controle(buscar_codbarra_btn)

    def atualizar_estado_quantidade():
        habilitado = state["produto_encontrado"] is not None
        quantidade_field.disabled = not habilitado
        quantidade_field.hint_text = (
            "Informe a quantidade"
            if habilitado
            else "Disponível após validar o código de barras"
        )
        atualizar_controle(quantidade_field)

    def limpar_produto():
        state["produto_encontrado"] = None
        produto_codprod.value = ""
        produto_codfab.value = ""
        produto_descricao.value = ""
        quantidade_field.value = ""
        produto_info.visible = False
        atualizar_estado_quantidade()
        atualizar_controle(produto_info)

    def salvar_edicao_item(page, dialog, indice_item, campo_quantidade):
        nova_quantidade = (campo_quantidade.value or "").strip()

        if not nova_quantidade:
            campo_quantidade.error_text = "Informe a quantidade."
            atualizar_controle(campo_quantidade)
            focar(campo_quantidade)
            return

        if not nova_quantidade.isdigit():
            campo_quantidade.error_text = "Digite apenas números."
            atualizar_controle(campo_quantidade)
            focar(campo_quantidade)
            return

        campo_quantidade.error_text = None
        quantidade = int(nova_quantidade)

        if indice_item < 0 or indice_item >= len(state["itens_resumo"]):
            page.close(dialog)
            snack_bar("Item não encontrado para edição.", colorVariaveis["erro"], colorVariaveis["texto"], page)
            return

        if quantidade == 0:
            state["itens_resumo"].pop(indice_item)
            atualizar_telas_auxiliares()
            page.close(dialog)
            snack_bar("Item removido do resumo.", colorVariaveis["sucesso"], colorVariaveis["texto"], page)
            return

        state["itens_resumo"][indice_item]["qt"] = quantidade
        atualizar_telas_auxiliares()
        page.close(dialog)
        snack_bar("Quantidade atualizada com sucesso.", colorVariaveis["sucesso"], colorVariaveis["texto"], page)

    def abrir_dialog_edicao_item(page, indice_item):
        if indice_item < 0 or indice_item >= len(state["itens_resumo"]):
            snack_bar("Item não encontrado para edição.", colorVariaveis["erro"], colorVariaveis["texto"], page)
            return

        item = state["itens_resumo"][indice_item]
        campo_editar_qt = ft.TextField(
            label="Nova Quantidade",
            value=str(item["qt"]),
            keyboard_type=ft.KeyboardType.NUMBER,
        )

        dialog_editar_qt = ft.AlertDialog(
            title=ft.Text("Editar Quantidade"),
            content=ft.Column(
                controls=[
                    ft.Text(f"Endereço: {item['codendereco']}", weight="bold"),
                    ft.Text(f"Codprod: {item['codprod']}"),
                    ft.Text(f"Codfab: {item['codfab']}"),
                    ft.Text(f"Descrição: {item['descricao']}"),
                    campo_editar_qt,
                    ft.Text(
                        "Se informar 0, o produto será removido da lista.",
                        color=colorVariaveis["restante"],
                    ),
                ],
                tight=True,
                scroll=ft.ScrollMode.AUTO,
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: page.close(dialog_editar_qt)),
                ft.TextButton(
                    "Salvar",
                    on_click=lambda _: salvar_edicao_item(page, dialog_editar_qt, indice_item, campo_editar_qt),
                ),
            ],
        )
        campo_editar_qt.on_submit = lambda _: salvar_edicao_item(page, dialog_editar_qt, indice_item, campo_editar_qt)
        page.open(dialog_editar_qt)
        focar(campo_editar_qt)

    def atualizar_resumo():
        resumo_body.controls.clear()

        if not state["itens_resumo"]:
            resumo_body.controls.append(
                ft.Text(
                    "Nenhum item lançado ainda.",
                    color=colorVariaveis["textoPreto"],
                )
            )
            atualizar_controle(resumo_body)
            return

        for indice_item, item in enumerate(state["itens_resumo"]):
            resumo_body.controls.append(
                ft.Container(
                    padding=12,
                    border_radius=10,
                    border=ft.border.all(1, colorVariaveis["bordarInput"]),
                    content=ft.Column(
                        spacing=6,
                        controls=[
                            ft.Text(
                                f"Endereço: {item['codendereco']}",
                                weight="bold",
                                color=colorVariaveis["titulo"],
                            ),
                            ft.Text(f"Codprod: {item['codprod']}"),
                            ft.Text(f"Codfab: {item['codfab']}",),
                            ft.Text(f"Descrição: {item['descricao']}", ),
                            ft.Text(f"Quantidade: {item['qt']}", ),
                            ft.TextButton(
                                "Editar Quantidade",
                                on_click=lambda e, indice_item=indice_item: abrir_dialog_edicao_item(e.page, indice_item),
                            ),
                        ],
                    ),
                )
            )

        atualizar_controle(resumo_body)

    def montar_payload_finalizacao():
        return {
            "produtos": [
                {
                    "codprod": item["codprod"],
                    "qt": item["qt"],
                    "codendereco": item["codendereco"],
                    "codfilial": codfilial,
                    "matricula": matricula,
                }
                for item in state["itens_resumo"]
            ],
        }

    def atualizar_finalizar():
        payload = montar_payload_finalizacao()
        finalizar_json.value = json.dumps(payload, ensure_ascii=False, indent=2)
        atualizar_controle(finalizar_json)

    def finalizar_contagem(e):
        payload = montar_payload_finalizacao()

        if not payload["produtos"]:
            snack_bar("Nenhum item para finalizar.", colorVariaveis["erro"], colorVariaveis["texto"], page)
            return

        try:
            response = requests.post(
                f"{base_url}/contagem_inventario_end",
                json=payload,
            )

            if response.status_code == 200:
                try:
                    mensagem = response.json().get("message", "Contagem finalizada com sucesso.")
                except ValueError:
                    mensagem = "Contagem finalizada com sucesso."
                snack_bar(mensagem, colorVariaveis["sucesso"], colorVariaveis["texto"], page)
                navigate_to("/menu")
                return

            try:
                mensagem = response.json().get("message", "Erro ao finalizar contagem.")
            except ValueError:
                mensagem = "Erro ao finalizar contagem."
            snack_bar(mensagem, colorVariaveis["erro"], colorVariaveis["texto"], page)
        except requests.RequestException as exc:
            print(f"Erro ao finalizar contagem: {exc}")
            snack_bar("Erro ao finalizar contagem.", colorVariaveis["erro"], colorVariaveis["texto"], page)

    def atualizar_telas_auxiliares():
        atualizar_resumo()
        atualizar_finalizar()

    def resetar_fluxo_endereco(e):
        novo_endereco = (codendereco_field.value or "").strip()
        if novo_endereco != state["codendereco_atual"]:
            state["codendereco_atual"] = ""
            state["endereco_confirmado"] = False
            codbarra_field.value = ""
            limpar_produto()
            atualizar_estado_codbarra()

    def validar_endereco(e):
        codendereco = (codendereco_field.value or "").strip()

        if not codendereco:
            snack_bar("Informe o código do endereço.", colorVariaveis["erro"], colorVariaveis["texto"], page)
            focar(codendereco_field)
            return

        state["codendereco_atual"] = codendereco
        state["endereco_confirmado"] = True
        atualizar_estado_codbarra()
        focar(codbarra_field)

    def resetar_busca_codbarra(e):
        if state["produto_encontrado"] is not None:
            limpar_produto()

    def buscar_codbarra(e):
        codbarra = (codbarra_field.value or "").strip()

        if not state["endereco_confirmado"]:
            snack_bar("Valide o endereço antes de informar o código de barras.", colorVariaveis["erro"], colorVariaveis["texto"], page)
            focar(codendereco_field)
            return

        if not codbarra:
            snack_bar("Informe o código de barras.", colorVariaveis["erro"], colorVariaveis["texto"], page)
            focar(codbarra_field)
            return

        try:
            response = requests.get(
                f"{base_url}/contagem_inventario_end",
                params={"codbarra": codbarra},
            )
            dados = response.json()
            mensagem = dados.get("message", "Erro ao consultar código de barras.")
            produto = dados.get("produto")

            if response.status_code == 200 and produto:
                state["produto_encontrado"] = {
                    "codprod": produto.get("codprod", ""),
                    "codfab": produto.get("codfab", ""),
                    "descricao": produto.get("descricao", ""),
                }
                produto_codprod.value = f"Codprod: {state['produto_encontrado']['codprod']}"
                produto_codfab.value = f"Codfab: {state['produto_encontrado']['codfab']}"
                produto_descricao.value = f"Descrição: {state['produto_encontrado']['descricao']}"
                produto_info.visible = True
                atualizar_controle(produto_info)
                atualizar_estado_quantidade()
                snack_bar(mensagem, colorVariaveis["sucesso"], colorVariaveis["texto"], page)
                focar(quantidade_field)
                return

            limpar_produto()
            snack_bar(mensagem, colorVariaveis["erro"], colorVariaveis["texto"], page)
            focar(codbarra_field)
        except requests.RequestException as exc:
            print(f"Erro ao consultar codbarra: {exc}")
            limpar_produto()
            snack_bar("Erro ao consultar o código de barras.", colorVariaveis["erro"], colorVariaveis["texto"], page)
            focar(codbarra_field)

    def confirmar_quantidade(e):
        quantidade = (quantidade_field.value or "").strip()

        if state["produto_encontrado"] is None:
            snack_bar("Valide o código de barras antes de informar a quantidade.", colorVariaveis["erro"], colorVariaveis["texto"], page)
            focar(codbarra_field)
            return

        if not quantidade:
            snack_bar("Informe a quantidade.", colorVariaveis["erro"], colorVariaveis["texto"], page)
            focar(quantidade_field)
            return

        if not quantidade.isdigit() or int(quantidade) <= 0:
            snack_bar("Informe uma quantidade válida.", colorVariaveis["erro"], colorVariaveis["texto"], page)
            focar(quantidade_field)
            return

        produto = state["produto_encontrado"]
        item = {
            "codendereco": state["codendereco_atual"],
            "codprod": produto["codprod"],
            "codfab": produto["codfab"],
            "descricao": produto["descricao"],
            "qt": int(quantidade),
        }
        state["itens_resumo"].append(item)
        atualizar_telas_auxiliares()

        codbarra_field.value = ""
        atualizar_controle(codbarra_field)
        limpar_produto()
        snack_bar("Item adicionado ao resumo.", colorVariaveis["sucesso"], colorVariaveis["texto"], page)
        focar(codbarra_field)

    produto_codprod = ft.Text("", color=colorVariaveis["textoPreto"], weight="bold")
    produto_codfab = ft.Text("", color=colorVariaveis["textoPreto"])
    produto_descricao = ft.Text("", color=colorVariaveis["textoPreto"])

    produto_info = ft.Container(
        visible=False,
        padding=12,
        border_radius=10,
        bgcolor="#f4f6fb",
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(
                    "Produto Encontrado",
                    size=18,
                    weight="bold",
                    color=colorVariaveis["titulo"],
                ),
                produto_codprod,
                produto_codfab,
                produto_descricao,
            ],
        ),
    )

    codendereco_field = ft.TextField(
        label="Código do Endereço",
        border_radius=ft.border_radius.all(10),
        border_width=2,
        autofocus=True,
        on_change=resetar_fluxo_endereco,
        on_submit=validar_endereco,
    )

    validar_endereco_btn = ft.ElevatedButton(
        text="Buscar Endereço",
        bgcolor=colorVariaveis["botaoAcao"],
        color=colorVariaveis["texto"],
        on_click=validar_endereco,
    )

    codbarra_field = ft.TextField(
        label="Código de Barras",
        border_radius=ft.border_radius.all(10),
        border_width=2,
        disabled=True,
        hint_text="Disponível após validar o endereço",
        on_change=resetar_busca_codbarra,
        on_submit=buscar_codbarra,
    )

    buscar_codbarra_btn = ft.ElevatedButton(
        text="Buscar Código de Barras",
        bgcolor=colorVariaveis["botaoAcao"],
        color=colorVariaveis["texto"],
        disabled=True,
        on_click=buscar_codbarra,
    )

    quantidade_field = ft.TextField(
        label="Quantidade",
        border_radius=ft.border_radius.all(10),
        border_width=2,
        disabled=True,
        hint_text="Disponível após validar o código de barras",
        keyboard_type=ft.KeyboardType.NUMBER,
        on_submit=confirmar_quantidade,
    )

    confirmar_quantidade_btn = ft.ElevatedButton(
        text="Confirmar Quantidade",
        bgcolor=colorVariaveis["botaoAcao"],
        color=colorVariaveis["texto"],
        on_click=confirmar_quantidade,
    )

    separar_body = ft.Column(
        spacing=16,
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Container(
                padding=16,
                border_radius=12,
                border=ft.border.all(1, colorVariaveis["bordarInput"]),
                content=ft.Column(
                    spacing=16,
                    controls=[
                        ft.Text(
                            "Etapa 1: Endereço",
                            size=18,
                            weight="bold",
                            color=colorVariaveis["titulo"],
                        ),
                        codendereco_field,
                        validar_endereco_btn,
                        ft.Divider(),
                        ft.Text(
                            "Etapa 2: Código de Barras",
                            size=18,
                            weight="bold",
                            color=colorVariaveis["titulo"],
                        ),
                        codbarra_field,
                        buscar_codbarra_btn,
                        produto_info,
                        ft.Divider(),
                        ft.Text(
                            "Etapa 3: Quantidade",
                            size=18,
                            weight="bold",
                            color=colorVariaveis["titulo"],
                        ),
                        quantidade_field,
                        confirmar_quantidade_btn,
                    ],
                ),
            )
        ],
    )

    resumo_body = ft.Column(
        spacing=10,
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        controls=[],
    )

    finalizar_json = ft.Text(
        "[]",
        selectable=True,
        color=colorVariaveis["textoPreto"],
        font_family="monospace",
    )

    finalizar_body = ft.Column(
        spacing=12,
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Text(
                "Produtos prontos para finalização:",
                weight="bold",
                color=colorVariaveis["titulo"],
            ),
            # ft.Container(
            #     padding=12,
            #     border_radius=10,
            #     border=ft.border.all(1, colorVariaveis["bordarInput"]),
            #     content=finalizar_json,
            # ),
            ft.ElevatedButton(
                text="Finalizar",
                bgcolor=colorVariaveis["botaoAcao"],
                color=colorVariaveis["texto"],
                on_click=finalizar_contagem,
            ),
        ],
    )

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

    atualizar_telas_auxiliares()

    return ft.View(
        route="/ajustar_contagem_end",
        controls=[
            header,
            titulo,
            tabs,
        ],
    )
