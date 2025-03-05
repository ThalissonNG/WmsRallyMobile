import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

# Global variables to track the current product index and store data from the API.
current_index = 0
global_dados_itens = []
global_dados_codbarras = []
global_dados_resumo = []
# List to track the origin addresses used when separating each product.
global_enderecos_origem = []

def separar_pedido(page, navigate_to, header):
    global current_index, global_dados_itens, global_dados_codbarras, global_dados_resumo, global_enderecos_origem

    matricula = user_info.get('matricula')
    dados_itens = []       # Items data from the API
    dados_codbarras = []   # Barcode data from the API

    try:
        response = requests.post(
            base_url + "/separarPedido",
            json={"matricula": matricula}
        )
        if response.status_code == 200:
            dados = response.json()
            dados_itens = dados.get("dados_itens", [])
            dados_codbarras = dados.get("dados_codbarras", [])
            dados_resumo = dados.get("dados_resumo", [])
        else:
            print("Deu erro")
    except Exception as exc:
        print(f"Erro: {exc}")

    # If no items found, display a message.
    if not dados_itens:
        return ft.View(
            route="/separar_pedido",
            controls=[
                header,
                ft.Text("Nenhum produto encontrado.", size=24, weight="bold", color=colorVariaveis['titulo'])
            ]
        )

    # Store the API data globally (only on the first load)
    if not global_dados_itens:
        global_dados_itens = dados_itens
    if not global_dados_codbarras:
        global_dados_codbarras = dados_codbarras
    if not global_dados_resumo:
        global_dados_resumo = dados_resumo
        # Initialize the list of origin addresses for each product in the summary.
        global_enderecos_origem = [[] for _ in range(len(global_dados_resumo))]

    # Define a helper to find the index (in global_dados_itens) for the next product that isn’t complete.
    def encontrar_proximo_produto_index():
        for resumo_item in global_dados_resumo:
            qt_pedida = resumo_item[4]
            qt_separada = resumo_item[5]
            if qt_separada < qt_pedida:
                next_codprod = resumo_item[0]
                # Return the first occurrence in global_dados_itens matching this product code.
                for i, item in enumerate(global_dados_itens):
                    if item[1] == next_codprod:
                        return i
        return None

    # Update current_index using the helper.
    proxima_posicao = encontrar_proximo_produto_index()
    if proxima_posicao is not None:
        current_index = proxima_posicao

    # The current product to be separated.
    produto_atual = global_dados_itens[current_index]
    # Filter all items for this product (they may have different addresses).
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
        on_click=lambda e: finalizar(e, global_dados_itens, global_dados_resumo)
    )

    # --- Functions for handling barcode and address validation ---

    def validar_endereco(e):
        endereco_digitado = inputCodendereco.value
        if endereco_digitado and endereco_digitado.strip():
            endereco_encontrado = None
            for item in itens_produto_atual:
                if int(endereco_digitado) == item[6]:
                    endereco_encontrado = item
                    break
            if endereco_encontrado:
                exibir_dialog_produto(e.page, endereco_encontrado)
            else:
                mostrar_snackbar(e.page, "Endereço incorreto!", colorVariaveis['erro'])
        else:
            mostrar_snackbar(e.page, "Digite um endereço válido.", colorVariaveis['erro'])
    
    def exibir_dialog_produto(page, item):
        codprod = item[1]
        codfab = item[2]
        descricao = item[3]
        qtpedida = item[4]
        qtseparada = item[5]
        codendereco = item[6]
        # Create a text widget to show the separated quantity.
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
                ft.TextButton("Confirmar", on_click=lambda e: validar_codbarra(e, item, qt_text, codendereco))
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.dialog = dialog
        dialog.open = True
        inputCodbarra.value = ""
        page.update()
    
    def validar_codbarra(e, item, qt_text, codendereco):
        codbarra_digitado = inputCodbarra.value
        codprod_encontrado = None
        for codbarras in global_dados_codbarras:
            if codbarras[1] == codbarra_digitado:
                codprod_encontrado = codbarras[0]
                break
        if codprod_encontrado is not None:
            if codprod_encontrado == item[1]:
                item[5] += 1
                qt_text.value = f"Quantidade Separada: {item[5]}"
                qt_text.update()
                inputCodbarra.value = ""
                inputCodbarra.update()

                # Update global summary for this product:
                atualizado = False
                for resumo_item in global_dados_resumo:
                    if resumo_item[0] == item[1]:
                        resumo_item[5] = item[5]
                        resumo_item[6] = resumo_item[4] - resumo_item[5]
                        if resumo_item[3] is None:
                            resumo_item[3] = codendereco
                        atualizado = True
                        break
                if not atualizado:
                    novo_resumo = [
                        item[1],  # codprod
                        item[2],  # codfab
                        item[3],  # descricao
                        item[6],  # coenderecoorigem
                        item[4],  # qtpedida
                        item[5],  # qtseparada
                        item[4] - item[5]  # qtrestante
                    ]
                    global_dados_resumo.append(novo_resumo)
                
                # Update the "Resumo" tab UI
                atualizar_resumo(page)
                
                if item[5] == item[4]:
                    mostrar_snackbar(e.page, "Quantidade completa para este item!", colorVariaveis['sucesso'])
                    fechar_dialog(e.page)
                    next_index = encontrar_proximo_produto_index()
                    if next_index is not None:
                        global current_index
                        current_index = next_index
                        navigate_to("/separar_pedido")
                    else:
                        inputCodendereco.value = ""
                        inputCodendereco.update()
                        # Clear the "Separar" tab to show a completion message.
                        tabsSeparar.content = ft.Column(
                            controls=[ft.Text("Todos os produtos foram separados!", size=20, weight="bold", color=colorVariaveis['sucesso'])]
                        )
                        tabsSeparar.update()
                        mostrar_snackbar(e.page, "Todos os produtos foram separados!", colorVariaveis['sucesso'])
                else:
                    mostrar_snackbar(e.page, "Produto validado com sucesso!", colorVariaveis['sucesso'])
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
    
    def finalizar(e, dados_itens_finalizar, dados_resumo_finalizar):
        print("Botão finalizar dados itens:", dados_itens_finalizar)
        print("Botão finalizar dados RESUMO:", dados_resumo_finalizar)
        try:
            response = requests.post(
                f"{base_url}/separarPedido",
                json={
                    "matricula": matricula,
                    "dados_itens_finalizar": global_dados_itens,
                    "dados_resumo_finalizar": global_dados_resumo,
                    "action": "finalizar"
                }
            )
            if response.status_code == 202:
                mostrar_snackbar(e.page, "Separação finalizada com sucesso!", colorVariaveis['sucesso'])
                global_dados_itens.clear()
                global_dados_codbarras.clear()
                global_dados_resumo.clear()
                global_enderecos_origem.clear()
                current_index = 0
                navigate_to("/buscar_pedido")
            else:
                print("Erro ao enviar pedido para finalização")
        except Exception as exc:
            print(f"Erro: {exc}")
        e.page.update()
    
    # Function to update the "Resumo" tab based on global_dados_resumo.
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
                                ft.Text(descricao, no_wrap=False, width=200)
                            ]
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    controls=[
                        ft.Column(
                            controls=[ft.Text("Qtd Pedida", weight="bold"), ft.Text(str(qtpedida))]
                        ),
                        ft.Column(
                            controls=[ft.Text("Qtd Separada", weight="bold"), ft.Text(str(qtseparada))]
                        ),
                        ft.Column(
                            controls=[ft.Text("Qtd Restante", weight="bold"), ft.Text(str(qtrestante))]
                        ),
                    ],
                ),
                ft.Divider(),
            ])
        # Rebuild the Column and update the container.
        novo_column = ft.Column(controls=resumo_controls, scroll=ft.ScrollMode.AUTO)
        tabsResumo.content = novo_column
        tabsResumo.update()
        page.update()
    
    # Function to find the index of the next product (in global_dados_itens) that is not fully separated.
    def encontrar_proximo_produto_index():
        for resumo_item in global_dados_resumo:
            if resumo_item[5] < resumo_item[4]:
                next_codprod = resumo_item[0]
                for i, item in enumerate(global_dados_itens):
                    if item[1] == next_codprod:
                        return i
        return None
    
    # --- Build the "Separar" tab UI ---
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
                            ft.Column(controls=[ft.Text("Mod", weight="bold"), ft.Text(mod_val)]),
                            ft.Column(controls=[ft.Text("Rua", weight="bold"), ft.Text(rua_val)]),
                            ft.Column(controls=[ft.Text("Edf", weight="bold"), ft.Text(edf_val)]),
                            ft.Column(controls=[ft.Text("Niv", weight="bold"), ft.Text(niv_val)]),
                            ft.Column(controls=[ft.Text("Apt", weight="bold"), ft.Text(apt_val)]),
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
                            controls=[ft.Text("Vá ao endereço:", weight="bold", size=20)]
                        ),
                        ft.Divider(),
                        *enderecos_controls,
                        inputCodendereco,
                        botaoEndereco,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            ],
            scroll=ft.ScrollMode.AUTO
        )
    )
    
    # --- Build the "Resumo" tab UI using global_dados_resumo ---
    resumo_controls = []
    for idx, item in enumerate(global_dados_resumo):
        codprod = item[0]
        codfab = item[1]
        descricao = item[2]
        coenderecoorigem = item[3]
        qtpedida = item[4]
        qtseparada = item[5]
        qtrestante = item[6]
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
                            ft.Text(descricao, no_wrap=False, width=200)
                        ]
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                controls=[
                    ft.Column(
                        controls=[ft.Text("Qtd Pedida", weight="bold"), ft.Text(str(qtpedida))]
                    ),
                    ft.Column(
                        controls=[ft.Text("Qtd Separada", weight="bold"), ft.Text(str(qtseparada))]
                    ),
                    ft.Column(
                        controls=[ft.Text("Qtd Restante", weight="bold"), ft.Text(str(qtrestante))]
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
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
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
        height="100%"
    )
    
    return ft.View(
        route="/separar_pedido",
        controls=[
            header,
            title,
            ft.Container(height=10),
            main_container
        ]
    )
