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
                # Endereço correto: abre o dialog para inserir apenas o código de barras
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
                    "action": "validar_codbarra",
                    "dados_os": dados_os
                }
            )
            if response.status_code == 200:
                print("Código de barras válido")
            else:
                print("Código de barras inválido")
            
            e.page.dialog.open = False
            e.page.update()
        
        dialog_codbarra = ft.AlertDialog(
            title=ft.Text("Inserir Código de Barras"),
            content=ft.Column(controls=[campo_codbarra]),
            actions=[ft.TextButton("Confirmar", on_click=lambda e: confirmar_codbarra(e, campo_codbarra.value))],
        )
        e.page.dialog = dialog_codbarra
        dialog_codbarra.open = True
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
