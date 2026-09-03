# Implementação na API — seleção automática ou por endereço no Inventário Geral

## Objetivo

Alterar o endpoint existente `POST /contagem_inventario` para permitir duas formas de iniciar ou retomar uma contagem:

1. **Seleção automática:** o cliente envia somente filial e matrícula, e a API escolhe o próximo endereço disponível segundo a ordenação atual.
2. **Seleção por endereço:** o cliente também envia `codendereco`, e a API tenta iniciar especificamente a OS desse endereço.

A mudança deve ser retrocompatível com o WMS Mobile atual. O formato de `dados_os` e todas as ações já atendidas pelo endpoint devem continuar funcionando.

## Escopo desta tarefa

Projeto da API:

```text
/Users/thalissonmanoel/Documents/GitHub/SistemaRally
```

Arquivo principal:

```text
app/routes/routes_wmsMobile.py
```

Endpoint:

```text
POST /contagem_inventario
```

Não alterar o aplicativo `WmsRallyMobile` nesta tarefa. Não criar tabelas nem migrations. Reutilizar `INVENTARIOC`, `CADASTROENDERECO` e o formato de resposta existentes.

## Comportamento atual que deve ser preservado

Atualmente, uma chamada inicial sem `action`:

```json
{
  "codfilial": 1,
  "matricula": 1234
}
```

faz o seguinte:

1. Procura uma OS ainda não finalizada atribuída ao funcionário.
2. Se encontrar, retorna essa OS com HTTP `202`.
3. Caso contrário, escolhe automaticamente a próxima OS que ainda não foi iniciada.
4. Preenche `INVENTARIOC.CODFUNC` e `INVENTARIOC.DATAINICIOCONTAGEM`.
5. Retorna a OS no campo `dados_os` com HTTP `200`.

As ações existentes `validar_codbarra`, `confirmar_quantidade`, `editar_contagem` e `finalizar_contagem` não podem sofrer regressão.

## Novo contrato da chamada inicial

### 1. Seleção automática

O payload atual permanece válido:

```http
POST /contagem_inventario
Content-Type: application/json
```

```json
{
  "codfilial": 1,
  "matricula": 1234
}
```

A API deve escolher o próximo endereço disponível usando exatamente a ordenação automática já existente.

### 2. Seleção por código de endereço

O novo campo `codendereco` é opcional:

```http
POST /contagem_inventario
Content-Type: application/json
```

```json
{
  "codfilial": 1,
  "matricula": 1234,
  "codendereco": 98765
}
```

Quando `codendereco` for informado, a API não deve escolher outro endereço. Ela deve procurar exclusivamente uma OS desse endereço, na filial informada, que pertença ao inventário elegível e ainda não tenha sido iniciada nem finalizada.

O campo poderá chegar como número ou string numérica. Normalizar e validar sem montar SQL por interpolação; continuar usando bind variables do Oracle.

### Formato de `dados_os`

Preservar o array posicional atualmente consumido pelo aplicativo:

```text
dados_os[0][0] = NUMINVENTARIO
dados_os[0][1] = NUMOS
dados_os[0][2] = CODENDERECO
dados_os[0][3] = MODULO
dados_os[0][4] = RUA
dados_os[0][5] = EDIFICIO
dados_os[0][6] = NIVEL
dados_os[0][7] = APTO
```

Não renomear `dados_os` e não transformar essa estrutura em objeto nesta alteração.

## Regras de negócio

### Validação obrigatória

Na chamada inicial, validar:

- `codfilial` obrigatório e numérico;
- `matricula` obrigatória e numérica, respeitando o tipo que o banco já utiliza;
- `codendereco`, quando enviado, obrigatório após normalização e numérico;
- corpo JSON ausente ou inválido deve produzir resposta controlada, sem exceção não tratada.

Usar HTTP `400` para payload inválido.

### OS pendente do próprio funcionário

Antes de iniciar uma nova OS, verificar se o funcionário já possui contagem iniciada e não finalizada.

- Na seleção automática, manter o comportamento atual: retornar a OS pendente com HTTP `202`.
- Na seleção manual, se a OS pendente for exatamente do `codendereco` solicitado, retorná-la com HTTP `202`, permitindo retomar a contagem.
- Na seleção manual, se a OS pendente for de outro endereço, não iniciar uma segunda OS. Retornar HTTP `409`, incluir a OS pendente em `dados_os` e informar que ela precisa ser concluída antes de iniciar outro endereço.

Exemplo:

```json
{
  "dados_os": [[100, 200, 12345, 1, 2, 3, 4, 5]],
  "mensagem": "Existe outro endereço pendente para este funcionário.",
  "codigo": "OS_PENDENTE"
}
```

Essa regra é necessária porque o aplicativo atual trabalha somente com `dados_os[0]` e não gerencia várias contagens simultâneas.

### Endereço solicitado disponível

Para ser iniciado, o registro de `INVENTARIOC` deve atender simultaneamente a:

```sql
c.codfilial = :codfilial
c.codendereco = :codendereco
c.datainiciocontagem IS NULL
c.datafimcontagem IS NULL
```

