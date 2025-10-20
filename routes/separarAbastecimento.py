import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def separar_abastecimento(page: ft.Page, navigate_to, header, arguments):
    matricula = user_info.get("matricula")
    codfilial = user_info.get("codfilial")
    numos = arguments.get("num_os")
    print(f"User config na tela Separar Abastecimento: {matricula}, Num OS: {numos}")

    def snackbar(mensagem, bgcolor, page):
        snack = ft.SnackBar(
            content=ft.Text(
                mensagem,
                color="white"
            ),
            bgcolor=bgcolor)
        page.open(snack)

    def buscar_dados_os(numos):
        response = requests.post(
            base_url + "/abastecimento",
            json={
                "numos": numos,
                "matricula": matricula,
                "codfilial": codfilial,
                "action": "buscar_dados_os"
            },
        )
        print(f"Status code: {response.status_code}")
        # print(f"Response: {response.json()}")
        resposta = response.json()
        mensagem = resposta.get("message")
        # print(mensagem)

        if response.status_code == 200:
            dados_os = resposta.get("dados_os")
            dados_endereco = resposta.get("dados_endereco")
            print("Dados encontrados da OS:", dados_os)
            return dados_os, dados_endereco

            snackbar(mensagem, colorVariaveis['sucesso'], page)
            # Aqui você pode adicionar a lógica para exibir os dados da OS na tela
        elif response.status_code == 404:
            snackbar(mensagem, colorVariaveis['erro'], page)

    def atualizar_quantidade_separada(numos, codprod, quantidade, codendereco):
        response = requests.post(
            base_url + "/abastecimento",
            json={
                "numos": numos,
                "codprod": codprod,
                "quantidade": quantidade,
                "codendereco": codendereco,
                "matricula": matricula,
                "codfilial": codfilial,
                "action": "atualizar_quantidade_separada"
            },
        )
        print(f"Status code: {response.status_code}")
        # print(f"Response: {response.json()}")
        resposta = response.json()
        mensagem = resposta.get("message")
        # print(mensagem)

        if response.status_code == 200:
            snackbar(mensagem, colorVariaveis['sucesso'], page)
            # Aqui você pode adicionar a lógica para exibir os dados da OS na tela
        elif response.status_code == 404:
            snackbar(mensagem, colorVariaveis['erro'], page)

    def container_dados_os(dados_os):
        if not dados_os:
            return ft.Text("Nenhum dado disponível.")

        itens = []
        for item in dados_os:
            numos_item = item[0]
            codprod_item = item[1]
            descricao_item = item[2]
            quantidade_item = item[3]
            qtSeparada_item = item[4]
            codfilial_item = item[5]

            itens.append(
                ft.ListTile(
                    ft.Text(f"Codprod = {codprod_item} - Quantidade: {quantidade_item} - Qt.Separada: {qtSeparada_item}"),
                    subtitle=ft.Text(f"Descrição: {descricao_item}")
                )
            )
        return ft.Column(itens)

    def container_endereco(dados_endereco):
        if not dados_endereco:
            return ft.Text("Nenhum dado disponível.")

        itens = []
        for endereco in dados_endereco:
            codendereco = endereco[0]
            modulo = endereco[1]
            rua = endereco[2]
            edificio = endereco[3]
            nivel = endereco[4]
            apto = endereco[5]
            qt_endereco = endereco[7]

            itens.append(
                ft.Text(f"MOD: {modulo} - RUA: {rua} - EDI: {edificio} - NIV: {nivel} - APTO: {apto} - Qtde: {qt_endereco}")
            )
        return ft.Column(itens)

    def validar_endereco(e, dados_endereco):
        codendereco = int(dados_endereco[0][0])
        codendereco_input = int(input_codendereco.value.strip())

        print(f"Validando endereço: Input={codendereco_input}, Esperado={codendereco}")

        if codendereco_input == codendereco:
            dialog_quantidade()
            snackbar("Endereço válido!", colorVariaveis['sucesso'], page)
        else:
            snackbar("Endereço inválido. Tente novamente.", colorVariaveis['erro'], page)

    def dialog_quantidade():
        codendereco = int(dados_endereco[0][0])
        numos = int(dados_os[0][0])
        qt_endereco = dados_endereco[0][7]
        codprod = int(dados_os[0][1])
        def fechar_dialog(e):
            dialog.open = False
            page.update()

        def validar_qt(e):
            quantidade_informada = int(input_quantidade.value.strip())

            if not quantidade_informada:
                snackbar("Informe a quantidade", colorVariaveis['erro'], page)
                return
            
            if quantidade_informada <= qt_endereco:
                snackbar(f"Quantidade {quantidade_informada} confirmada.", colorVariaveis['sucesso'], page)
                atualizar_quantidade_separada(numos, codprod, quantidade_informada, codendereco)
                fechar_dialog(e)
            else:
                fechar_dialog(e)
                snackbar(f"Quantidade inválida. Máximo permitido: {qt_endereco}.", colorVariaveis['erro'], page)

        input_quantidade = ft.TextField(
            label="Quantidade",
            keyboard_type=ft.KeyboardType.NUMBER
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
                    button_confirmar
                ],
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: fechar_dialog(e)),
            ],
        )
        page.overlay.append(dialog)

        dialog.open = True
        page.update()

    dados_os, dados_endereco = buscar_dados_os(numos)
    
    if dados_os:
        container_dados_os = container_dados_os(dados_os)
    else:
        container_dados_os = ft.Text("Nenhum dado disponível.")

    if dados_endereco:
        container_endereco = container_endereco(dados_endereco)
    else:
        container_endereco = ft.Text("Nenhum dado disponível.")

    input_codendereco = ft.TextField(
        label="Código Endereço",
        on_submit=lambda e: validar_endereco(e, dados_endereco)
    )
    button_validarEndereco = ft.ElevatedButton(
        "Validar Endereço",
        on_click=lambda e: validar_endereco(e, dados_endereco)
    )

    return ft.View(
        route="/separar_abastecimento",  # Define a rota da página
        controls=[
            header,
            ft.Text(f"Número da OS: {numos}", size=16),
            container_dados_os,
            container_endereco,
            input_codendereco,
            button_validarEndereco
        ]
    )