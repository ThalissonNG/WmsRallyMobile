import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info


# ... (imports e início iguais)

def separar_pedido_unico(page: ft.Page, navigate_to, header):
    print("Entrou na tela de separar pedido UNICO")
    matricula = user_info.get("matricula")
    codfilial = user_info.get("codfilial")

    def show_snack(message: str, error: bool = False):
        text_color = ft.Colors.WHITE if error else ft.Colors.BLACK
        page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color=text_color),
            bgcolor=colorVariaveis['erro'] if error else colorVariaveis['sucesso'],
            duration=3000,
        )
        page.snack_bar.open = True
        page.update()

    def buscar_itens():
        try:
            resp = requests.post(
                f"{base_url}/separarPedidoUnico",
                json={"action": "buscar_dados", "matricula": matricula, "codfilial": codfilial},
            )
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            show_snack(f"Erro ao buscar itens: {e}", error=True)
            return {}

    dados = buscar_itens()

    raw_resumo = dados.get("dados_resumo", [])
    dados_resumo = [[list(item) for item in grupo] for grupo in raw_resumo]

    raw_itens = dados.get("dados_itens", [])
    dados_itens = []
    for grp in raw_itens:
        if isinstance(grp, (list, tuple)):
            dados_itens.extend(grp)

    try:
        dados_itens.sort(key=lambda it: (it[7], it[8], it[9], it[10], it[11]))
    except Exception as err:
        print("WARN sort itens:", err)

    if not dados_itens and isinstance(raw_itens, list) and raw_itens and isinstance(raw_itens[0], dict):
        dados_itens = raw_itens

    raw_codbarra = dados.get("dados_codbarras", [])
    dados_codbarra = []
    for grupo in raw_codbarra:
        for tup in grupo:
            if isinstance(tup, (list, tuple)) and len(tup) >= 3:
                dados_codbarra.append(tuple(tup))  # (codprod, codbarra, codendereco)

    produtos = []
    for it in dados_itens:
        codprod = it[1]
        if codprod not in produtos:
            produtos.append(codprod)

    if not produtos:
        show_snack("Nenhum item para separar", error=True)
        return ft.View(route="/separar_pedido_unico", controls=[header, ft.Text("Nenhum item para separar")])

    prod_idx = 0

    def load_context():
        nonlocal produto_atual, codfab_atual, desc_atual, enderecos, detalhes
        produto_atual = produtos[prod_idx]
        subset = [it for it in dados_itens if it[1] == produto_atual]
        codfab_atual, desc_atual = subset[0][2], subset[0][3]
        enderecos = []
        detalhes.clear()
        for it in subset:
            codend = it[6]
            if codend not in enderecos:
                enderecos.append(codend)
                detalhes.append({'mod': it[7], 'rua': it[8], 'edi': it[9], 'niv': it[10], 'apt': it[11]})

    produto_atual = codfab_atual = desc_atual = None
    enderecos = []
    detalhes = []
    try:
        load_context()
    except Exception as e:
        show_snack(f"Erro ao preparar itens: {e}", error=True)
        # ❗ NÃO use appbar=header aqui
        return ft.View(route="/separar_pedido_unico", controls=[header, ft.Text("Erro ao preparar itens.")])

    current_endereco = None

    title = ft.Text(
        "Separar Pedido - Único",
        size=24, weight="bold",
        color=colorVariaveis['titulo'],
        text_align="center",
    )

    separar_body = ft.Column(spacing=10, expand=True)

    address_field = ft.TextField(
        label="Endereço",
        autofocus=True,
        on_submit=lambda e: validate_address_btn.on_click(e),
    )
    validate_address_btn = ft.ElevatedButton(text="Validar Endereço")

    barcode_field = ft.TextField(
        label="Código de Barras",
        # deixe autofocus só em UM campo por etapa
        on_submit=lambda e: validate_barcode_btn.on_click(e),
        autofocus=True,
    )
    validate_barcode_btn = ft.ElevatedButton(text="Bipar Produto")
    skip_prod_btn = ft.ElevatedButton(text="Pular Produto")

    def gerar_resumo_list():
        controls = []
        for grupo in dados_resumo or []:
            for item in grupo:
                if not isinstance(item, (list, tuple)) or len(item) < 8:
                    print("Formato inesperado em dados_resumo:", item)
                    continue
                codprod, codfab, desc, orig, total, sep, rest, numped = item[:8]

                if sep == total:
                    bg, fg = colorVariaveis['sucesso'], colorVariaveis['textoPreto']
                elif sep == 0:
                    bg, fg = None, None
                elif isinstance(sep, (int, float)) and isinstance(total, (int, float)) and sep > total:
                    bg, fg = colorVariaveis['erro'], colorVariaveis['texto']
                else:
                    bg, fg = colorVariaveis.get('restante'), colorVariaveis['textoPreto']

                controls.append(
                    ft.Container(
                        padding=ft.padding.all(12),
                        bgcolor=bg,
                        content=ft.Column(
                            spacing=6,
                            controls=[
                                ft.Text(f"Pedido: {numped}", color=fg),
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    controls=[
                                        ft.Text(f"Cód: {codprod}", color=fg),
                                        ft.Text(f"Fab: {codfab}", color=fg),
                                        ft.Text(f"Origem: {orig}", color=fg),
                                    ],
                                ),
                                ft.Text(str(desc), color=fg),
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    controls=[
                                        ft.Text(f"Total: {total}", color=fg),
                                        ft.Text(f"Sep: {sep}", color=fg),
                                        ft.Text(f"Rest: {rest}", color=fg),
                                    ],
                                ),
                                ft.Divider(),
                            ],
                        ),
                    )
                )
        return controls

    def construir_separar_ui():
        separar_body.controls.clear()
        address_field.value = ""
        barcode_field.value = ""

        separar_body.controls.append(ft.Text("Selecione o endereço:"))

        if detalhes:
            try:
                separar_body.controls.append(
                    ft.DataTable(
                        column_spacing=35,
                        horizontal_margin=10,
                        columns=[ft.DataColumn(ft.Text(h)) for h in ["MOD", "RUA", "EDI", "NIV", "APT"]],
                        rows=[
                            ft.DataRow(
                                cells=[ft.DataCell(ft.Text(str(d[c]))) for c in ['mod', 'rua', 'edi', 'niv', 'apt']]
                            )
                            for d in detalhes
                        ],
                        expand=True,
                    )
                )
            except Exception as err:
                print("Erro ao montar DataTable:", err)
                separar_body.controls.append(ft.Text("Falha ao exibir endereços."))

        separar_body.controls.extend([address_field, validate_address_btn])

    def mostrar_barcode_ui():
        separar_body.controls.clear()
        barcode_field.value = ""
        separar_body.controls.extend([
            ft.Text(f"Cód: {produto_atual} | Fab: {codfab_atual}", weight="bold"),
            ft.Text(desc_atual),
            ft.Text("Digite ou bipar o produto (código de barras):"),
            barcode_field,
            validate_barcode_btn,
            skip_prod_btn,
        ])
        page.update()

    def finalizar_separacao_ui():
        separar_body.controls.clear()
        separar_body.controls.append(ft.Text("Separação concluída!", weight="bold"))

    def validar_endereco(e):
        nonlocal current_endereco
        v = address_field.value.strip()
        if v and v.isdigit() and int(v) in enderecos:
            current_endereco = int(v)
            show_snack(f"Endereço {v} válido!", False)
            for grupo in dados_resumo:
                for item in grupo:
                    if len(item) >= 4 and item[0] == produto_atual:
                        item[3] = current_endereco
            mostrar_barcode_ui()
        else:
            show_snack("Endereço incorreto!", True)

    def validar_barcode(e):
        nonlocal prod_idx
        codigo = (barcode_field.value or "").strip()
        validos = [str(t[1]) for t in dados_codbarra if t[0] == produto_atual and t[2] == current_endereco]
        print(f"Códigos válidos para produto {produto_atual}, endereço {current_endereco}: {validos}")

        if codigo and codigo in validos:
            barcode_field.value = ""
            for grupo in dados_resumo:
                for item in grupo:
                    if len(item) >= 7:
                        codprod, total, sep = item[0], item[4], item[5]
                        if codprod == produto_atual and sep < total:
                            item[5] = sep + 1
                            item[6] = total - item[5]
                            break

            try:
                resumo_controls = gerar_resumo_list()
            except Exception as err:
                print("Erro ao montar resumo:", err)
                resumo_controls = []

            resumo_tab.content = ft.ListView(
                expand=True,
                spacing=4,
                padding=ft.padding.symmetric(vertical=8),
                controls=resumo_controls,
            )
            show_snack("Produto separado!")

            restante = sum(
                item[6] for grupo in dados_resumo for item in grupo
                if isinstance(item, (list, tuple)) and len(item) >= 7 and item[0] == produto_atual
            )
            if restante == 0:
                prod_idx += 1
                if prod_idx < len(produtos):
                    load_context()
                    show_snack(f"Iniciando produto {produto_atual}")
                    construir_separar_ui()
                else:
                    show_snack("Separação concluída!", False)
                    finalizar_separacao_ui()
            else:
                mostrar_barcode_ui()
        else:
            barcode_field.value = ""
            barcode_field.focus()
            show_snack("Código de barras inválido!", True)

        page.update()

    def pular_produto(e):
        nonlocal prod_idx
        produto_pulado = produtos.pop(prod_idx)
        produtos.append(produto_pulado)
        if prod_idx >= len(produtos):
            prod_idx = len(produtos) - 1
        load_context()
        show_snack(f"Produto {produto_pulado} pulado!")
        construir_separar_ui()

    def finalizar(e):
        try:
            resp = requests.post(
                f"{base_url}/separarPedidoUnico",
                json={"action": "finalizar", "matricula": matricula, "dados_resumo": dados_resumo},
            )
            if resp.status_code == 200:
                show_snack("Separação finalizada com sucesso!")
                navigate_to("/buscar_pedido_unico")
            else:
                show_snack("Erro ao finalizar separação!", error=True)
        except Exception as err:
            print("Erro ao finalizar separação (requisicao):", err)
            show_snack("Erro ao finalizar separação! (requisicao)", error=True)

    validate_address_btn.on_click = validar_endereco
    validate_barcode_btn.on_click = validar_barcode
    skip_prod_btn.on_click = pular_produto

    construir_separar_ui()

    separar_tab = ft.Tab(text="Separar", content=separar_body)

    try:
        resumo_controls = gerar_resumo_list()
    except Exception as err:
        print("Erro ao montar resumo inicial:", err)
        resumo_controls = [ft.Text("Falha ao carregar resumo.")]

    resumo_tab = ft.Tab(
        text="Resumo",
        content=ft.ListView(
            expand=True,
            spacing=4,
            padding=ft.padding.symmetric(vertical=8),
            controls=resumo_controls,
        ),
    )
    finalizar_tab = ft.Tab(
        text="Finalizar",
        content=ft.Column(
            controls=[ft.Text("Concluir separação", color=colorVariaveis['titulo']),
                      ft.ElevatedButton(text="Finalizar", on_click=lambda e: finalizar(e))],
            expand=True,
        ),
    )

    tabs = ft.Tabs(selected_index=0, tabs=[separar_tab, resumo_tab, finalizar_tab], expand=True)

    # ✅ header vai em controls; nada de appbar
    return ft.View(route="/separar_pedido_unico", controls=[header, title, tabs])
