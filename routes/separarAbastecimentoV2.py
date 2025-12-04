import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def separar_abastecimentoV2(page: ft.Page, navigate_to, header, arguments):
    matricula = user_info.get("matricula")
    codfilial = user_info.get("codfilial")
    numos = arguments.get("num_os")
    print(f"User config na tela Separar Abastecimento V2: {matricula}, Num OS: {numos}")

    container_principal = ft.Container(
        content=ft.Column(
            controls=[
            ]
        )
    )

    def snackbar(mensagem, bgcolor, page):
        snack = ft.SnackBar(
            content=ft.Text(mensagem, color="white"),
            bgcolor=bgcolor,
        )
        page.open(snack)

    def buscar_pulmao(numos, matricula, codfilial):
        response = requests.get(
            base_url + f"/separar_abastecimentoV2/{numos}",
            params={
                "numos": numos,
                "matricula": matricula,
                "codfilial": codfilial,
                "tipoendereco": 'pulmao'
            },
        )
        print(f"Status code: {response.status_code}")
        resposta = response.json()
        mensagem = resposta.get("message")
        dados_pulmao = resposta.get("dados_pulmao")
        print(mensagem, dados_pulmao)

        if response.status_code == 200:
            container_principal.content.controls.clear()
            container_principal.content.controls.extend(construir_container_pulmao(dados_pulmao))
            page.update()

            snackbar(mensagem, colorVariaveis['sucesso'], page)
        elif response.status_code == 202:
            # container_principal.content.controls.clear()
            # container_principal.content.controls.append(ft.Text(f"Terminou de separação, mas ainda não cadastrou o picking: {mensagem}"))
            buscar_picking(numos, codfilial)
            page.update()

            snackbar(mensagem, colorVariaveis['erro'], page)
        else:
            container_principal.content.controls.clear()
            container_principal.content.controls.append(ft.Text(f"Erro ao buscar dados do pulmao: {mensagem}"))
            page.update()

            snackbar(mensagem, colorVariaveis['erro'], page)

    def construir_container_pulmao(dados_pulmao):
        codendereco = dados_pulmao[7]
        mod = dados_pulmao[8]
        rua = dados_pulmao[9]
        edf = dados_pulmao[10]
        niv = dados_pulmao[11]
        apt = dados_pulmao[12]
        qt_endereco = dados_pulmao[14]

        def validar_endereco(codendereco, input_codendereco):
            if not input_codendereco:
                snackbar("Informe o código do endereço", colorVariaveis['erro'], page)
                return
            
            print(f"Validando endereço: Input={input_codendereco}, Esperado={codendereco}")
            if int(input_codendereco) == int(codendereco):
                container_principal.content.controls.clear()
                container_principal.content.controls.extend(construir_container_produto(dados_pulmao))
                page.update()

                snackbar("Endereço válido!", colorVariaveis["sucesso"], page)
            else:
                snackbar("Endereço inválido. Tente novamente.", colorVariaveis["erro"], page)

        input_codendereco = ft.TextField(
            label="Código do endereço",
            keyboard_type=ft.KeyboardType.NUMBER,
            autofocus=True,
            on_submit=lambda e: validar_endereco(codendereco, input_codendereco.value),
        )
        button_validarEndereco = ft.ElevatedButton(
            text="Validar Endereço",
            on_click=lambda e: validar_endereco(codendereco, input_codendereco.value),
        )

        return[
            ft.Row(
                controls=[
                    ft.Text(f"Mod: {mod}"),
                    ft.Text(f"Rua: {rua}"),
                    ft.Text(f"Edf: {edf}")
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            ft.Divider(),
            ft.Row(
                controls=[
                    ft.Text(f"Niv: {niv}"),
                    ft.Text(f"Apt: {apt}"),
                    ft.Text(f"Qt_End: {qt_endereco}")
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            input_codendereco,
            button_validarEndereco
        ]

    def construir_container_produto(dados_pulmao):
        codprod = dados_pulmao[1]
        codfab = dados_pulmao[2]
        descricao = dados_pulmao[3],
        qt_solicitada = dados_pulmao[4]
        qt_separada = dados_pulmao[5]
        qt_restante = dados_pulmao[6]
        qt_endereco = dados_pulmao[14]
        codendereco = dados_pulmao[7]

        def validar_codbarra(codbarra, codprod, numos):
            if not codbarra:
                snackbar("Informe o código de barras", colorVariaveis['erro'], page)
                return

            response = requests.patch(
                base_url + f"/separar_abastecimentoV2/{numos}",
                json={
                    "codprod": codprod,
                    "codbarra": codbarra,
                    "numos": numos,
                    "matricula": matricula,
                    "codfilial": codfilial
                },
            )
            print(f"Status code: {response.status_code}")
            resposta = response.json()
            mensagem = resposta.get("message")
            print(mensagem)

            if response.status_code == 200:
                dialog_qt_produto(codprod, qt_separada, qt_solicitada, qt_restante, qt_endereco, codendereco)

                snackbar(mensagem, colorVariaveis['sucesso'], page)
            else:
                snackbar(mensagem, colorVariaveis['erro'], page)

        input_codbarra = ft.TextField(
            label="Código de barra",
            autofocus=True,
            on_submit=lambda e: validar_codbarra(input_codbarra.value, codprod, numos),
        )
        button_validarCodbarra = ft.ElevatedButton(
            text="Validar Código de Barra",
            on_click=lambda e: validar_codbarra(input_codbarra.value, codprod, numos),
        )

        return[
            ft.Row(
                controls=[
                    ft.Text(f"Codprod: {codprod}"),
                    ft.Text(f"Codfab: {codfab}"),
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            ft.Text(f"Descrição: {descricao}"),
            ft.Divider(),
            ft.Row(
                controls=[
                    ft.Text(f"Qt Solicitada: {qt_solicitada}"),
                    ft.Text(f"Qt Separada: {qt_separada}"),
                    ft.Text(f"Qt Restante: {qt_restante}")
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                wrap=True
            ),
            input_codbarra,
            button_validarCodbarra
        ]

    def dialog_qt_produto(codprod, qt_separada, qt_solicitada, qt_restante, qt_endereco, codendereco):
        def validar_quantidade(qt, codprod):
            if int(qt) > int(qt_endereco):
                snackbar("Quantidade maior que qt_endereco", colorVariaveis['erro'], page)
                return
            
            response = requests.patch(
                base_url + f"/separar_abastecimentoV2/{numos}",
                json={
                    "codprod": codprod,
                    "qt": qt,
                    "codendereco_origem": codendereco,
                    "numos": numos,
                    "matricula": matricula,
                    "codfilial": codfilial
                },
            )
            print(f"Status code: {response.status_code}")
            resposta = response.json()
            mensagem = resposta.get("message")
            print(mensagem)

            if response.status_code == 202:
                fechar_dialog(dialog_produto)

                # container_principal.content.controls.clear()
                # container_principal.content.controls.append(ft.Text("Endereço de picking"))
                # page.update()

                buscar_picking(numos, codfilial)

                snackbar(mensagem, colorVariaveis['sucesso'], page)
            elif response.status_code == 204:
                fechar_dialog(dialog_produto)

                buscar_pulmao(numos, matricula, codfilial)

                snackbar(mensagem, colorVariaveis['restante'], page)
            else:
                snackbar(mensagem, colorVariaveis['erro'], page)
        
        input_qt = ft.TextField(
            label="Quantidade",
            autofocus=True,
            keyboard_type=ft.KeyboardType.NUMBER,
            on_submit=lambda e: validar_quantidade(input_qt.value, codprod),
        )
        button_validarQt = ft.ElevatedButton(
            text="Validar Quantidade",
            on_click=lambda e: validar_quantidade(input_qt.value, codprod),
        )

        dialog_produto = ft.AlertDialog(
            title=ft.Text("Inserir Quantidade"),
            content=ft.Column(
                controls=[
                    ft.Text(f"Codprod: {codprod}"),
                    ft.Text(f"Qt Separada: {qt_separada}"),
                    ft.Text(f"Qt Solicitada: {qt_solicitada}"),
                    ft.Text(f"Qt Restante: {qt_restante}"),
                    ft.Text(f"Qt Endereço: {qt_endereco}"),
                    input_qt,
                    button_validarQt
                ],
                expand=True,
                scroll=ft.ScrollMode.AUTO
            ),
            actions=[
                ft.TextButton(text="Fechar", on_click=lambda _: fechar_dialog(dialog_produto))
            ],
        )

        page.open(dialog_produto)
        page.update()

        return dialog_produto

    def fechar_dialog(dialog):
        page.close(dialog)
        page.update()

    def buscar_picking(numos, codfilial):
        response = requests.get(
            base_url + f"/separar_abastecimentoV2/{numos}",
            params={
                "numos": numos,
                "codfilial": codfilial,
                "tipoendereco": 'picking'
            },
        )
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.json()}")

        resposta = response.json()
        mensagem = resposta.get("message")
        print(mensagem)

        if response.status_code == 200:
            dados_picking = resposta.get("dados_picking")
            print(dados_picking)

            container_principal.content.controls.clear()
            container_principal.content.controls.extend(construir_container_picking(dados_picking))
            
            page.update()

            snackbar(mensagem, colorVariaveis['sucesso'], page)
        elif response.status_code == 202:
            dados_picking = resposta.get("dados_picking")
            print(dados_picking)

            container_principal.content.controls.clear()
            container_principal.content.controls.extend(construir_container_picking(dados_picking))
            page.update()

            snackbar(mensagem, colorVariaveis['sucesso'], page)
        else:
            snackbar(mensagem, colorVariaveis['erro'], page)

    def construir_container_picking(dados_picking):
        input_picking = ft.TextField(
            label="Endereço Picking",
            autofocus=True,
            keyboard_type=ft.KeyboardType.NUMBER,
            # on_submit=lambda e: validar_picking(input_picking.value.strip(), page),
        )
        button_validarEndereco_picking = ft.ElevatedButton(
            text="Validar Endereço",
            on_click=lambda e: validar_picking(input_picking.value.strip(), page),
        )
        input_capacidade = ft.TextField(
            label="Capacidade",
            autofocus=True,
            keyboard_type=ft.KeyboardType.NUMBER,
            on_click=lambda e: validar_picking_capacidadde(input_picking.value.strip(), input_capacidade.value.strip(), page),
        )
        btn_validarEnderecoCapacidade = ft.ElevatedButton(
            text="Validar Endereço -",
            on_click=lambda e: validar_picking_capacidadde(input_picking.value.strip(), input_capacidade.value.strip(), page),
        )

        def validar_picking(input_picking, page):
            codendereco_picking = int(dados_picking[1])
            codendereco_input = int(input_picking)
            
            print(f"Validando endereço picking: Input={codendereco_input}, Esperado={codendereco_picking}")
            
            if codendereco_input == codendereco_picking:
                response = requests.put(
                    f"{base_url}/separar_abastecimentoV2/{numos}",
                    json={
                        "numos": numos,
                        "codfilial": codfilial,
                        "codendereco": codendereco_input
                    }
                )
                print(f"Status code: {response.status_code}")
                print(f"Response: {response.json()}")

                resposta = response.json()
                mensagem = resposta.get("message")
                print(mensagem)

                if response.status_code == 200:
                    navigate_to("/abastecimentoV2")
                    snackbar(mensagem, colorVariaveis['sucesso'], page)
                else:
                    snackbar(mensagem, colorVariaveis['erro'], page)
            else:
                snackbar("Endereço Picking inválido. Tente novamente.", colorVariaveis["erro"], page)

        def validar_picking_capacidadde(input_picking, input_capacidade, page):
            response = requests.post(
                f"{base_url}/separar_abastecimentoV2/{numos}",
                json={
                    "numos": numos,
                    "codfilial": codfilial,
                    "endereco_picking": input_picking,
                    "capacidade": input_capacidade
                }
            )
            print(f"Status code: {response.status_code}")
            print(f"Response: {response.json()}")

            resposta = response.json()
            mensagem = resposta.get("message")
            print(mensagem)

            if response.status_code == 200:
                navigate_to("/abastecimentoV2")
                snackbar(mensagem, colorVariaveis['sucesso'], page)
            else:
                snackbar(mensagem, colorVariaveis['erro'], page)

        if dados_picking:
            codendereco_picking = dados_picking[1]
            mod = dados_picking[2]
            rua = dados_picking[3]
            edf = dados_picking[4]
            nivel = dados_picking[5]
            apto = dados_picking[6]
            qt_picking = dados_picking[7]
            return[
                ft.Row(
                    controls=[
                        ft.Text(f"Mod: {mod}"),
                        ft.Text(f"Rua: {rua}"),
                        ft.Text(f"Edf: {edf}"),
                    ],
                    expand=True,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Row(
                    controls=[
                        ft.Text(f"Nivel: {nivel}"),
                        ft.Text(f"Apto: {apto}"),
                        ft.Text(f"Qt Endereço: {qt_picking}")
                    ],
                    expand=True,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                input_picking,
                button_validarEndereco_picking
            ]
        else:
            return[
                ft.Text("Cadastrar Picking"),
                input_picking,
                input_capacidade,
                btn_validarEnderecoCapacidade
            ]

    buscar_pulmao(numos, matricula, codfilial)

    return ft.View(
        route="/separar_abastecimento",
        controls=[
            header,
            ft.Text(f"Número da OS: {numos}", size=16),
            container_principal,
        ],
    )