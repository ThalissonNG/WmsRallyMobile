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
        else:
            print("Erro ao buscar os dados da transferência/devolução")
            dados_itens = []
    except Exception as exc:
        print(f"Erro: {exc}")
        dados_itens = []
    
    title = ft.Text(
        "Separar Transferência/Devolução",
        size=24,
        weight="bold",
        color=colorVariaveis['titulo']
    )

    # Exibir apenas o primeiro produto da lista
    if dados_itens:
        item = dados_itens[0]
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
                    )
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
    
    # Criar Tabs
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
