import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def contagem_inventario(e, navigate_to, header):
    matricula = user_info.get('matricula')
    codfilial = user_info.get('codfilial')
    
    # Container principal e container de resumo
    conteudo_dinamico = ft.Column()
    resumo_container = ft.Column(controls=[ft.Text("Resumo de Contagem:")])
    
    def atualizar_resumo(e, dados_os):
        """Faz uma requisição para o endpoint /resumo_contagem e atualiza o container de resumo."""
        try:
            response = requests.post(
                f"{base_url}/resumo_contagem",
                json={
                    "dados_os": dados_os
                }
            )
            if response.status_code == 200:
                resumo = response.json().get("resumo", [])
                resumo_container.controls.clear()
                resumo_container.controls.append(ft.Text("Resumo de Contagem:"))
                for item in resumo:
                    # Supondo que cada item tem o formato [codprod, descrição, codfab, quantidade]
                    texto_item = f"Produto: {item[0]} | Descrição: {item[1]} | CodFab: {item[2]} | Quantidade: {item[3]}"
                    resumo_container.controls.append(ft.Text(texto_item))
                e.page.update()
            else:
                print("Erro ao buscar resumo:", response.status_code)
        except Exception as exc:
            print("Erro ao atualizar resumo:", exc)
    
    def mostrar_campos_endereco(e, dados_os):
        conteudo_dinamico.controls.clear()
    
        campo_endereco = ft.TextField(label="Endereço")
    
        def confirmar_endereco(e):
            codigo_esperado = str(dados_os[0][2])
            if campo_endereco.value == codigo_esperado:
                abrir_dialog_codbarra(e, dados_os)
            else:
                e.page.snack_bar = ft.SnackBar(ft.Text("Endereço incorreto"))
                e.page.snack_bar.open = True
                e.page.update()
    
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
        # Adiciona o container de resumo à tela
        conteudo_dinamico.controls.append(resumo_container)
        e.page.update()
    
    def abrir_dialog_codbarra(e, dados_os):
        campo_codbarra = ft.TextField(label="Código de Barras")
        
        def confirmar_codbarra(e, codbarra):
            response = requests.post(
                f"{base_url}/contagem_inventario",
                json={
                    "codbarra": codbarra,
                    "matricula": matricula,
                    "codfilial": codfilial,
                    "dados_os": dados_os,
                    "action": "validar_codbarra"
                }
            )
            if response.status_code == 200:
                print("Código de barras válido")
                dados = response.json()
                produto = dados.get("produto")  # Ex.: [[codprod, descrição, codfab, None]]
                abrir_dialog_quantidade(e, codbarra, dados_os, produto)
            elif response.status_code == 500:
                print("Código de barras não cadastrado")
                abrir_dialog_codbarra_nao_cadastrado(e)
            else:
                print("Resposta inesperada:", response.status_code)
            # e.page.dialog.open = False
            # e.page.update()
        
        dialog_codbarra = ft.AlertDialog(
            title=ft.Text("Inserir Código de Barras"),
            content=ft.Column(controls=[campo_codbarra]),
            actions=[ft.TextButton("Confirmar", on_click=lambda e: confirmar_codbarra(e, campo_codbarra.value))]
        )
        e.page.dialog = dialog_codbarra
        dialog_codbarra.open = True
        e.page.update()
    
    def abrir_dialog_quantidade(e, codbarra, dados_os, produto):
        campo_quantidade = ft.TextField(label="Quantidade")
        
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
                e.page.snack_bar = ft.SnackBar(ft.Text(mensagem), bgcolor=colorVariaveis['sucesso'])
                e.page.snack_bar.open = True
                e.page.update()
                # Após confirmar a quantidade, atualiza o resumo fazendo uma nova requisição
                atualizar_resumo(e, dados_os)
                abrir_dialog_mais_produtos(e, dados_os)
            else:
                dados = response.json()
                mensagem = dados.get("mensagem")
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
                    ft.Text(f"DESCRIÇÃO: {produto[0][1]}"),
                    ft.Text(f"CODFAB: {produto[0][2]}"),
                    campo_quantidade
                ]
            ),
            actions=[ft.TextButton("Confirmar", on_click=lambda e: confirmar_quantidade(e))]
        )
        e.page.dialog = dialog_quantidade
        dialog_quantidade.open = True
        e.page.update()
    
    def abrir_dialog_mais_produtos(e, dados_os):
        def on_sim(e):
            e.page.dialog.open = False
            e.page.update()
            abrir_dialog_codbarra(e, dados_os)
        def on_nao(e):
            e.page.dialog.open = False
            e.page.update()
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
        response = requests.post(
            f"{base_url}/contagem_inventario",
            json={
                "dados_os": dados_os,
                "matricula": matricula,
                "codfilial": codfilial,
                "action": "finalizar_contagem"
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
                atualizar_resumo(e, dados_os)
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
