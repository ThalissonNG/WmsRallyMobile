import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

# Variável global para rastrear o índice do produto atual
current_index = 0
# Variáveis globais para armazenar os dados carregados
global_dados_itens = []
global_dados_codbarras = []
global_dados_resumo = []
# Lista para rastrear endereços de origem dos produtos separados
global_enderecos_origem = []

def separar_pedido(page, navigate_to, header):
    global current_index, global_dados_itens, global_dados_codbarras, global_dados_resumo, global_enderecos_origem

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
        # Inicializa a lista de endereços de origem
        global_enderecos_origem = [[] for _ in range(len(global_dados_resumo))]

    # Função auxiliar para encontrar o próximo produto (índice) que ainda não foi totalmente separado
    def encontrar_proximo_produto_index():
        next_codprod = None
        for resumo_item in global_dados_resumo:
            qt_pedida = resumo_item[4]
            qt_separada = resumo_item[5]
            if qt_separada < qt_pedida:
                next_codprod = resumo_item[0]
                break
        if next_codprod is not None:
            for i, item in enumerate(global_dados_itens):
                if item[1] == next_codprod:
                    return i
        return None

    # Atualiza o índice atual com base no próximo produto incompleto
    proxima_posicao = encontrar_proximo_produto_index()
    if proxima_posicao is not None:
        current_index = proxima_posicao

    # Produto atual (a ser separado)
    produto_atual = global_dados_itens[current_index]
    # Filtra todos os itens com o mesmo codprod
    itens_produto_atual = [item for item in global_dados_itens if item[1] == produto_atual[1]]

    title = ft.Text(
        "Separar pedido",
        size=24,
        weight="bold",
        color=colorVariaveis['titulo']
    )

    # Exibe informações do produto atual (por exemplo, descrição e código)
    produto_info_text = ft.Text(
        f"Produto atual: {produto_atual[3]} (Código: {produto_atual[1]})",
        size=16,
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
        if endereco_digitado and endereco_digitado.strip():
            endereco_encontrado = None
            for item in itens_produto_atual:
                if int(endereco_digitado) == item[6]:
                    endereco_encontrado = item
                    break
            if endereco_encontrado:
                print("Endereço válido")
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
        print(f"Código de barras digitado: {codbarra_digitado}")
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
                print(f"Quantidade separada atualizada: {item[5]}")
                print(f"Dados_itens atualizado: {global_dados_itens}")
                
                # Atualiza o resumo global para este produto
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
                    novo_resumo = [item[1], item[2], item[3], item[6], item[4], item[5], item[4] - item[5]]
                    global_dados_resumo.append(novo_resumo)
                
                atualizar_resumo_visual(e.page)
                
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
                        tabsSeparar.content = ft.Column(
                            controls=[ft.Text("Todos os produtos foram separados!", size=20, weight="bold", color=colorVariaveis['sucesso'])]
                        )
                        tabsSeparar.update()
                        mostrar_snackbar(e.page, "Todos os produtos foram separados!", colorVariaveis['sucesso'])
                else:
                    mostrar_snackbar(e.page, "Produto validado com sucesso!", colorVariaveis['sucesso'])
                atualizar_resumo_visual(e.page)
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
    
    # Função para atualizar visualmente a aba Resumo (atualiza a página inteira)
    def atualizar_resumo_visual(page):
        page.update()
    
    # Função para encontrar o índice do próximo produto que não esteja totalmente separado
    def encontrar_proximo_produto_index():
        next_codprod = None
        for resumo_item in global_dados_resumo:
            if resumo_item[5] < resumo_item[4]:
                next_codprod = resumo_item[0]
                break
        if next_codprod is not None:
            for i, item in enumerate(global_dados_itens):
                if item[1] == next_codprod:
                    return i
        return None
    
    # Construção do tab "Separar" com os endereços disponíveis para o produto atual
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
                        produto_info_text,
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
    
    # Construção dinâmica do tab "Resumo" usando os dados de global_dados_resumo
    resumo_controls = []
    for idx, item in enumerate(global_dados_resumo):
        codprod = item[0]
        codfab = item[1]
        descricao = item[2]
        coenderecoorigem = item[3]
        qtpedida = item[4]
        qtseparada = item[5]
        qtrestante = item[6]
        
        # Monta a linha com as informações desejadas
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
                ft.Text("Progresso Geral", weight="bold", size=18),
                ft.Text(f"{sum(item[5] for item in global_dados_resumo)} de {sum(item[4] for item in global_dados_resumo)} itens separados"),
                ft.ProgressBar(value=sum(item[5] for item in global_dados_resumo) / sum(item[4] for item in global_dados_resumo) if sum(item[4] for item in global_dados_resumo) > 0 else 0),
                ft.Container(height=20),
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
