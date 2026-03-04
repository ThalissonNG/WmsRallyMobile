import flet as ft
import requests
from routes.config.config import colorVariaveis, base_url, user_info, snack_bar

def separar_multiplos_pedidos(page: ft.Page, navigate_to, header, arguments=None):
    print(f"Arguments recebidos: {arguments}")
    
    codfilial = user_info.get("codfilial")
    matricula = user_info.get("matricula")
    dados_itens = None
    
    # Extrair os números dos pedidos de 'arguments' e formatar como string separada por vírgula
    numpeds_list = [str(arg.get("numped")) for arg in arguments] if arguments else []
    numpeds_str = ", ".join(numpeds_list)

    def buscar_itens_pedido(numpeds, codfilial):
        try:
            response = requests.get(
                f"{base_url}/separar_multiplos_pedido",
                params={
                    "numpeds": numpeds,
                    "codfilial": codfilial,
                    "matricula": matricula
                }
            )
            if response.status_code == 200:
                print(response.json())
                return response.json()
            else:
                print(f"Erro ao buscar itens: {response.status_code}")
                return None
        except Exception as e:
            print(f"Exceção ao buscar itens: {e}")
            return None

    def refresh_separar_view():
        nonlocal dados_itens
        dados_itens = buscar_itens_pedido(numpeds_str, codfilial)
        aba_separar.content.controls.clear()
        if dados_itens and "pedidos" in dados_itens:
            pedidos_recebidos = dados_itens.get("pedidos", [])
            if isinstance(pedidos_recebidos, list) and len(pedidos_recebidos) > 0:
                if isinstance(pedidos_recebidos[0], list):
                    item = pedidos_recebidos[0]
                else:
                    item = pedidos_recebidos
                aba_separar.content.controls.extend(construir_endereco(item))
            else:
                aba_separar.content.controls.append(
                    ft.Container(
                        content=ft.Text("Todos os pedidos foram separados!", size=20, weight="bold"),
                        padding=20,
                        alignment=ft.alignment.center
                    )
                )
        page.update()

    def validar_etiqueta_modal(item):
        codetiqueta_esperada = str(item[16])
        
        def validar_etiquet_acao(e):
            if input_etiqueta.value == codetiqueta_esperada:
                snack_bar("Etiqueta validada com sucesso!", colorVariaveis['sucesso'], colorVariaveis['textoPreto'], page)
                page.close(modal_etiqueta)
                refresh_separar_view()
            else:
                snack_bar("Etiqueta incorreta!", colorVariaveis['erro'], colorVariaveis['texto'], page)
                input_etiqueta.value = ""
                input_etiqueta.focus()
                page.update()

        input_etiqueta = ft.TextField(
            label="Validar Etiqueta",
            autofocus=True,
            on_submit=validar_etiquet_acao
        )

        modal_etiqueta = ft.AlertDialog(
            modal=True,
            title=ft.Text("Validar Etiqueta do Produto"),
            content=ft.Column([
                ft.Text(f"Leia a etiqueta: {codetiqueta_esperada}", size=16, weight="bold"),
                input_etiqueta,
                ft.ElevatedButton(
                    "Confirmar Etiqueta",
                    bgcolor=colorVariaveis['botaoAcao'],
                    color=colorVariaveis['texto'],
                    on_click=validar_etiquet_acao,
                    width=300
                )
            ], tight=True),
        )
        page.open(modal_etiqueta)

    def contruir_produto(item):
        codprod_item = item[1]
        codfab_item = item[2]
        descricao_item = item[3]
        qt_pedida_item = item[4]
        qt_separada_item = item[5]
        qt_restante_item = item[6]
        qt_endereco_item = item[7]
        codendereco_item = item[8]
        codetiqueta_item = item[16]
        numped_item = item[17]

        txt_qt_separada = ft.Text(f"Qt Separada: {qt_separada_item}")
        txt_qt_restante = ft.Text(f"Qt Restante: {qt_restante_item}")

        input_codbarra = ft.TextField(
            label="Código de Barras",
            expand=True,
            autofocus=True,
            keyboard_type=ft.KeyboardType.NUMBER,
            on_submit=lambda e: validar_codbarra(input_codbarra.value, codprod_item)
        )

        def validar_codbarra(codbarra, codprod):
            if not codbarra:
                snack_bar("Código de barras obrigatório.", colorVariaveis['erro'], colorVariaveis['texto'], page)
                return
            try:
                response = requests.get(
                    f"{base_url}/separar_multiplos_pedido",
                    params={
                        "codfilial": codfilial,
                        "codbarra": codbarra,
                        "codprod": codprod,
                        "qtrestante": qt_restante_item,
                        "codendereco": codendereco_item,
                        "numped": numped_item,
                        "numpeds": numpeds_str,
                        "codetiqueta": codetiqueta_item
                    }
                )
                resposta = response.json()
                mensagem = resposta.get("message")
                
                if response.status_code == 200:
                    snack_bar(mensagem, colorVariaveis['sucesso'], colorVariaveis['textoPreto'], page)
                    # Atualiza dados internos e UI do modal
                    novos_dados = buscar_itens_pedido(numpeds_str, codfilial)
                    if novos_dados and "pedidos" in novos_dados:
                        peds = novos_dados.get("pedidos", [])
                        # Encontra o item atual na nova lista para atualizar as quantidades
                        item_atualizado = None
                        if isinstance(peds[0], list):
                            for p in peds:
                                if str(p[1]) == str(codprod) and str(p[17]) == str(numped_item):
                                    item_atualizado = p
                                    break
                        else:
                            if str(peds[1]) == str(codprod) and str(peds[17]) == str(numped_item):
                                item_atualizado = peds
                        
                        if item_atualizado:
                            txt_qt_separada.value = f"Qt Separada: {item_atualizado[5]}"
                            txt_qt_restante.value = f"Qt Restante: {item_atualizado[6]}"
                            input_codbarra.value = ""
                            input_codbarra.focus()
                            page.update()

                elif response.status_code == 202:
                    snack_bar(mensagem, colorVariaveis['sucesso'], colorVariaveis['textoPreto'], page)
                    page.close(modal_produto)
                    validar_etiqueta_modal(item)
                else:
                    snack_bar(mensagem, colorVariaveis['erro'], colorVariaveis['texto'], page)
            except Exception as ex:
                snack_bar(f"Erro: {str(ex)}", colorVariaveis['erro'], colorVariaveis['texto'], page)

        modal_content = ft.Column(
            controls=[
                ft.Text(f"Codprod: {codprod_item}"),
                ft.Text(f"Codfab: {codfab_item}"),
                ft.Text(f"Descrição: {descricao_item}"),
                ft.Row(
                    controls=[
                        ft.Text(f"Qt Pedida: {qt_pedida_item}"),
                        txt_qt_separada,
                        ft.Text(f"Qt Endereço: {qt_endereco_item}"),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    wrap=True,
                    expand=True
                ),
                txt_qt_restante,
                ft.Divider(),
                input_codbarra,
                ft.ElevatedButton(
                    "Confirmar",
                    bgcolor=colorVariaveis['botaoAcao'],
                    color=colorVariaveis['texto'],
                    on_click=lambda e: validar_codbarra(input_codbarra.value, codprod_item),
                    width=300
                ),
            ],
            tight=True,
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
        )

        modal_produto = ft.AlertDialog(
            title=ft.Text("Conferência de Produto"),
            content=modal_content,
        )
        
        page.open(modal_produto)

    def construir_endereco(item):
        qt_separada = int(item[5])
        codendereco_item = int(item[8])
        mod_item = item[9]
        rua_item = item[10]
        edi_item = item[11]
        nivel_item = item[12]
        apto_item = item[13]
        tipo_entrega = item[15] if len(item) > 15 and item[15] is not None else "Entrega Própria"

        def validar_endereco(e):
            try:
                if not input_coendereco.value:
                    return
                
                codendereco_digitado = int(input_coendereco.value)
                if codendereco_digitado == codendereco_item:
                    snack_bar("Endereço validado!", colorVariaveis['sucesso'], colorVariaveis['textoPreto'], page)
                    contruir_produto(item)
                else:
                    snack_bar("Endereço incorreto.", colorVariaveis['erro'], colorVariaveis['texto'], page)
            except ValueError:
                snack_bar("Código inválido.", colorVariaveis['erro'], colorVariaveis['texto'], page)

        
        input_coendereco = ft.TextField(
            label="Código do Endereço",
            expand=True,
            autofocus=True,
            keyboard_type=ft.KeyboardType.NUMBER,
            on_submit=validar_endereco
        )

        return [
            ft.Text(f"Tipo de entrega: {tipo_entrega}", weight="bold", size=12, color=ft.Colors.RED_400),
            ft.Text("Endereço do produto", weight="bold", size=16),
            ft.Row(
                controls=[
                    ft.Text(f"Qt Separada: {qt_separada}", weight="bold"),
                    ft.Text(f"Módulo: {mod_item}", weight="bold"),
                    ft.Text(f"Rua: {rua_item}", weight="bold"),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.Row(
                controls=[
                    ft.Text(f"Edi: {edi_item}", weight="bold"),
                    ft.Text(f"Nível: {nivel_item}", weight="bold"),
                    ft.Text(f"Apto: {apto_item}", weight="bold"),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.Divider(),
            input_coendereco,
            ft.ElevatedButton(
                "Validar endereço",
                expand=True,
                bgcolor=colorVariaveis['botaoAcao'],
                color=colorVariaveis['texto'],
                on_click=validar_endereco
            )
        ]


    titulo = ft.Text(
        "Separar Múltiplos Pedidos",
        size=24, weight="bold",
        color=colorVariaveis['titulo']
    )

    aba_separar = ft.Tab(
        text="Separar",
        content=ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True, controls=[])
    )
    
    aba_resumo = ft.Tab(
        text="Resumo",
        content=ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True, controls=[ft.Text("Resumo em breve")])
    )
    
    aba_finalizar = ft.Tab(
        text="Finalizar",
        content=ft.Column(controls=[ft.Text("Finalizar em breve")], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

    # Chamada inicial para preencher a tela
    refresh_separar_view()

    # Abas
    tabs = ft.Tabs(
        selected_index=0,
        tabs=[aba_separar, aba_resumo, aba_finalizar],
        expand=1,
    )

    return ft.View(
        route="/separar_multiplos_pedidos",
        controls=[
            header,
            titulo,
            ft.Container(height=10),
            tabs
        ]
    )
