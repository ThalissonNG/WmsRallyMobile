import flet as ft
import requests
from routes.config.config import base_url, user_info, colorVariaveis

def enderecar_produto(page: ft.Page, navigate_to, header, arguments):
    codprod = arguments.get("codprod", "N/A")
    codfab = arguments.get("codfab", "N/A")
    descricao = arguments.get("descricao", "N/A")
    qt = int(arguments.get("qt", 0))
    numbonus = arguments.get("numbonus", "N/A")
    classevenda = arguments.get("classevenda", "N/A")
    codetiqueta = arguments.get("codetiqueta", "N/A")
    matricula = user_info.get("matricula", "N/A")
    codfilial = user_info.get("codfilial", "N/A")

    container_endereco = ft.Container(
        content=ft.Column(
            controls=[
            ]
        )
    )

    print(f"Bônus: {numbonus} - Produto: {codprod} - Codfab: {codfab} - Descricao: {descricao} - Quantidade: {qt}")
    print(f"Informações do arquivo config: Matricula: {matricula} - codfilial: {codfilial}")

    
    def guardar_produto(page, codendereco, numbonus):
        try:
            response = requests.post(
                f"{base_url}/guardarProduto",
                json={
                    "codendereco": codendereco,
                    "matricula": matricula,
                    "codfilial": codfilial,
                    "numbonus": numbonus,
                    "codetiqueta": codetiqueta,
                    "codprod": codprod,
                    "qt": qt,
                }
            )

            if response.status_code == 200:
                print("Produto guardado com sucesso")
                snackbar_sucess = ft.SnackBar(
                    content=ft.Text("Produto guardado com sucesso"),
                    bgcolor=ft.Colors.GREEN,
                    show_close_icon=True,
                    duration=1000,
                )
                # page.overlay.append(snackbar_sucess)
                # snackbar_sucess.open = True
                page.open(snackbar_sucess)
                page.update()
                navigate_to("/armazenar_bonus")
                
            elif response.status_code == 400 or response.status_code == 500:
                resposta = response.json()
                mensagem = resposta.get("mensagem")
                print(f"Erro: {mensagem}")
                snackbar_sucess = ft.SnackBar(
                    content=ft.Text(mensagem, color="white"),
                    # bgcolor=ft.Colors,
                    show_close_icon=True,
                    duration=1000,
                )
                page.overlay.append(snackbar_sucess)
                snackbar_sucess.open = True
                page.update()

                page.update()
        except Exception as e:
            print(e)

    def consultar_endereco(codprod, codfilial):
        codprod = str(codprod)
        response = requests.post(
            f"{base_url}/consultarProdutoEndereco",
            json={
                "codbarra": codprod,
                "codfilial": codfilial
            },
        )

        if response.status_code == 200:
            dados_endereco = response.json()
            enderecos = dados_endereco.get("dados_produto_filial", [])

            container_endereco.content.controls.clear()
            
            for enderecos in enderecos:
                container_endereco.content.controls.extend(
                    construir_enderecos(enderecos)
                )

            page.update()
            return dados_endereco

    def construir_enderecos(dados_endereco):
        mod = dados_endereco[4]
        rua = dados_endereco[5]
        edf = dados_endereco[6]
        nivel = dados_endereco[7]
        apto = dados_endereco[8]
        qt_endereco = dados_endereco[2]

        return [
            ft.Text(
                "Endereço:",
                size=18,
                weight="bold",
            ),
            ft.Row(
                controls=[
                    ft.Text(f"Mod: {mod}"),
                    ft.Text(f"Rua: {rua}"),
                    ft.Text(f"Edf: {edf}"),
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            ft.Row(
                controls=[
                    ft.Text(f"Nivel: {nivel}"),
                    ft.Text(f"Apto: {apto}"),
                    ft.Text(f"Qt Endereço: {qt_endereco}")
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            ft.Divider()
        ]

    consultar_endereco(codprod, codfilial)
    # print(dados_endereco1)

    codendereco = ft.TextField(
        label="CODENDERECO",
        # prefix_icon=ft.icons.STORAGE,
        border_radius=ft.border_radius.all(10),
        border_color=colorVariaveis['bordarInput'],
        border_width=2,
    )
    numbonus_container = ft.Container(
        content=ft.Text(
            f"Número do bônus: {numbonus}",
            size=16,
            text_align="left",
        ),
        padding=10,
        alignment=ft.alignment.center_left,
    )
    infosProduto = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text(
                                    "CODPROD:",
                                    weight="bold",
                                ),
                                ft.Text(codprod),
                            ],
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(
                                    "CODFAB:",
                                    weight="bold",
                                ),
                                ft.Text(codfab),
                            ],
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(
                                    "QT:",
                                    weight="bold",
                                ),
                                ft.Text(qt),
                            ],
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(
                                    "CLASSE:",
                                    weight="bold",
                                ),
                                ft.Text(classevenda),
                            ],
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_AROUND
                ),
                ft.Divider(),
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text(
                                    "DESCRIÇÃO:",
                                    weight="bold",
                                ),
                                ft.Text(descricao),
                            ],
                            expand=True,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Divider(),
            ],
        ),
        padding=10,
        expand=True,
    )
    buttonGuardar = ft.ElevatedButton(
        text="Guardar",
        bgcolor=colorVariaveis['botaoAcao'],
        color=colorVariaveis['texto'],
        on_click=lambda e: guardar_produto(
            e.page,
            codendereco.value,
            numbonus,
            ) 
    )
    

    return ft.View(
        route="/enderecarBonus",
        controls=[
            header,
            ft.Container(height=10),
            ft.Container(
                content=ft.Column(
                    controls=[
                        numbonus_container,
                        infosProduto,
                        codendereco,
                        buttonGuardar,
                        container_endereco
                    ],
                )
            ),
        ],
        scroll="always",
    )