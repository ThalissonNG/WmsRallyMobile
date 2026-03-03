import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, user_info, snack_bar

def buscar_multiplos_dist(page: ft.Page, navigate_to, header):
    matricula = user_info.get("matricula")
    codfilial = user_info.get("codfilial")
    
    content_container = ft.Column(
        controls=[
            ft.ElevatedButton(
                text="Buscar Pedido",
                on_click=lambda e: buscar_pedido(matricula, codfilial)
            )
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )

    inputs_etiquetas = {}

    def buscar_pedido(matricula, codfilial):
        response = requests.get(
            f"{base_url}/buscar_multiplos_pedido",
            params={
                "matricula": matricula,
                "codfilial": codfilial
            }
        )
        resposta = response.json()
        mensagem = resposta.get("message")
        if response.status_code == 200:
            print(resposta)
            snack_bar(mensagem, colorVariaveis['sucesso'], colorVariaveis['textoPreto'], page)
            pedidos = resposta.get("pedidos", [])
            construir_atribuir_etiqueta(pedidos)
        else:
            snack_bar(mensagem, colorVariaveis['erro'], colorVariaveis['texto'], page)

    def enviar_etiquetas(e):
        dados_envio = []
        todas_preenchidas = True
        
        for numped, text_field in inputs_etiquetas.items():
            if not text_field.value:
                todas_preenchidas = False
                break
            dados_envio.append({
                "numped": numped,
                "codetiqueta": text_field.value
            })
        
        if not todas_preenchidas:
            snack_bar("Por favor, preencha as etiquetas de TODOS os pedidos.", colorVariaveis['erro'], colorVariaveis['texto'], page)
            return

        if not dados_envio:
            snack_bar("Nenhum pedido encontrado para envio.", colorVariaveis['erro'], colorVariaveis['texto'], page)
            return

        try:
            response = requests.put(
                f"{base_url}/buscar_multiplos_pedido", # Assumindo PUT para salvar baseado no padrão do buscarPedidosDIst.py
                json={
                    "matricula": matricula,
                    "codfilial": codfilial,
                    "pedidos": dados_envio
                }
            )
            resposta = response.json()
            mensagem = resposta.get("message")
            if response.status_code == 200:
                snack_bar(mensagem, colorVariaveis['sucesso'], colorVariaveis['textoPreto'], page)
                # navigate_to("/menu")
            else:
                snack_bar(mensagem, colorVariaveis['erro'], colorVariaveis['texto'], page)
        except Exception as ex:
            snack_bar(f"Erro: {str(ex)}", colorVariaveis['erro'], colorVariaveis['texto'], page)

    def construir_atribuir_etiqueta(pedidos):
        content_container.controls.clear()
        inputs_etiquetas.clear()
        text_fields = []

        for i, pedido in enumerate(pedidos):
            # A API retorna no formato [[numped], [numped], ...]
            numped = pedido[0] if isinstance(pedido, list) else pedido
            
            tf = ft.TextField(
                label=f"Etiqueta para pedido {numped}",
                keyboard_type=ft.KeyboardType.NUMBER,
                border_radius=10,
                autofocus=True if i == 0 else False, # Seleciona o primeiro campo
            )

            # Define o comportamento do Enter para navegar entre os campos
            def on_submit_handler(e, current_idx=i):
                if current_idx + 1 < len(text_fields):
                    text_fields[current_idx + 1].focus()
                else:
                    enviar_etiquetas(None) # Opcional: envia ao dar enter no último

            tf.on_submit = on_submit_handler
            
            inputs_etiquetas[numped] = tf
            text_fields.append(tf)
            
            content_container.controls.append(
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(f"Pedido: {numped}", size=18, weight="bold"),
                            tf
                        ]
                    ),
                    padding=10,
                    border=ft.border.all(1, colorVariaveis['bordarInput']),
                    border_radius=10,
                    margin=ft.margin.only(bottom=10)
                )
            )
        
        content_container.controls.append(
            ft.ElevatedButton(
                text="Enviar",
                bgcolor=colorVariaveis['botaoAcao'],
                color=colorVariaveis['texto'],
                on_click=enviar_etiquetas,
                width=300
            )
        )
        page.update()

    titulo = ft.Text(
        "Separar Múltiplos Dist",
        size=24, weight="bold",
        color=colorVariaveis['titulo']
    )

    return ft.View(
        route="/buscar_multiplos_dist",
        controls=[
            header,
            titulo,
            ft.Container(height=20),
            content_container
        ]
    )
