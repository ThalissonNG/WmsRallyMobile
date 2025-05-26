import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info


def separar_pedido(page: ft.Page, navigate_to, header):
    # Matrícula do usuário logado
    matricula = user_info.get("matricula")

    # Função para exibir snackbars de feedback
    def show_snack(message: str, error: bool = False):
        text_color = ft.colors.WHITE if error else ft.colors.BLACK
        page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color=text_color),
            bgcolor=colorVariaveis['erro'] if error else colorVariaveis['sucesso'],
            action=ft.IconButton(
                icon=ft.icons.CLOSE,
                on_click=lambda e: setattr(page.snack_bar, "open", False) or page.update()
            )
        )
        page.snack_bar.open = True
        page.update()

    # Requisição para buscar dados da separação
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

    # Extrai dados_codigo de barras: lista de tuplas (codprod, codbarra, codendereco)
    raw_codbarra = dados.get("dados_codbarras", [])
    dados_codbarra = []
    for grupo in raw_codbarra:
        if isinstance(grupo, (list, tuple)):
            for tup in grupo:
                if isinstance(tup, (list, tuple)) and len(tup) >= 3:
                    dados_codbarra.append(tuple(tup))

    # Extrai e achata dados_itens
    raw_itens = dados.get("dados_itens", [])
    dados_itens = []
    for grp in raw_itens:
        if isinstance(grp, (list, tuple)):
            for row in grp:
                if isinstance(row, (list, tuple)):
                    dados_itens.append(row)
    if not dados_itens and isinstance(raw_itens, list) and raw_itens and isinstance(raw_itens[0], dict):
        dados_itens = raw_itens

    # Extrai dados_resumo
    dados_resumo = dados.get("dados_resumo", [])

    # Determina produto, fábrica, descrição e detalhes de endereços
    produto_atual = None
    codfab_atual = None
    desc_atual = None
    enderecos = []
    detalhes = []
    if dados_itens:
        primeiro = dados_itens[0]
        if isinstance(primeiro, (list, tuple)):
            produto_atual, codfab_atual, desc_atual = primeiro[2], primeiro[3], primeiro[4]
            seen = set()
            for it in dados_itens:
                if it[2] == produto_atual and len(it) > 12:
                    addr = it[7]
                    if addr not in seen:
                        seen.add(addr)
                        enderecos.append(addr)
                        detalhes.append({
                            'mod': it[8], 'rua': it[9], 'edi': it[10],
                            'niv': it[11], 'apt': it[12]
                        })
        else:
            produto_atual = primeiro.get('codprod')
            codfab_atual = primeiro.get('codfab')
            desc_atual = primeiro.get('descricao')
            seen = set()
            for it in dados_itens:
                if it.get('codprod') == produto_atual:
                    addr = it.get('codendereco')
                    if addr not in seen:
                        seen.add(addr)
                        enderecos.append(addr)
                        detalhes.append({
                            'mod': it.get('modulo'), 'rua': it.get('rua'),
                            'edi': it.get('edificio'), 'niv': it.get('nivel'),
                            'apt': it.get('apto')
                        })

    # Estado de endereço selecionado
    current_endereco = None

    # Componentes para as abas
    title = ft.Text(
        "Separar Pedido", size=24, weight="bold",
        color=colorVariaveis['titulo'], text_align="center"
    )

    # Aba "Separar"
    separar_body = ft.Column(spacing=10, expand=True)
    address_field = ft.TextField(label="Endereço", autofocus=True)
    validate_address_btn = ft.ElevatedButton(text="Validar Endereço")
    barcode_field = ft.TextField(label="Código de Barras")
    validate_barcode_btn = ft.ElevatedButton(text="Validar Código")

    def validar_endereco(e):
        nonlocal current_endereco
        v = address_field.value
        if v and v in [str(x) for x in enderecos]:
            current_endereco = v
            show_snack(f"Endereço {v} validado!", error=False)
            separar_body.controls.clear()
            separar_body.controls.append(ft.Text(f"Cód: {produto_atual} | Fab: {codfab_atual}", weight="bold"))
            separar_body.controls.append(ft.Text(desc_atual or ""))
            separar_body.controls.append(ft.Text("Digite ou bipar o código de barras:"))
            separar_body.controls.append(barcode_field)
            separar_body.controls.append(validate_barcode_btn)
            page.update()
        else:
            show_snack("Endereço incorreto!", error=True)

    def validar_barcode(e):
        codigo = barcode_field.value
        validos = [str(tup[1]) for tup in dados_codbarra
                   if str(tup[0]) == str(produto_atual) and str(tup[2]) == str(current_endereco)]
        show_snack(
            f"Código de barras {codigo} validado!" if codigo in validos else "Código de barras inválido!",
            error=not (codigo in validos)
        )

    validate_address_btn.on_click = validar_endereco
    validate_barcode_btn.on_click = validar_barcode

    if produto_atual is None:
        separar_body.controls.append(ft.Text("Nenhum item a separar"))
    else:
        if detalhes:
            separar_body.controls.append(ft.Text("Endereços:", weight="bold"))
            separar_body.controls.append(
                ft.DataTable(
                    columns=[ft.DataColumn(ft.Text(h)) for h in ["MOD", "RUA", "EDI", "NIV", "APT"]],
                    rows=[
                        ft.DataRow(cells=[ft.DataCell(ft.Text(str(d[col]))) for col in ['mod','rua','edi','niv','apt']])
                        for d in detalhes
                    ], expand=True
                )
            )
            separar_body.controls.append(ft.Divider())
        separar_body.controls.append(ft.Text("Digite ou bipar o endereço:"))
        separar_body.controls.append(address_field)
        separar_body.controls.append(validate_address_btn)

    separar_tab = ft.Tab(text="Separar", content=separar_body)

    # Aba "Resumo"
    resumo_items = []
    for grupo in dados_resumo:
        for item in grupo:
            if item[6] == 0:
                bg, fg = None, ft.colors.BLACK
            elif item[5] == item[4]:
                bg, fg = colorVariaveis['sucesso'], ft.colors.BLACK
            elif item[5] > item[4]:
                bg, fg = colorVariaveis['erro'], ft.colors.WHITE
            else:
                bg, fg = colorVariaveis.get('restante'), ft.colors.BLACK
            resumo_items.append(
                ft.Container(
                    padding=ft.padding.all(8), bgcolor=bg,
                    content=ft.Column(
                        spacing=4,
                        controls=[
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text(str(item[0]), color=fg),
                                    ft.Text(str(item[1]), color=fg),
                                    ft.Text(str(item[3]) if item[3] is not None else '', color=fg),
                                ]
                            ),
                            ft.Text(item[2], color=fg),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text(str(item[4]), color=fg),
                                    ft.Text(str(item[5]), color=fg),
                                    ft.Text(str(item[6]), color=fg),
                                ]
                            ),
                        ]
                    )
                )
            )
            resumo_items.append(ft.Divider())
    resumo_tab = ft.Tab(
        text="Resumo",
        content=ft.Column(expand=True, controls=[
            ft.Text("Resumo do pedido:", color=colorVariaveis['titulo']),
            ft.ListView(expand=True, spacing=4,
                padding=ft.padding.symmetric(vertical=8), controls=resumo_items)
        ])
    )

    # Aba "Finalizar"
    finalizar_tab = ft.Tab(
        text="Finalizar",
        content=ft.Column(
            controls=[
                ft.Text("Concluir separação", color=colorVariaveis['titulo']),
                ft.ElevatedButton(text="Finalizar", on_click=lambda e: navigate_to("/finalizar"))
            ], expand=True
        )
    )

    tabs = ft.Tabs(selected_index=0,
                   tabs=[separar_tab, resumo_tab, finalizar_tab], expand=True)
    return ft.View(route="/separar_pedido", controls=[header, title, tabs], scroll=ft.ScrollMode.AUTO)

if __name__ == "__main__":
    ft.app(target=separar_pedido)
