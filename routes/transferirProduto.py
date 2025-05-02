import flet as ft
import requests
from routes.config.config import base_url, user_info, colorVariaveis

def transferir_produto(page, navigate, header):
    # Container para os resultados da consulta de endereço
    lista_produtos = ft.Column(scroll=ft.ScrollMode.AUTO)
    matricula = user_info.get("matricula")
    codfilial = user_info.get("codfilial")

    
    # Container para os resultados da consulta do produto (codbarra)
    produtoInfoContainer = ft.Container()

    # Campo para preencher endereço de destino no dialog de produto
    enderecoDestinoField = ft.TextField(
        label="Endereço Destino",
        border_radius=ft.border_radius.all(10),
        border_color=colorVariaveis['bordarInput'],
        border_width=2,
    )
    # Campo para quantidade, que será pré-preenchido
    quantidadeField = ft.TextField(
        label="Quantidade",
        border_radius=ft.border_radius.all(10),
        border_color=colorVariaveis['bordarInput'],
        border_width=2,
    )
    
    title = ft.Text(
        "Transferir Produto",
        size=24,
        weight="bold",
        color=colorVariaveis['titulo']
    )
    
    # Campo para inserir o endereço atual
    codenderecoAtual = ft.TextField(
        label="CODENDERECO",
        prefix_icon=ft.icons.BARCODE_READER,
        border_radius=ft.border_radius.all(10),
        border_color=colorVariaveis['bordarInput'],
        border_width=2,
    )
    # Botão para consultar produtos no endereço
    buttonConsultarEndereco = ft.ElevatedButton(
        text="Consultar",
        color=colorVariaveis['texto'],
        bgcolor=colorVariaveis['botaoAcao'],
        on_click=lambda e: consultar_endereco(codenderecoAtual.value, e),
    )
    
    # Campo para inserir o código de barras no diálogo de endereço
    codbarra_dialog = ft.TextField(
        label="CODBARRA",
        prefix_icon=ft.icons.BARCODE_READER,
        border_radius=ft.border_radius.all(10),
        border_color=colorVariaveis['bordarInput'],
        border_width=2,
    )
    
    # Botão para transferir (consulta por codbarra)
    buttonTransferirProduto = ft.ElevatedButton(
        text="Transferir",
        color=colorVariaveis['texto'],
        bgcolor=colorVariaveis['botaoAcao'],
        on_click=lambda e: consultar_codbarra(codbarra_dialog.value, codenderecoAtual.value, e)
    )
    
    # Dialog de Endereço: exibe os produtos do endereço e permite digitar o CODBARRA
    dialogEnderecoContent = ft.Column(
        controls=[
            lista_produtos,
            codbarra_dialog,
            buttonTransferirProduto
        ],
        scroll=ft.ScrollMode.AUTO
    )
    dialogEndereco = ft.AlertDialog(
        title=ft.Text("Itens do endereço"),
        content=dialogEnderecoContent,
        actions=[
            ft.ElevatedButton(
                "Fechar",
                color=colorVariaveis['texto'],
                bgcolor=colorVariaveis['botaoAcao'],
                on_click=lambda e: fechar_dialogEndereco(e)
            )
        ],
    )
    
    # Dialog de Produto: exibe as informações do produto selecionado e os campos para endereço destino e quantidade
    dialogProdutoContent = ft.Column(
        controls=[
            produtoInfoContainer,  # Container que receberá as informações do produto
            enderecoDestinoField,  # Campo para endereço destino
            quantidadeField,       # Campo para quantidade (pré-preenchido)
            ft.ElevatedButton(
                "Confirmar",
                color=colorVariaveis['texto'],
                bgcolor=colorVariaveis['botaoAcao'],
                on_click=lambda e: confirmar_transferencia(codbarra_dialog.value, codenderecoAtual.value, enderecoDestinoField.value, quantidadeField.value, e))
        ],
        scroll=ft.ScrollMode.AUTO
    )
    dialogProduto = ft.AlertDialog(
        title=ft.Text("Confirmação de Transferência"),
        content=dialogProdutoContent,
        actions=[
            ft.ElevatedButton(
                "Fechar",
                color=colorVariaveis['texto'],
                bgcolor=colorVariaveis['botaoAcao'],
                on_click=lambda e: fechar_dialogProduto(e))
        ],
    )
    
    # Funções para abrir/fechar os diálogos:
    def abrir_dialogEndereco():
        page.dialog = dialogEndereco
        dialogEndereco.open = True
        page.update()
    
    def fechar_dialogEndereco(e):
        dialogEndereco.open = False
        new_lista_produtos = ft.Column(scroll=ft.ScrollMode.AUTO)
        dialogEndereco.content = ft.Column(
            controls=[new_lista_produtos, codbarra_dialog, buttonTransferirProduto],
            scroll=ft.ScrollMode.AUTO
        )
        nonlocal lista_produtos
        lista_produtos = new_lista_produtos
        codbarra_dialog.value = ""
        page.update()
    
    def abrir_dialogProduto():
        page.dialog = dialogProduto
        dialogProduto.open = True
        page.update()
    
    def fechar_dialogProduto(e):
        dialogProduto.open = False
        produtoInfoContainer.content = None
        enderecoDestinoField.value = ""
        quantidadeField.value = ""
        page.update()
    
    # Função para criar um container com o layout de um produto (para consulta de endereço ou produto)
    def criar_container_produto(row):
        # Para consulta de endereço, assumimos que row é: [codprod, codfab, qt, descricao]
        codprod, codfab, qt, descricao = row
        return ft.Container(
            padding=10,
            content=ft.Column(
                controls=[
                    ft.Row(
                        expand=True,
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        controls=[
                            ft.Column(
                                controls=[ft.Text("CODPROD", weight="BOLD"), ft.Text(str(codprod))]
                            ),
                            ft.Column(
                                controls=[ft.Text("CODFAB", weight="BOLD"), ft.Text(str(codfab))]
                            ),
                            ft.Column(
                                controls=[ft.Text("QT", weight="BOLD"), ft.Text(str(qt))]
                            ),
                        ],
                    ),
                    ft.Divider(),
                    ft.Row(
                        controls=[
                            ft.Column(
                                expand=True,
                                controls=[ft.Text("PRODUTO", weight="BOLD"), ft.Text(descricao)]
                            )
                        ],
                    ),
                ]
            ),
            border=ft.border.all(1, colorVariaveis['bordarInput']),
        )
    
    # Consulta de endereço: preenche o container com os produtos desse endereço e abre dialogEndereco
    def consultar_endereco(codenderecoAtual, e):
        lista_produtos.controls.clear()
        try:
            response = requests.post(
                f"{base_url}/transferirProduto",
                json={
                    "codenderecoAtual": codenderecoAtual,
                    "codfilial": codfilial,
                    "action": "consultarEndereco",
                }
            )
            if response.status_code == 200:
                dados = response.json()
                dados_endereco = dados.get("dados_endereco", [])
                lista_produtos.controls.clear()
                for row in dados_endereco:
                    container_end = criar_container_produto(row)
                    lista_produtos.controls.append(container_end)
                abrir_dialogEndereco()
            elif response.status_code == 402:
                dados = response.json()
                mensagem = dados.get("mensagem")
                snackbar_error = ft.SnackBar(
                    ft.Text(mensagem, color=colorVariaveis['texto'], size=20),
                    bgcolor=colorVariaveis['erro'],
                    show_close_icon=True,
                )
                page.overlay.append(snackbar_error)
                snackbar_error.open = True
            e.page.update()
        except Exception as exc:
            print("Erro na requisição (endereco):", exc)
        e.page.update()
    
    # Consulta de produto (codbarra): preenche o dialogProduto com as informações do produto
    def consultar_codbarra(codbarra, codenderecoAtual, e):
        try:
            response = requests.post(
                f"{base_url}/transferirProduto",
                json={
                    "codbarra": codbarra,
                    "codenderecoAtual": codenderecoAtual,
                    "codfilial": codfilial,
                    "action": "consultarProduto"
                }
            )
            if response.status_code == 201:
                dados = response.json()
                dados_produto = dados.get("dados_produto", [])
                if dados_produto:
                    # Pega o primeiro produto retornado
                    row = dados_produto[0]
                    container_prod = criar_container_produto(row)
                    produtoInfoContainer.content = container_prod
                    # Preenche o campo de quantidade com o qt do produto
                    quantidadeField.value = str(row[2])
                    abrir_dialogProduto()
            elif response.status_code == 403:
                dados = response.json()
                mensagem = dados.get("mensagem")
                snackbar_error = ft.SnackBar(
                    ft.Text(mensagem, color=colorVariaveis['texto'], size=20),
                    bgcolor=colorVariaveis['erro'],
                    show_close_icon=True,
                )
                page.overlay.append(snackbar_error)
                snackbar_error.open = True
            e.page.update()
        except Exception as exc:
            print("Erro na requisição (produto):", exc)
        e.page.update()
    
    # Função para confirmar a transferência (exemplo)
    def confirmar_transferencia(codbarra, codenderecoAtual, codenderecoNovo, quantidade, e):
        try:
            response  =requests.post(
                f"{base_url}/transferirProduto",
                json={"codbarra": codbarra,
                    "codenderecoAtual": codenderecoAtual,
                    "codenderecoNovo": codenderecoNovo,
                    "quantidade": quantidade
                }
            )
            if response.status_code == 202:
                print("Atualizado com sucesso")
            elif response.status_code == 405:
                print("Erro na atualização")
        except Exception as exc:
            print("Erro na requisição (produto):", exc)
        e.page.update()
        fechar_dialogProduto(e)
    
    # Como a tela sempre consulta o endereço, usamos apenas um tab (de Endereço)
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        height=200,
        tabs=[
            ft.Tab(
                text="Endereço",
                content=ft.Column(
                    [
                        ft.Text("Informe o código de barras do endereço", size=16),
                        codenderecoAtual,
                        buttonConsultarEndereco,
                    ]
                ),
            ),
        ],
    )
    
    return ft.View(
        route="/transferirProduto",
        controls=[
            header,
            title,
            tabs,
        ],
        scroll=ft.ScrollMode.AUTO,
    )
