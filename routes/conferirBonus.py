import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def conferir_bonus(page, navigate_to, header, arguments):
    matricula = user_info.get("matricula")
    codfilial = user_info.get("codfilial")
    numbonus = arguments.get("numbonus", "N/A")
    print(f"Tela de conferir bonusMatricula: {matricula} - Codfilial: {codfilial} - Numbonus: {numbonus}")

    
    try:
        response = requests.post(
            f"{base_url}/conferir_bonus",
            json={"numbonus": numbonus},
        )

        if response.status_code == 200:
            resposta = response.json()
            itens_bonus = resposta.get("itens_bonus")
            itens_bonus_etiqueta = resposta.get("itens_bonus_etiqueta")
        else:
            resposta = response.json()
            mensagem = resposta.get("message")
            snackbar(mensagem, colorVariaveis['erro'], page)
    except Exception as exc:
        print("Erro na requisição (buscarItens):", exc)

    print(f"Itens: {itens_bonus} - Itens Etiqueta: {itens_bonus_etiqueta}")

    def snackbar(mensagem, bgcolor, page):
        snack = ft.SnackBar(
            content=ft.Text(
                mensagem,
                color="white"
            ),
            bgcolor=bgcolor)
        page.open(snack)

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

    # …e então, no lugar de um único `tabItens`, faça:

    tabResumo = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            # para cada item em itens_bonus, gera um Container via construir_resumo()
            *[construir_resumo(item) for item in itens_bonus_etiqueta]
        ],
    )


    def ValidarEtiqueta(codetiqueta, page):
        try:
            response = requests.post(
                f"{base_url}/conferir_bonus",
                json={"codetiqueta": codetiqueta},
            )
            if response.status_code == 200:
                resposta = response.json()
                mensagem = resposta.get("message")
                print(mensagem)
                snackbar(mensagem, colorVariaveis['sucesso'], page)
            elif response.status_code == 201:
                resposta = response.json()
                mensagem = resposta.get("message")
                print(mensagem)
                snackbar(mensagem, colorVariaveis['restante'], page)
        except Exception as exc:
            print("Erro na requisição (validarEtiqueta):", exc)


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
        on_click=lambda e: print(f"Etiqueta: {inputEtiqueta.value}")
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

    tabItens = ft.Container(
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
                                ft.Text(1200),
                            ]
                        ),
                        ft.Column(
                            controls=[
                                ft.Text("codfab", weight="bold"),
                                ft.Text(1200),
                            ]
                        ),
                        ft.Column(
                            controls=[
                                ft.Text("qt", weight="bold"),
                                ft.Text(1200),
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
                                    "CAMARA AR DIAN/TRASEIRA CG/TITAN/YBR SA -18 3.00 X 18 - LEVORIN",
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
    
    # tabResumo = ft.Container(
    #     padding=10,
    #     expand=True,
    #     content=ft.Column(
    #         expand=True,
    #         horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
    #         controls=[
    #             ft.Row(
    #                 alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    #                 controls=[
    #                     ft.Column(
    #                         controls=[
    #                             ft.Text("codprod", weight="bold"),
    #                             ft.Text(1200),
    #                         ]
    #                     ),
    #                     ft.Column(
    #                         controls=[
    #                             ft.Text("codfab", weight="bold"),
    #                             ft.Text(1200),
    #                         ]
    #                     ),
    #                 ]
    #             ),
    #             ft.Row(
    #                 alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    #                 controls=[
    #                     ft.Column(
    #                         expand=True,
    #                         controls=[
    #                             ft.Text("descricao", weight="bold"),
    #                             ft.Text(
    #                                 "CAMARA AR DIAN/TRASEIRA CG/TITAN/YBR SA -18 3.00 X 18 - LEVORIN",
    #                                 no_wrap=False,
    #                             ),
    #                         ]
    #                     ),
    #                 ]
    #             ),
    #             ft.Row(
    #                 alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    #                 controls=[
    #                     ft.Column(
    #                         controls=[
    #                             ft.Text("etiqueta", weight="bold"),
    #                             ft.Text(8080),
    #                         ]
    #                     ),
    #                     ft.Column(
    #                         controls=[
    #                             ft.Text("Qt", weight="bold"),
    #                             ft.Text(60),
    #                         ]
    #                     ),
    #                     ft.Column(
    #                         controls=[
    #                             ft.IconButton(
    #                                 icon=ft.Icons.EDIT,
    #                                 padding=10
    #                             )
    #                         ]
    #                     ),
    #                 ]
    #             ),
    #             ft.Divider()
    #         ]
    #     )
    # )

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