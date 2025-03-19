import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def separar_transferencia_devolucao(e, navigate_to, header):
    matricula = user_info.get('matricula')
    codfilial = user_info.get('codfilial')
    
    try:
        response = requests.post(
            f"{base_url}/buscar_dados_transferencia_devolucao",
            json={"matricula": matricula, "codfilial": codfilial}
        )
        if response.status_code == 200:
            dados = response.json()
            dados_itens = dados.get("dados_itens", [])
            dados_resumo = dados.get("dados_resumo", [])
        else:
            print("Erro ao buscar os dados da transferência/devolução")
            dados_itens = []
            dados_resumo = []
    except Exception as exc:
        print(f"Erro: {exc}")
        dados_itens = []
        dados_resumo = []
    
    title = ft.Text(
        "Separar Transferência/Devolução",
        size=24,
        weight="bold",
        color=colorVariaveis['titulo']
    )

    def validar_endereco(e, endereco_digitado, item):
        if endereco_digitado.isdigit() and int(endereco_digitado) == item[6]:
            abrir_dialogo_produto(e, item)
        else:
            snack = ft.SnackBar(
                content=ft.Text("Endereço incorreto!", color="white"),
                bgcolor=colorVariaveis['erro']
            )
            e.page.snack_bar = snack
            snack.open = True
            e.page.update()
    
    def abrir_dialogo_produto(e, item):
        def fechar_dialogo(e):
            e.page.dialog.open = False
            e.page.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text("Confirmação de Produto"),
            content=ft.Column(
                controls=[
                    ft.Text(f"Código do Produto: {item[1]}"),
                    ft.Text(f"Descrição: {item[3]}"),
                    ft.Text(f"Quantidade Pedida: {item[4]}"),
                    ft.Text(f"Quantidade Separada: 0"),
                    ft.TextField(label="Código de Barras"),
                ]
            ),
            actions=[
                ft.TextButton("Confirmar", on_click=lambda e: print("Produto confirmado!")),
                ft.TextButton("Cancelar", on_click=fechar_dialogo),
            ],
        )
        e.page.dialog = dialog
        dialog.open = True
        e.page.update()

    if dados_itens:
        item = dados_itens[0]
        input_endereco = ft.TextField(label="Digite o código do endereço")
        botao_validar = ft.ElevatedButton(
            text="Validar Endereço",
            bgcolor=colorVariaveis['botaoAcao'],
            color=colorVariaveis['texto'],
            on_click=lambda e: validar_endereco(e, input_endereco.value, item)
        )

        produto_container = ft.Container(
            padding=10,
            border=ft.border.all(1, color=colorVariaveis['bordarInput']),
            border_radius=10,
            content=ft.Column(
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Column(controls=[ft.Text("CODPROD", weight="bold"), ft.Text(str(item[1]))]),
                            ft.Column(controls=[ft.Text("CODFAB", weight="bold"), ft.Text(item[2])]),
                            ft.Column(controls=[ft.Text("QT", weight="bold"), ft.Text(str(item[4]))]),
                        ]
                    ),
                    ft.Text(item[3], weight="bold"),
                    ft.Divider(),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Column(controls=[ft.Text("MOD", weight="bold"), ft.Text(str(item[7]))]),
                            ft.Column(controls=[ft.Text("RUA", weight="bold"), ft.Text(str(item[8]))]),
                            ft.Column(controls=[ft.Text("EDI", weight="bold"), ft.Text(str(item[9]))]),
                            ft.Column(controls=[ft.Text("NIV", weight="bold"), ft.Text(str(item[10]))]),
                            ft.Column(controls=[ft.Text("APT", weight="bold"), ft.Text(str(item[11]))]),
                        ]
                    ),
                    input_endereco,
                    botao_validar,
                ]
            )
        )
    else:
        produto_container = ft.Text("Nenhum produto para separar", size=18, color=colorVariaveis['erro'])
    
    tabsSeparar = ft.Container(
        padding=10,
        expand=True,
        content=ft.Column(
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[ft.Text("Vá ao endereço:", weight="bold", size=20)]
                ),
                ft.Divider(),
                produto_container,
            ],
            scroll=ft.ScrollMode.AUTO
        )
    )
    
    tabsResumo = ft.Container(
        content=ft.Text("Resumo dos produtos", size=20, weight="bold"),
    )
    
    tabsFinalizar = ft.Container(
        content=ft.Column(
            controls=[
                ft.ElevatedButton(
                    text="Finalizar",
                    bgcolor=colorVariaveis['botaoAcao'],
                    color=colorVariaveis['texto'],
                    on_click=lambda e: print("Clicou pra finalizar")
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )
    
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=200,
        tabs=[
            ft.Tab(text="Separar", content=tabsSeparar),
            ft.Tab(text="Resumo", content=tabsResumo),
            ft.Tab(text="Finalizar", content=tabsFinalizar),
        ],
    )
    
    main_container = ft.Container(
        content=tabs,
        expand=True,
        width="100%",
        height="100%"
    )
    
    return ft.View(
        route="/separar_transferencia_devolucao",
        controls=[
            header,
            title,
            ft.Container(height=10),
            main_container
        ]
    )