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

        # Cria o campo de texto para o endereço e guarda a referência
        campo_endereco = ft.TextField(label="Endereço")

        # Função para fechar o dialog
        def fechar_dialog(e):
            e.page.dialog.open = False
            e.page.update()

        # Função para confirmar e validar o endereço
        def confirmar_endereco(e):
            campo_codbarra = ft.TextField(label="Código de Barras")
            # Considerando que o código esperado está na posição 3 do primeiro item de dados_os
            codigo_esperado = str(dados_os[0][2])
            if campo_endereco.value == codigo_esperado:
                # Se estiver correto, cria um dialog informando sucesso
                dialog = ft.AlertDialog(
                    title=ft.Text("Sucesso"),
                    content=ft.Column(
                        [
                            ft.Text(f"Endereço: {campo_endereco.value}"),
                            campo_codbarra
                        ]
                    ),    
                    actions=[
                        ft.TextButton("Cancelar", on_click=fechar_dialog),
                        ft.TextButton("OK", lambda e: print("Código de barras:", campo_codbarra.value)) 
                    ]
                )
                e.page.dialog = dialog
                dialog.open = True
                e.page.update()
            else:
                # Se estiver incorreto, mostra um snackbar com a mensagem
                e.page.snack_bar = ft.SnackBar(ft.Text("Endereço incorreto"))
                e.page.snack_bar.open = True
                e.page.update()

        # Adiciona os controles à tela, incluindo os textos, o campo de entrada e o botão de confirmação
        conteudo_dinamico.controls.append(
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(f"Nº Inventário: {dados_os[0][0]}"),
                        ft.Text(f"Nº OS: {dados_os[0][1]}"),
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
