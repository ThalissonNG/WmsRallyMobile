import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def conferir_bonus(page, navigate_to, header, arguments):
    matricula = user_info.get("matricula")
    codfilial = user_info.get("codfilial")
    numbonus = arguments.get("numbonus", "N/A")

    dados_bonus = []
    print(f"Tela de conferir bonusMatricula: {matricula} - Codfilial: {codfilial} - Numbonus: {numbonus}")

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
                json={"numbonus": numbonus},
            )

            if response.status_code == 200:
                resposta = response.json()
                itens_bonus = resposta.get("itens_bonus")
                itens_bonus_etiqueta = resposta.get("itens_bonus_etiqueta")
                dados_bonus.append(itens_bonus)
                dados_bonus.append(itens_bonus_etiqueta)
                return dados_bonus
            else:
                resposta = response.json()
                mensagem = resposta.get("message")
                snackbar(mensagem, colorVariaveis['erro'], page)
        except Exception as exc:
            print("Erro na requisição (buscarItens):", exc)

    dados_bonus = buscar_dados_bonus(numbonus)
    itens_bonus = dados_bonus[0]
    itens_bonus_etiqueta = dados_bonus[1]

    # print(f"Itens: {itens_bonus} - Itens Etiqueta: {itens_bonus_etiqueta}")

    def construir_itens(item):
        return ft.Container(
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
                                    ft.Text("codprod", weight="bold"),
                                    ft.Text(str(item[2])),
                                ]
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text("codfab", weight="bold"),
                                    ft.Text(str(item[3])),
                                ]
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text("qt", weight="bold"),
                                    ft.Text(str(item[5])),
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
                                    ft.Text("descricao", weight="bold"),
                                    ft.Text(
                                        str(item[4]),
                                        no_wrap=False,
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
    # desenha apenas um bloco para um único item
        return ft.Container(
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
                                    ft.Text("codprod", weight="bold"),
                                    ft.Text(str(item[0])),
                                ]
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text("codfab", weight="bold"),
                                    ft.Text(str(item[1])),
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
                                    ft.Text("descrição", weight="bold"),
                                    ft.Text(
                                        item[2],
                                        no_wrap=False,
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
                                    ft.Text("Etiqueta", weight="bold"),
                                    ft.Text(str(item[6])),
                                ]
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text("Qt", weight="bold"),
                                    ft.Text(str(item[3])),
                                ]
                            ),
                            ft.Column(
                                controls=[
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT,
                                        padding=10
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
                dialogo_codbarra()
            else:
                resposta = response.json()
                mensagem = resposta.get("message")
                print(mensagem)
                snackbar(mensagem, colorVariaveis['erro'], page)
        except Exception as exc:
            print("Erro na requisição (validarEtiqueta):", exc)

    def dialogo_codbarra():
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
                ),
            ]
        )
        page.open(dialog_codbarra)
        page.update()

    tabItens = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            # para cada item em itens_bonus, gera um Container via construir_itens()
            *[construir_itens(item) for item in itens_bonus]
        ],
    )

    tabResumo = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            # para cada item em itens_bonus, gera um Container via construir_resumo()
            *[construir_resumo(item) for item in itens_bonus_etiqueta]
        ],
    )

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
            ft.Tab(text="Itens", content=tabItens),
            ft.Tab(text="Resumo", content=tabResumo,),
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