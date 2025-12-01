import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def separar_abastecimento(page: ft.Page, navigate_to, header, arguments):
    matricula = user_info.get("matricula")
    codfilial = user_info.get("codfilial")
    numos = arguments.get("num_os")
    print(f"User config na tela Separar Abastecimento: {matricula}, Num OS: {numos}")
    
    # Será definida adiante (usada no 202)
    container_principal = None  # placeholder para manter escopo

    def snackbar(mensagem, bgcolor, page):
        snack = ft.SnackBar(
            content=ft.Text(mensagem, color="white"),
            bgcolor=bgcolor,
        )
        page.open(snack)

    def buscar_dados_os(numos):
        response = requests.post(
            base_url + "/abastecimento",
            json={
                "numos": numos,
                "matricula": matricula,
                "codfilial": codfilial,
                "action": "buscar_dados_os",
            },
        )
        print(f"Status code: {response.status_code}")
        resposta = response.json()
        mensagem = resposta.get("message")

        if response.status_code == 200:
            dados_os = resposta.get("dados_os")
            dados_endereco = resposta.get("dados_endereco")
            print("Dados encontrados da OS:", dados_os)
            return dados_os, dados_endereco
        elif response.status_code == 404:
            snackbar(mensagem, colorVariaveis["erro"], page)
            return [], []

    def container_dados_os(dados_os):
        if not dados_os:
            return ft.Text("Nenhum dado disponível.")

        itens = []
        for item in dados_os:
            codprod_item = item[1]
            descricao_item = item[2]
            quantidade_item = item[3]
            qtSeparada_item = item[4]

            itens.append(
                ft.ListTile(
                    ft.Text(
                        f"Codprod = {codprod_item} - Quantidade: {quantidade_item} - Qt.Separada: {qtSeparada_item}"
                    ),
                    subtitle=ft.Text(f"Descrição: {descricao_item}"),
                )
            )
        return ft.Column(itens)

    def container_endereco(dados_endereco):
        if not dados_endereco:
            return ft.Text("Nenhum dado disponível.")

        itens = []
        for endereco in dados_endereco:
            modulo = endereco[1]
            rua = endereco[2]
            edificio = endereco[3]
            nivel = endereco[4]
            apto = endereco[5]
            qt_endereco = endereco[7]

            itens.append(
                ft.Text(
                    f"MOD: {modulo} - RUA: {rua} - EDI: {edificio} - NIV: {nivel} - APTO: {apto} - Qtde: {qt_endereco}"
                )
            )
        return ft.Column(itens)

    # Helpers para construir conteúdo (mantém referência de Column para refresh)
    def construir_container_dados_os(dados_os):
        itens = []
        if not dados_os:
            itens.append(ft.Text("Nenhum dado disponível."))
        else:
            for item in dados_os:
                codprod_item = item[1]
                descricao_item = item[2]
                quantidade_item = item[3]
                qtSeparada_item = item[4]
                itens.append(
                    ft.ListTile(
                        ft.Text(
                            f"Codprod = {codprod_item} - Quantidade: {quantidade_item} - Qt.Separada: {qtSeparada_item}"
                        ),
                        subtitle=ft.Text(f"Descrição: {descricao_item}"),
                    )
                )
        return ft.Column(itens)

    def construir_container_endereco(dados_endereco):
        itens = []
        if not dados_endereco:
            itens.append(ft.Text("Nenhum dado disponível."))
        else:
            for endereco in dados_endereco:
                modulo = endereco[1]
                rua = endereco[2]
                edificio = endereco[3]
                nivel = endereco[4]
                apto = endereco[5]
                qt_endereco = endereco[7]
                itens.append(
                    ft.Text(
                        f"MOD: {modulo} - RUA: {rua} - EDI: {edificio} - NIV: {nivel} - APTO: {apto} - Qtde: {qt_endereco}"
                    )
                )
        return ft.Column(itens)

    def construir_container_picking(dados_picking):
        def validar_picking(input_picking, page):
            codendereco_picking = int(dados_picking[0][0])
            codendereco_input = int(input_picking.value.strip())
    
            print(f"Validando endereço picking: Input={codendereco_input}, Esperado={codendereco_picking}")
    
            if codendereco_input == codendereco_picking:
                atualizar_endereco_picking(codendereco_input, numos, page)
                snackbar("Endereço Picking válido!", colorVariaveis["sucesso"], page)
            else:
                snackbar("Endereço Picking inválido. Tente novamente.", colorVariaveis["erro"], page)

        
        input_codendereco_picking = ft.TextField(
            label="Endereço Picking",
            keyboard_type=ft.KeyboardType.NUMBER,
            on_submit=lambda e: validar_picking(input_codendereco_picking, page),
        )
        button_validarEndereco_picking = ft.ElevatedButton(
            text="Validar Endereço",
            on_click=lambda e: validar_picking(input_codendereco_picking, page),
        )

        itens = []
        if not dados_picking:
            itens.append(ft.Text("Nenhum dado disponível."))
        else:
            for endereco in dados_picking:
                modulo = endereco[1]
                rua = endereco[2]
                edificio = endereco[3]
                nivel = endereco[4]
                apto = endereco[5]
                qt_endereco = endereco[7]
                itens.append(
                    ft.Text(
                        f"MOD: {modulo} - RUA: {rua} - EDI: {edificio} - NIV: {nivel} - APTO: {apto} - Qtde: {qt_endereco}"
                    )
                )
            itens.append(input_codendereco_picking)
            itens.append(button_validarEndereco_picking)
        return ft.Column(itens)

    def atualizar_endereco_picking(codendereco, numos, page):
        response = requests.post(
            base_url + "/abastecimento",
            json={
                "codendereco": codendereco,
                "numos": numos,
                "matricula": matricula,
                "codfilial": codfilial,
                "codprod": dados_os[0][1],
                "action": "atualizar_endereco_picking",
            },
        )
        print(f"Status code: {response.status_code}")
        resposta = response.json()
        mensagem = resposta.get("message")

        if response.status_code == 200:
            snackbar(mensagem, colorVariaveis["sucesso"], page)
            navigate_to("/menu")
        elif response.status_code == 404:
            snackbar(mensagem, colorVariaveis["erro"], page)

    def construir_container_sem_picking(numos, page):
        print(f"Nenhum endereço de picking disponível.{numos}")
        input_codendereco_picking = ft.TextField(
            label="Endereço Picking",
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        btn_validar_novo_picking = ft.ElevatedButton(
            text="Validar Endereço",
            on_click=lambda e: atualizar_endereco_picking(input_codendereco_picking.value, numos, page)
        )
        return [
            ft.Text("Nenhum endereço de picking disponível."),
            ft.Text("Cadastrar endereço"),
            input_codendereco_picking,
            btn_validar_novo_picking,
        ]

    def busca_picking(codprod, codfilial):
        response = requests.post(
            base_url + "/abastecimento",
            json={
                "codprod": codprod,
                "codfilial": codfilial,
                "matricula": matricula,
                "action": "buscar_picking",
            },
        )
        print(f"Status code: {response.status_code}")
        resposta = response.json()
        mensagem = resposta.get("message")

        if response.status_code == 200:
            dados_picking = resposta.get("dados_picking")
            print("Dados encontrados do picking:", dados_picking)
            return dados_picking
        elif response.status_code == 404:
            print(" 1- Erro 404 ao atualizar quantidade separada.")
            container_principal.content.controls.clear()
            container_principal.content.controls.extend(
                        construir_container_sem_picking(numos, page)
                    )
            page.update()
            snackbar(mensagem, colorVariaveis["erro"], page)
            return []

    def atualizar_quantidade_separada(numos, codprod, quantidade, codendereco):
        nonlocal container_principal
        response = requests.post(
            base_url + "/abastecimento",
            json={
                "numos": numos,
                "codprod": codprod,
                "quantidade": quantidade,
                "codendereco": codendereco,
                "matricula": matricula,
                "codfilial": codfilial,
                "action": "atualizar_quantidade_separada",
            },
        )
        print(f"Status code: {response.status_code}")
        resposta = response.json()
        mensagem = resposta.get("message")

        if response.status_code == 200:
            snackbar(mensagem, colorVariaveis["sucesso"], page)
            return 200
        elif response.status_code == 202:
            dados_picking = busca_picking(codprod, codfilial)
            print("Dados do picking após atualização:", dados_picking)
            # Limpa o container principal para permitir nova informação
            if container_principal and isinstance(container_principal.content, ft.Column):
                container_principal.content.controls.clear()

                if dados_picking:
                    container_principal.content.controls.append(
                        construir_container_picking(dados_picking)
                    )
                else:
                    print(f"Não tem endereço de picknis")
                    container_principal.content.controls.clear()
                    container_principal.content.controls.extend(
                        construir_container_sem_picking(numos, page)
                    )
            page.update()
            snackbar(mensagem, colorVariaveis["sucesso"], page)
            page.update()
            return 202
        elif response.status_code == 404:
            print(" 2- Erro 404 ao atualizar quantidade separada.")
            container_principal.content.controls.append(
                        construir_container_sem_picking(numos, page)
                    )
            snackbar(mensagem, colorVariaveis["erro"], page)
            return 404

    def validar_endereco(e, dados_endereco):
        codendereco = int(dados_endereco[0][0])
        codendereco_input = int(input_codendereco.value.strip())

        print(f"Validando endereço: Input={codendereco_input}, Esperado={codendereco}")

        if codendereco_input == codendereco:
            dialog_quantidade()
            snackbar("Endereço válido!", colorVariaveis["sucesso"], page)
        else:
            snackbar("Endereço inválido. Tente novamente.", colorVariaveis["erro"], page)

    def dialog_quantidade():
        codendereco = int(dados_endereco[0][0])
        numos = int(dados_os[0][0])
        qt_endereco = dados_endereco[0][7]
        codprod = int(dados_os[0][1])

        def fechar_dialog(e):
            dialog.open = False
            page.update()

        def validar_qt(e):
            nonlocal dados_os, dados_endereco, container_dados_os, container_endereco, input_codendereco, button_validarEndereco
            quantidade_informada = int(input_quantidade.value.strip())

            if not quantidade_informada:
                snackbar("Informe a quantidade", colorVariaveis["erro"], page)
                return

            if quantidade_informada <= qt_endereco:
                snackbar(
                    f"Quantidade {quantidade_informada} confirmada.",
                    colorVariaveis["sucesso"],
                    page,
                )
                status = atualizar_quantidade_separada(
                    numos, codprod, quantidade_informada, codendereco
                )
                if status == 202:
                    fechar_dialog(e)
                    return

                # Recarrega os dados atualizados e atualiza a interface
                dados_os, dados_endereco = buscar_dados_os(numos)

                # Atualiza os containers na tela mantendo as referências
                novo_container_os = construir_container_dados_os(dados_os)
                novo_container_end = construir_container_endereco(dados_endereco)
                container_dados_os.controls = novo_container_os.controls
                container_endereco.controls = novo_container_end.controls

                # Atualiza os handlers para usarem o novo dados_endereco
                input_codendereco.on_submit = lambda ev: validar_endereco(
                    ev, dados_endereco
                )
                button_validarEndereco.on_click = lambda ev: validar_endereco(
                    ev, dados_endereco
                )
                input_codendereco.value = ""
                page.update()
                fechar_dialog(e)
            else:
                fechar_dialog(e)
                snackbar(
                    f"Quantidade inválida. Máximo permitido: {qt_endereco}.",
                    colorVariaveis["erro"],
                    page,
                )

        input_quantidade = ft.TextField(
            label="Quantidade",
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        button_confirmar = ft.ElevatedButton(
            "Confirmar",
            on_click=lambda e: validar_qt(e),
        )

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Quantidade"),
            content=ft.Column(
                controls=[
                    ft.Text("Informe a quantidade"),
                    input_quantidade,
                    button_confirmar,
                ],
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: fechar_dialog(e)),
            ],
        )
        page.overlay.append(dialog)

        dialog.open = True
        page.update()

    # Busca inicial
    dados_os, dados_endereco = buscar_dados_os(numos)

    # Cria containers como Column para poder atualizar seu conteúdo posteriormente
    container_dados_os = construir_container_dados_os(dados_os)
    container_endereco = construir_container_endereco(dados_endereco)

    input_codendereco = ft.TextField(
        label="Código Endereço",
        on_submit=lambda e: validar_endereco(e, dados_endereco),
    )
    button_validarEndereco = ft.ElevatedButton(
        "Validar Endereço",
        on_click=lambda e: validar_endereco(e, dados_endereco),
    )

    # Container principal (limpado quando API retorna 202)
    container_principal = ft.Container(
        content=ft.Column(
            controls=[
                container_dados_os,
                container_endereco,
                input_codendereco,
                button_validarEndereco,
            ]
        )
    )

    return ft.View(
        route="/separar_abastecimento",
        controls=[
            header,
            ft.Text(f"Número da OS: {numos}", size=16),
            container_principal,
        ],
    )

