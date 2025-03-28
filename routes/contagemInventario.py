import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def contagem_inventario(e, navigate_to, header):
    matricula = user_info.get('matricula')
    codfilial = user_info.get('codfilial')

    # Cria uma referência dinâmica para os elementos que mudam
    conteudo_dinamico = ft.Column()

    def mostrar_campos_endereco(e, dados_os):
        # Limpa o conteúdo dinâmico
        conteudo_dinamico.controls.clear()

        # Campo para o usuário digitar o endereço
        campo_endereco = ft.TextField(label="Endereço")

        # Lista para armazenar os produtos inseridos
        produtos = []  # Cada item será uma tupla: (codendereco, codbarra, quantidade)

        # Função para fechar um dialog aberto
        def fechar_dialog(e):
            e.page.dialog.open = False
            e.page.update()

        # Função para abrir o dialog de inserção do produto (código de barras e quantidade)
        def abrir_dialog_produto(e):
            campo_codbarra = ft.TextField(label="Código de Barras")
            campo_quantidade = ft.TextField(label="Quantidade", keyboard_type=ft.KeyboardType.NUMBER)

            def confirmar_produto(e):
                # Adiciona o produto na lista utilizando o endereço digitado
                produtos.append((campo_endereco.value, campo_codbarra.value, campo_quantidade.value))
                fechar_dialog(e)  # Fecha o dialog de inserção do produto
                abrir_dialog_confirmacao(e)  # Abre o dialog para perguntar se há mais produtos

            dialog_produto = ft.AlertDialog(
                title=ft.Text("Adicionar Produto"),
                content=ft.Column(
                    controls=[
                        ft.Text(f"Endereço: {campo_endereco.value}"),
                        campo_codbarra,
                        campo_quantidade
                    ]
                ),
                actions=[
                    ft.TextButton("Cancelar", on_click=fechar_dialog),
                    ft.TextButton("OK", on_click=confirmar_produto)
                ]
            )
            e.page.dialog = dialog_produto
            dialog_produto.open = True
            e.page.update()

        # Função para abrir o dialog que pergunta se há mais produtos nesse endereço
        def abrir_dialog_confirmacao(e):
            def adicionar_mais(e):
                fechar_dialog(e)
                abrir_dialog_produto(e)  # Reabre o dialog para inserir outro produto

            def finalizar(e):
                fechar_dialog(e)
                # Aqui você pode, por exemplo, atualizar a interface com a lista ou enviar para backend
                print("Lista de produtos:", produtos)
                e.page.snack_bar = ft.SnackBar(ft.Text("Produtos adicionados com sucesso!"))
                e.page.snack_bar.open = True
                conteudo_dinamico.controls.clear()  # Limpa o conteúdo dinâmico
                conteudo_dinamico.controls.append(botao_iniciar)
                e.page.update()

            dialog_confirmacao = ft.AlertDialog(
                title=ft.Text("Confirmação"),
                content=ft.Text("Tem mais produtos nesse endereço?"),
                actions=[
                    ft.TextButton("Sim", on_click=adicionar_mais),
                    ft.TextButton("Não", on_click=finalizar)
                ]
            )
            e.page.dialog = dialog_confirmacao
            dialog_confirmacao.open = True
            e.page.update()

        # Função para confirmar o endereço informado
        def confirmar_endereco(e):
            codigo_esperado = str(dados_os[0][2])
            if campo_endereco.value == codigo_esperado:
                # Endereço correto: abre o dialog para inserir o produto
                abrir_dialog_produto(e)
            else:
                e.page.snack_bar = ft.SnackBar(ft.Text("Endereço incorreto"))
                e.page.snack_bar.open = True
                e.page.update()

        # Adiciona os controles iniciais para entrada do endereço
        conteudo_dinamico.controls.append(
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(f"Nº Inventário: {dados_os[0][0]}"),
                        ft.Text(f"Nº OS: {dados_os[0][1]}"),
                        ft.Text(f"Endereço: {dados_os[0][2]}"),
                        campo_endereco,
                        ft.ElevatedButton(
                            "Confirmar Endereço",
                            on_click=confirmar_endereco
                        )
                    ]
                )
            )
        )
        e.page.update()

    def buscar_os(e, codfilial, matricula):
        try:
            response = requests.post(
                f"{base_url}/contagem_inventario",
                json={
                    "codfilial": codfilial,
                    "matricula": matricula
                }
            )
            if response.status_code in [200, 202]:
                dados = response.json()
                dados_os = dados.get("dados_os", [])
                mensagem = dados.get("mensagem")
                print(f"Dados os: {dados_os}")
                print(f"Mensagem: {mensagem}")
                mostrar_campos_endereco(e, dados_os)
            else:
                dados = response.json()
                dados_os = dados.get("dados_os", [])
                mensagem = dados.get("mensagem")
                print("Não iniciou contagem")
                print(f"Dados os: {dados_os}")
                print(f"Mensagem: {mensagem}")

        except Exception as exc:
            print(exc)

    title = ft.Text(
        "Buscar Inventário",
        size=24,
        weight="bold",
        color=colorVariaveis['titulo']
    )

    botao_iniciar = ft.ElevatedButton(
        "Iniciar Inventário",
        on_click=lambda e: buscar_os(e, codfilial, matricula)
    )

    conteudo_dinamico.controls.append(botao_iniciar)

    return ft.View(
        route="/contagem_inventario",
        controls=[
            header,
            title,
            conteudo_dinamico
        ]
    )
