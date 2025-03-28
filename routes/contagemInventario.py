import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info

def contagem_inventario(e, navigate_to, header):
    matricula = user_info.get('matricula')
    codfilial = user_info.get('codfilial')

    # Cria uma referência dinâmica para os elementos que mudam
    conteudo_dinamico = ft.Column()

    def mostrar_campos_endereco(e):
        conteudo_dinamico.controls.clear()
        conteudo_dinamico.controls.append(
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(f"Nº Inventário: 001"),
                        ft.Text("Nº OS: 7"),
                        ft.TextField(label="Endereço"),
                        ft.ElevatedButton(
                            "Confirmar Endereço",
                            on_click=lambda e: print("Clicou confirmar")
                        )
                    ]
                )
            )
        )
        e.page.update()

    def buscar_os(e, codfilial, matricula):
        try:
            response = requests.post(
                f"{base_url}/contagem_inventario",
                json={
                    "codfilial": codfilial,
                    "matricula": matricula
                }
            )
            if response.status_code == 200:
                print("Iniciada contagem")
                dados = response.json()
                dados_os = dados.get("dados_os", [])
                print(dados_os)
                mostrar_campos_endereco(e)
            else:
                print("Nao iniciou contagem")

        except Exception as exc:
            print(exc)

    title = ft.Text(
        "Buscar Inventário",
        size=24,
        weight="bold",
        color=colorVariaveis['titulo']
    )

    botao_iniciar = ft.ElevatedButton(
        "Iniciar Inventário",
        on_click=lambda e: buscar_os(e, codfilial, matricula)
    )

    conteudo_dinamico.controls.append(botao_iniciar)

    return ft.View(
        route="/contagem_inventario",
        controls=[
            header,
            title,
            conteudo_dinamico
        ]
    )
