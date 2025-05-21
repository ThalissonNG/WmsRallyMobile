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
            content=ft.Text(
                message,
                color=text_color,
            ),
            bgcolor=colorVariaveis['erro'] if error else colorVariaveis['sucesso'],
        )
        page.snack_bar.open = True
        page.update()

    # Busca dados de separação via API
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

    # Título da página
    title = ft.Text(
        "Separar Pedido",
        size=24,
        weight="bold",
        color=colorVariaveis['titulo'],
        text_align="center"
    )

    # Determina produto atual, codfab, descrição e endereços
    produto_atual = None
    codfab_atual = None
    desc_atual = None
    enderecos = []
    if dados_itens:
        primeiro = dados_itens[0]
        if isinstance(primeiro, dict):
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
        else:
            produto_atual = primeiro[2]
            codfab_atual = primeiro[3]
            desc_atual = primeiro[4]
            seen = set()
            for it in dados_itens:
                if isinstance(it, (list, tuple)) and len(it) > 7 and it[2] == produto_atual:
                    addr = it[7]
                    if addr not in seen:
                        seen.add(addr)
                        enderecos.append(addr)

    # Campo de endereço e botão de validação
    address_field = ft.TextField(
        label="Endereço",
        # hint_text=enderecos and "Ex: " + ", ".join(str(e) for e in enderecos) or "",
        autofocus=True
    )

    def validar_endereco(e):
        valor = address_field.value
        print(f"Valor do endereço: {valor}")
        if valor and valor in [str(x) for x in enderecos]:
            show_snack(f"Endereço {valor} validado!", error=False)
        else:
            show_snack(f"Endereço incorreto!", error=True)

    validate_button = ft.ElevatedButton(
        text="Validar",
        on_click=validar_endereco
    )

    # Monta aba "Separar"
    separar_controls = []
    if produto_atual is None:
        separar_controls.append(ft.Text("Nenhum item a separar"))
    else:
        separar_controls.append(
            ft.Text(f"Cód: {produto_atual} | Fab: {codfab_atual}", weight="bold")
        )
        separar_controls.append(ft.Text(desc_atual or ""))
        separar_controls.append(ft.Text("Digite ou bipar o endereço:"))
        separar_controls.append(
            ft.Row(
                controls=[address_field, validate_button],
                alignment=ft.MainAxisAlignment.START,
                spacing=10
            )
        )
    separar_tab = ft.Tab(
        text="Separar",
        content=ft.Column(controls=separar_controls, expand=True)
    )

    # Monta aba "Resumo"
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
                    padding=ft.padding.all(8),
                    bgcolor=bg,
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
        content=ft.Column(
            expand=True,
            controls=[
                ft.Text("Resumo do pedido:", color=colorVariaveis['titulo']),
                ft.ListView(
                    expand=True,
                    spacing=4,
                    padding=ft.padding.symmetric(vertical=8),
                    controls=resumo_items
                )
            ]
        )
    )

    # Monta aba "Finalizar"
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
        controls=[header, title, tabs],
        scroll=ft.ScrollMode.AUTO
    )