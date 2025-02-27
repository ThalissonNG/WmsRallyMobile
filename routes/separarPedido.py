import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

# Variável global para rastrear o índice do produto atual
current_index = 0
# Variáveis globais para armazenar os dados carregados
global_dados_itens = []
global_dados_codbarras = []
global_dados_resumo = []

def separar_pedido(page, navigate_to, header):
    global current_index, global_dados_itens, global_dados_codbarras, global_dados_resumo

    matricula = user_info.get('matricula')
    dados_itens = []       # Dados dos itens do pedido
    dados_codbarras = []   # Dados dos códigos de barras

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
            dados_resumo = dados.get("dados_resumo", [])
            print(f"Dados resumo: {dados_resumo}")
            print(f"Dados itens: {dados_itens}")
            print(f"Dados codbarras: {dados_codbarras}")
        else:
            print("Deu erro")
    except Exception as exc:
        print(f"Erro: {exc}")

    # Se não houver dados, exiba uma mensagem apropriada
    if not dados_itens:
        return ft.View(
            route="/separar_pedido",
            controls=[
                header,
                ft.Text("Nenhum produto encontrado.", size=24, weight="bold", color=colorVariaveis['titulo'])
            ]
        )

    # Armazena os dados globalmente, se ainda não foram armazenados
    if not global_dados_itens:
        global_dados_itens = dados_itens
    if not global_dados_codbarras:
        global_dados_codbarras = dados_codbarras
    if not global_dados_resumo:
        global_dados_resumo = dados_resumo

    # Use o produto atual com base no índice global
    produto_atual = global_dados_itens[current_index]

    # Filtra todos os itens com o mesmo codprod (código do produto)
    itens_produto_atual = [item for item in global_dados_itens if item[1] == produto_atual[1]]

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

    botaoFinalizar = ft.ElevatedButton(
        text="Finalizar",
        bgcolor=colorVariaveis['botaoAcao'],
        color=colorVariaveis['texto'],
        width=300,
        on_click=lambda e: finalizar(e)
    )

    def validar_endereco(e):
        endereco_digitado = inputCodendereco.value
        print(f"Endereço digitado: {endereco_digitado}")
        if dados_itens:
            # Verifica se o endereço digitado corresponde a algum dos endereços do produto atual
            endereco_encontrado = None
            for item in itens_produto_atual:
                if int(endereco_digitado) == item[6]:  # Índice 6: codendereco
                    endereco_encontrado = item
                    break

            if endereco_encontrado:
                print("Endereço válido")
                exibir_dialog_produto(e.page, endereco_encontrado)
            else:
                mostrar_snackbar(e.page, "Endereço incorreto!", colorVariaveis['erro'])
        else:
            mostrar_snackbar(e.page, "Nenhum produto encontrado.", colorVariaveis['erro'])

    def exibir_dialog_produto(page, item):
        codprod = item[1]      # Índice 1: Código do produto
        codfab = item[2]       # Índice 2: Código do fabricante
        descricao = item[3]    # Índice 3: Descrição
        qtpedida = item[4]     # Índice 4: Quantidade pedida
        qtseparada = item[5]   # Índice 5: Quantidade separada

        # Widget para exibir a quantidade separada e que será atualizado
        qt_text = ft.Text(f"Quantidade Separada: {qtseparada}")

        dialog = ft.AlertDialog(
            title=ft.Text("Produto"),
            content=ft.Column(
                controls=[
                    ft.Text(f"Código do Produto: {codprod}"),
                    ft.Text(f"Código do Fabricante: {codfab}"),
                    ft.Text(f"Descrição: {descricao}"),
                    ft.Text(f"Quantidade Pedida: {qtpedida}"),
                    qt_text,
                    inputCodbarra
                ]
            ),
            actions=[
                ft.TextButton("Confirmar", on_click=lambda e: validar_codbarra(e, item, qt_text))
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    def validar_codbarra(e, item, qt_text):
        codbarra_digitado = inputCodbarra.value
        print(f"Código de barras digitado: {codbarra_digitado}")

        codprod_encontrado = None
        for codbarras in global_dados_codbarras:
            if codbarras[1] == codbarra_digitado:  # Índice 1: Código de barras
                codprod_encontrado = codbarras[0]   # Índice 0: Código do produto
                break

        if codprod_encontrado is not None:
            if codprod_encontrado == item[1]:  # Verifica se corresponde ao produto atual
                item[5] += 1  # Atualiza a quantidade separada
                qt_text.value = f"Quantidade Separada: {item[5]}"
                qt_text.update()
                inputCodbarra.value = ""
                inputCodbarra.update()
                print(f"Quantidade separada atualizada: {item[5]}")
                print(f"Dados_itens atualizado: {global_dados_itens}")

                if item[5] == item[4]:
                    mostrar_snackbar(e.page, "Quantidade completa! Passando para o próximo item.", colorVariaveis['sucesso'])
                    atualizar_resumo(e.page)
                    fechar_dialog(e.page)
                    global current_index
                    if current_index < len(global_dados_itens) - 1:
                        current_index += 1
                        navigate_to("/separar_pedido")
                    else:
                        mostrar_snackbar(e.page, "Todos os produtos foram separados!", colorVariaveis['sucesso'])
                else:
                    mostrar_snackbar(e.page, "Produto validado com sucesso!", colorVariaveis['sucesso'])
                atualizar_resumo(e.page)
            else:
                mostrar_snackbar(e.page, "Produto não corresponde ao endereço!", colorVariaveis['erro'])
        else:
            mostrar_snackbar(e.page, "Código de barras inválido!", colorVariaveis['erro'])
        e.page.update()

    def fechar_dialog(page):
        page.dialog.open = False
        page.update()

    def mostrar_snackbar(page, mensagem, cor):
        snackbar = ft.SnackBar(
            content=ft.Text(mensagem, color="white"),
            bgcolor=cor,
        )
        page.overlay.append(snackbar)
        snackbar.open = True
        page.update()

    def finalizar(e):
        print("Botão finalizar:", global_dados_itens)
        e.page.update()

    # Função para atualizar a aba "Resumo" com os dados atuais
    def atualizar_resumo(page):
        resumo_controls = []
        for item in global_dados_resumo:
            codprod = item[0]
            codfab = item[1]
            descricao = item[2]
            coenderecoorigem = item[3]
            qtpedida = item[4]
            qtseparada = item[5]
            qtrestante = item[6]
            resumo_controls.append(
                ft.Row(
                    controls=[
                        ft.Text(f"Codprod: {codprod}", weight="bold"),
                        ft.Text(f"Codfab: {codfab}", weight="bold"),
                        ft.Text(f"Descrição: {descricao}", weight="bold"),
                        ft.Text(f"End. Origem: {coenderecoorigem}", weight="bold"),
                        ft.Text(f"Qtd Pedida: {qtpedida}", weight="bold"),
                        ft.Text(f"Qtd Separada: {qtseparada}", weight="bold"),
                        ft.Text(f"Qtd Restante: {qtrestante}", weight="bold")
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )
            )
            resumo_controls.append(ft.Divider())
        tabsResumo.content = ft.Column(
            controls=resumo_controls,
            scroll=ft.ScrollMode.AUTO
        )
        tabsResumo.update()
        page.update()


    # Construção do tab "Separar" com os dados do endereço do produto atual
    enderecos_controls = []
    for item in itens_produto_atual:
        mod_val = str(item[7])
        rua_val = str(item[8])
        edf_val = str(item[9])
        niv_val = str(item[10])
        apt_val = str(item[11])
        enderecos_controls.append(
            ft.Column(
                controls=[
                    ft.Row(
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
                ]
            )
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
                                ft.Text("Vá ao endereço:", weight="bold", size=20)
                            ]
                        ),
                        ft.Divider(),
                        *enderecos_controls,  # Adiciona todos os endereços
                        inputCodendereco,
                        botaoEndereco,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            ],
            scroll=ft.ScrollMode.AUTO  # Permite a rolagem vertical
        )
    )

    # Construção dinâmica do tab "Resumo"
    resumo_controls = []
    for item in global_dados_resumo:
        codprod = item[0]      # Código do produto
        codfab = item[1]       # Código do fabricante
        descricao = item[2]    # Descrição
        qt = item[4]           # Quantidade pedida
        sep = item[5]          # Quantidade separada
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
                            ft.Text("Codfab", weight="bold"),
                            ft.Text(str(codfab))
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

    tabsfinalizar = ft.Container(
        content=ft.Column(
            controls=[
                botaoFinalizar
            ]
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
                    content=tabsfinalizar,
                    expand=True,
                    width="100%"
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