Além disso, selecionar somente o inventário que esteja elegível/aberto conforme as regras já existentes no banco/projeto. Antes de implementar, verificar no próprio projeto ou esquema qual campo identifica o inventário aberto. Não criar uma nova regra arbitrária. Se não existir filtro adicional hoje, documentar isso no código/testes e preservar o comportamento atual.

Se mais de uma OS elegível existir para o mesmo endereço, a escolha deve ser determinística, usando ao menos `NUMOS ASC`, e retornar apenas uma linha.

### Endereço indisponível

Quando houver `codendereco` e nenhuma OS disponível for encontrada, distinguir, por consulta parametrizada, os seguintes cenários:

- endereço não pertence a nenhuma OS elegível do inventário/filial: HTTP `404`, código `ENDERECO_NAO_ENCONTRADO`;
- contagem do endereço já foi finalizada: HTTP `409`, código `ENDERECO_FINALIZADO`;
- endereço já foi iniciado por outro funcionário: HTTP `409`, código `ENDERECO_INDISPONIVEL`.

Exemplos:

```json
{
  "dados_os": [],
  "mensagem": "Endereço não encontrado no inventário aberto.",
  "codigo": "ENDERECO_NAO_ENCONTRADO"
}
```

```json
{
  "dados_os": [],
  "mensagem": "Este endereço já foi iniciado por outro funcionário.",
  "codigo": "ENDERECO_INDISPONIVEL"
}
```

```json
{
  "dados_os": [],
  "mensagem": "A contagem deste endereço já foi finalizada.",
  "codigo": "ENDERECO_FINALIZADO"
}
```

Na seleção automática, se não existir nenhuma OS disponível, manter `dados_os: []`, mas retornar uma mensagem clara como `Nenhum endereço disponível para contagem`. Preservar o status esperado pelo cliente atual se houver dependência confirmada; caso contrário, usar `404` como já ocorre hoje.

## Alterações de implementação

### 1. Ler o parâmetro opcional

No início de `contagem_inventario()`, passar a obter:

```python
payload = request.get_json(silent=True) or {}
codfilial = payload.get("codfilial")
matricula = payload.get("matricula")
codendereco = payload.get("codendereco")
action = payload.get("action")
```

Aplicar as novas validações somente ao ramo de início/busca. Não exigir `codfilial`, `matricula` ou `codendereco` indevidamente das ações existentes que hoje possuem contratos diferentes.

### 2. Separar busca automática da busca por endereço

Refatorar a função interna atual `consultar_os(codfilial)` para deixar explícitos os dois modos. Pode ser uma função com parâmetro opcional ou duas funções, por exemplo:

```python
consultar_proxima_os(codfilial)
consultar_os_por_endereco(codfilial, codendereco)
```

Na busca automática, preservar a ordenação atual por módulo, paridade/número do apartamento, rua, edifício e nível.

Na busca manual, aplicar `c.codendereco = :codendereco` e não executar a seleção automática como fallback. Se o endereço solicitado não estiver disponível, nunca devolver silenciosamente outro endereço.

### 3. Tornar a atribuição atômica e segura contra concorrência

Hoje a API consulta uma OS e depois executa um `UPDATE` que não confirma se ela continua livre. Dois operadores podem selecionar a mesma OS e o segundo sobrescrever `CODFUNC`.

Alterar `update_inicioContagem` para receber também `codendereco` e proteger o `UPDATE`:

```sql
UPDATE inventarioc c
SET c.codfunc = :matricula,
    c.datainiciocontagem = SYSDATE
WHERE c.codfilial = :codfilial
  AND c.numinventario = :numinventario
  AND c.numos = :numos
  AND c.codendereco = :codendereco
  AND c.datainiciocontagem IS NULL
  AND c.datafimcontagem IS NULL
  AND c.codfunc IS NULL
```

Regras do resultado:

- `cursor.rowcount == 1`: fazer `commit` e retornar sucesso;
- `cursor.rowcount == 0`: fazer `rollback` e tratar como conflito; nunca retornar HTTP `200`;
- exceção Oracle: fazer `rollback`, registrar o erro tecnicamente e retornar uma resposta controlada;
- não retornar apenas uma string de sucesso/erro da função interna: retornar um resultado inequívoco que permita ao endpoint escolher o HTTP correto.

Para a seleção manual, falha de concorrência deve retornar `409 ENDERECO_INDISPONIVEL`.

Para a seleção automática, caso outra sessão capture a OS entre o `SELECT` e o `UPDATE`, repetir de forma limitada a escolha do próximo endereço disponível. Não criar loop infinito. Outra opção válida é fazer seleção e atribuição na mesma transação com bloqueio Oracle adequado, desde que não mantenha locks além do necessário.

Não fazer `commit` do início antes de confirmar `rowcount == 1`.

### 4. Preservar e melhorar o retorno

Sucesso por busca manual:

```json
{
  "dados_os": [[100, 200, 98765, 1, 2, 3, 4, 5]],
  "mensagem": "Contagem iniciada com sucesso.",
  "modo_busca": "manual"
}
```

