import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def conferir_bonus(page, navigate_to, header, arguments):
    matricula = user_info.get("matricula")
    codfilial = user_info.get("codfilial")
    numbonus = arguments.get("numbonus", "N/A")

    # dados_bonus = []
    print(f"Tela de conferir bonusMatricula: {matricula} - Codfilial: {codfilial} - Numbonus: {numbonus}")

    tab_itens_container = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO, controls=[])
    tab_resumo_container = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO, controls=[])

    def snackbar(mensagem, bgcolor, page):
        snack = ft.SnackBar(
            content=ft.Text(
                mensagem,
                color="white"
            ),
            bgcolor=bgcolor)
        page.open(snack)

    def buscar_dados_bonus(numbonus):
        try:
            response = requests.post(
                f"{base_url}/conferir_bonus",
                json={
                    "numbonus": numbonus,
                    "action": "buscar_itens"
                },
            )

            if response.status_code == 200:
                resposta = response.json()
                itens_bonus = resposta.get("itens_bonus")
                itens_bonus_etiqueta = resposta.get("itens_bonus_etiqueta")
                return itens_bonus, itens_bonus_etiqueta
            else:
                resposta = response.json()
                mensagem = resposta.get("message")
                snackbar(mensagem, colorVariaveis['erro'], page)
        except Exception as exc:
            print("Erro na requisição (buscarItens):", exc)

    def atualizar_tabs():
        print("Atualizando tabs")
        itens, resumo = buscar_dados_bonus(numbonus)
        # print(f"resumo: {resumo}")
        # Atualiza aba Itens
        tab_itens_container.controls.clear()
        tab_itens_container.controls = [construir_itens(item) for item in itens]
        # Atualiza aba Resumo
        tab_resumo_container.controls.clear()
        tab_resumo_container.controls = [construir_resumo(item) for item in resumo]
        page.update()

    def construir_itens(item):
        if item[6] == 0:
            corfundo = None
            cortexto = None
        elif item[6] ==item[5]:
            corfundo = colorVariaveis['sucesso']
            cortexto = ft.Colors.BLACK
        elif item[6] < item[5]:
            corfundo = colorVariaveis['restante']
            cortexto = ft.Colors.BLACK
        elif item[6] > item[5]:
            corfundo = colorVariaveis['erro']
            cortexto = ft.Colors.WHITE
        return ft.Container(
            bgcolor=corfundo,
            padding=10,
            expand=True,
            content=ft.Column(
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text("codprod", weight="bold", color=cortexto),
                                    ft.Text(str(item[2]), color=cortexto),
                                ]
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text("codfab", weight="bold", color=cortexto),
                                    ft.Text(str(item[3]), color=cortexto),
                                ]
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text("qt", weight="bold", color=cortexto),
                                    ft.Text(str(item[5]), color=cortexto),
                                ]
                            ),
                        ]
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Column(
                                expand=True,
                                controls=[
                                    ft.Text("descricao", weight="bold", color=cortexto),
                                    ft.Text(
                                        str(item[4]),
                                        no_wrap=False,
                                        color=cortexto
                                    ),
                                ]
                            ),
                        ]
                    ),
                    ft.Divider()
                ]
            )
        )

    def construir_resumo(item):
        if item[5] ==item[4]:
            corfundo = colorVariaveis['sucesso']
            cortexto = ft.Colors.BLACK
        elif item[5] < item[4]:
            corfundo = colorVariaveis['restante']
            cortexto = ft.Colors.BLACK
        elif item[5] > item[4]:
            corfundo = colorVariaveis['erro']
            cortexto = ft.Colors.WHITE
        else:
            corfundo = ft.Colors.WHITE
            cortexto = ft.Colors.BLACK
    
        def dialogo_editar(page, codprod, codfab, descricao, numbonus, qt, codetiqueta):
            print(f"dialogo_editar - Codprod: {codprod} - Codfab: {codfab} - Descricao: {descricao} - Qt: {qt} - Bônus: {numbonus} - Etiqueta: {codetiqueta}")
            campo_editar_qt = ft.TextField(
                label="Nova Quantidade",
                value=str(qt),
            )
            dialog_editar_qt = ft.AlertDialog(
                title=ft.Text("Editar Quantidade"),
                content=ft.Column(
                    controls=[
                        ft.Text(f"Produto: {descricao}", weight="bold"),
                        ft.Text(f"Codprod: {codprod}"),
                        ft.Text(f"Codfab: {codfab}"),
                        ft.Text(f"Etiqueta: {codetiqueta}"),
                        campo_editar_qt,
                    ],
                    expand=True,
                    height="100%",
                    tight=True,
                    scroll=ft.ScrollMode.AUTO
                ),
                actions=[
                    ft.TextButton("Cancelar", on_click=lambda _: page.close(dialog_editar_qt)),
                    ft.TextButton("Salvar", on_click=lambda _: (
                        print("Salvar nova quantidade", campo_editar_qt.value),
                        page.close(dialog_editar_qt)
                    ))
                ]
            )
            page.open(dialog_editar_qt)
            page.update()

    # desenha apenas um bloco para um único item
        return ft.Container(
            bgcolor=corfundo,
            padding=10,
            expand=True,
            content=ft.Column(
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text("codprod", weight="bold", color=cortexto),
                                    ft.Text(str(item[0]), color=cortexto),
                                ]
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text("codfab", weight="bold", color=cortexto),
                                    ft.Text(str(item[1]), color=cortexto),
                                ]
                            ),
                        ]
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Column(
                                expand=True,
                                controls=[
                                    ft.Text("descrição", weight="bold", color=cortexto),
                                    ft.Text(
                                        item[2],
                                        no_wrap=False,
                                        color=cortexto
                                    ),
                                ]
                            ),
                        ]
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text("Etiqueta", weight="bold", color=cortexto),
                                    ft.Text(str(item[6]), color=cortexto),
                                ]
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text("Qt", weight="bold", color=cortexto),
                                    ft.Text(str(item[3]), color=cortexto),
                                ]
                            ),
                            ft.Column(
                                controls=[
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT,
                                        padding=10,
                                        icon_color=cortexto,
                                        on_click=lambda ev: dialogo_editar(page, item[0], item[1], item[2], numbonus, item[3], item[6])
                                    )
                                ]
                            ),
                        ]
                    ),
                    ft.Divider()
                ],
            )
        )

    def ValidarEtiqueta(codetiqueta, page):
        if not codetiqueta:
            snackbar("Etiqueta inválida!", colorVariaveis['erro'], page)
            return

        try:
            response = requests.post(
                f"{base_url}/conferir_bonus",
                json={
                    "codetiqueta": codetiqueta,
                    "action": "validar_etiqueta",
                },
            )
            if response.status_code == 200:
                resposta = response.json()
                dialogo_codbarra(page, codetiqueta)
            else:
                resposta = response.json()
                mensagem = resposta.get("message")
                print(mensagem)
                snackbar(mensagem, colorVariaveis['erro'], page)
        except Exception as exc:
            print("Erro na requisição (validarEtiqueta):", exc)

    def ValidarCodbarra(codbarra, codetiqueta, page):
        if not codbarra:
            snackbar("Código de Barras inválido!", colorVariaveis['erro'], page)
            return
        
        try:
            response = requests.post(
                f"{base_url}/conferir_bonus",
                json={
                    "codbarra": codbarra,
                    "action": "validar_codbarra",
                }
            )
            if response.status_code == 200:
                resposta = response.json()
                dados_codbarra = resposta.get("dados_codbarra")
                print(dados_codbarra)
                dialogo_produto(page, codetiqueta, dados_codbarra)
            else:
                resposta = response.json()
                mensagem = resposta.get("message")
                print(mensagem)
                snackbar(mensagem, colorVariaveis['erro'], page)
        except Exception as exc:
            print("Erro na requisição (validarCodbarra):", exc)

    def ValidarQuantidade(codprod, codetiqueta, numbonus, codbarra,  qt, page):
        if not qt:
            snackbar("Quantidade inválida!", colorVariaveis['erro'], page)
            return

        try:
            response = requests.post(
                f"{base_url}/conferir_bonus",
                json={
                    "codprod": codprod,
                    "qt": qt,
                    "numbonus": numbonus,
                    "codetiqueta": codetiqueta,
                    "codbarra": codbarra,
                    "action": "validar_quantidade",
                }
            )
            if response.status_code == 200:
                resposta = response.json()
                atualizar_tabs()
                # guardar_produto(page, codetiqueta, qt)
            else:
                resposta = response.json()
                mensagem = resposta.get("message")
                print(mensagem)
                snackbar(mensagem, colorVariaveis['erro'], page)
        except Exception as exc:
            print("Erro na requisição (validarQuantidade):", exc)

    def dialogo_codbarra(page, codetiqueta):
        campo_codbarra = ft.TextField(
            label="Código de Barras"
        )

        dialog_codbarra = ft.AlertDialog(
            title=ft.Text("Inserir Código de Barras"),
            content=campo_codbarra,
            actions=[
                ft.TextButton(
                    "Cancelar",
                    on_click=lambda _: page.close(dialog_codbarra),
                ),
                ft.TextButton(
                    "Confirmar",
                    on_click=lambda _: ValidarCodbarra(campo_codbarra.value, codetiqueta, page),
                ),
            ]
        )
        page.open(dialog_codbarra)
        page.update()

    def dialogo_produto(page, codetiqueta, dados_codbarra):
        campo_qt = ft.TextField(
            label="Quantidade"
        )
        dialog_produto = ft.AlertDialog(
            title=ft.Text("Inserir Produto"),
            content=ft.Column(
                controls=[
                    ft.Text(f"Etiqueta: {codetiqueta}", weight="bold"),
                    ft.Text(f"NUmbonus: {numbonus}", weight="bold"),
                    ft.Text(f"Codprod: {dados_codbarra[0][0]}"),
                    ft.Text(f"Codfab: {dados_codbarra[0][2]}"),
                    ft.Text(f"Descrição: {dados_codbarra[0][1]}"),
                    campo_qt,
                ],
                tight=True,
                scroll=ft.ScrollMode.AUTO
            ),
            actions=[
                ft.TextButton(
                    "Cancelar",
                    on_click=lambda _: page.close(dialog_produto),
                ),
                ft.TextButton(
                    "Confirmar",
                    on_click=lambda e: (
                        ValidarQuantidade(
                            dados_codbarra[0][0],
                            codetiqueta,
                            numbonus,
                            dados_codbarra[0][3],
                            campo_qt.value,
                            page
                        ),
                        page.close(dialog_produto),
                        setattr(inputEtiqueta, "value", ""),
                        page.update(),
                        # atualizar_tabs()
                    )
                ),
            ]
        )
        page.open(dialog_produto)
        page.update()

    atualizar_tabs()

    titulo = ft.Text(
        "Conferir Bonus",
        size=24, weight="bold",
        color=colorVariaveis['titulo']
    )
    cabecalho = ft.Row(
        controls=[
            ft.Text(
                f"Número do bonus: {numbonus}",
                size=16, weight="bold"
            )
        ]
    )
    inputEtiqueta = ft.TextField(
        label="Etiqueta",
        border_radius=ft.border_radius.all(10),
        border_color=colorVariaveis['bordarInput'],
    )
    btnValidarEtiqueta = ft.ElevatedButton(
        text="Validar Etiqueta",
        on_click=lambda e: ValidarEtiqueta(inputEtiqueta.value, page)
    )

    tabConferir = ft.Container(
        padding=10,
        content=ft.Column(
            controls=[
                inputEtiqueta,
                btnValidarEtiqueta,
            ]
        )
    )

    tabFinalizar = ft.Container(
        padding=10,
        content=ft.Column(
            controls=[
                ft.ElevatedButton(
                    text="Finalizar",
                    on_click=lambda e: print("Finalizar")
                )
            ]
        )
    )

    tabs = ft.Tabs(
        expand=True,
        width="100%",
        height="100%",
        selected_index=0,
        tabs=[
            ft.Tab(text="Conferir", content=tabConferir),
            ft.Tab(text="Itens", content=tab_itens_container,),
            ft.Tab(text="Resumo", content=tab_resumo_container,),
            ft.Tab(text="Finalizar", content=tabFinalizar),
        ]
    )


    return ft.View(
        route="/conferir_bonus",
        controls=[
            header,
            titulo,
            cabecalho,
            tabs
        ],
    )