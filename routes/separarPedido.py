import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info


def separar_pedido(page: ft.Page, navigate_to, header):
    matricula = user_info.get("matricula")

    def show_snack(message: str, error: bool = False):
        text_color = ft.colors.WHITE if error else ft.colors.BLACK
        page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color=text_color),
            bgcolor=colorVariaveis['erro'] if error else colorVariaveis['sucesso'],
        )
        page.snack_bar.open = True
        page.update()

    def buscar_itens():
        try:
            resp = requests.post(
                f"{base_url}/separarPedido",
                json={"action": "buscar_dados", "matricula": matricula}
            )
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            show_snack(f"Erro ao buscar itens: {e}", error=True)
            return {}

    dados = buscar_itens()

    # Prepara dados resumo e itens
    raw_resumo = dados.get("dados_resumo", [])
    dados_resumo = [[list(item) for item in grupo] for grupo in raw_resumo]
    raw_itens = dados.get("dados_itens", [])
    dados_itens = []
    for grp in raw_itens:
        if isinstance(grp, (list, tuple)):
            dados_itens.extend(grp)
    if not dados_itens and isinstance(raw_itens, list) and raw_itens and isinstance(raw_itens[0], dict):
        dados_itens = raw_itens

    # Processa dados de códigos de barras
    raw_codbarra = dados.get("dados_codbarras", [])
    dados_codbarra = []
    for grupo in raw_codbarra:
        for tup in grupo:
            if isinstance(tup, (list, tuple)) and len(tup) >= 3:
                dados_codbarra.append(tuple(tup))

    # Monta lista única de produtos
    produtos = []
    for it in dados_itens:
        cod = it[2]
        if cod not in produtos:
            produtos.append(cod)
    prod_idx = 0
    etiqueta_idx = 0

    # Atualiza contexto do produto atual (etiquetas, endereços)
    def load_context():
        nonlocal produto_atual, codfab_atual, desc_atual, etiquetas, enderecos, detalhes
        produto_atual = produtos[prod_idx]
        subset = [it for it in dados_itens if it[2] == produto_atual]
        codfab_atual, desc_atual = subset[0][3], subset[0][4]
        etiquetas = []
        enderecos = []
        detalhes.clear()
        for it in subset:
            # coleta etiquetas únicas
            if it[1] not in etiquetas:
                etiquetas.append(it[1])
            # coleta endereços ligados ao produto
            addr = it[7]
            if addr not in enderecos and len(it) > 12:
                enderecos.append(addr)
                detalhes.append({'mod': it[8], 'rua': it[9], 'edi': it[10], 'niv': it[11], 'apt': it[12]})

    produto_atual = codfab_atual = desc_atual = None
    etiquetas = []
    enderecos = []
    detalhes = []
    load_context()
    current_endereco = None
    current_pedido = None

    title = ft.Text(
        "Separar Pedido", size=24, weight="bold",
        color=colorVariaveis['titulo'], text_align="center"
    )

    separar_body = ft.Column(spacing=10, expand=True)
    address_field = ft.TextField(label="Endereço", autofocus=True)
    validate_address_btn = ft.ElevatedButton(text="Validar Endereço")
    pedido_field = ft.TextField(label="Código Etiqueta (Pedido)")
    expected_label_text = ft.Text("")
    validate_pedido_btn = ft.ElevatedButton(text="Validar Etiqueta")
    barcode_field = ft.TextField(label="Código de Barras")
    validate_barcode_btn = ft.ElevatedButton(text="Bipar Produto")

    # Monta controles de resumo (sem alterações)
    def gerar_resumo_list():
        controls = []
        for grupo in dados_resumo:
            for item in grupo:
                codprod, codfab, desc, orig, total, sep, rest, numped, etiqueta = item
                if sep == total:
                    bg, fg = colorVariaveis['sucesso'], colorVariaveis['textoPreto']
                elif sep == 0:
                    bg, fg = None, colorVariaveis['texto']
                elif sep > total:
                    bg, fg = colorVariaveis['erro'], colorVariaveis['texto']
                else:
                    bg, fg = colorVariaveis.get('restante'), colorVariaveis['textoPreto']
                controls.append(
                    ft.Container(
                        padding=ft.padding.all(12), bgcolor=bg,
                        content=ft.Column(spacing=6, controls=[
                            ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                   controls=[ft.Text(f"Pedido: {numped}", color=fg), ft.Text(f"Etiqueta: {etiqueta}", color=fg)]),
                            ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                   controls=[ft.Text(f"Cód: {codprod}", color=fg), ft.Text(f"Fab: {codfab}", color=fg), ft.Text(f"Origem: {orig}", color=fg)]),
                            ft.Text(desc, color=fg),
                            ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                   controls=[ft.Text(f"Total: {total}", color=fg), ft.Text(f"Sep: {sep}", color=fg), ft.Text(f"Rest: {rest}", color=fg)]),
                            ft.Divider()
                        ])
                    )
                )
        return controls

    def construir_separar_ui():
        separar_body.controls.clear()
        # limpa campos ao voltar
        address_field.value = ""
        pedido_field.value = ""
        separar_body.controls.append(ft.Text("Selecione o endereço:"))
        # sempre mostra tabela de detalhes de endereços
        if detalhes:
            separar_body.controls.append(
                ft.DataTable(
                    columns=[ft.DataColumn(ft.Text(h)) for h in ["MOD", "RUA", "EDI", "NIV", "APT"]],
                    rows=[
                        ft.DataRow(cells=[ft.DataCell(ft.Text(str(d[c]))) for c in ['mod', 'rua', 'edi', 'niv', 'apt']])
                        for d in detalhes
                    ], expand=True
                )
            )
        separar_body.controls.extend([
            address_field,
            validate_address_btn
        ])

    def validar_endereco(e):
        nonlocal current_endereco
        v = address_field.value
        if v and int(v) in enderecos:
            current_endereco = int(v)
            show_snack(f"Endereço {v} válido!", False)
            separar_body.controls.clear()
            expected_label_text.value = f"Etiqueta esperada: {etiquetas[etiqueta_idx]}"
            pedido_field.value = ""
            separar_body.controls.extend([
                ft.Text("Digite o código da etiqueta (pedido):"),
                expected_label_text,
                pedido_field,
                validate_pedido_btn
            ])
            page.update()
        else:
            show_snack("Endereço incorreto!", True)

    def validar_pedido(e):
        nonlocal current_pedido
        v = pedido_field.value
        if v and int(v) == etiquetas[etiqueta_idx]:
            current_pedido = int(v)
            show_snack(f"Etiqueta {v} válida!", False)
            separar_body.controls.clear()
            separar_body.controls.extend([
                ft.Text(f"Pedido: {current_pedido}", weight="bold"),
                ft.Text(f"Cód: {produto_atual} | Fab: {codfab_atual}", weight="bold"),
                ft.Text(desc_atual),
                ft.Text("Digite ou bipar produto (código de barras):"),
                barcode_field,
                validate_barcode_btn
            ])
            page.update()
        else:
            show_snack("Etiqueta inválida!", True)

    def validar_barcode(e):
        nonlocal etiqueta_idx, prod_idx, current_pedido, current_endereco
        codigo = barcode_field.value
        validos = [str(t[1]) for t in dados_codbarra if t[0] == produto_atual and t[2] == current_endereco]
        print(f"Códigos válidos para produto {produto_atual}, endereço {current_endereco}: {validos}")
        if codigo in validos and current_pedido is not None:
            # encontra item correspondente para atualizar
            item_concluido = False
            for grupo in dados_resumo:
                for item in grupo:
                    codprod, *_ , total, sep, rest, numped, etiqueta = item
                    if etiqueta == current_pedido and codprod == produto_atual:
                        item[5] += 1
                        item[6] = total - item[5]
                        if item[5] == total:
                            item_concluido = True
                        break
                if item_concluido:
                    break

            # limpa campo bip
            barcode_field.value = ""
            barcode_field.focus()
            # atualiza aba Resumo
            resumo_tab.content = ft.ListView(
                expand=True,
                spacing=4,
                padding=ft.padding.symmetric(vertical=8),
                controls=gerar_resumo_list()
            )
            # só volta para selecionar endereço se etiqueta finalizada
            if item_concluido:
                etiqueta_idx += 1
                if etiqueta_idx < len(etiquetas):
                    current_pedido = etiquetas[etiqueta_idx]
                    show_snack(f"Próxima etiqueta {current_pedido}")
                else:
                    prod_idx += 1
                    etiqueta_idx = 0
                    if prod_idx < len(produtos):
                        load_context()
                        show_snack(f"Iniciando produto {produto_atual}")
                    else:
                        show_snack("Separação concluída!", False)
                construir_separar_ui()
            page.update()
        else:
            barcode_field.value = ""
            barcode_field.focus()
            show_snack("Código de barras inválido!", True)
            page.update()

    validate_address_btn.on_click = validar_endereco
    validate_pedido_btn.on_click = validar_pedido
    validate_barcode_btn.on_click = validar_barcode

    # UI inicial de Separar
    construir_separar_ui()

    separar_tab = ft.Tab(text="Separar", content=separar_body)
    resumo_tab = ft.Tab(
        text="Resumo",
        content=ft.ListView(
            expand=True,
            spacing=4,
            padding=ft.padding.symmetric(vertical=8),
            controls=gerar_resumo_list()
        )
    )
    finalizar_tab = ft.Tab(
        text="Finalizar",
        content=ft.Column(
            controls=[
                ft.Text("Concluir separação", color=colorVariaveis['titulo']),
                ft.ElevatedButton(text="Finalizar", on_click=lambda e: navigate_to("/finalizar"))
            ],
            expand=True
        )
    )
    tabs = ft.Tabs(
        selected_index=0,
        tabs=[separar_tab, resumo_tab, finalizar_tab],
        expand=True
    )
    return ft.View(route="/separar_pedido", controls=[header, title, tabs])