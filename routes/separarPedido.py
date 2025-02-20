import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def separar_pedido(e, navigate_to, header):
    matricula = user_info.get('matricula')
    dados_itens = []  # Inicializa a variável dados_itens
    dados_codbarras = []

    try:
        response = requests.post(
            base_url + "/separarPedido",
            json={"matricula": matricula}
        )
        if response.status_code == 200:
            dados = response.json()
            print("Recebido com sucesso")
            dados_itens = dados.get("dados_itens", [])
            dados_codbarras = dados.get("dados_codbarras", [])
            print(f"Dados itens: {dados_itens}")
            print(f"Dados codbarras: {dados_codbarras}")
        else:
            print("Deu erro")
    except Exception as exc:
        print(f"Erro: {exc}")

    # Extração dos dados de endereço do primeiro item (se houver)
    if dados_itens and len(dados_itens[0]) >= 12:
        mod_val = str(dados_itens[0][7])
        rua_val = str(dados_itens[0][8])
        edf_val = str(dados_itens[0][9])
        niv_val = str(dados_itens[0][10])
        apt_val = str(dados_itens[0][11])
    else:
        mod_val = rua_val = edf_val = niv_val = apt_val = "N/A"

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
        on_click=lambda e: validar_endereco(e)
    )

    inputCodbarra = ft.TextField(
        label="Bipar produto",
        prefix_icon=ft.icons.SCANNER,
        border_radius=ft.border_radius.all(10),
        border_color=colorVariaveis['bordarInput'],
        border_width=2,
        keyboard_type=ft.KeyboardType.NUMBER
    )

    def validar_endereco(e):
        endereco_digitado = inputCodendereco.value
        print(f"Endereço digitado: {inputCodendereco.value}")
        if dados_itens:
            endereco_solicitado = dados_itens[0][6]  # Índice 6: codendereco
            print(f"Endereço solicitado: {endereco_solicitado}")
            if int(endereco_digitado) == endereco_solicitado:
                print("Endereços iguais")
                exibir_dialog_produto(e.page, dados_itens[0])
            else:
                mostrar_snackbar(e, "Endereço incorreto!", colorVariaveis['erro'])

    def exibir_dialog_produto(page, item):
        codprod = item[1]      # Índice 1: Código do produto
        codfab = item[2]       # Índice 2: Código do fabricante
        descricao = item[3]    # Índice 3: Descrição
        qtpedida = item[4]     # Índice 4: Quantidade pedida
        qtseparada = item[5]   # Índice 5: Quantidade separada

        dialog = ft.AlertDialog(
            title=ft.Text("Produto"),
            content=ft.Column(
                controls=[
                    ft.Text(f"Código do Produto: {codprod}"),
                    ft.Text(f"Código do Fabricante: {codfab}"),
                    ft.Text(f"Descrição: {descricao}"),
                    ft.Text(f"Quantidade Pedida: {qtpedida}"),
                    ft.Text(f"Quantidade Separada: {qtseparada}"),
                    inputCodbarra
                ]
            ),
            actions=[
                ft.TextButton("Confirmar", on_click=lambda e: validar_codbarra(e, item))
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    def validar_codbarra(e, item):
        codbarra_digitado = inputCodbarra.value
        print(f"Código de barras digitado: {codbarra_digitado}")

        # Verificar se o código de barras existe em dados_codbarras
        codprod_encontrado = None
        for codbarras in dados_codbarras:
            if codbarras[1] == codbarra_digitado:  # Índice 1: Código de barras
                codprod_encontrado = codbarras[0]  # Índice 0: Código do produto
                break  # Para a busca assim que encontrar um código de barras válido

        if codprod_encontrado is not None:
            # Verificar se o codprod encontrado corresponde ao item atual
            if codprod_encontrado == item[1]:  # Índice 1: Código do produto
                # Atualizar a quantidade separada
                item[5] += 1  # Índice 5: Quantidade separada
                print(f"Quantidade separada atualizada: {item[5]}")
                print(f"Dados_itens atualizado: {dados_itens}")

                # Verificar se a quantidade separada é igual à quantidade pedida
                if item[5] == item[4]:  # Índice 4: Quantidade pedida
                    mostrar_snackbar(e, "Quantidade completa! Passando para o próximo item.", colorVariaveis['sucesso'])
                    fechar_dialog(e)
                    # Aqui você pode adicionar a lógica para passar para o próximo item
                else:
                    mostrar_snackbar(e, "Produto validado com sucesso!", colorVariaveis['sucesso'])
            else:
                mostrar_snackbar(e, "Produto não corresponde ao endereço!", colorVariaveis['erro'])
        else:
            mostrar_snackbar(e, "Código de barras inválido!", colorVariaveis['erro'])

    def fechar_dialog(e):
        e.page.dialog.open = False
        e.page.update()

    def mostrar_snackbar(e, mensagem, cor):
        snackbar = ft.SnackBar(
            content=ft.Text(mensagem, color="white"),
            bgcolor=cor,
        )
        e.page.overlay.append(snackbar)
        snackbar.open = True
        e.page.update()

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
                                        ft.Text("Mod", weight="bold"),
                                        ft.Text(mod_val)
                                    ]
                                ),
                                ft.Column(
                                    controls=[
                                        ft.Text("Rua", weight="bold"),
                                        ft.Text(rua_val)
                                    ]
                                ),
                                ft.Column(
                                    controls=[
                                        ft.Text("Edf", weight="bold"),
                                        ft.Text(edf_val)
                                    ]
                                ),
                                ft.Column(
                                    controls=[
                                        ft.Text("Niv", weight="bold"),
                                        ft.Text(niv_val)
                                    ]
                                ),
                                ft.Column(
                                    controls=[
                                        ft.Text("Apt", weight="bold"),
                                        ft.Text(apt_val)
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

    # Criação dinâmica dos itens no tab "Resumo"
    resumo_controls = []
    for item in dados_itens:
        codprod = item[1]   # Índice 1: Código do produto
        descricao = item[3] # Índice 3: Descrição
        qt = item[4]        # Índice 4: Quantidade
        sep = item[5]
        resumo_controls.extend([
            ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text("Codprod", weight="bold"),
                            ft.Text(str(codprod))
                        ]
                    ),
                    ft.Column(
                        controls=[
                            ft.Text("Descrição", weight="bold"),
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
                            ft.Text("Qt", weight="bold"),
                            ft.Text(str(qt))
                        ]
                    ),
                    ft.Column(
                        controls=[
                            ft.Text("Sep", weight="bold"),
                            ft.Text(str(sep))
                        ]
                    ),
                    ft.Column(
                        controls=[
                            ft.Text("Dif", weight="bold"),
                            ft.Text(str(int(qt) - int(sep)))
                        ]
                    ),
                ],
            ),
            ft.Divider(),
        ])

    tabsResumo = ft.Container(
        content=ft.Column(
            controls=resumo_controls,
            scroll=ft.ScrollMode.AUTO
        )
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
                    content=ft.Text("Finalizar separação"),
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