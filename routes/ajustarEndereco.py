import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def ajustar_endereco(page: ft.Page, navigate_to, header):
    matricula = user_info.get("matricula")
    codfilial = user_info.get("codfilial")

    def snack_bar(mensagem, bgcolor, color, page):
        snack = ft.SnackBar(
            content=ft.Text(
                mensagem,
                color="white"
            ),
            bgcolor=bgcolor
        )
        page.open(snack)

    def validar_endereco(codendereco, codfilial):
        response = requests.get(
            f"{base_url}/ajustar_endereco/{codendereco}",
        )
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.json()}")

        if response.status_code == 200:
            dados_endereco = response.json().get("dados_endereco", [])
            container_principal.content = construir_container(dados_endereco)
            page.update()

            snack_bar("Endereço ajustado com sucesso!", colorVariaveis['sucesso'], colorVariaveis['textoPreto'], page)
        else:
            mensagem = response.json().get("message")
            snack_bar(mensagem, colorVariaveis['erro'], colorVariaveis['texto'], page)

    def atualizar_dados(codendereco, codprod, capacidade, reposicao, validade, qt):
        response = requests.put(
            f"{base_url}/ajustar_endereco/{codendereco}",
            json={
                "codprod": codprod,
                "qt": qt,
                "capacidade": capacidade,
                "reposicao": reposicao,
                "validade": validade
            }
        )
        print(f"Status code: {response.status_code}")
        resposta = response.json()
        mensagem = resposta.get("message")

        if response.status_code == 200:
            snack_bar(mensagem, colorVariaveis['sucesso'], colorVariaveis['textoPreto'], page)
        else:
            snack_bar(mensagem, colorVariaveis['erro'], colorVariaveis['texto'], page)

    # Dialog controls para exibir/editar (sem salvar por enquanto)
    info_produto_text = ft.Text("")
    codprod_text = ft.Text("")
    codendereco_txt = ft.Text("")
    tf_capacidade = ft.TextField(label="Capacidade")
    tf_validade = ft.TextField(label="Validade")
    tf_reposicao = ft.TextField(label="Reposicao")
    tf_quantidade = ft.TextField(label="Quantidade")

    editar_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Ajustar Endereco"),
        content=ft.Column(
            tight=True,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                info_produto_text,
                codprod_text,
                # codendereco_txt,
                tf_capacidade,
                tf_validade,
                tf_reposicao,
                tf_quantidade,
            ],
        ),
        actions=[
            ft.TextButton(
                "Salvar",
                on_click=lambda e: atualizar_dados(codendereco_txt.value, codprod_text.value, tf_capacidade.value, tf_reposicao.value, tf_validade.value, tf_quantidade.value),
            ),
            ft.TextButton("Fechar", on_click=lambda e: fechar_dialog()),
        ],
    )

    def abrir_dialog(codprod, codfab, descricao, qt, capacidade, reposicao, validade, codendereco):
        print("Clicou para abrir")
        info_produto_text.value = f"{descricao}"
        codprod_text.value = f"Codprod: {codprod}"
        codendereco_txt.value = f"{codendereco}"
        tf_capacidade.value = str(capacidade) if capacidade is not None else ""
        tf_validade.value = str(validade) if validade is not None else ""
        tf_reposicao.value = str(reposicao) if reposicao is not None else ""
        tf_quantidade.value = str(qt) if qt is not None else ""

        page.update()
        page.open(editar_dialog)

    def fechar_dialog():
        page.close(editar_dialog)

    def construir_container(lista_enderecos):
        cards = []

        for linha in lista_enderecos:
            codprod, codfab, descricao, qt, tipoendereco, capacidade, reposicao, validade, codendereco = linha
            
            card = ft.Container(
                padding=10,
                border=ft.border.all(1, ft.Colors.GREY_400),
                border_radius=8,
                margin=ft.margin.symmetric(vertical=4, horizontal=6),
                content=ft.Column(
                    spacing=4,
                    controls=[
                        ft.Text(descricao, weight="bold", size=14),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(f"Codprod: {codprod}", size=12),
                                ft.Text(f"Codfab: {codfab}", size=12),
                            ]
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(f"Qt: {qt}", size=12, weight="bold"),
                                ft.Text(f"Validade: {validade}", size=12),
                            ]
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(f"Capacidade: {capacidade}", size=12),
                                ft.Text(f"Reposição: {reposicao}", size=12,),
                            ]
                        ),
                        ft.Container(height=10),
                        ft.Button(
                            text="Ajustar Endereço",
                            icon=ft.Icons.EDIT,                            bgcolor=colorVariaveis['botaoAcao'],
                            color=colorVariaveis['texto'],
                            on_click=(
                                lambda e, codprod=codprod, codfab=codfab, descricao=descricao, qt=qt, capacidade=capacidade, reposicao=reposicao, validade=validade, codendereco=codendereco: abrir_dialog(codprod, codfab, descricao, qt, capacidade, reposicao, validade, codendereco)
                            ),
                        )
                    ]
                )
            )
            cards.append(card)

        return ft.Column(controls=cards, spacing=10, expand=True, scroll=ft.ScrollMode.AUTO)

    titulo = ft.Text(
        "Ajustar Endereço",
        size=24,
        weight="bold",
        color=colorVariaveis['titulo']
    )
    input_codendereco = ft.TextField(
        label="Código Endereço",
        autofocus=True,
        keyboard_type=ft.KeyboardType.NUMBER,
        on_submit=lambda e: validar_endereco(input_codendereco.value, codfilial)
    )
    buscar_endereco = ft.ElevatedButton(
        "Buscar Endereço",
        bgcolor=colorVariaveis['botaoAcao'],
        color=colorVariaveis['texto'],
        on_click=lambda e: validar_endereco(input_codendereco.value, codfilial)
    )
    container_principal = ft.Container(
        expand=True,
        margin=ft.margin.symmetric(vertical=4, horizontal=6),
        content=ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO
        )
    )
    return ft.View(
        route="/ajustar_endereco",
        controls=[
            header,
            ft.Column(
                expand=True,
                controls=[
                    titulo,
                    ft.Container(height=20),
                    input_codendereco,
                    buscar_endereco,
                    ft.Divider(),
                    container_principal
                ]
            )
        ]
    )
