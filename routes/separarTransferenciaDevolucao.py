import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

# Placeholder de requisição: sempre que atualizar a quantidade separada
# retorne 200 se a requisição der certo ou 303 se der errado.
def requisicao_atualizar_quantidade(payload: dict) -> int:
    print(f"Payload para atualizar quantidade: {payload}")
    try:
        response = requests.post(
            f"{base_url}/buscar_dados_transferencia_devolucao",
            json={
                "payload": payload,
                "action": "atualizar_qt_separada"
            }
        )
        if response.status_code == 200:
            return 200
        else:
            print("Erro ao buscar os dados da transferência/devolução")
            print(f"Status code: {response.status_code}, Response: {response.text}")
            return 303
    except Exception:
        return 303

def separar_transferencia_devolucao(e, navigate_to, header, arguments):
    matricula = user_info.get('matricula')
    codfilial = user_info.get('codfilial')
    numnota = arguments.get('numnota')
    print(matricula, codfilial, numnota)

    itens_sucesso = []
    
    try:
        response = requests.post(
            f"{base_url}/buscar_dados_transferencia_devolucao",
            json={
                "matricula": matricula,
                "codfilial": codfilial,
                "numnota": numnota
            }
        )
        if response.status_code == 200:
            dados = response.json()
            raw_itens = dados.get("dados_itens", [])
            dados_itens = [list(i) for i in raw_itens]
            raw_resumo = dados.get("dados_resumo", [])
            dados_resumo = [list(i) for i in raw_resumo]
            # Normaliza campo "restante" (índice 6) de acordo com o que já veio separado (índice 5)
            for r in dados_resumo:
                # Garante tamanho mínimo até o índice 6
                while len(r) <= 6:
                    r.append(0)
                # Recalcula restante: total (4) - separado (5)
                try:
                    total_pedido = int(r[4])
                except Exception:
                    total_pedido = r[4]
                try:
                    ja_separado = int(r[5])
                except Exception:
                    ja_separado = r[5]
                r[6] = total_pedido - ja_separado
            raw_barras = dados.get("dados_codbarras", [])
            dados_codbarras = [list(i) for i in raw_barras]
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

    def envio_resumo(dados_resumo, page, navigate_to, itens_sucesso, numnota):
        try:
            response = requests.post(
                f"{base_url}/finalizar_transferencia_devolucao",
                json={
                    "dados_resumo": dados_resumo,
                    "matricula": matricula,
                    "codfilial": codfilial,
                    "itens_sucesso": itens_sucesso,
                    "numnota": numnota
                }
            )
            dados = response.json()
            mensagem = dados.get("mensagem", "Sem mensagem da API.")

            snackbar = ft.SnackBar(
                content=ft.Text(mensagem, color="white"),
                bgcolor=colorVariaveis['sucesso'] if response.status_code == 200 else colorVariaveis['erro']
            )
            # page.snack_bar = snackbar
            # snackbar.open = True
            # page.update()
            page.open(snackbar)

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


    def filtrar_itens_pendentes():
        # Mantém apenas itens (endereços) de produtos que ainda têm saldo a separar
        codprod_pendentes = {r[0] for r in dados_resumo if len(r) > 5 and r[5] < r[4]}
        if codprod_pendentes:
            dados_itens[:] = [it for it in dados_itens if it[1] in codprod_pendentes]
        else:
            # Se nenhum pendente, esvazia a lista para forçar mensagem de fim
            dados_itens.clear()


    def atualizar_tab_separar():
    # Verifica se ainda há produtos para separar
        filtrar_itens_pendentes()
        if dados_itens:
            next_item = dados_itens[0]
            # Cria os controles para o próximo produto
            novo_input_endereco = ft.TextField(label="Digite o código do endereço")
            novo_botao_validar = ft.ElevatedButton(
                text="Validar Endereço",
                bgcolor=colorVariaveis['botaoAcao'],
                color=colorVariaveis['texto'],
                on_click=lambda e: validar_endereco(e, novo_input_endereco.value)
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
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Column(controls=[ft.Text("MOD", weight="bold"), ft.Text(str(next_item[8]))]),
                                ft.Column(controls=[ft.Text("RUA", weight="bold"), ft.Text(str(next_item[9]))]),
                                ft.Column(controls=[ft.Text("EDI", weight="bold"), ft.Text(str(next_item[10]))]),
                                ft.Column(controls=[ft.Text("NIV", weight="bold"), ft.Text(str(next_item[11]))]),
                                ft.Column(controls=[ft.Text("APT", weight="bold"), ft.Text(str(next_item[12]))]),
                            ]
                        ),
                        ft.Row(
                            controls=[ft.Text("Disponível:", weight="bold"), ft.Text(str(next_item[5]))]
                        ),
                        novo_input_endereco,
                        novo_botao_validar,
                    ]
                )
            )
            # Atualiza o terceiro controle do Column que compõe o tabsSeparar (onde o produto é exibido)
            tabsSeparar.content.controls[2] = novo_produto_container
            tabsSeparar.update()
        else:
            # Se não houver mais produtos, exibe uma mensagem apropriada
            tabsSeparar.content.controls[2] = ft.Text("Nenhum produto para separar", size=18, color=colorVariaveis['erro'])
            tabsSeparar.update()

    def validar_endereco(e, endereco_digitado):
        try:
            endereco = int(endereco_digitado)
        except ValueError:
            endereco = None
        if endereco is None:
            snack = ft.SnackBar(
                content=ft.Text("Endereço incorreto!", color="white"),
                bgcolor=colorVariaveis['erro']
            )
            e.page.open(snack)
            return

        for endereco_item in dados_itens:
            if endereco == endereco_item[7]:
                for resumo_item in dados_resumo:
                    if resumo_item[0] == endereco_item[1]:
                        abrir_dialogo_produto(e, resumo_item, endereco_item)
                        return
        snack = ft.SnackBar(
            content=ft.Text("Endereço incorreto!", color="white"),
            bgcolor=colorVariaveis['erro']
        )
        # e.page.snack_bar = snack
        # snack.open = True
        # e.page.update()
        e.page.open(snack)
    
    def abrir_dialogo_produto(e, resumo_item, endereco_item):
        # Segurança: assegura que o "restante" (índice 6) está coerente com o que já foi separado (índice 5)
        while len(resumo_item) <= 6:
            resumo_item.append(0)
        try:
            total_pedido = int(resumo_item[4])
        except Exception:
            total_pedido = resumo_item[4]
        try:
            ja_separado = int(resumo_item[5])
        except Exception:
            ja_separado = resumo_item[5]
        # Se vier inconsistente do backend, rebaseia
        if resumo_item[6] != total_pedido - ja_separado:
            resumo_item[6] = total_pedido - ja_separado
        qt_separada = ft.Text(f"Quantidade Separada: {resumo_item[5]}/{resumo_item[4]}")
        qt_falta = ft.Text(f"Quantidade Faltante: {resumo_item[4] - resumo_item[5]}")
        qt_endereco = ft.Text(f"Disponível neste endereço: {endereco_item[5]}")
        input_codbarra = ft.TextField(label="Código de Barras")
        input_qt_total = ft.TextField(label="Quantidade Total")

        def validar_codbarra(evt):
            codbarra_digitado = input_codbarra.value.strip()
            # Se válido, atualiza quantidade baseado no input_qt_total
            for cod in dados_codbarras:
                if cod[0] == resumo_item[0] and cod[1] == codbarra_digitado:
                    # Lê quantidade nova do campo, garantindo inteiro
                    try:
                        nova_qt = int(input_qt_total.value)
                    except ValueError:
                        # Mostra erro se não for número
                        snack = ft.SnackBar(
                            content=ft.Text("Informe um número válido!", color="white"),
                            bgcolor=colorVariaveis['erro']
                        )
                        evt.page.open(snack)
                        return
                    qtrestante = resumo_item[4] - resumo_item[5]
                    print(f"Qt Restante: {qtrestante}")
                    adicional = qtrestante - nova_qt 
                    # adicioanl = adicional * -1
                    # adicional = quantidade digitada - qt_separada resumo
                    # if adicional <= 0 or adicional > endereco_item[5]:
                    #     print(f"Adicional: {adicional}, Disponível: {endereco_item[5]}")
                    #     snack = ft.SnackBar(
                    #         content=ft.Text("Quantidade maior que disponível!", color="white"),
                    #         bgcolor=colorVariaveis['erro']
                    #     )
                    #     evt.page.open(snack)
                    #     return
                    # resumo_item[5] = qtrestante - adicional
                    resumo_item[6] = resumo_item[6] - nova_qt 
                    print(f"Quantidade separada validacao1: {resumo_item[6]}")

                    if resumo_item[6] < 0:
                        # print(f"Quantidade maior que a solciitada")


                        fechar_dialogo(evt)
                        snack = ft.SnackBar(
                            content=ft.Text("Quantidade maior que a solicitada!", color="white"),
                            bgcolor=colorVariaveis['erro']
                        )
                        evt.page.open(snack)
                        # print(f"Item removido do sucesso antes - mais que solicitada: {itens_sucesso}")
                        # itens_sucesso.pop()
                        # print(f"Item removido do sucesso depois - mais que solicitada: {itens_sucesso}")
                        resumo_item[6] = resumo_item[6] + nova_qt
                        print(f"Quantidade separada validacao2: {resumo_item[6]}")
                        # print(f"Quantidade separada validacao: {resumo_item[5]}")
                        # resumo_item[5] = 0
                        # print(f"Quantidade separada validacao: {resumo_item[5]}")
                        return

                    resumo_item[5] = resumo_item[4] - resumo_item[6]
                    print(f"Quantidade separada validacao AA: {resumo_item[5]}")
                    # resumo_item[5] = 99999

                    if resumo_item[5] > resumo_item[4]:
                        print(f"Quantidade maior que a solciitada")
                        print(f"Quantidade separada validacao3: {resumo_item[5]}")
                        # resumo_item[5] = resu
                        print(f"Quantidade separada validacao4: {resumo_item[5]}")
                        return

                    if len(resumo_item) > 6:
                        pass
                    endereco_item[5] -= nova_qt
                    print(f"Quantidade disponível negativo: {endereco_item[5]}")

                    print(f"dados itens0: {dados_itens}")
                    

                    # Atualiza textos
                    print(f"Quantidade separada aaqui: {resumo_item[5]}")
                    # if resumo_item[5] > 0:
                    #     resumo_item[5] = resumo_item[5] - nova_qt
                    
                    print(f"Quantidade separada aaqui novo: {resumo_item[5]}")
                    qt_separada.value = f"Quantidade Separada: {resumo_item[5]}/{resumo_item[4]}"
                    qt_separada.update()
                    qt_endereco.value = f"Disponível neste endereço: {endereco_item[5]}"
                    qt_endereco.update()
                    input_codbarra.value = ""
                    input_codbarra.update()
                    # Atualiza Resumo
                    tabsResumo.content = construir_tabs_resumo()
                    tabsResumo.update()
                    evt.page.update()

                    itens_sucesso.clear()
                    itens_sucesso.append({
                        "codendereco": endereco_item[7],
                        "codprod":     endereco_item[1],
                        "quantidade":  nova_qt
                    })
                    print(f"Item adicionado ao sucesso: {itens_sucesso}")

                    # Dispara requisição sempre que atualizar a quantidade separada
                    # Envia a quantidade TOTAL já separada (resumo_item[5])
                    # em vez da quantidade digitada (nova_qt), para evitar
                    # sobrescrever o valor existente no backend.
                    status_req = requisicao_atualizar_quantidade({
                        "codendereco": endereco_item[7],
                        "codprod":     endereco_item[1],
                        "quantidade":  nova_qt,
                        "numnota":     numnota,
                        "matricula":   matricula,
                        "codfilial":   codfilial,
                    })
                    if status_req == 200:
                        # Sucesso (200) - você pode adicionar sua lógica aqui se desejar
                        pass
                    else:
                        # Erro (303) - você pode adicionar sua lógica de erro aqui
                        pass
                    # Se atingiu o pedido, remove e fecha

                    if endereco_item[5] < 0:
                        atualizar_tab_separar()
                        # print("Voc~e digitou a quantidade superior a disponivel")
                        snack = ft.SnackBar(
                            content=ft.Text("Você digitou a quantidade superior a disponivel!", color="white"),
                            bgcolor=colorVariaveis['erro']
                        )
                        print(f"Item removido do sucesso antes - mais que o endereco: {itens_sucesso}")
                        itens_sucesso.pop()
                        print(f"Item removido do sucesso depois - mais que o endereco: {itens_sucesso}")

                        evt.page.open(snack)
                        endereco_item[5] += nova_qt
                        resumo_item[5] = resumo_item[5] - nova_qt 
                        resumo_item[6] = resumo_item[6] + nova_qt
                        # Atualiza Resumo
                        tabsResumo.content = construir_tabs_resumo()
                        tabsResumo.update()
                        evt.page.update()

                        

                        print(f"Quantidade se for maior que a disponivel: {resumo_item[5]}")
                        print(f"Quantidade maior que a disponivel: {endereco_item[5]}")
                    elif endereco_item[5] == 0:
                        print(f"codendereco: {endereco_item[7]} | quantidade {endereco_item[5]} | produto {endereco_item[1]}")

                        

                        dados_itens.remove(endereco_item)

                    # if endereco_item[5] == 0:
                    #     dados_itens.remove(endereco_item)
                    #     if endereco_item in dados_itens:
                    #         print(f"Dados itens antes: {dados_itens}")
                    #         print(f"Endereço a ser removido: {endereco_item}")
                    #         atualizar_tab_separar()
                            # dados_itens.remove(endereco_item)
                    if resumo_item[5] >= resumo_item[4]:
                        dados_itens[:] = [it for it in dados_itens if it[1] != resumo_item[0]]

                        
                    
                    
                    atualizar_tab_separar()
                    evt.page.close(dialog)
                    return
            # Se não encontrou código
            snack = ft.SnackBar(
                content=ft.Text("Código de barras incorreto!", color="white"),
                bgcolor=colorVariaveis['erro']
            )
            evt.page.open(snack)

        def fechar_dialogo(evt):
            evt.page.close(dialog)

        dialog = ft.AlertDialog(
            title=ft.Text("Confirmação de Produto"),
            content=ft.Column(
                controls=[
                    ft.Text(f"Código do Produto: {resumo_item[0]}"),
                    ft.Text(f"Descrição: {resumo_item[2]}"),
                    ft.Text(f"Quantidade Pedida: {resumo_item[4]}"),
                    qt_endereco,
                    qt_separada,
                    qt_falta,
                    input_codbarra,
                    input_qt_total
                ],
                scroll=True,
                spacing=10
            ),
            actions=[
                ft.TextButton("Confirmar", on_click=validar_codbarra),
                ft.TextButton("Cancelar", on_click=fechar_dialogo)
            ]
        )
        e.page.open(dialog)

    filtrar_itens_pendentes()
    if dados_itens:
        item = dados_itens[0]
        input_endereco = ft.TextField(label="Digite o código do endereço")
        botao_validar = ft.ElevatedButton(
            text="Validar Endereço",
            bgcolor=colorVariaveis['botaoAcao'],
            color=colorVariaveis['texto'],
            on_click=lambda e: validar_endereco(e, input_endereco.value)
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
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Column(controls=[ft.Text("MOD", weight="bold"), ft.Text(str(item[8]))]),
                            ft.Column(controls=[ft.Text("RUA", weight="bold"), ft.Text(str(item[9]))]),
                            ft.Column(controls=[ft.Text("EDI", weight="bold"), ft.Text(str(item[10]))]),
                            ft.Column(controls=[ft.Text("NIV", weight="bold"), ft.Text(str(item[11]))]),
                            ft.Column(controls=[ft.Text("APT", weight="bold"), ft.Text(str(item[12]))]),
                        ]
                    ),
                    ft.Row(
                        controls=[ft.Text("Disponível:", weight="bold"), ft.Text(str(item[5]))]
                    ),
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
                            ft.Row([
                                ft.Text(f"Qt Ped: {item[4]}", weight="bold"),
                                ft.Text(f"Qt Sep: {item[5]}", weight="bold"),
                                ft.Text(f"Qt Rest: {item[4] - item[5]}", weight="bold"),
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
        # Cria uma lista com as divergências encontradas
        divergencias = [
            f"Produto {item[0]}: Qt Pedida {item[4]} vs Qt Separada {item[5]}"
            for item in dados_resumo if item[4] != item[5]
        ]
        
        if divergencias:
            # Monta o conteúdo do dialog mostrando os detalhes das divergências
            content_dialog = ft.Column(
                controls=[
                    ft.Text("Divergências encontradas:"),
                    ft.Column(controls=[ft.Text(text) for text in divergencias]),
                    ft.Divider(),
                    ft.Text("Deseja finalizar assim mesmo?")
                ]
            )
            
            # Função para confirmar a finalização mesmo havendo divergências
            def confirmar_finalizacao(e):
                print("Finalização confirmada, mesmo com divergências.")
                # e.page.dialog.open = False
                # e.page.update()
                e.page.close(dialog)
                envio_resumo(dados_resumo, e.page, navigate_to, itens_sucesso, numnota)
                # Aqui você pode inserir a lógica final de finalização
            
            # Cria o AlertDialog com os botões de ação
            dialog = ft.AlertDialog(
                title=ft.Text("Divergências Encontradas"),
                content=content_dialog,
                actions=[
                    ft.TextButton("Finalizar Assim Mesmo", on_click=confirmar_finalizacao),
                    ft.TextButton("Cancelar", on_click=lambda e: (setattr(e.page.dialog, "open", False), e.page.update()))
                ]
            )
            # e.page.dialog = dialog
            # dialog.open = True
            # e.page.update()
            e.page.open(dialog)
        else:
            print("Nenhuma divergência encontrada, finalizando...")
            print(f"dados resumo : {dados_resumo}")
            print(f"resumo separado: {itens_sucesso}")
            envio_resumo(dados_resumo, e.page, navigate_to, itens_sucesso, numnota)
            # Prossegue com a finalização normalmente


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
