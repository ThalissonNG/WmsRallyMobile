import flet as ft
import requests
from routes.config.config import colorVariaveis, base_url, user_info, snack_bar

def separar_multiplos_pedidos(page: ft.Page, navigate_to, header, arguments=None):
    print(f"Arguments recebidos: {arguments}")
    
    codfilial = user_info.get("codfilial")
    matricula = user_info.get("matricula")
    
    # Extrair os números dos pedidos de 'arguments' e formatar como string separada por vírgula
    numpeds_list = [str(arg.get("numped")) for arg in arguments] if arguments else []
    numpeds_str = ", ".join(numpeds_list)

    def buscar_itens_pedido(numpeds, codfilial):
        try:
            response = requests.get(
                f"{base_url}/separar_multiplos_pedido",
                params={
                    "numped": numpeds,
                    "codfilial": codfilial,
                    "matricula": matricula
                }
            )
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Erro ao buscar itens: {response.status_code}")
                return None
        except Exception as e:
            print(f"Exceção ao buscar itens: {e}")
            return None

    # Chamada inicial para buscar os itens
    dados_itens = buscar_itens_pedido(numpeds_str, codfilial)
    print(f"Itens recuperados: {dados_itens}")

    def contruir_produto(item):
        codprod_item = item[1]
        codfab_item = item[2]
        descricao_item = item[3]
        qt_pedida_item = item[4]
        qt_separada_item = item[5]
        qt_restante_item = item[6]
        qt_endereco_item = item[7]
        codendereco_item = item[8]

        input_codbarra = ft.TextField(
            label="Código de Barras (Em breve)",
            expand=True,
            autofocus=True,
            keyboard_type=ft.KeyboardType.NUMBER,
            on_submit=lambda e: validar_codbarra(input_codbarra.value, codprod_item)
        )

        def finalizar_modal(e):
            page.close(modal_produto)
            # Aqui no futuro chamaria buscar_itens_pedido novamente ou validaria o codbarra
            snack_bar("Produto processado (Simulação)", colorVariaveis['sucesso'], colorVariaveis['textoPreto'], page)

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
                        "codendereco": codendereco_item
                    }
                )
                resposta = response.json()
                mensagem = resposta.get("message")
                if response.status_code == 200:
                    snack_bar(mensagem, colorVariaveis['sucesso'], colorVariaveis['textoPreto'], page)
                else:
                    snack_bar(mensagem, colorVariaveis['erro'], colorVariaveis['texto'], page)
            except ValueError:
                snack_bar("Código inválido.", colorVariaveis['erro'], colorVariaveis['texto'], page)


        modal_content = ft.Column(
            controls=[
                ft.Text(f"Codprod: {codprod_item}"),
                ft.Text(f"Codfab: {codfab_item}"),
                ft.Text(f"Descrição: {descricao_item}"),
                ft.Row(
                    controls=[
                        ft.Text(f"Qt Pedida: {qt_pedida_item}"),
                        ft.Text(f"Qt Separada: {qt_separada_item}"),
                        ft.Text(f"Qt Endereço: {qt_endereco_item}"),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    wrap=True,
                    expand=True
                ),
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

    # Chamada inicial para buscar os itens
    dados_itens = buscar_itens_pedido(numpeds_str, codfilial)
    if dados_itens and "pedidos" in dados_itens:
        pedidos_recebidos = dados_itens.get("pedidos", [])
        if isinstance(pedidos_recebidos, list) and len(pedidos_recebidos) > 0:
            # Verifica se é uma lista de listas ou uma lista única de um item
            # Se o primeiro elemento for uma lista, pegamos essa lista como o primeiro item
            # Se não for (ex: é um int correspondente ao codfilial), a própria pedidos_recebidos é o item
            if isinstance(pedidos_recebidos[0], list):
                primeiro_item = pedidos_recebidos[0]
            else:
                primeiro_item = pedidos_recebidos
            
            aba_separar.content.controls.extend(construir_endereco(primeiro_item))

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
