import flet as ft
import requests
from routes.config.config import base_url, colorVariaveis, app_version
from routes.menu import menu_page
from routes.configuracoes import configuracoes_page
from routes.armazenarEtiqueta import buscar_etiqueta
from routes.enderecarProduto import enderecar_produto
from routes.consultarProdutoEndereco import consultar_produto_endereco
from routes.transferirProduto import transferir_produto
from routes.buscarPedidoMultiplos import buscar_pedido
from routes.atribuirEtiqueta import atribuir_etiqueta_pedido
from routes.separarPedidoMultiplos import separar_pedido
from routes.buscarTransferenciaDevolucao import buscar_transferencia_devolucao
from routes.buscarDevolucao import buscar_devolucao
from routes.separarTransferenciaDevolucao import separar_transferencia_devolucao
from routes.separarDevolucao import separar_devolucao
from routes.contagemInventario import contagem_inventario
from routes.cadastrarCodbarra import cadastrar_codbarra
from routes.contagemInventarioRotativo import contagem_inventario_rotativo
from routes.osAvulsa import os_avulsa
from routes.osAvulsaSaida import os_avulsa_saida
from routes.osAvulsaEntrada import os_avulsa_entrada
from routes.buscarBonus import buscar_bonus
from routes.conferirBonus import conferir_bonus
from routes.buscarPedidoUnico import buscar_pedido_unico
from routes.separarPedidoUnico import separar_pedido_unico
from routes.abastecimento import abastecimento
from routes.separarAbastecimento import separar_abastecimento
from routes.ajustarEndereco import ajustar_endereco
from routes.buscarPedidosDIst import buscar_pedido_dist
from routes.separarPedidoDist import separar_pedido_dist
from routes.abastecimentoV2 import abastecimentoV2
from routes.separarAbastecimentoV2 import separar_abastecimentoV2

