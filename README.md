# 4 Cavalos Backtracking

## Apresentação

Este repositório apresenta uma implementação do problema dos 4 cavalos utilizando a técnica de `backtracking`, escrita inteiramente em `Python`. O movimento das peças é restrito ao sentido horário do ciclo, o que reduz bastante o espaço de busca e permite encontrar a solução ótima (16 movimentos) com poucos retrocessos.

O material encontra-se organizado em três partes principais:

- `backtracking.py`: implementação do algoritmo de backtracking;
- `backtracking_cavalos.py`: script que executa o algoritmo e gera `passos.json` a partir dele;
- `index.html` e `passos.json`: aplicação web estática para visualização passo a passo da solução encontrada.

## Compatibilidade

As instruções deste documento contemplam os seguintes ambientes:

- `macOS`;
- `Linux`;
- `Windows` com `WSL` ou `Python` instalado nativamente.

## Requisitos

Para a execução do projeto, é necessário apenas:

- `Python 3` instalado e acessível pelo terminal.

Não há dependências externas — o projeto usa somente a biblioteca padrão do Python.

## Execução Do Algoritmo

### Rodar a busca e ver o resumo/trilha no terminal

```bash
python3 backtracking.py
```

Imprime o resumo da execução (total de impasses, retrocessos e passos) e o caminho completo da solução, estado a estado.

### Gerar os dados consumidos pela aplicação web

```bash
python3 backtracking_cavalos.py
```

Executa o mesmo algoritmo de `backtracking.py` e regera o arquivo `passos.json` — rode este comando sempre que alterar `backtracking.py`.

## Execução Da Aplicação Web

A aplicação web é **estática**: `index.html` lê os dados de `passos.json` via `fetch`. Por isso, não pode ser aberta diretamente com duplo clique (o navegador bloqueia `fetch` em arquivos `file://`) — é preciso servir os arquivos por HTTP, mesmo que localmente.

```bash
python3 -m http.server 8000
```

Em seguida, acesse no navegador:

```text
http://localhost:8000/index.html
```

Se a porta `8000` estiver ocupada, basta trocar por outra:

```bash
python3 -m http.server 8010
```

## Estrutura Do Projeto

```text
.
├── index.html
├── passos.json
├── backtracking.py
├── backtracking_cavalos.py
└── README.md
```
