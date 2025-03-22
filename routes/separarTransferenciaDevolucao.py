import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def separar_transferencia_devolucao(e, navigate_to, header):
    matricula = user_info.get('matricula')
    codfilial = user_info.get('codfilial')
    
    try:
        response = requests.post(
            f"{base_url}/buscar_dados_transferencia_devolucao",
            json={"matricula": matricula, "codfilial": codfilial}
        )
        if response.status_code == 200:
            dados = response.json()
            dados_itens = dados.get("dados_itens", [])
            dados_resumo = dados.get("dados_resumo", [])
            dados_codbarras = dados.get("dados_codbarras", [])
        else:
            print("Erro ao buscar os dados da transferência/devolução")
            dados_itens = []
            dados_resumo = []
            dados_codbarras = []
    except Exception as exc:
        print(f"Erro: {exc}")
        dados_itens = []
        dados_resumo = []
        dados_codbarras = []
    
    title = ft.Text(
        "Separar Transferência/Devolução",
        size=24,
        weight="bold",
        color=colorVariaveis['titulo']
    )

    def envio_resumo(dados_resumo, page, navigate_to):
        try:
            response = requests.post(
                f"{base_url}/finalizar_transferencia_devolucao",
                json={
                    "dados_resumo": dados_resumo,
                    "matricula": matricula,
                    "codfilial": codfilial
                }
            )
            dados = response.json()
            mensagem = dados.get("mensagem", "Sem mensagem da API.")

            snackbar = ft.SnackBar(
                content=ft.Text(mensagem, color="white"),
                bgcolor=colorVariaveis['sucesso'] if response.status_code == 200 else colorVariaveis['erro']
            )
            page.snack_bar = snackbar
            snackbar.open = True
            page.update()

            if response.status_code == 200:
                navigate_to("/buscar_transferencia_devolucao")

        except Exception as exc:
            snackbar = ft.SnackBar(
                content=ft.Text(f"Erro ao enviar o resumo: {str(exc)}", color="white"),
                bgcolor=colorVariaveis['erro']
            )
            page.snack_bar = snackbar
            snackbar.open = True
            page.update()

    def atualizar_tab_separar():
    # Verifica se ainda há produtos para separar
        if dados_itens:
            next_item = dados_itens[0]
            # Filtra todos os itens referentes ao mesmo produto para exibir os endereços disponíveis
            itens_produto = [it for it in dados_itens if it[1] == next_item[1]]
            if len(itens_produto) > 1:
                endereco_disponiveis = ft.Column(
                    controls=[
                        ft.Text(
                            f"MOD: {it[7]}, RUA: {it[8]}, EDI: {it[9]}, NIV: {it[10]}, APT: {it[11]}",
                            size=14
                        )
                        for it in itens_produto
                    ]
                )
            else:
                endereco_disponiveis = ft.Text(
                    f"MOD: {next_item[7]}, RUA: {next_item[8]}, EDI: {next_item[9]}, NIV: {next_item[10]}, APT: {next_item[11]}",
                    size=14
                )
            
            novo_input_endereco = ft.TextField(label="Digite o código do endereço")
            novo_botao_validar = ft.ElevatedButton(
                text="Validar Endereço",
                bgcolor=colorVariaveis['botaoAcao'],
                color=colorVariaveis['texto'],
                on_click=lambda e: validar_endereco(e, novo_input_endereco.value, next_item)
            )
            novo_produto_container = ft.Container(
                padding=10,
                border=ft.border.all(1, color=colorVariaveis['bordarInput']),
                border_radius=10,
                content=ft.Column(
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Column(controls=[ft.Text("CODPROD", weight="bold"), ft.Text(str(next_item[1]))]),
                                ft.Column(controls=[ft.Text("CODFAB", weight="bold"), ft.Text(next_item[2])]),
                                ft.Column(controls=[ft.Text("QT", weight="bold"), ft.Text(str(next_item[4]))]),
                            ]
                        ),
                        ft.Text(next_item[3], weight="bold"),
                        ft.Divider(),
                        # ft.Row(
                        #     alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        #     controls=[
                        #         ft.Column(controls=[ft.Text("MOD", weight="bold"), ft.Text(str(next_item[7]))]),
                        #         ft.Column(controls=[ft.Text("RUA", weight="bold"), ft.Text(str(next_item[8]))]),
                        #         ft.Column(controls=[ft.Text("EDI", weight="bold"), ft.Text(str(next_item[9]))]),
                        #         ft.Column(controls=[ft.Text("NIV", weight="bold"), ft.Text(str(next_item[10]))]),
                        #         ft.Column(controls=[ft.Text("APT", weight="bold"), ft.Text(str(next_item[11]))]),
                        #     ]
                        # ),
                        # Exibe os endereços disponíveis (sem o código do endereço)
                        endereco_disponiveis,
                        novo_input_endereco,
                        novo_botao_validar,
                    ]
                )
            )
            tabsSeparar.content.controls[2] = novo_produto_container
            tabsSeparar.update()
        else:
            tabsSeparar.content.controls[2] = ft.Text("Nenhum produto para separar", size=18, color=colorVariaveis['erro'])
            tabsSeparar.update()

    # Função para fechar o diálogo (mantida para uso em outras partes, se necessário)
    def fechar_dialogo(e):
        if e.page.dialog:
            e.page.dialog.open = False
            e.page.update()

    # --- Função de validação do endereço ---
    def validar_endereco(e, endereco_digitado, current_item):
        product_code = current_item[1]
        # Filtra todos os itens de dados_itens com o mesmo produto
        itens_produto = [it for it in dados_itens if it[1] == product_code]
        for it in itens_produto:
            if int(endereco_digitado) == it[6]:
                abrir_dialogo_produto(e, it)
                return
        snack = ft.SnackBar(
            content=ft.Text("Endereço incorreto!", color="white"),
            bgcolor=colorVariaveis['erro']
        )
        e.page.snack_bar = snack
        snack.open = True
        e.page.update()
    
    # --- Função para abrir o diálogo de confirmação do produto ---
    def abrir_dialogo_produto(e, item_valido):
        qt_separada_text = ft.Text(f"Quantidade Separada: 0")
        input_codbarra = ft.TextField(label="Código de Barras")
        
        def validar_codbarra(e):
            codbarra_digitado = input_codbarra.value
            for cod in dados_codbarras:
                if cod[0] == item_valido[1] and cod[1] == codbarra_digitado:
                    validated_address = item_valido[6]
                    # Atualiza ou cria o item de resumo para este produto
                    for resumo_item in dados_resumo:
                        if resumo_item[0] == item_valido[1]:
                            if resumo_item[3] is None:
                                resumo_item[3] = str(validated_address)
                            else:
                                addresses = resumo_item[3].split(", ")
                                if str(validated_address) not in addresses:
                                    resumo_item[3] += f", {validated_address}"
                            resumo_item[5] += 1
                            resumo_item[6] = resumo_item[4] - resumo_item[5]
                            qt_separada_text.value = f"Quantidade Separada: {resumo_item[5]}"
                            qt_separada_text.update()
                            input_codbarra.value = ""
                            input_codbarra.update()
                            tabsResumo.content = construir_tabs_resumo()
                            tabsResumo.update()
                            e.page.update()
                            # Se a quantidade separada deste endereço atingir a pedida, remove o item
                            if item_valido[5] + 1 >= item_valido[4]:
                                try:
                                    dados_itens.remove(item_valido)
                                except ValueError:
                                    pass
                                atualizar_tab_separar()
                                fechar_dialogo(e)
                            return
            snack = ft.SnackBar(
                content=ft.Text("Código de barras incorreto!", color="white"),
                bgcolor=colorVariaveis['erro']
            )
            e.page.snack_bar = snack
            snack.open = True
            e.page.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text("Confirmação de Produto"),
            content=ft.Column(
                controls=[
                    ft.Text(f"Código do Produto: {item_valido[1]}"),
                    ft.Text(f"Descrição: {item_valido[3]}"),
                    ft.Text(f"Quantidade Pedida: {item_valido[4]}"),
                    ft.Text(f"Endereço: {item_valido[6]}"),
                    qt_separada_text,
                    input_codbarra,
                ]
            ),
            actions=[
                ft.TextButton("Confirmar", on_click=validar_codbarra),
                ft.TextButton("Cancelar", on_click=lambda e: fechar_dialogo(e))
            ],
        )
        e.page.dialog = dialog
        dialog.open = True
        e.page.update()

    if dados_itens:
        # Usa o primeiro item como referência para o produto a ser separado
        item = dados_itens[0]
        # Filtra os endereços disponíveis para este produto
        itens_produto = [it for it in dados_itens if it[1] == item[1]]
        if len(itens_produto) > 1:
            endereco_disponiveis = ft.Column(
                controls=[
                    ft.Text(
                        f"Código: {it[6]}, MOD: {it[7]}, RUA: {it[8]}, EDI: {it[9]}, NIV: {it[10]}, APT: {it[11]}",
                        size=14
                    )
                    for it in itens_produto
                ]
            )
        else:
            endereco_disponiveis = ft.Text(
                f"Código: {item[6]}, MOD: {item[7]}, RUA: {item[8]}, EDI: {item[9]}, NIV: {item[10]}, APT: {item[11]}",
                size=14
            )
        
        input_endereco = ft.TextField(label="Digite o código do endereço")
        botao_validar = ft.ElevatedButton(
            text="Validar Endereço",
            bgcolor=colorVariaveis['botaoAcao'],
            color=colorVariaveis['texto'],
            on_click=lambda e: validar_endereco(e, input_endereco.value, item)
        )

        produto_container = ft.Container(
            padding=10,
            border=ft.border.all(1, color=colorVariaveis['bordarInput']),
            border_radius=10,
            content=ft.Column(
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Column(controls=[ft.Text("CODPROD", weight="bold"), ft.Text(str(item[1]))]),
                            ft.Column(controls=[ft.Text("CODFAB", weight="bold"), ft.Text(item[2])]),
                            ft.Column(controls=[ft.Text("QT", weight="bold"), ft.Text(str(item[4]))]),
                        ]
                    ),
                    ft.Text(item[3], weight="bold"),
                    ft.Divider(),
                    # ft.Row(
                    #     alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    #     controls=[
                    #         ft.Column(controls=[ft.Text("MOD", weight="bold"), ft.Text(str(item[7]))]),
                    #         ft.Column(controls=[ft.Text("RUA", weight="bold"), ft.Text(str(item[8]))]),
                    #         ft.Column(controls=[ft.Text("EDI", weight="bold"), ft.Text(str(item[9]))]),
                    #         ft.Column(controls=[ft.Text("NIV", weight="bold"), ft.Text(str(item[10]))]),
                    #         ft.Column(controls=[ft.Text("APT", weight="bold"), ft.Text(str(item[11]))]),
                    #     ]
                    # ),
                    # Exibe os endereços disponíveis diretamente no tab
                    endereco_disponiveis,
                    input_endereco,
                    botao_validar,
                ]
            )
        )
    else:
        produto_container = ft.Text("Nenhum produto para separar", size=18, color=colorVariaveis['erro'])
    
    def construir_tabs_resumo():
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Resumo dos produtos", size=20, weight="bold"),
                    *[
                        ft.Column([
                            ft.Row([
                                ft.Text(f"CODPROD: {item[0]}", weight="bold"),
                                ft.Text(f"CODFAB: {item[1]}", weight="bold"),
                            ]),
                            ft.Text(item[2], weight="bold"),
                            ft.Text(f"Endereço(s): {item[3] if item[3] else 'N/A'}", weight="bold"),
                            ft.Row([
                                ft.Text(f"Qt Pedida: {item[4]}", weight="bold"),
                                ft.Text(f"Qt Separada: {item[5]}", weight="bold"),
                                ft.Text(f"Qt Restante: {item[6]}", weight="bold"),
                            ]),
                            ft.Divider()
                        ])
                        for item in dados_resumo
                    ]
                ],
                scroll=ft.ScrollMode.AUTO
            )
        )
    
    def finalizar(e):
        divergencias = [
            f"Produto {item[0]}: Qt Pedida {item[4]} vs Qt Separada {item[5]}"
            for item in dados_resumo if item[4] != item[5]
        ]
        
        if divergencias:
            content_dialog = ft.Column(
                controls=[
                    ft.Text("Divergências encontradas:"),
                    ft.Column(controls=[ft.Text(text) for text in divergencias]),
                    ft.Divider(),
                    ft.Text("Deseja finalizar assim mesmo?")
                ]
            )
            
            def confirmar_finalizacao(e):
                print("Finalização confirmada, mesmo com divergências.")
                fechar_dialogo(e)
                envio_resumo(dados_resumo, e.page, navigate_to)
            
            dialog = ft.AlertDialog(
                title=ft.Text("Divergências Encontradas"),
                content=content_dialog,
                actions=[
                    ft.TextButton("Finalizar Assim Mesmo", on_click=confirmar_finalizacao),
                    ft.TextButton("Cancelar", on_click=lambda e: fechar_dialogo(e))
                ]
            )
            e.page.dialog = dialog
            dialog.open = True
            e.page.update()
        else:
            print("Nenhuma divergência encontrada, finalizando...")
            envio_resumo(dados_resumo, e.page, navigate_to)
    
    tabsSeparar = ft.Container(
        padding=10,
        expand=True,
        content=ft.Column(
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[ft.Text("Vá ao endereço:", weight="bold", size=20)]
                ),
                ft.Divider(),
                produto_container,
            ],
            scroll=ft.ScrollMode.AUTO
        )
    )
    
    tabsResumo = construir_tabs_resumo()
    
    tabsFinalizar = ft.Container(
        content=ft.Column(
            controls=[
                ft.ElevatedButton(
                    text="Finalizar",
                    bgcolor=colorVariaveis['botaoAcao'],
                    color=colorVariaveis['texto'],
                    on_click=lambda e: finalizar(e)
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )
    
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=200,
        tabs=[
            ft.Tab(text="Separar", content=tabsSeparar),
            ft.Tab(text="Resumo", content=tabsResumo),
            ft.Tab(text="Finalizar", content=tabsFinalizar),
        ],
    )
    
    main_container = ft.Container(
        content=tabs,
        expand=True,
        width="100%",
        height="100%"
    )
    
    return ft.View(
        route="/separar_transferencia_devolucao",
        controls=[
            header,
            title,
            ft.Container(height=10),
            main_container
        ]
    )