Sucesso por busca automática:

```json
{
  "dados_os": [[100, 200, 98765, 1, 2, 3, 4, 5]],
  "mensagem": "Contagem iniciada com sucesso.",
  "modo_busca": "automatico"
}
```

`modo_busca` é um campo novo opcional para facilitar diagnóstico; o aplicativo atual pode ignorá-lo. O campo `dados_os` continua obrigatório nas respostas desse fluxo.

### 5. Gerenciamento de conexão e cursor

Revisar as funções tocadas para evitar referências a `cursor` ou `conn` no `finally` antes de terem sido criados. Inicializar como `None` ou usar o padrão de gerenciamento adotado no projeto.

Não fechar a mesma conexão/cursor em vários pontos do mesmo caminho. Garantir `rollback` em falhas de escrita e fechamento no `finally`.

## Fluxo final esperado

```text
Recebe chamada inicial
        |
        v
Valida codfilial, matricula e codendereco opcional
        |
        v
Consulta OS pendente do funcionário
        |
        +-- mesma OS solicitada --> retorna 202 para retomada
        |
        +-- outra OS pendente ----> retorna 409 OS_PENDENTE
        |
        v
codendereco foi informado?
        |
        +-- sim --> busca exclusivamente o endereço solicitado
        |
        +-- não --> seleciona automaticamente o próximo
        |
        v
Tenta atribuir com UPDATE condicional
        |
        +-- rowcount 1 --> commit e retorna dados_os
        |
        +-- rowcount 0 --> rollback e trata concorrência
```

## Cuidados para não causar regressões

- Não criar novo endpoint se o mesmo contrato puder ser estendido com `codendereco` opcional.
- Não modificar o formato posicional de `dados_os`.
- Não alterar os contratos de leitura de código de barras, quantidade, edição, resumo ou finalização.
- Não remover a retomada de OS pendente.
- Não permitir que a busca manual caia na automática quando o endereço solicitado falhar.
- Não permitir iniciar uma segunda OS enquanto o funcionário possui outra pendente.
- Não permitir sobrescrever `CODFUNC` de uma contagem já iniciada.
- Não usar SQL com interpolação de valores.
- Não criar tabela, coluna ou migration.
- Manter a alteração concentrada no fluxo de Inventário Geral.

## Testes obrigatórios

Adicionar testes automatizados no padrão disponível no projeto. Se não houver infraestrutura de testes para essa rota, criar ao menos testes unitários do fluxo com conexão/cursor Oracle mockados e documentar como executá-los.

Cobrir no mínimo:

1. Payload sem `codendereco` seleciona automaticamente e mantém a ordenação existente.
2. Payload com `codendereco` seleciona exatamente o endereço solicitado.
3. Endereço manual inexistente retorna `404 ENDERECO_NAO_ENCONTRADO`.
4. Endereço manual já finalizado retorna `409 ENDERECO_FINALIZADO`.
5. Endereço manual iniciado por outro funcionário retorna `409 ENDERECO_INDISPONIVEL`.
6. OS pendente do próprio funcionário é retomada com `202`.
7. Busca manual da mesma OS pendente retorna essa OS com `202`.
8. Busca manual de outro endereço com OS pendente retorna `409 OS_PENDENTE` e não altera o banco.
9. `UPDATE` com `rowcount == 0` não retorna sucesso e executa rollback.
10. Duas tentativas concorrentes não deixam dois funcionários iniciarem a mesma OS.
11. Falta de `codfilial` ou `matricula` na chamada inicial retorna `400`.
12. `codendereco` inválido retorna `400`.
13. O formato e a ordem dos oito campos de `dados_os` permanecem iguais.
14. As ações `validar_codbarra`, `confirmar_quantidade`, `editar_contagem` e `finalizar_contagem` continuam chegando aos seus ramos corretos.

## Critérios de aceite

A tarefa da API estará concluída quando:

- o payload antigo continuar selecionando automaticamente o próximo endereço;
- o payload com `codendereco` iniciar somente o endereço solicitado;
- uma OS pendente puder ser retomada;
- outra OS não puder ser iniciada enquanto houver pendência do funcionário;
- endereço inexistente, finalizado ou ocupado produzir respostas distintas e controladas;
- uma disputa entre operadores não puder sobrescrever a atribuição da OS;
- `dados_os` continuar compatível com o aplicativo atual;
- nenhuma ação existente do endpoint sofrer regressão;
- os testes relevantes passarem;
- o agente informar os arquivos alterados, comandos de validação executados e qualquer ponto que não tenha conseguido validar contra um Oracle real.

## Fora do escopo

Depois que esta API estiver implementada e validada, o `WmsRallyMobile` será alterado separadamente para oferecer:

- campo para digitar ou ler o código do endereço;
- ação para buscar esse endereço específico;
- ação para solicitar o próximo endereço automaticamente;
- tratamento das respostas `OS_PENDENTE`, `ENDERECO_NAO_ENCONTRADO`, `ENDERECO_INDISPONIVEL` e `ENDERECO_FINALIZADO`.

Não implementar essa interface no projeto da API.
