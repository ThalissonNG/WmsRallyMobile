import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def separar_pedido_dist(page: ft.Page, navigate_to, header, arguments=None):
    matricula = user_info.get("matricula")
    codfilial = user_info.get("codfilial")
    pedido = arguments.get("numped")
    # print(f"User config na tela Separar Pedido Dist: {matricula}, pedido: {pedido}")

    titulo = ft.Text(
        f"Pedido: {pedido}",
        size=24, weight="bold",
        color=colorVariaveis['titulo']
    )
    aba_separar = ft.Tab(
        text="Separar",
        content=ft.Column(
            spacing=10,
            controls=[
                
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True
        ),
    )
    aba_resumo = ft.Tab(
        text="Resumo",
        content=ft.Column(
            spacing=10,
            controls=[
                
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True
        ),
    )
    abas = ft.Tabs(
        tabs=[
            aba_separar,
            aba_resumo,
            ft.Tab(text="Separar Abastecimento", content=ft.Column(controls=[
                ft.Text("Conteúdo da aba Separar Abastecimento")
            ]))
        ],
        scrollable=True,
        selected_index=0,
        expand=1
    )

    def snack_bar(mensagem, bgcolor, color, page):
        snack = ft.SnackBar(
            content=ft.Text(
                mensagem,
                color="white"
            ),
            bgcolor=bgcolor
        )
        page.open(snack)

    def buscar_itens_pedido(numped, codfilial):
        # print(f"Buscando itens do pedido {numped} na filial {codfilial}")
        response = requests.get(
            f"{base_url}/separarPedidoDist/{numped}",
            params={
                "codfilial": codfilial,
            }
        )
        resposta = response.json()

        if response.status_code == 200:
            itens = resposta.get("data", [])
            resumo = resposta.get("resumo", [])
            print(f"Resumo do pedido {numped}: {resumo}")
            # print(f"Itens do pedido {numped}: {itens}")
            
            aba_separar.content.controls.clear()
            aba_resumo.content.controls.clear()
            if itens:
                item = itens
                aba_separar.content.controls.extend(construir_endereco(item))
                for res in resumo:
                    aba_resumo.content.controls.extend(construir_resumo(res))
            else:
                aba_separar.content.controls.append(
                    ft.Text("Todos os itens do pedido foram separados!", size=16)
                )
                for res in resumo:
                    aba_resumo.content.controls.extend(construir_resumo(res))
            
            page.update()
            return itens
        else:
            mensagem = resposta.get("message")
            print(f"Erro ao buscar itens do pedido {numped}: {mensagem}")
            return []

    def construir_endereco(item):
        # print(f"Construindo endereço para o item: {item}")
        qt_separada = int(item[5])
        codendereco_item = int(item[8])
        mod_item = item[9]
        rua_item = item[10]
        edi_item = item[11]
        nivel_item = item[12]
        apto_item = item[13]

        def validar_endereco(e):
            print("Validando endereço...")
            print(f"Endereco esperado: {codendereco_item}")
            print("Endereco digitado:", input_coendereco.value)
            codendereco_digitado = int(input_coendereco.value)
            # print(f"Validando endereço {codendereco_digitado} para o item {item}")

            if codendereco_digitado == codendereco_item:
                snack_bar("Endereço validado com sucesso!", colorVariaveis['sucesso'], colorVariaveis['textoPreto'], page)

                aba_separar.content.controls.clear()
                aba_separar.content.controls.extend(contruir_produto(item))
                page.update()
                # construir_endereco(item)
                # dialog_produto(item)
            else:
                snack_bar("Endereço incorreto. Tente novamente.", colorVariaveis['erro'], colorVariaveis['texto'], page)

        input_coendereco = ft.TextField(
            label="Código do Endereço",
            expand=True,
            autofocus=True,
            keyboard_type=ft.KeyboardType.NUMBER,
            on_submit=lambda e: validar_endereco(page)
        )
        btn_confirmar_endereco = ft.ElevatedButton(
            "Validar endereço",
            expand=True,
            bgcolor=colorVariaveis['botaoAcao'],
            color=colorVariaveis['texto'],
            on_click=lambda e: validar_endereco(page)
        )

        return [
        ft.Text("Endereço do produto", weight="bold", size=16),

                # Linha 1: módulo / rua
        ft.Row(
            controls=[
                ft.Text(f"Qt Separada: {qt_separada}", weight="bold"),
                ft.Text(f"Módulo: {mod_item}", weight="bold"),
                ft.Text(f"Rua: {rua_item}", weight="bold"),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),

        # Linha 2: edi / nível / apto
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
        btn_confirmar_endereco
    ]

    # def dialog_produto(item):
    #     codprod_item = item[1]
    #     codfab_item = item[2]
    #     descricao_item = item[3]
    #     qt_pedida_item = item[4]
    #     qt_separada_item = item[5]
    #     qt_endereco_item = item[6]

    #     def validar_codbarras(e, codprod_item, codbarra):
    #         print(f"Validando código de barras {codbarra} para o produto {codprod_item}")
    #         try:
    #             response = requests.get(
    #                 f"{base_url}/separarPedidoDist/{pedido}",
    #                 params={
    #                     "codprod": codprod_item,
    #                     "codbarra": codbarra
    #                 }
    #             )
    #             resposta = response.json()

    #             if response.status_code == 200:
    #                 buscar_itens_pedido(pedido, codfilial)
    #                 page.open(dialog_produto)
    #                 mensagem = resposta.get("message")
    #                 snack_bar(mensagem, colorVariaveis['sucesso'], colorVariaveis['textoPreto'], page)
    #             else:
    #                 mensagem = resposta.get("message")
    #                 snack_bar(mensagem, colorVariaveis['erro'], colorVariaveis['texto'], page)
    #         except Exception as e:
    #             print(f"Erro ao validar código de barras: {e}")

    #         snack_bar(f"Código de barras {codbarra} validado com sucesso para o produto {codprod_item}!", colorVariaveis['sucesso'], colorVariaveis['textoPreto'], page)

    #     input_codbarras = ft.TextField(
    #         label="Código de Barras",
    #         expand=True,
    #         autofocus=True,
    #         on_submit=lambda e: validar_codbarras(e, codprod_item, input_codbarras.value)
    #     )
    #     btn_validar_codbarras = ft.ElevatedButton(
    #         "Validar Código de Barras",
    #         expand=True,
    #         bgcolor=colorVariaveis['botaoAcao'],
    #         color=colorVariaveis['texto'],
    #         on_click=lambda e: validar_codbarras(e, codprod_item, input_codbarras.value)
    #     )

    #     dialog_produto = ft.AlertDialog(
    #         title=ft.Text(f"Codprod: {codprod_item}"),
    #         content=ft.Column(
    #             controls=[
    #                 ft.Text(f"Codfab: {codfab_item}"),
    #                 ft.Text(f"Descrição: {descricao_item}"),
    #                 ft.Row(
    #                     controls=[
    #                         ft.Text(f"Qt Pedida: {qt_pedida_item}"),
    #                         ft.Text(f"Qt Separada: {qt_separada_item}"),
    #                         ft.Text(f"Qt Endereço: {qt_endereco_item}"),
    #                     ],
    #                     alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    #                     wrap=True
    #                 ),
    #                 ft.Divider(),
    #                 input_codbarras,
    #                 btn_validar_codbarras
    #             ],
    #             scroll=ft.ScrollMode.AUTO,

    #         ),
    #         actions=[
    #             ft.ElevatedButton(
    #                 "Fechar",
    #                 on_click=lambda e: page.close(dialog_produto)
    #             )
    #         ]
    #     )
    #     page.open(dialog_produto)
    #     page.update()
    #     return dialog_produto

    def contruir_produto(item):
        codprod_item = item[1]
        codfab_item = item[2]
        descricao_item = item[3]
        qt_pedida_item = item[4]
        qt_separada_item = item[5]
        qt_restante_item = item[6]
        qt_endereco_item = item[7]
        print(f"Qt restante do item {codprod_item}: {qt_restante_item}")

        def validar_codbarras(e, codprod_item, codbarra):
            # print(f"Validando código de barras {codbarra} para o produto {codprod_item}")
            try:
                response = requests.get(
                    f"{base_url}/separarPedidoDist/{pedido}",
                    params={
                        "codprod": codprod_item,
                        "codbarra": codbarra,
                        "qtrestante": qt_restante_item
                    }
                )
                resposta = response.json()

                if response.status_code == 200:
                    item = buscar_itens_pedido(pedido, codfilial)
                    print(f"Resta ainda conferir {item[6]} unidades do item {codprod_item}")
                    
                    aba_separar.content.controls.clear()
                    aba_separar.content.controls.extend(contruir_produto(item))
                    page.update()

                    mensagem = resposta.get("message")
                    snack_bar(mensagem, colorVariaveis['sucesso'], colorVariaveis['textoPreto'], page)
                elif response.status_code == 202:
                    snack_bar("Produto totalmente separado!", colorVariaveis['sucesso'], colorVariaveis['textoPreto'], page)

                    item = buscar_itens_pedido(pedido, codfilial)

                    aba_separar.content.controls.clear()
                    aba_separar.content.controls.extend(construir_endereco(item))
                    page.update()
                    return
                else:
                    mensagem = resposta.get("message")
                    snack_bar(mensagem, colorVariaveis['erro'], colorVariaveis['texto'], page)
            except Exception as e:
                print(f"Erro ao validar código de barras: {e}")

            snack_bar(f"Código de barras {codbarra} validado com sucesso para o produto {codprod_item}!", colorVariaveis['sucesso'], colorVariaveis['textoPreto'], page)

        def pular_produto(e, codprod_item):
            try:
                response = requests.patch(
                    f"{base_url}/separarPedidoDist/{pedido}",
                    json={
                        "codprod": codprod_item,
                        "action": "pular"
                    }
                )
                resposta = response.json()

                if response.status_code == 200:
                    item = buscar_itens_pedido(pedido, codfilial)
                    print(f"Resta ainda conferir {item[6]} unidades do item {codprod_item}")
                    
                    aba_separar.content.controls.clear()
                    aba_separar.content.controls.extend(construir_endereco(item))
                    page.update()

                    mensagem = resposta.get("message")
                    snack_bar(mensagem, colorVariaveis['sucesso'], colorVariaveis['textoPreto'], page)
                else:
                    mensagem = resposta.get("message")
                    snack_bar(mensagem, colorVariaveis['erro'], colorVariaveis['texto'], page)
            except Exception as e:
                print(f"Erro ao pular produto: {e}")

        input_codbarras = ft.TextField(
            label="Código de Barras",
            expand=True,
            autofocus=True,
            on_submit=lambda e: validar_codbarras(e, codprod_item, input_codbarras.value)
        )
        btn_validar_codbarras = ft.ElevatedButton(
            "Validar Código de Barras",
            expand=True,
            bgcolor=colorVariaveis['botaoAcao'],
            color=colorVariaveis['texto'],
            on_click=lambda e: validar_codbarras(e, codprod_item, input_codbarras.value)
        )
        btn_pular_produto = ft.ElevatedButton(
            "Pular Produto",
            expand=True,
            bgcolor=colorVariaveis['erro'],
            color=colorVariaveis['texto'],
            on_click=lambda e: pular_produto(e, codprod_item)
        )

        return [
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
                wrap=True
            ),
            ft.Divider(),
            input_codbarras,
            btn_validar_codbarras,
            ft.Container(height=20),
            btn_pular_produto
        ]

    def construir_resumo(resumo):
        codfilial_resumo = resumo[0]
        codprod_resumo = resumo[1]
        codfab_resumo = resumo[2]
        descricao_resumo = resumo[3]
        qt_pedida_resumo = resumo[4]
        qt_restante_resumo = resumo[5]
        qt_separada_resumo = resumo[6]
        pendencia_resumo = resumo[7]
        codetiqueta_resumo = resumo[8]

        cor_resumo = None
        cor_resumo_texto = None

        if int(qt_separada_resumo) == 0:
            print(f"Produto {codprod_resumo} ainda não separado.")
            cor_resumo = None
            cor_resumo_texto = None
        elif qt_separada_resumo < qt_pedida_resumo:
            print(f"Adicionando resumo do produto {codprod_resumo} com pendência {pendencia_resumo}")
            cor_resumo = colorVariaveis['restante']
            cor_resumo_texto = colorVariaveis['textoPreto']
        elif qt_separada_resumo == qt_pedida_resumo:
            print(f"Produto {codprod_resumo} totalmente separado.")
            cor_resumo = colorVariaveis['sucesso']
            cor_resumo_texto = colorVariaveis['textoPreto']
        elif qt_separada_resumo > qt_pedida_resumo:
            print(f"Produto {codprod_resumo} separado com excesso de {qt_separada_resumo - qt_pedida_resumo} unidades.")
            cor_resumo = colorVariaveis['erro']
            cor_resumo_texto = colorVariaveis['texto']
        

        return [
            ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        f"Codprod: {codprod_resumo}",
                                        color=cor_resumo_texto
                                    ),
                                    ft.Text(
                                        f"Codfab: {codfab_resumo}",
                                        color=cor_resumo_texto
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            ft.Text(
                                f"Descrição: {descricao_resumo}",
                                color=cor_resumo_texto
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        f"Qt Pedida: {qt_pedida_resumo}",
                                        color=cor_resumo_texto
                                    ),
                                    ft.Text(
                                        f"Qt Separada: {qt_separada_resumo}",
                                        color=cor_resumo_texto
                                    ),
                                    ft.Text(
                                        f"Qt Restante: {qt_restante_resumo}",
                                        color=cor_resumo_texto
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                wrap=True
                            ),
                            ft.Divider(),
                        ],
                    ),
                    bgcolor=cor_resumo,
                    padding=10,
                )
        ]

    itens = buscar_itens_pedido(pedido, codfilial)
    # print(f"Itens para separar do pedido {itens}")
    
    return ft.View(
        route="/separar_pedido_dist",
        controls=[
            header,
            titulo,
            abas
        ]
    )