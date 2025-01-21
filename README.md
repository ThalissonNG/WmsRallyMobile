# WMS Rally Mobile

Este projeto foi desenvolvido para a aplicação **WMS Rally Mobile**, utilizando o Flet e Flutter. Siga as etapas abaixo para configurar o ambiente de desenvolvimento e instalar as dependências necessárias.

## Requisitos

Antes de começar, você precisará instalar as seguintes ferramentas:

1. **Flutter** versão 3.24.5  
2. **Java JDK** versão 11.0.21  
3. **Android Studio** versão mais recente

## Passo a passo

### 1. Instalar o Flutter versão 3.24.5

Baixe a versão 3.24.5 do Flutter no seguinte link:

- [Flutter SDK - versão 3.24.5](https://flutter-ko.dev/development/tools/sdk/releases)

Após o download, extraia o arquivo em um diretório de sua escolha e adicione o Flutter à variável de ambiente `PATH` para garantir que o comando `flutter` esteja disponível no terminal.

### 2. Instalar o Java JDK versão 11.0.21

Baixe o JDK versão 11.0.21 no link abaixo:

- [Java JDK 11.0.21](https://www.oracle.com/br/java/technologies/javase/jdk11-archive-downloads.html)

Após a instalação, adicione o JDK ao `PATH` e configure a variável de ambiente `JAVA_HOME`.

### 3. Instalar o Android Studio

Baixe a versão mais recente do Android Studio:

- [Android Studio](https://developer.android.com/studio?hl=pt-br)

Siga o assistente de instalação do Android Studio e certifique-se de que todos os componentes necessários, como o Android SDK e o emulador, sejam instalados.

### 4. Criar o Projeto Flutter

Crie um novo projeto Flutter utilizando o comando abaixo (não é necessário detalhar este passo, pois o comando é simples):


```bash
flutter create wms_rally_mobile
```
### 5. Criar o Ambiente Virtual

1. Navegue até a pasta do projeto recém-criado:

    ```bash
    cd wms_rally_mobile
    ```

2. Crie o ambiente virtual para o projeto com o seguinte comando:

    ```bash
    python -m venv venv
    ```

3. Ative o ambiente virtual:

   - **No Windows**:

    ```bash
    venv\Scripts\activate
    ```

   - **No macOS/Linux**:

    ```bash
    source venv/bin/activate
    ```

### 6. Instalar o Flet versão 0.24.0

1. No diretório do projeto, crie o arquivo `requirements.txt` com o seguinte conteúdo:

    ```txt
    flet==0.24.0
    ```

2. Instale as dependências utilizando o comando:

    ```bash
    pip install -r requirements.txt
    ```

Agora, o **Flet versão 0.24.0** estará instalado e pronto para ser utilizado no seu projeto.