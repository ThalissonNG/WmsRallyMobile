import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def armazenar_etiqueta_v2(page: ft.Page, navigate_to, header, arguments):
    codfilial = user_info.get("codfilial")
    matricula = user_info.get("matricula")
    codetiqueta = arguments.get("codetiqueta")

    titulo = ft.Text(
        f"Armazenar Etiqueta {codetiqueta}",
        size=24, weight="bold",
        color=colorVariaveis['titulo']
    )
    container_produto = ft.Column(
        controls=[
            
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )
    container_endereco = ft.Column(
        controls=[
            
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )

    def snack_bar(mensagem, bgcolor, color, page):
        snack = ft.SnackBar(
            content=ft.Text(
                mensagem,
                color="white"
            ),
            bgcolor=bgcolor
        )
        page.open(snack)

    def buscar_dados(codetiqueta):
        try:
            response = requests.get(
                f"{base_url}/armazenar_etiqueta/{codetiqueta}",
                params={
                    "codfilial": codfilial
                }
            )
            resposta = response.json()
            if response.status_code == 200:
                dados_etiqueta = resposta.get("dados_etiqueta")
                dados_endereco = resposta.get("dados_endereco")

                if dados_etiqueta:
                    container_produto.controls.clear()
                    container_produto.controls.extend(construir_container_produto(dados_etiqueta))
                    
                    page.update()
                else:
                    mensagem = resposta.get("message")
                    snack_bar(mensagem, colorVariaveis['erro'], "white", page)
                    return None

                if dados_endereco:
                    container_endereco.controls.clear()
                    container_endereco.controls.append(ft.Text("Endereços", weight="bold"))
                    
                    for endereco in dados_endereco:
                        container_endereco.controls.extend(construir_container_endereco(endereco))
                    
                    page.update()
            else:
                mensagem = resposta.get("message")
                snack_bar(mensagem, colorVariaveis['erro'], "white", page)
                return None
        except Exception as e:
            print(f"Erro ao buscar dados: {e}")
            mensagem = "Erro ao buscar dados"
            snack_bar(mensagem, colorVariaveis['erro'], "white", page)
            return None

    def construir_container_produto(dados_etiqueta):
        codprod = dados_etiqueta[0]
        codfab = dados_etiqueta[1]
        descricao = dados_etiqueta[2]
        classe = dados_etiqueta[3]
        qtetiqueta = dados_etiqueta[4]
        numbonus = dados_etiqueta[5]

        input_codendereco = ft.TextField(
            label="Código do endereço",
            keyboard_type=ft.KeyboardType.NUMBER,
            autofocus=True,
            on_submit=lambda e: validar_endereco(input_codendereco.value, matricula, codprod, qtetiqueta, codetiqueta, numbonus),
        )
        btn_validar_endereco = ft.ElevatedButton(
            text="Validar Endereço",
            on_click=lambda e: validar_endereco(input_codendereco.value, matricula, codprod, qtetiqueta, codetiqueta, numbonus),
        )
        
    
        return [
            ft.Text(f"Bonus: {numbonus}", weight="bold" ),
            ft.Row(
                controls=[
                    ft.Text(f"Codprod: {codprod}"),
                    ft.Text(f"Codfab: {codfab}"),
                    ft.Text(f"Qt. Etiqueta: {qtetiqueta}", weight="bold"),
                    ft.Text(f"Classe: {classe}"),
                ],
                wrap=True
            ),
            ft.Text(f"Descrição: {descricao}"),
            input_codendereco,
            btn_validar_endereco
        ]

    def validar_endereco(codendereco, matricula, codprod, qt, codetiqueta, numbonus):
        if not codendereco:
            mensagem = "Código do endereço é obrigatório"
            snack_bar(mensagem, colorVariaveis['erro'], "white", page)
            return
        print(codendereco, matricula, codprod, qt, codetiqueta, numbonus)

        try:
            response = requests.post(
                f"{base_url}/armazenar_etiqueta/{codetiqueta}",
                json={
                    "codfilial": codfilial,
                    "matricula": matricula,
                    "codendereco": codendereco,
                    "codprod": codprod,
                    "qt": qt,
                    "numbonus": numbonus
                }
            )
            resposta = response.json()
            if response.status_code == 200:
                mensagem = resposta.get("message")
                snack_bar(mensagem, colorVariaveis['sucesso'], "white", page)
                navigate_to("/buscar_etiqueta_v2")
                return None

            else:
                mensagem = resposta.get("message")
                snack_bar(mensagem, colorVariaveis['erro'], "white", page)
                return None
        except Exception as e:
            print(f"Erro ao atualizar endereço: {e}")
            mensagem = "Erro ao atualizar endereço"
            snack_bar(mensagem, colorVariaveis['erro'], "white", page)
            return None

    def construir_container_endereco(dados_endereco):
        codendereco = dados_endereco[0]
        mod = dados_endereco[1]
        rua = dados_endereco[2]
        edi = dados_endereco[3]
        nivel = dados_endereco[4]
        apto = dados_endereco[5]
        tipo_endereco = dados_endereco[6]
        qt_endereco = dados_endereco[7]
        endereco = dados_endereco[9]

        return [
            ft.Container(
                content=ft.Column(
                    spacing=6,
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text(f"MOD: {mod}"),
                                ft.Text(f"Rua: {rua}"),
                                ft.Text(f"EDI: {edi}"),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.Row(
                            controls=[
                                ft.Text(f"Nível: {nivel}"),
                                ft.Text(f"APTO: {apto}"),
                                ft.Text(f"Qt. Endereço: {qt_endereco}"),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.Row(
                            controls=[
                                ft.Text(f"TipoEndereço: {tipo_endereco}"),
                                ft.Text(f"Endereço: {endereco}")
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.Divider(),
                    ],
                ),
                padding=10,
            )
        ]

    buscar_dados(codetiqueta)

    return ft.View(
        route="/armazenar_etiqueta_v2",
        controls=[
            header,
            titulo,
            container_produto,
            container_endereco
        ],
        scroll=ft.ScrollMode.AUTO,
        # expand=True
    )
