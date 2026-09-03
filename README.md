# 4 Cavalos Backtracking

## Apresentação

Este repositório apresenta uma implementação do problema dos 4 cavalos utilizando a técnica de `backtracking`. A solução principal foi desenvolvida em `C++`, enquanto scripts auxiliares em `Python` foram incluídos para facilitar a execução do algoritmo e a visualização dos estados intermediários.

O material encontra-se organizado em três partes principais:

- `solver.cpp`: implementação do algoritmo em C++;
- `backtracking_cavalos.py`: script que compila e executa automaticamente o programa em C++;
- `backtracking_app/`: aplicação web em Python para visualização passo a passo da solução encontrada;
- `index.html` e `passos.json`: versão estática da visualização, adequada para deploy no Vercel.

## Compatibilidade

As instruções deste documento contemplam os seguintes ambientes:

- `macOS`;
- `Linux`;
- `Windows` com `MinGW`;
- `Windows` com `WSL`.

## Requisitos

Para a execução do projeto, é necessário que o ambiente possua:

- um compilador `g++` com suporte ao padrão `C++17`;
- `Python 3` instalado e acessível pelo terminal.

## Execução Do Algoritmo Pelo Script Python

O modo mais simples de utilizar o projeto consiste em executar o script Python localizado na raiz do repositório. Esse script compila o arquivo `solver.cpp`, executa o binário gerado e imprime no terminal todos os estados da solução.

### macOS e Linux

```bash
python3 backtracking_cavalos.py
```

### Windows com MinGW

```bash
python backtracking_cavalos.py
```

Caso o comando acima não esteja disponível, pode-se utilizar:

```bash
py backtracking_cavalos.py
```

### Windows com WSL

```bash
python3 backtracking_cavalos.py
```

## Compilação E Execução Manual Do Programa Em C++

Também é possível compilar e executar diretamente o código-fonte em `C++`, sem utilizar o script Python.

### macOS e Linux

```bash
g++ -std=c++17 solver.cpp -o solver
./solver
```

### Windows com MinGW

```bash
g++ -std=c++17 solver.cpp -o solver.exe
solver.exe
```

### Windows com WSL

```bash
g++ -std=c++17 solver.cpp -o solver
./solver
```

## Execução Da Aplicação Web

A aplicação web foi desenvolvida com o objetivo de apresentar, de maneira visual, cada passo produzido pelo algoritmo.

### macOS e Linux

```bash
cd backtracking_app
python3 app.py
```

Em seguida, deve-se acessar no navegador:

```text
http://127.0.0.1:8000
```

Se a porta `8000` estiver ocupada, pode-se iniciar o servidor em outra porta:

```bash
PORT=8010 python3 app.py
```

Depois disso, basta abrir:

```text
http://127.0.0.1:8010
```

### Windows com MinGW

```bash
cd backtracking_app
python app.py
```

Se necessário, o comando também pode ser executado como:

```bash
cd backtracking_app
py app.py
```

O acesso deve ser feito pelo navegador no endereço:

```text
http://127.0.0.1:8000
```

Caso a porta `8000` esteja em uso:

```bash
cd backtracking_app
set PORT=8010 && python app.py
```

### Windows com WSL

```bash
cd backtracking_app
python3 app.py
```

Depois, acesse:

```text
http://127.0.0.1:8000
```

## Deploy Estático No Vercel

O repositório também contém uma versão estática da interface, composta pelos arquivos `index.html` e `passos.json` na raiz do projeto. Essa versão não depende de servidor Python e pode ser publicada diretamente no Vercel.

Para realizar o deploy:

1. envie o repositório para o GitHub;
2. importe o projeto no painel do Vercel;
3. mantenha a configuração padrão, sem necessidade de framework específico;
4. conclua o deploy.

Como a aplicação estática lê os dados diretamente de `passos.json`, não há necessidade de configurar funções serverless, compilação em tempo de execução ou backend adicional.

## Estrutura Do Projeto

```text
.
├── index.html
├── passos.json
├── solver.cpp
├── backtracking_cavalos.py
├── README.md
└── backtracking_app/
    ├── app.py
    └── index.html
```
