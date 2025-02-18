import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def separar_pedido(e, navigate_to, header):
    matricula = user_info.get('matricula')
    dados_itens = []  # Inicializa a variável dados_itens

    try:
        response = requests.post(
            base_url + "/separarPedido",
            json={"matricula": matricula}
        )
        if response.status_code == 200:
            dados = response.json()
            print("Recebido com sucesso")
            dados_itens = dados.get("dados_itens", [])  # Atualiza dados_itens com a resposta da API
            print(dados_itens)
        else:
            print("Deu erro")
    except Exception as exc:
        print(f"Erro: {exc}")

    title = ft.Text(
        "Separar pedido",
        size=24,
        weight="bold",
        color=colorVariaveis['titulo']
    )

    inputCodendereco = ft.TextField(
        label="Bipar Endereço",
        prefix_icon=ft.icons.SCANNER,
        border_radius=ft.border_radius.all(10),
        border_color=colorVariaveis['bordarInput'],
        border_width=2,
        keyboard_type=ft.KeyboardType.NUMBER
    )

    botaoEndereco = ft.ElevatedButton(
        text="buscar",
        bgcolor=colorVariaveis['botaoAcao'],
        color=colorVariaveis['texto'],
        width=600,
    )

    tabsSeparar = ft.Container(
        padding=10,
        expand=True,
        content=ft.Column(
            controls=[
                ft.Column(
                    expand=True,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Text(
                                    "Vá ao endereço:",
                                    weight="bold",
                                    size=20,
                                )
                            ]
                        ),
                        ft.Divider(),
                        ft.Row(
                            expand=True,
                            alignment=ft.MainAxisAlignment.SPACE_AROUND,
                            controls=[
                                ft.Column(
                                    controls=[
                                        ft.Text(
                                            "Mod",
                                            weight="bold"
                                        ),
                                        ft.Text("1")
                                    ]
                                ),
                                ft.Column(
                                    controls=[
                                        ft.Text(
                                            "Rua",
                                            weight="bold"
                                        ),
                                        ft.Text("3")
                                    ]
                                ),
                                ft.Column(
                                    controls=[
                                        ft.Text(
                                            "Edf",
                                            weight="bold"
                                        ),
                                        ft.Text("22")
                                    ]
                                ),
                                ft.Column(
                                    controls=[
                                        ft.Text(
                                            "Niv",
                                            weight="bold"
                                        ),
                                        ft.Text("3")
                                    ]
                                ),
                                ft.Column(
                                    controls=[
                                        ft.Text(
                                            "Apt",
                                            weight="bold"
                                        ),
                                        ft.Text("15")
                                    ]
                                ),
                            ]
                        ),
                        ft.Divider(),
                        inputCodendereco,
                        botaoEndereco,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            ]
        )
    )

    # Criação dinâmica dos itens no tabsResumo
    resumo_controls = []
    for item in dados_itens:
        codprod = item[1]  # Índice 1: Código do produto
        descricao = item[3]  # Índice 3: Descrição
        qt = item[4]  # Índice 4: Quantidade

        resumo_controls.extend([
            ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text(
                                "Codprod",
                                weight="bold"
                            ),
                            ft.Text(str(codprod))
                        ]
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                "Descrição",
                                weight="bold"
                            ),
                            ft.Text(
                                descricao,
                                no_wrap=False,
                                width=200
                            )
                        ]
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text(
                                "Qt",
                                weight="bold"
                            ),
                            ft.Text(str(qt))
                        ]
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                "Sep",
                                weight="bold"
                            ),
                            ft.Text("5")
                        ]
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                "Dif",
                                weight="bold"
                            ),
                            ft.Text(-4)
                        ]
                    ),
                ],
            ),
            ft.Divider(),
        ])

    tabsResumo = ft.Container(
        content=ft.Column(
            controls=resumo_controls,  # Adiciona os controles dinâmicos aqui
            scroll=ft.ScrollMode.AUTO
        ),
        
    )

    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=200,
        tabs=[
            ft.Tab(
                text="Separar",
                content=ft.Container(
                    content=tabsSeparar,
                    expand=True,
                    width="100%"
                ),
            ),
            ft.Tab(
                text="Resumo",
                content=ft.Container(
                    content=tabsResumo,
                    expand=True,
                    width="100%"
                ),
            ),
            ft.Tab(
                text="Finalizar",
                content=ft.Container(
                    ft.Text("Finalizar separação"),
                ),
            ),
        ],
    )

    main_container = ft.Container(
        content=tabs,
        expand=True,
        width="100%",
        height="100%",
    )

    return ft.View(
        route="/separar_pedido",
        controls=[
            header,
            title,
            ft.Container(height=10),
            main_container
        ],
    )