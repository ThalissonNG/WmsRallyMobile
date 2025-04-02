import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def contagem_inventario(e, navigate_to, header):
    matricula = user_info.get('matricula')
    codfilial = user_info.get('codfilial')
    
    # Área dinâmica para atualizar a tela
    conteudo_dinamico = ft.Column()
    
    def mostrar_campos_endereco(e, dados_os):
        # Limpa o conteúdo dinâmico
        conteudo_dinamico.controls.clear()
    
        # Campo para o usuário digitar o endereço
        campo_endereco = ft.TextField(label="Endereço")
    
        # Função para confirmar o endereço informado
        def confirmar_endereco(e):
            codigo_esperado = str(dados_os[0][2])
            if campo_endereco.value == codigo_esperado:
                # Endereço correto: abre o dialog para inserir o código de barras
                abrir_dialog_codbarra(e, dados_os)
            else:
                e.page.snack_bar = ft.SnackBar(ft.Text("Endereço incorreto"))
                e.page.snack_bar.open = True
                e.page.update()
    
        # Adiciona os controles para entrada do endereço
        conteudo_dinamico.controls.append(
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(f"Nº Inventário: {dados_os[0][0]}"),
                        ft.Text(f"Nº OS: {dados_os[0][1]}"),
                        ft.Text(f"Endereço: {dados_os[0][2]}"),
                        campo_endereco,
                        ft.ElevatedButton("Confirmar Endereço", on_click=confirmar_endereco)
                    ]
                )
            )
        )
        e.page.update()
    
    def abrir_dialog_codbarra(e, dados_os):
        # Cria o campo para inserir o código de barras
        campo_codbarra = ft.TextField(label="Código de Barras")
        
        # Função para confirmar o código de barras
        def confirmar_codbarra(e, codbarra):
            response = requests.post(
                f"{base_url}/contagem_inventario",
                json={
                    "codbarra": codbarra,
                    "matricula": matricula,
                    "codfilial":codfilial,
                    "dados_os": dados_os,
                    "action": "validar_codbarra",
                }
            )
            if response.status_code == 200:
                print("Código de barras válido")
                # Se a validação retornar 200, abre o dialog para inserir a quantidade
                dados = response.json()
                mensagem = dados.get("mensagem")
                produto = dados.get("produto")
                print(produto)
                abrir_dialog_quantidade(e, codbarra, dados_os, produto)
            elif response.status_code == 500:
                print("Código de barras não cadastrado")
                abrir_dialog_codbarra_nao_cadastrado(e)
            else:
                print("Resposta inesperada:", response.status_code)
            # Não feche o dialog aqui, para não interferir no dialog aberto pela função chamada
    
        dialog_codbarra = ft.AlertDialog(
            title=ft.Text("Inserir Código de Barras"),
            content=ft.Column(controls=[campo_codbarra]),
            actions=[ft.TextButton("Confirmar", on_click=lambda e: confirmar_codbarra(e, campo_codbarra.value))]
        )
        e.page.dialog = dialog_codbarra
        dialog_codbarra.open = True
        e.page.update()
    
    def abrir_dialog_quantidade(e, codbarra, dados_os, produto):
        # Cria o campo para inserir a quantidade
        campo_quantidade = ft.TextField(label="Quantidade")
        
        # Função para confirmar a quantidade
        def confirmar_quantidade(e):
            response = requests.post(
                f"{base_url}/contagem_inventario",
                json={
                    "codbarra": codbarra,
                    "quantidade": campo_quantidade.value,
                    "dados_os": dados_os,
                    "action": "confirmar_quantidade"
                }
            )
            if response.status_code == 200:
                dados = response.json()
                mensagem = dados.get("mensagem")
                print(mensagem)
                e.page.snack_bar = ft.SnackBar(ft.Text(mensagem), bgcolor=colorVariaveis['sucesso'])
                e.page.snack_bar.open = True
                e.page.update()
                # Após confirmação, abre o dialog perguntando se há mais produtos
                abrir_dialog_mais_produtos(e, dados_os)
            else:
                dados = response.json()
                mensagem = dados.get("mensagem")
                print("Erro ao confirmar quantidade:", response.status_code)
                print(mensagem)
                e.page.snack_bar = ft.SnackBar(ft.Text(mensagem), bgcolor=colorVariaveis['erro'])
                e.page.snack_bar.open = True
                e.page.update()
            # e.page.dialog.open = False
            # e.page.update()
        
        dialog_quantidade = ft.AlertDialog(
            title=ft.Text("Inserir Quantidade"),
            content=ft.Column(
                controls=[
                    ft.Text(f"CODPROD: {produto[0][0]}"),
                    ft.Text(f"CODFAB: {produto[0][1]}"),
                    ft.Text(f"DESCRIÇÃO: {produto[0][2]}"),
                    campo_quantidade
                ]
            ),
            actions=[ft.TextButton("Confirmar", on_click=lambda e: confirmar_quantidade(e))]
        )
        e.page.dialog = dialog_quantidade
        dialog_quantidade.open = True
        e.page.update()
    
    def abrir_dialog_mais_produtos(e, dados_os):
        # Dialog perguntando se há mais produtos nesse endereço
        def on_sim(e):
            e.page.dialog.open = False
            e.page.update()
            # Abre novamente o dialog para inserir o código de barras
            abrir_dialog_codbarra(e, dados_os)
        def on_nao(e):
            e.page.dialog.open = False
            e.page.update()
            # Chama a função finalizar
            finalizar(e, dados_os)
        dialog_mais = ft.AlertDialog(
            title=ft.Text("Tem mais algum produto nesse endereço?"),
            actions=[
                ft.TextButton("Sim", on_click=lambda e: on_sim(e)),
                ft.TextButton("Não", on_click=lambda e: on_nao(e))
            ]
        )
        e.page.dialog = dialog_mais
        dialog_mais.open = True
        e.page.update()
    
    def finalizar(e, dados_os):
        # Espaço para a requisição de finalização
        response = requests.post(
            f"{base_url}/contagem_inventario",
            json={
                "dados_os": dados_os,
                "matricula": matricula,
                "codfilial": codfilial,
                "action": "finalizar_contagem"
                # Adicione outros parâmetros conforme necessário
            }
        )
        if response.status_code == 200:
            dados = response.json()
            mensagem = dados.get("mensagem")
            e.page.snack_bar = ft.SnackBar(ft.Text(mensagem), bgcolor=colorVariaveis['sucesso'])
            e.page.snack_bar.open = True
            navigate_to("/contagem_inventario")
            e.page.update()
            
        else:
            dados = response.json()
            mensagem = dados.get("mensagem")
            e.page.snack_bar = ft.SnackBar(ft.Text(mensagem), bgcolor=colorVariaveis['erro'])
            e.page.snack_bar.open = True
            e.page.update()
    
    def abrir_dialog_codbarra_nao_cadastrado(e):
        # Dialog para código de barras não cadastrado
        dialog_nao_cadastrado = ft.AlertDialog(
            title=ft.Text("Código de Barras não cadastrado"),
            actions=[ft.TextButton("Cadastrar", on_click=lambda e: navigate_to("/cadastrar_codbarra"))]
        )
        e.page.dialog = dialog_nao_cadastrado
        dialog_nao_cadastrado.open = True
        e.page.update()
    
    def buscar_os(e, codfilial, matricula):
        try:
            response = requests.post(
                f"{base_url}/contagem_inventario",
                json={"codfilial": codfilial, "matricula": matricula}
            )
            if response.status_code in [200, 202]:
                dados = response.json()
                dados_os = dados.get("dados_os", [])
                mostrar_campos_endereco(e, dados_os)
            else:
                print("Erro ao buscar OS")
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
        controls=[header, title, conteudo_dinamico]
    )
