import flet as ft
import requests
from routes.config.config import base_url, user_info, colorVariaveis

def transferir_produto(page, navigate_to, header):
    matricula = user_info.get("matricula")
    codfilial = user_info.get("codfilial")

    titulo = ft.Text(
        "Transferir Produto",
        size=24, weight="bold",
        color=colorVariaveis['titulo']
    )
    button_voltar = ft.IconButton(
        icon=ft.icons.ARROW_BACK,
        icon_color=colorVariaveis['texto'],
        on_click=lambda e: navigate_to("/transferirProduto"),
    )
    titulobarra = ft.Row(
        controls=[
            titulo,
            button_voltar,
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    # --- 1) Cria todos os campos e botões usados na tela ---
    codenderecoAtual_field = ft.TextField(
        label="Endereço Atual",
        prefix_icon=ft.icons.BARCODE_READER,
        border_radius=ft.border_radius.all(10),
        border_color=colorVariaveis['bordarInput'],
        border_width=2,
    )
    button_consultar_endereco = ft.ElevatedButton(
        text="Consultar Endereço",
        color=colorVariaveis['texto'],
        bgcolor=colorVariaveis['botaoAcao'],
        on_click=lambda e: consultar_endereco(e),
    )

    codbarra_field = ft.TextField(
        label="Código de Barras",
        prefix_icon=ft.icons.BARCODE_READER,
        border_radius=ft.border_radius.all(10),
        border_color=colorVariaveis['bordarInput'],
        border_width=2,
    )
    button_consultar_produto = ft.ElevatedButton(
        text="Consultar Produto",
        color=colorVariaveis['texto'],
        bgcolor=colorVariaveis['botaoAcao'],
        on_click=lambda e: consultar_produto(e),
    )

    enderecoDestino_field = ft.TextField(
        label="Endereço Destino",
        border_radius=ft.border_radius.all(10),
        border_color=colorVariaveis['bordarInput'],
        border_width=2,
    )
    quantidade_field = ft.TextField(
        label="Quantidade",
        border_radius=ft.border_radius.all(10),
        border_color=colorVariaveis['bordarInput'],
        border_width=2,
    )
    button_confirmar = ft.ElevatedButton(
        text="Confirmar Transferência",
        color=colorVariaveis['texto'],
        bgcolor=colorVariaveis['botaoAcao'],
        on_click=lambda e: confirmar_transferencia(e),
    )

    produto_info = ft.Column()  # container para exibir o produto consultado
    lista_produtos = ft.Column()  # container para exibir produtos do endereço

    # --- 2) O main_container, que será atualizado dinamicamente ---
    main_container = ft.Column(
        controls=[
            ft.Text("Informe o endereço para consulta:", size=16),
            codenderecoAtual_field,
            button_consultar_endereco
        ],
        scroll=ft.ScrollMode.AUTO
    )

    # --- 3) Função para exibir um snackbar genérico ---
    def show_snack(message, error=False):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=colorVariaveis['erro'] if error else colorVariaveis['sucesso'],
        )
        page.snack_bar.open = True
        page.update()

    # --- 4) Handler de consulta de endereço ---
    def consultar_endereco(e):
        endereco = codenderecoAtual_field.value.strip()
        if not endereco:
            show_snack("Informe um endereço", error=True)
            return
        try:
            resp = requests.post(
                f"{base_url}/transferirProduto",
                json={
                    "action": "consultarEndereco",
                    "codenderecoAtual": endereco,
                    "codfilial": codfilial
                }
            )
            if resp.status_code == 200:
                dados = resp.json().get("dados_endereco", [])
                # endereco_completo = resp.json().get("endereco_completo", "")
                # print(f"Endereço completo: {endereco_completo}")

                # mod, rua, edf, niv, apt = endereco_completo[0]  # ajuste de acordo com seu JSON

                # # monta o row dinamicamente dentro do handler
                # endereco_lista.controls.clear()
                # endereco_lista = ft.Row(
                #     controls=[
                #         ft.Column(controls=[ft.Text("MOD", weight="BOLD"), ft.Text(str(mod))]),
                #         ft.Column(controls=[ft.Text("RUA", weight="BOLD"), ft.Text(str(rua))]),
                #         ft.Column(controls=[ft.Text("EDF", weight="BOLD"), ft.Text(str(edf))]),
                #         ft.Column(controls=[ft.Text("NIV", weight="BOLD"), ft.Text(str(niv))]),
                #         ft.Column(controls=[ft.Text("APT", weight="BOLD"), ft.Text(str(apt))]),
                #     ],
                #     alignment=ft.MainAxisAlignment.SPACE_AROUND,
                #     expand=True,
                # )

                if not dados:
                    show_snack("Nenhum produto neste endereço", error=True)
                    return
                # atualiza a tela com a lista de produtos + campo de codbarra
                lista_produtos.controls.clear()
                for row in dados:
                    lista_produtos.controls.append(criar_container_produto(row))

                main_container.controls = [
                    ft.Text(f"Endereço:", size=16, weight="BOLD"),
                    # endereco_lista,
                    ft.Divider(),
                    lista_produtos,
                    ft.Divider(),
                    codbarra_field,
                    button_consultar_produto
                ]
                page.update()
            else:
                show_snack(resp.json().get("mensagem","Erro"), error=True)
        except Exception as ex:
            print("Erro ao consultar endereço:", ex)
            show_snack("Erro na requisição", error=True)

    # --- 5) Handler de consulta de produto ---
    def consultar_produto(e):
        codbarra = codbarra_field.value.strip()
        endereco = codenderecoAtual_field.value.strip()
        if not codbarra:
            show_snack("Informe o código de barras", error=True)
            return
        try:
            resp = requests.post(
                f"{base_url}/transferirProduto",
                json={
                    "action": "consultarProduto",
                    "codbarra": codbarra,
                    "codenderecoAtual": endereco,
                    "codfilial": codfilial
                }
            )
            if resp.status_code == 201:
                dados = resp.json().get("dados_produto", [])
                if not dados:
                    show_snack("Produto não encontrado", error=True)
                    return
                # exibe o primeiro produto encontrado + campos de destino/quantidade
                produto_info.controls.clear()
                produto_info.controls.append(criar_container_produto(dados[0]))
                quantidade_field.value = str(dados[0][2])
                main_container.controls = [
                    ft.Text("Dados do produto:", size=16),
                    produto_info,
                    enderecoDestino_field,
                    quantidade_field,
                    button_confirmar
                ]
                page.update()
            else:
                show_snack(resp.json().get("mensagem","Erro"), error=True)
        except Exception as ex:
            print("Erro ao consultar produto:", ex)
            show_snack("Erro na requisição", error=True)

    # --- 6) Handler de confirmação da transferência ---
    def confirmar_transferencia(e):
        codbarra = codbarra_field.value.strip()
        origem   = codenderecoAtual_field.value.strip()
        destino  = enderecoDestino_field.value.strip()
        qt       = quantidade_field.value.strip()
        if not all([codbarra, origem, destino, qt]):
            show_snack("Preencha todos os campos", error=True)
            return
        try:
            resp = requests.post(
                f"{base_url}/transferirProduto",
                json={
                    "action": "transferir",
                    "codbarra": codbarra,
                    "codenderecoAtual": origem,
                    "codenderecoNovo": destino,
                    "quantidade": qt,
                    "codfilial": codfilial
                }
            )
            if resp.status_code == 202:
                show_snack("Transferência realizada com sucesso")
                # volta ao estado inicial, limpando tudo
                codenderecoAtual_field.value = ""
                codbarra_field.value = ""
                enderecoDestino_field.value = ""
                quantidade_field.value = ""
                main_container.controls = [
                    ft.Text("Informe o endereço para consulta:", size=16),
                    codenderecoAtual_field,
                    button_consultar_endereco
                ]
                page.update()
            else:
                show_snack(resp.json().get("mensagem","Erro"), error=True)
        except Exception as ex:
            print("Erro na transferência:", ex)
            show_snack("Erro na requisição", error=True)

    # --- 7) Função auxiliar para criar o layout de cada produto ---
    def criar_container_produto(row):
        codprod, codfab, qt, descricao = row
        return ft.Container(
            padding=10,
            content=ft.Column([
                ft.Row([
                    ft.Text("CODPROD:", weight="BOLD"),
                    ft.Text("CODFAB:", weight="BOLD"),
                    ft.Text("QT:",     weight="BOLD"),
                ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
                ft.Row([
                    ft.Text(str(codprod)),
                    ft.Text(str(codfab)),
                    ft.Text(str(qt)),
                ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
                
                ft.Divider(),
                ft.Text(descricao)
            ]),
            border=ft.border.all(1, colorVariaveis['bordarInput']),
            border_radius=ft.border_radius.all(5),
            margin=5
        )

    # --- 8) Retorna a View com o main_container dinâmico ---
    return ft.View(
        route="/transferirProduto",
        controls=[
            header,
            titulobarra,
            main_container
        ],
        scroll=ft.ScrollMode.AUTO
    )