def main(page: ft.Page):
    page.title = "Login"
    page.window.width = 360
    page.window.height = 640
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    # Cabeçalho que usa as variáveis globais definidas após o login
    def create_header():
        # Importa o módulo config para acessar as informações atualizadas
        import routes.config.config as config
        return ft.AppBar(
            ft.ElevatedButton(
                # icon=ft.icons.HOME,
                text="Menu",
                on_click=lambda e: navigate_to("/menu"),
            ),
            title=ft.Text(f"{config.user_info.get('matricula', '')} - {config.user_info.get('usuario', '')}"),
            actions=[
                ft.ElevatedButton(
                    # icon=ft.icons.LOGOUT,
                    text="Sair",
                    on_click=lambda e: navigate_to("/login"),
                )
            ],
            bgcolor=colorVariaveis['botaoAcao'],
        )

    # Função de navegação entre rotas
    def navigate_to(route, arguments=None):
        page.views.clear()
        if route == "/login":
            page.views.append(create_login_view())
        elif route == "/configuracoes":
            page.views.append(configuracoes_page(page, navigate_to, create_header()))
        elif route == "/menu":
            page.views.append(menu_page(page, navigate_to, create_header()))
        elif route == "/armazenar_bonus":
            page.views.append(buscar_etiqueta(navigate_to, create_header(),))
        elif route == "/enderecarProduto":
            page.views.append(enderecar_produto(page, navigate_to, create_header(), arguments))
        elif route == "/consultarProdutoEndereco":
            page.views.append(consultar_produto_endereco(navigate_to, create_header()))
        elif route == "/transferirProduto":
            page.views.append(transferir_produto(page, navigate_to, create_header()))
        elif route == "/buscar_pedido_multiplos":
            page.views.append(buscar_pedido(page, navigate_to, create_header()))
        elif route == "/atribuir_etiqueta":
            page.views.append(atribuir_etiqueta_pedido(page, navigate_to, create_header()))
        elif route == "/separar_pedido_multiplos":
            page.views.append(separar_pedido(page, navigate_to, create_header()))
        elif route == "/buscar_transferencia_devolucao":
            page.views.append(buscar_transferencia_devolucao(page, navigate_to, create_header()))
        elif route == "/buscar_devolucao":
            page.views.append(buscar_devolucao(page, navigate_to, create_header()))
        elif route == "/separar_transferencia_devolucao":
            page.views.append(separar_transferencia_devolucao(page, navigate_to, create_header(), arguments))
        elif route == "/separar_devolucao":
            page.views.append(separar_devolucao(page, navigate_to, create_header(), arguments))
        elif route == "/contagem_inventario":
            page.views.append(contagem_inventario(page, navigate_to, create_header()))
        elif route == "/cadastrar_codbarra":
            page.views.append(cadastrar_codbarra(page, navigate_to, create_header()))
        elif route == "/contagem_inventario_rotativo":
            page.views.append(contagem_inventario_rotativo(page, navigate_to, create_header()))
        elif route == "/os_avulsa":
            page.views.append(os_avulsa(page, navigate_to, create_header()))
        elif route == "/os_avulsa_saida":
            page.views.append(os_avulsa_saida(page, navigate_to, create_header()))
        elif route == "/os_avulsa_entrada":
            page.views.append(os_avulsa_entrada(page, navigate_to, create_header()))
        elif route == "/buscar_bonus":
            page.views.append(buscar_bonus(page, navigate_to, create_header()))
        elif route == "/conferir_bonus":
            page.views.append(conferir_bonus(page, navigate_to, create_header(), arguments))
        elif route == "/buscar_pedido_unico":
            page.views.append(buscar_pedido_unico(page, navigate_to, create_header()))
        elif route == "/separar_pedido_unico":
            page.views.append(separar_pedido_unico(page, navigate_to, create_header()))
        elif route == "/abastecimento":
            page.views.append(abastecimento(page, navigate_to, create_header()))
        elif route == "/separar_abastecimento":
            page.views.append(separar_abastecimento(page, navigate_to, create_header(), arguments))
        elif route == "/ajustar_endereco":
            page.views.append(ajustar_endereco(page, navigate_to, create_header()))
        elif route == "/buscar_pedido_dist":
            page.views.append(buscar_pedido_dist(page, navigate_to, create_header()))
        elif route == "/separar_pedido_dist":
            page.views.append(separar_pedido_dist(page, navigate_to, create_header(), arguments))
        elif route == "/abastecimentoV2":
            page.views.append(abastecimentoV2(page, navigate_to, create_header()))
        elif route == "/separar_abastecimentoV2":
            page.views.append(separar_abastecimentoV2(page, navigate_to, create_header(), arguments))
        page.update()

    # Tela de login
    def create_login_view():
        def login(e):
            username.value = username.value.upper()
            password.value = password.value.upper()
            page.update()

            try:
                response = requests.post(
                    base_url + "/login",
                    json={"username": username.value, "password": password.value},
                )
                print(f"Status code: {response.status_code}")
                print(f"Response: {response.json()}")

                if response.status_code == 200:
                    response_data = response.json()
                    global usuario, matricula, codfilial, nomeCompleto
                    usuario = response_data.get('usuario')
                    matricula = response_data.get('matricula')
                    codfilial = response_data.get('codfilial')
                    nomeCompleto = response_data.get('nomeCompleto')

                    # Atualiza o dicionário global de usuário no módulo config
                    import routes.config.config as config
                    config.user_info.update({
                        'matricula': matricula,
                        'usuario': usuario,
                        'codfilial': codfilial,
                        'nomeCompleto': nomeCompleto,
                    })

                    print(matricula, usuario, codfilial)
                    print(f"UserConfig: {config.user_info}")

                    snackbar_sucess = ft.SnackBar(
                        content=ft.Text("Login com sucesso"),
                        bgcolor=colorVariaveis['sucesso'],
                        show_close_icon=True,
                        duration=1000,
                    )
                    page.overlay.append(snackbar_sucess)
                    snackbar_sucess.open = True
                    page.update()
                    navigate_to("/menu", arguments={
                        'matricula': matricula,
                        'usuario': usuario,
                        'codfilial': codfilial,
                        'nomeCompleto': nomeCompleto
                    })
                elif response.status_code == 404:
                    snackbar_error = ft.SnackBar(
                        content=ft.Text(
                            f"Usuário não encontrado {response.json()}",
                            color=colorVariaveis['texto'],
                            size=20,
                        ),
                        bgcolor=colorVariaveis['erro'],
                        show_close_icon=True,
                    )
                    page.overlay.append(snackbar_error)
                    snackbar_error.open = True
                else:
                    snackbar_error = ft.SnackBar(
                        content=ft.Text(
                            "Login incorreto",
                            color=colorVariaveis['texto'],
                            size=20
                        ),
                        bgcolor=colorVariaveis['erro'],
                        show_close_icon=True,
                    )
                    page.overlay.append(snackbar_error)
                    snackbar_error.open = True
            except requests.RequestException as exc:
                snackbar_error = ft.SnackBar(
                    content=ft.Text(
                        f"Erro na conexão: {str(exc)}",
                        color=colorVariaveis['texto'],
                        size=20
                    ),
                    bgcolor=colorVariaveis['erro'],
                    show_close_icon=True,
                )
                page.overlay.append(snackbar_error)
                snackbar_error.open = True
            page.update()

        def validar_versao():
            try:
                r = requests.post(f"{base_url}/verificarVersao", json={"versao": app_version}, timeout=8)

                if r.status_code in (200, 204):
                    print("Versão atualizada")
                    return

                if r.status_code in (409, 426):
                    data = r.json()
                    link = data.get("download")
                    dlg = ft.AlertDialog(
                        title=ft.Text(f"Nova versão {data.get('latest')} disponível"),
                        content=ft.Text("Deseja atualizar agora?"),
                        actions=[
                            ft.TextButton("Depois", on_click=lambda e: page.close(dlg)),
                            ft.ElevatedButton("Baixar e instalar", on_click=lambda e: page.launch_url(link)),
                        ],
                    )
                    page.open(dlg)
                    return

                print("Falha ao verificar versão:", r.status_code, r.text)

            except Exception as exc:
                print("Erro:", exc)


        validar_versao()
        username = ft.TextField(
            label="Usuário",
            # prefix_icon=ft.icons.PERSON,
            border_radius=ft.border_radius.all(10),
            border_color=colorVariaveis['bordarInput'],
            border_width=2,
            width=300,
        )
        password = ft.TextField(
            label="Senha",
            # prefix_icon=ft.icons.PASSWORD,
            border_radius=ft.border_radius.all(10),
            border_color=colorVariaveis['bordarInput'],
            border_width=2,
            password=True,
            can_reveal_password=True,
            width=300,
            on_submit=login,
        )
        button_login = ft.ElevatedButton(
            text="Login",
            bgcolor=colorVariaveis['botaoAcao'],
            color=colorVariaveis['texto'],
            width=300,
            on_click=login,
        )
        versao = ft.Text(
            f"Versão: {app_version}" 
        )
        button_settings = ft.IconButton(
            icon=ft.Icons.SETTINGS,
            on_click=lambda e:navigate_to("/configuracoes")
        )

        return ft.View(
            route="/login",
            controls=[
                ft.Container(
                    expand=True,
                    content=ft.Column(
                        controls=[
                            ft.Container(
                                content=button_settings,
                                alignment=ft.alignment.top_left,
                                padding=10,  # distância das bordas
                            ),

                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        username,
                                        password,
                                        button_login,
                                        versao,
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                alignment=ft.alignment.center,
                                expand=True,
                            ),
                        ]
                    ),
                )
            ],
        )


    # Inicializa a navegação na tela de login
    navigate_to("/login")

# Inicializa o aplicativo
ft.app(target=main)
