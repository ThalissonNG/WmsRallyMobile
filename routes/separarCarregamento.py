import flet as ft
import requests
from routes.config.config import colorVariaveis, user_info, base_url, snack_bar

def separar_carregamento(page: ft.Page, navigate_to, header, arguments):
    codfilial = user_info['codfilial']
    matricula = user_info['matricula']
    numcar = arguments['numcar']

    titulo = ft.Text(
        f"Separar Carregamento - {numcar}",
        size=24,
        weight="bold",
        color=colorVariaveis['titulo']
    )
    aba_separar = ft.Tab(
        text="Separar",
        content=ft.Column(
            controls=[
                
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )
    )
    aba_resumo = ft.Tab(
        text="Resumo",
        content=ft.Column(
            controls=[

            ],
            spacing=10,
            # scroll=ft.ScrollMode.AUTO,
            expand=True
        )
    )
    
    aba_finalizar = ft.Tab(
        text="Finalizar"
    )
    abas = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        expand=1,
        tabs=[
            aba_separar,
            aba_resumo,
            aba_finalizar,
        ],
    )

    def buscar_dados(numcar):
        try:
            url = f"{base_url}/separar_carregamento/{numcar}"
            response = requests.get(url)
            # print(response.json())
            mensagem = response.json()['message']
            resumo = response.json()['resumo']
            codbarras = response.json()['codbarras']
            if response.status_code == 200:
                # print(resumo)
                snack_bar(mensagem, colorVariaveis['sucesso'], colorVariaveis['texto'], page)

                aba_resumo.content.controls.clear()
                for res in resumo:
                    aba_resumo.content.controls.extend(contruir_resumo(res))

                aba_separar.content.controls.extend(contruir_separar(codbarras))
                page.update()

                return True
            else:
                snack_bar(mensagem, colorVariaveis['erro'], colorVariaveis['texto'], page)
                return False
        except Exception as e:
            print(e)
            return False

    def contruir_resumo(resumo):
        numped = resumo[0]
        codcli = resumo[1]
        cliente = resumo[2]
        destino = resumo[3]
        volume = resumo[4]

        return [
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text(
                                    f"Numped: {numped}"
                                ),
                                ft.Text(
                                    f"Destino: {destino}"
                                ),
                                ft.Text(
                                    f"Volume: {volume}"
                                )
                            ]
                        ),
                        ft.Row(
                            controls=[
                                ft.Text(
                                    f"Cliente: {codcli} - {cliente}"
                                )
                            ],
                            wrap=True
                        ),
                        ft.Divider(),
                    ]
                )
            ),
            ]

    def contruir_separar(codbarras):
        print(codbarras)
        codveiculo = codbarras[0][2]
        carro = codbarras[0][3]

        def validar_codbarra():
            cod = input_codbarra.value

            if any(cod == item[1] for item in codbarras):
                dialog_veiculo(numcar, cod, codveiculo)
                print("Validado")
            else:
                print("Invalidado")
                snack_bar("Código de barra inválido", colorVariaveis['erro'], colorVariaveis['texto'], page)
                input_codbarra.value = ""
                page.update()   

        input_codbarra = ft.TextField(
            label="Código de Barra",
            autofocus=True,
            on_submit=lambda e: validar_codbarra()
        )
        btn_codbarra = ft.ElevatedButton(
            text="Validar",
            on_click=lambda e: validar_codbarra()
        )

        return [
            ft.Container(
                content=ft.Column(
                    controls=[
                        input_codbarra,
                        btn_codbarra,
                        ft.Row(
                            controls=[
                                ft.Text(
                                    f"Veículo: {codveiculo} - {carro}",
                                    expand=True,
                                    no_wrap=False
                                ),
                            ]
                        ),
                        ft.Divider(),
                        *[
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        f"Pedidos: {codbarra[0]}"
                                    )
                                ]
                            )
                            for codbarra in codbarras
                        ]
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    expand=True
                )
            ),
        ]

    def dialog_veiculo(numcar, codbarranumped, codveiculo):
        print(numcar, codbarranumped, codveiculo)

        def validar_codveiculo():
            codveiculo_input = input_codveiculo.value
            if int(codveiculo) == int(codveiculo_input):
                print("Validado")
            else:
                print("Invalidado")
                snack_bar("Véiculo incorreto", colorVariaveis['erro'], colorVariaveis['texto'], page)
                input_codveiculo.value = ""
                page.update()

        input_codveiculo = ft.TextField(
            label="Código do Veículo",
            autofocus=True,
            on_submit=lambda e: validar_codveiculo()
        )
        btn_confirmar = ft.ElevatedButton(
            text="Confirmar",
            on_click=lambda e: validar_codveiculo()
        )
        dialog_codveiculo = ft.AlertDialog(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Informe o véiculo"
                    ),
                    input_codveiculo,
                    btn_confirmar
                ],
            ),
            actions=[ft.TextButton("Fechar", on_click=lambda e: fechar_dialog())],
            
        )
        page.open(dialog_codveiculo)
        page.update()
    
        def fechar_dialog():
            page.close(dialog_codveiculo)
            page.update()

    buscar_dados(numcar)
    return ft.View(
        route="/separar_carregamento",
        controls=[
            header,
            titulo,
            abas
        ]
    )
