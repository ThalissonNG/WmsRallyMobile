import toml
import os

# Configurações gerais
toml.load
base_url = "http://192.168.1.100:5000/wmsMobile"
user_info = {}
colorVariaveis = {
    'botaoAcao': "#0366FF",
    'texto': "#ffffff",
    'textoPreto': "#000000",
    'bordarInput': "#0a0a0a",
    'icones': "#ffffff",
    'titulo': "#4f4ce5",
    'sucesso': "#10b650",
    'erro': "#ff0000",
    'restante': "#ffb300"
}

# Determina a raiz do projeto (duas pastas acima de config.py)
ROOT_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),  # routes/config
        os.pardir,                    # routes
        os.pardir                     # projeto raiz
    )
)

# Carrega versão direto do pyproject.toml na raiz
_py = toml.load(os.path.join(ROOT_DIR, "pyproject.toml"))
app_version = _py.get("project", {}).get("version")
