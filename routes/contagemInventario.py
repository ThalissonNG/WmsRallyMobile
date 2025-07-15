import flet as ft
import requests
import datetime
from routes.config.config import base_url, colorVariaveis, user_info

def contagem_inventario(e, navigate_to, header):
    matricula = user_info.get('matricula')
    codfilial = user_info.get('codfilial')
    
    # Container principal e container de resumo
    conteudo_dinamico = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        spacing=50,
        controls=[
            
        ]
    )
    resumo_container = ft.Column(
        controls=[
            ft.Text("Resumo de Contagem:")
        ]
    )
    
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
                    texto_item = ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Text(f"Codprod:  {item[0]}", weight="bold"),
                                    ft.Text(f"CodFab: {item[2]}"),
                                    ft.Text(f"Qt: {item[3]}", weight="bold")
                                ]   
                            ),
                            ft.Text("Descrição: " + item[1])
                        ]
                    )
                    # Cria uma linha com o texto e o botão de editar
                    row = ft.Column(
                        controls=[
                            # ft.Text(texto_item),
                            texto_item,
                            ft.TextButton(
                                icon=ft.Icons.EDIT,
                                text="Editar",
                                on_click=lambda e, item=item: editar_item(e, item, dados_os)
                            ),
                            ft.Divider()
                        ]
                    )
                    resumo_container.controls.append(row)
                finalizar_btn = ft.ElevatedButton(
                    text="Finalizar",
                    bgcolor=colorVariaveis['botaoAcao'],
                    color=colorVariaveis['texto'],
                    on_click=lambda e: finalizar(e, dados_os)
                )
                resumo_container.controls.append(finalizar_btn)
                e.page.update()
            else:
                print("Erro ao buscar resumo:", response.status_code)
        except Exception as exc:
            print("Erro ao atualizar resumo:", exc)
    
    def editar_item(e, item, dados_os):
        """Abre um diálogo para editar a quantidade de um item do resumo."""
        def apenas_numeros(valor: str) -> str:
            # Remove qualquer caractere que não seja dígito e limita a 8 caracteres.
            return "".join(filter(str.isdigit, valor))[:8]

        def validar_data(e):
            # Valida se o campo tem exatamente 8 caracteres (mínimo)
            if len(e.control.value) < 8:
                e.control.error_text = "Digite 8 dígitos (DDMMYYYY)"
            else:
                e.control.error_text = None
            e.control.update()
        
        novo_qt = ft.TextField(label="Nova Quantidade", value=str(item[3]))
        default_date = datetime.date.today() + datetime.timedelta(days=365)
        formatted_date = default_date.strftime("%d%m%Y")

        campo_validade = ft.TextField(
            label="Data de Validade (DDMMYYYY)",
            value=formatted_date,
            max_length=8,
            hint_text="Ex: 25062025",
            on_change=lambda e: (
                setattr(e.control, "value", apenas_numeros(e.control.value)),
                validar_data(e)
            ),
            on_blur=validar_data  # Validação extra quando o campo perde o foco.
        )
    
        def confirmar_edicao(e):
            # Realiza uma requisição para atualizar a quantidade (endpoint '/editar_contagem' é um exemplo)
            response = requests.post(
                f"{base_url}/contagem_inventario",
                json={
                    "codprod": item[0],
                    "nova_quantidade": novo_qt.value,
                    "dados_os": dados_os,
                    "validade": campo_validade.value,
                    "action": "editar_contagem"
                }
            )
            if response.status_code == 200:
                e.page.snack_bar = ft.SnackBar(ft.Text("Quantidade atualizada"), bgcolor=colorVariaveis['sucesso'])
                e.page.snack_bar.open = True
                dialog_edicao.open = False
                atualizar_resumo(e, dados_os)
            else:
                e.page.snack_bar = ft.SnackBar(ft.Text("Erro ao atualizar quantidade"), bgcolor=colorVariaveis['erro'])
                e.page.snack_bar.open = True
    
        dialog_edicao = ft.AlertDialog(
            title=ft.Text("Editar Quantidade"),
            content=ft.Column(
                controls=[
                    novo_qt,
                    campo_validade
            ]),
            actions=[ft.TextButton("Confirmar", on_click=lambda e: confirmar_edicao(e))]
        )
        e.page.open(dialog_edicao)
    def mostrar_campos_endereco(e, dados_os):
        conteudo_dinamico.controls.clear()
    
        campo_endereco = ft.TextField(label="Endereço")
    
        def confirmar_endereco(e):
            print("Endereço:", campo_endereco.value)
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
                        ft.Text(f"MOD: {dados_os[0][3]}, RUA: {dados_os[0][4]}, EDI: {dados_os[0][5]}, NIV: {dados_os[0][6]}, APT: {dados_os[0][7]}"),
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
                print("Resposta do servidor:", response.json())
                print(response.status_code)
                dados = response.json()
                produto = dados.get("produto")  # Ex.: [[codprod, descrição, codfab, None]]
                abrir_dialog_quantidade(e, codbarra, dados_os, produto)
            elif response.status_code == 500:
                print("Código de barras não cadastrado")
                abrir_dialog_codbarra_nao_cadastrado(e)
            else:
                print("Resposta inesperada:", response.status_code)
        
        dialog_codbarra = ft.AlertDialog(
            title=ft.Text("Inserir Código de Barras invent"),
            content=ft.Column(controls=[campo_codbarra]),
            actions=[ft.TextButton("Confirmar", on_click=lambda e: confirmar_codbarra(e, campo_codbarra.value))]
        )
        e.page.open(dialog_codbarra)
    
    def abrir_dialog_quantidade(e, codbarra, dados_os, produto):
        print("abrir dialog_quantidade")
        campo_quantidade = ft.TextField(label="Quantidade")
        def apenas_numeros(valor: str) -> str:
            # Remove qualquer caractere que não seja dígito e limita a 8 caracteres.
            return "".join(filter(str.isdigit, valor))[:8]

        def validar_data(e):
            # Valida se o campo tem exatamente 8 caracteres (mínimo)
            if len(e.control.value) < 8:
                e.control.error_text = "Digite 8 dígitos (DDMMYYYY)"
            else:
                e.control.error_text = None
            e.control.update()

        default_date = datetime.date.today() + datetime.timedelta(days=365)
        formatted_date = default_date.strftime("%d%m%Y")

        campo_validade = ft.TextField(
            label="Data de Validade (DDMMYYYY)",
            value=formatted_date,
            max_length=8,
            hint_text="Ex: 25062025",
            on_change=lambda e: (
                setattr(e.control, "value", apenas_numeros(e.control.value)),
                validar_data(e)
            ),
            on_blur=validar_data  # Validação extra quando o campo perde o foco.
        )
        
        def confirmar_quantidade(e):
            response = requests.post(
                f"{base_url}/contagem_inventario",
                json={
                    "codbarra": codbarra,
                    "quantidade": campo_quantidade.value,
                    "dados_os": dados_os,
                    "validade": campo_validade.value,
                    "action": "confirmar_quantidade"
                }
            )
            if response.status_code == 200:
                dados = response.json()
                mensagem = dados.get("mensagem")
                e.page.snack_bar = ft.SnackBar(ft.Text(mensagem), bgcolor=colorVariaveis['sucesso'])
                e.page.snack_bar.open = True
                e.page.update()
                atualizar_resumo(e, dados_os)
                abrir_dialog_mais_produtos(e, dados_os)
            else:
                dados = response.json()
                mensagem = dados.get("mensagem")
                e.page.snack_bar = ft.SnackBar(ft.Text(mensagem), bgcolor=colorVariaveis['erro'])
                e.page.snack_bar.open = True
                e.page.update()
        
        dialog_quantidade = ft.AlertDialog(
            title=ft.Text("Inserir Quantidade"),
            content=ft.Column(
                controls=[
                    ft.Text(f"CODPROD: {produto[0][0]}"),
                    ft.Text(f"DESCRIÇÃO: {produto[0][1]}"),
                    ft.Text(f"CODFAB: {produto[0][2]}"),
                    campo_quantidade,
                    campo_validade
                ]
            ),
            actions=[ft.TextButton("Confirmar", on_click=lambda e: confirmar_quantidade(e))]
        )
        e.page.open(dialog_quantidade)
    
    def abrir_dialog_mais_produtos(e, dados_os):
        def on_sim(evt):
            evt.page.close(dialog_mais)           # fecha este diálogo
            abrir_dialog_codbarra(evt, dados_os)  # segue para o próximo
        def on_nao(evt):
            evt.page.close(dialog_mais)           # fecha este diálogo
            # finalizar(evt, dados_os) 
        dialog_mais = ft.AlertDialog(
            title=ft.Text("Tem mais algum produto nesse endereço?"),
            actions=[
                ft.TextButton("Sim", on_click=lambda e: on_sim(e)),
                ft.TextButton("Não", on_click=lambda e: on_nao(e))
            ]
        )
        e.page.open(dialog_mais)
    
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
        e.page.open(dialog_nao_cadastrado)
    
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
        scroll=True,
        controls=[header, title, conteudo_dinamico]
    )
