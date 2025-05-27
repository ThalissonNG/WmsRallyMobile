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

    # Busca dados da API
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

    dados_resumo = dados.get("dados_resumo", [])
    print(f"Dados resumo: {dados_resumo}")

    # Processa dados_codbarras
    raw_codbarra = dados.get("dados_codbarras", [])
    dados_codbarra = []
    for grupo in raw_codbarra:
        for tup in grupo:
            if isinstance(tup, (list, tuple)) and len(tup) >= 3:
                dados_codbarra.append(tuple(tup))

    # Processa dados_itens
    raw_itens = dados.get("dados_itens", [])
    dados_itens = []
    for grp in raw_itens:
        if isinstance(grp, (list, tuple)):
            for row in grp:
                if isinstance(row, (list, tuple)):
                    dados_itens.append(row)
    if not dados_itens and isinstance(raw_itens, list) and raw_itens and isinstance(raw_itens[0], dict):
        dados_itens = raw_itens

        # Processa dados_resumo

    # Identifica produto e endereços
    produto_atual = None
    codfab_atual = None
    desc_atual = None
    enderecos = []
    detalhes = []
    if dados_itens:
        primeiro = dados_itens[0]
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

    # Estados
    current_endereco = None
    current_pedido = None

    # Cabeçalho e título
    title = ft.Text(
        "Separar Pedido", size=24, weight="bold",
        color=colorVariaveis['titulo'], text_align="center"
    )

    # Função para reconstruir aba Resumo
    resumo_listview = ft.ListView(expand=True, spacing=4, padding=ft.padding.symmetric(vertical=8))

    # Componentes aba Separar
    separar_body = ft.Column(spacing=10, expand=True)
    address_field = ft.TextField(label="Endereço", autofocus=True)
    validate_address_btn = ft.ElevatedButton(text="Validar Endereço")
    pedido_field = ft.TextField(label="Código Etiqueta (Pedido)")
    expected_label_text = ft.Text("")
    validate_pedido_btn = ft.ElevatedButton(text="Validar Etiqueta")
    barcode_field = ft.TextField(label="Código de Barras")
    validate_barcode_btn = ft.ElevatedButton(text="Bipar Produto")

    # Validações
    def validar_endereco(e):
        nonlocal current_endereco
        v = address_field.value
        if v in [str(x) for x in enderecos]:
            current_endereco = int(v)
            show_snack(f"Endereço {v} validado!", error=False)
            separar_body.controls.clear()
            valid_pedidos = [str(it[1]) for it in dados_itens if it[7] == current_endereco]
            expected_label_text.value = f"Etiqueta esperada: {valid_pedidos[0] if valid_pedidos else ''}"
            separar_body.controls.extend([
                ft.Text("Digite o código da etiqueta (pedido):"),
                expected_label_text,
                pedido_field,
                validate_pedido_btn
            ])
            page.update()
        else:
            show_snack("Endereço incorreto!", error=True)

    def validar_pedido(e):
        nonlocal current_pedido
        v = pedido_field.value
        valid_pedidos = [str(it[1]) for it in dados_itens if it[7] == current_endereco]
        if v in valid_pedidos:
            current_pedido = int(v)
            show_snack(f"Etiqueta {v} validada!", error=False)
            separar_body.controls.clear()
            separar_body.controls.extend([
                ft.Text(f"Pedido: {current_pedido}", weight="bold"),
                ft.Text(f"Cód: {produto_atual} | Fab: {codfab_atual}", weight="bold"),
                ft.Text(desc_atual or ''),
                ft.Text("Digite ou bipar produto (código de barras):"),
                barcode_field,
                validate_barcode_btn
            ])
            page.update()
        else:
            show_snack("Etiqueta inválida!", error=True)

    def validar_barcode(e):
        codigo = barcode_field.value
        validos = [str(t[1]) for t in dados_codbarra if t[0] == produto_atual and t[2] == current_endereco]
        if codigo in validos:
            show_snack(f"Bipado {codigo}! separados.", error=False)
        else:
            show_snack("Código de barras inválido!", error=True)

    validate_address_btn.on_click = validar_endereco
    validate_pedido_btn.on_click = validar_pedido
    validate_barcode_btn.on_click = validar_barcode

        # UI inicial
    if not produto_atual:
        separar_body.controls.append(ft.Text("Nenhum item a separar"))
    else:
        separar_body.controls.append(ft.Text("Selecione o endereço:"))
        if detalhes:
            separar_body.controls.append(
                ft.DataTable(
                    columns=[ft.DataColumn(ft.Text(h)) for h in ["MOD", "RUA", "EDI", "NIV", "APT"]],
                    rows=[
                        ft.DataRow(cells=[ft.DataCell(ft.Text(str(d[c]))) for c in ['mod', 'rua', 'edi', 'niv', 'apt']])
                        for d in detalhes
                    ],
                    expand=True
                )
            )
        separar_body.controls.extend([address_field, validate_address_btn])

    separar_tab = ft.Tab(text="Separar", content=separar_body)

            # Aba Resumo - primeiro teste: exibir apenas código do produto
    resumo_items = []
    for grupo in dados_resumo:
        for item in grupo:
            # 1º controle
            resumo_items.append(
                ft.Text(f"Pedido: {item[7]} - Etiqueta: {item[8]}")
            )
            # 2º controle
            resumo_items.append(
                ft.Text(f"Codprod: {item[0]} - codfab: {item[1]} - origem:{item[3]}")
            )
            # 3º controle
            resumo_items.append(
                ft.Text(f"Descrição: {item[2]}")
            )
            # 4º controle
            resumo_items.append(
                ft.Text(f"QT: {item[4]} - Sep: {item[5]} - Rest: {item[6]}")
            )
            # divisor
            resumo_items.append(ft.Divider())
    resumo_tab = ft.Tab(
        text="Resumo",
        content=ft.ListView(
            expand=True,
            spacing=4,
            padding=ft.padding.symmetric(vertical=8),
            controls=resumo_items
        )
    )

        # Aba Finalizar
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

    # Componente de abas
    tabs = ft.Tabs(
        selected_index=0,
        tabs=[separar_tab, resumo_tab, finalizar_tab],
        expand=True
    )

    return ft.View(
        route="/separar_pedido",
        controls=[header, title, tabs]
    )

if __name__ == "__main__":
    ft.app(target=separar_pedido)
