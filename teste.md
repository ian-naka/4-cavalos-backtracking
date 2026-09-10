# Material de Estudo — Projeto e Análise de Algoritmos (CSI546)
### Conteúdo necessário para resolver a Lista 1

---

## Sumário

1. [Prova por Indução Matemática](#1-prova-por-indução-matemática)
2. [Invariante de Laço](#2-invariante-de-laço)
3. [Notação Assintótica (O, Ω, Θ)](#3-notação-assintótica-o-ω-θ)
4. [Contando Operações em Algoritmos](#4-contando-operações-em-algoritmos)
5. [Análise Empírica de Algoritmos](#5-análise-empírica-de-algoritmos)
6. [Como Projetar um Algoritmo do Zero](#6-como-projetar-um-algoritmo-do-zero)
7. [Mapa: qual seção usar em cada questão da Lista 1](#7-mapa-qual-seção-usar-em-cada-questão-da-lista-1)

---

## 1. Prova por Indução Matemática

### 1.1 A ideia central

Indução matemática serve para provar que uma afirmação `P(n)` é verdadeira **para todo n** a partir de um certo ponto (geralmente n = 0 ou n = 1).

A lógica é a de dominós: se o primeiro dominó cai (**base**), e cada dominó que cai garante que o próximo também cai (**passo indutivo**), então todos os dominós caem.

A prova sempre tem **duas partes obrigatórias**:

| Parte | O que você faz |
|---|---|
| **Base** | Mostra que `P(n₀)` é verdadeira para o menor valor de n considerado. |
| **Passo indutivo** | Assume que `P(k)` é verdadeira (isso é a **hipótese de indução**, HI) e prova, a partir disso, que `P(k+1)` também é verdadeira. |

Se as duas partes fecham, `P(n)` vale para todo `n ≥ n₀`.

### 1.2 Exemplo completo e comentado

**Objetivo:** provar que, para todo n ≥ 0,

$$\sum_{i=0}^{n} i = \frac{n(n+1)}{2}$$

**Passo 1 — Base (n = 0):**

Lado esquerdo: $\sum_{i=0}^{0} i = 0$.
Lado direito: $\frac{0 \cdot 1}{2} = 0$.

Os dois lados batem. Base verificada. ✓

**Passo 2 — Hipótese de indução:**

Suponha que a fórmula vale para um certo `k`, ou seja, **assuma como verdadeiro**:

$$\sum_{i=0}^{k} i = \frac{k(k+1)}{2} \qquad \text{(HI)}$$

**Passo 3 — Tese (o que precisamos provar):**

Queremos mostrar que a fórmula também vale para `k+1`:

$$\sum_{i=0}^{k+1} i = \frac{(k+1)(k+2)}{2}$$

**Passo 4 — Demonstração do passo indutivo:**

O truque quase sempre é o mesmo: **separar o último termo da soma** para poder aplicar a hipótese de indução no que sobrou.

$$\sum_{i=0}^{k+1} i = \underbrace{\left(\sum_{i=0}^{k} i\right)}_{\text{aplico a HI aqui}} + (k+1)$$

Substituindo pela HI:

$$= \frac{k(k+1)}{2} + (k+1)$$

Colocando `(k+1)` em evidência:

$$= (k+1)\left(\frac{k}{2} + 1\right) = (k+1) \cdot \frac{k+2}{2} = \frac{(k+1)(k+2)}{2}$$

Que é exatamente a tese que queríamos provar. **∎ (fim da prova)**

### 1.3 O padrão que se repete (para Q2, Q3, Q4)

Toda prova de somatório por indução segue este roteiro:

1. Verifique a base substituindo `n` pelo menor valor.
2. Escreva a HI (a fórmula assumida verdadeira para `k`).
3. Escreva a tese (a fórmula que quer provar para `k+1`).
4. Separe o termo `k+1` da somatória.
5. Substitua a parte que sobrou pela HI.
6. Manipule algebricamente (fatorar, tirar MMC, etc.) até chegar exatamente na tese.

Só muda a álgebra do passo 6 — o "esqueleto" da prova é sempre este.

### 1.4 Provando desigualdades (para Q5 e Q6)

A estrutura é idêntica (base + passo indutivo), mas em vez de igualdade você trabalha com `≥` ou `≤`. A ferramenta mais usada é a **transitividade**:

> Se $A \geq B$ e $B \geq C$, então $A \geq C$.

**Exemplo de raciocínio (Bernoulli, Q5):** para provar $(1+x)^{k+1} \geq 1 + (k+1)x$, você parte de $(1+x)^{k+1} = (1+x)^k \cdot (1+x)$, usa a HI para trocar $(1+x)^k$ por algo $\geq 1+kx$ (cuidado: só pode multiplicar a desigualdade por $(1+x)$ mantendo o sentido se $(1+x) > 0$ — por isso o enunciado exige $x > -1$), expande o produto e mostra que o resultado é $\geq 1 + (k+1)x$, descartando um termo que sabe ser não-negativo.

**Dica geral para desigualdades por indução:** sempre que multiplicar ambos os lados de uma desigualdade por uma expressão, confirme que essa expressão é positiva — senão a desigualdade inverte.

---

## 2. Invariante de Laço

### 2.1 Por que existe esse método

Testes mostram que um algoritmo funciona *para os casos testados*. Para provar que funciona **sempre**, usamos uma técnica análoga à indução matemática, mas aplicada a laços (`for`, `while`): o **invariante de laço**.

Um invariante é uma **afirmação sobre o estado das variáveis do programa** que permanece verdadeira toda vez que o laço está prestes a começar uma nova iteração.

### 2.2 As três etapas obrigatórias

Para provar a corretude de um algoritmo com laço, você sempre faz:

| Etapa | O que prova |
|---|---|
| **1. Inicialização** | O invariante é verdadeiro **antes** da primeira iteração. |
| **2. Manutenção** | **Se** o invariante é verdadeiro no início de uma iteração, **então** ele continua verdadeiro no início da próxima iteração (ou seja: o corpo do laço não estraga a propriedade). |
| **3. Conclusão (Término)** | Quando o laço termina (a condição de parada falha), usamos o invariante + a condição de parada para concluir que o algoritmo produziu o resultado correto. |

Note o paralelo com indução matemática:
- Inicialização ↔ Base
- Manutenção ↔ Passo indutivo
- Conclusão é o "bônus" específico de invariantes: usa a condição de parada do laço para fechar o argumento.

### 2.3 Exemplo completo — encontrar o menor elemento (base para a Q7)

```
menor(A[1..n]):
    m = A[1]
    for i = 2 to n:
        if A[i] < A[m_valor]:   // comparando valores
            m = i               // (ou guardando o valor, dependendo da versão)
    return m
```

**Definição do invariante:**
> No início de cada iteração `i` do laço, a variável `m` contém o índice (ou valor) do **menor elemento entre A[1..i-1]**.

**1. Inicialização:**
Antes da primeira execução do laço, `i = 2`, e `m = A[1]`. O subvetor `A[1..i-1] = A[1..1]` tem um único elemento, que é trivialmente o menor dele mesmo. Invariante verdadeiro. ✓

**2. Manutenção:**
Suponha que o invariante vale no início de uma iteração `i`: `m` é o menor de `A[1..i-1]`.
No corpo do laço, comparamos `A[i]` com o valor guardado em `m`:
- Se `A[i] < m`, atualizamos `m` para `A[i]` — agora `m` é o menor de `A[1..i]`.
- Se não, `m` continua sendo o mesmo — e como `m` já era ≤ todos de `A[1..i-1]` e `A[i] ≥ m`, `m` continua sendo o menor de `A[1..i]`.

Em ambos os casos, ao final da iteração (quando `i` é incrementado), o invariante vale para o próximo `i`. ✓

**3. Conclusão:**
O laço termina quando `i = n+1` (a condição `i ≤ n` falha). Pelo invariante, nesse momento `m` é o menor elemento de `A[1..i-1] = A[1..n]` — ou seja, o vetor inteiro. Logo o algoritmo está correto. ∎

### 2.4 Checklist para aplicar em qualquer algoritmo (útil para a Q7 e outros exercícios de projeto)

Ao construir a prova, pergunte-se:
1. **O que já está "resolvido" ou "garantido"** no prefixo do vetor/estrutura processado até agora? Essa é a sua candidata a invariante.
2. A invariante é verdadeira **antes de qualquer iteração acontecer** (com os valores iniciais das variáveis)?
3. O corpo do laço, ao processar mais um elemento, **preserva** essa propriedade?
4. Quando o laço para, a invariante + condição de parada **implicam exatamente** o que o algoritmo promete devolver?

---

## 3. Notação Assintótica (O, Ω, Θ)

### 3.1 A ideia intuitiva (mais importante que a fórmula com quantificadores)

Quando comparamos algoritmos, não importa o tempo exato — importa **como o tempo cresce** quando a entrada cresce. As notações assintóticas classificam funções por essa taxa de crescimento:

| Notação | Significado intuitivo | Tipo de limite |
|---|---|---|
| `f(n) ∈ O(g(n))` | f cresce **no máximo** tão rápido quanto g | limite **superior** |
| `f(n) ∈ Ω(g(n))` | f cresce **no mínimo** tão rápido quanto g | limite **inferior** |
| `f(n) ∈ Θ(g(n))` | f cresce **na mesma ordem** que g (O e Ω juntos) | limite **justo** |
| `f(n) ∈ o(g(n))` | f cresce **estritamente mais devagar** que g | superior estrito |
| `f(n) ∈ ω(g(n))` | f cresce **estritamente mais rápido** que g | inferior estrito |

### 3.2 Como provar `f(n) ∈ O(g(n))` na prática

**Definição formal:** existe uma constante `c > 0` e um `n₀` tais que, para todo `n ≥ n₀`:

$$0 \leq f(n) \leq c \cdot g(n)$$

**Na prática, a tarefa é: ache um `c` e um `n₀` que façam a desigualdade acima ser verdadeira.** Você não precisa provar que são os "melhores" valores, só que existem valores que funcionam.

**Exemplo 1 — provar que `n ∈ O(n²)`:**

Escolha `c = 1` e `n₀ = 1`. Para todo `n ≥ 1`:
$$n \leq 1 \cdot n^2 \quad \Leftrightarrow \quad n \leq n^2 \quad \Leftrightarrow \quad 1 \leq n$$
que é verdade para todo `n ≥ 1`. Como achamos `c` e `n₀` que funcionam, está provado. ∎

**Exemplo 2 — provar que `√n ∈ O(n)`:**

Escolha `c = 1` e `n₀ = 1`. Para `n ≥ 1`, queremos $\sqrt{n} \leq n$. Elevando ambos os lados ao quadrado (válido pois ambos são não-negativos): $n \leq n^2$, que já sabemos ser verdade para `n ≥ 1`. ∎

**Exemplo 3 — provar que `lg(n!) ∈ O(n·lg(n))`:**

Aqui usamos uma cota conhecida: $n! \leq n^n$. Aplicando log dos dois lados:
$$\lg(n!) \leq \lg(n^n) = n \lg(n)$$
Isso já é a desigualdade que precisamos, com `c = 1` e `n₀ = 1`. ∎

*(Um resultado mais fino usaria a aproximação de Stirling, mas para O(n·lg n) essa cota simples basta.)*

### 3.3 Propriedades úteis (evitam refazer a prova do zero)

- **Reflexividade:** `f(n) ∈ O(f(n))` — trivial, use `c = 1`.
- **Transitividade:** se `f ∈ O(g)` e `g ∈ O(h)`, então `f ∈ O(h)`. Permite encadear comparações sem refazer a definição.
- **Simetria (só para Θ):** `f ∈ Θ(g)` ⟺ `g ∈ Θ(f)`.
- **Simetria transposta:** `f ∈ O(g)` ⟺ `g ∈ Ω(f)`.

### 3.4 Regra prática que resolve a maioria dos casos rapidamente

> **Em uma soma de termos, a notação assintótica é dominada pelo termo de maior ordem de crescimento — os demais termos e as constantes multiplicativas são descartados.**

Exemplo: $3n^2 + 5n + 2 \in \Theta(n^2)$, porque para `n` grande o termo `n²` domina completamente os outros. Isso é extremamente útil para resolver rapidamente exercícios de análise de laços (seção 4).

---

## 4. Contando Operações em Algoritmos

### 4.1 A técnica geral

Para descobrir a complexidade de um trecho de código, você conta **quantas vezes cada operação relevante é executada**, em função do tamanho da entrada `n`, e depois soma tudo.

### 4.2 Casos-padrão

**Laço simples:**
```c
for (i = 0; i < n; i++) {
    A();   // executa n vezes
}
```
→ Custo: **Θ(n)**

**Laços aninhados independentes** (o laço interno não depende do índice do externo):
```c
for (i = 0; i < n; i++) {
    for (j = 0; j < n; j++) {
        A();   // n × n execuções
    }
}
```
→ Custo: **Θ(n²)**

**Laços aninhados dependentes (padrão "triangular")** — muito comum em problemas de pares/triplas:
```c
for (i = 0; i < n; i++) {
    for (j = i+1; j < n; j++) {
        A();
    }
}
```
Aqui, para cada `i`, o laço interno executa `(n - i - 1)` vezes. O total de execuções de `A()` é:

$$\sum_{i=0}^{n-1} (n - i - 1)$$

Essa é uma soma aritmética — da mesma família das somas provadas por indução na Seção 1! Resolvendo, o resultado é da ordem de $\frac{n(n-1)}{2}$, ou seja:

→ Custo: **Θ(n²)**

**Três laços aninhados no mesmo padrão** (como o algoritmo de força bruta para triplas que somam zero, ou para ternos pitagóricos da Q9):

→ Custo: **Θ(n³)**

### 4.3 Contando uma operação específica (útil para a Q9, Q16, Q17)

Às vezes a pergunta não é "quantas instruções no total", mas "quantas vezes uma operação específica ocorre" (ex: multiplicações, comparações, incrementos).

**Método:** identifique a linha onde a operação de interesse acontece, descubra em função de quê ela é executada (dentro de qual laço, com que condição), e monte o somatório correspondente — geralmente recaindo em uma soma aritmética ou geométrica conhecida.

**Exemplo (baseado no problema de avaliação de polinômios, Q17):**
```c
float pwr(float b, int e) {
    float r = b;
    for (i = 1; i < e; i++) { r = r * b; }  // e-1 multiplicações
    return r;
}

float eval(float *a, int n, float x) {
    float s = a[0];
    for (i = 1; i < n; i++) {
        s = s + a[i] * pwr(x, i);   // 1 multiplicação aqui + (i-1) dentro de pwr(x,i)
    }
    return s;
}
```
Para cada `i` no laço de `eval`, o número de multiplicações é `1 + (i - 1) = i`. Somando de `i = 1` até `n-1`:

$$\sum_{i=1}^{n-1} i = \frac{(n-1)n}{2} \in \Theta(n^2)$$

Isso mostra que a versão ingênua é **quadrática** em multiplicações. A regra de Horner (Q17-b) reorganiza os cálculos para fazer apenas **uma** multiplicação por termo, chegando em Θ(n) — um exemplo de como a mesma tarefa pode ter complexidades bem diferentes dependendo do algoritmo escolhido.

### 4.4 Melhor caso, pior caso e caso médio

Quando o número de operações **depende dos valores de entrada** (não só do tamanho `n`), distinguimos três cenários:

- **Melhor caso:** a entrada mais favorável possível (ex.: já ordenado, ou o elemento buscado está na primeira posição).
- **Pior caso:** a entrada mais desfavorável possível — geralmente o que reportamos como "a complexidade do algoritmo", pois é a garantia mais forte.
- **Caso médio:** a expectativa sobre uma distribuição de entradas (requer alguma suposição sobre a distribuição, ex: todas as posições igualmente prováveis).

Isso é relevante para exercícios como o Q16, onde o número de incrementos de uma variável dentro de um `while` com condição depende dos valores concretos de entrada, não apenas de `n`.

---

## 5. Análise Empírica de Algoritmos

### 5.1 Quando e por que usar

Além da análise matemática (contar operações), podemos **medir o tempo de execução real** e inferir a complexidade a partir dos dados — útil quando o código é complexo demais para contar operações à mão, ou para **validar** uma análise teórica.

### 5.2 O método (passo a passo)

1. **Medir:** execute o algoritmo para vários tamanhos de entrada `N` (ex.: 1000, 2000, 4000, 8000...) e registre o tempo `T(N)`.
2. **Plotar em escala log-log:** se o algoritmo tem complexidade polinomial, ou seja, $T(N) \approx a \cdot N^b$, então:
$$\log(T(N)) \approx \log(a) + b \cdot \log(N)$$
Isso é a equação de uma **reta** no gráfico log(T) × log(N), com inclinação `b`. Quanto mais "reto" o gráfico em escala log-log, mais confiável é o modelo polinomial.
3. **Estimar o expoente `b`** (a classe de complexidade) usando dois pontos da tabela:

$$b \approx \frac{\log(T_2 / T_1)}{\log(N_2 / N_1)}$$

4. **Verificar (prever e confirmar):** use o modelo ajustado para prever `T` em um tamanho `N` que você ainda não mediu, execute de fato, e compare a previsão com o valor observado. Se forem próximos, o modelo está validado.

### 5.3 Exemplo resolvido (aplicável diretamente à Q15)

Tabela de tempos observados:

| N | 1000 | 2000 | ... | 10000 |
|---|---|---|---|---|
| T(N) | 11.996 | 24.303 | ... | 140.538 |

Usando os pontos extremos (N₁=1000, T₁=11.996) e (N₂=10000, T₂=140.538):

$$b \approx \frac{\log(140.538 / 11.996)}{\log(10000/1000)} = \frac{\log(11.72)}{\log(10)} \approx \frac{1.069}{1} \approx 1.07$$

O expoente está bem próximo de **1**, então o algoritmo é aproximadamente **linear**, ou seja, `T(N) ∈ Θ(N)`.

**Confirmação por outro caminho — a "regra da razão":** se o algoritmo é `Θ(N^b)`, dobrar `N` deve multiplicar `T` por aproximadamente `2^b`. Veja: de N=1000 para N=2000 (dobrou), o tempo foi de 11.996 para 24.303 — uma razão de $24.303/11.996 \approx 2.03$, bem próxima de $2^1 = 2$. Isso reforça que `b ≈ 1` (linear), e não `b ≈ 2` (o que daria razão ≈ 4) nem `b ≈ 3` (razão ≈ 8).

Essa "regra da razão" é uma forma rápida de estimar `b` sem nem precisar de logaritmo: basta ver quanto o tempo multiplica quando `N` dobra.

| Se dobrar N multiplica T por... | então b é aproximadamente... | classe |
|---|---|---|
| ~1 (quase não muda) | 0 | Θ(1) ou Θ(log n) |
| ~2 | 1 | Θ(n) |
| ~4 | 2 | Θ(n²) |
| ~8 | 3 | Θ(n³) |

### 5.4 Aspectos que afetam a medição (importante para discutir os resultados)

- **Independentes de sistema:** o algoritmo em si e os dados de entrada usados.
- **Dependentes de sistema:** hardware (CPU, memória, cache), software (compilador, coletor de lixo) e o estado geral da máquina (outros processos rodando).

Por isso, medições empíricas têm ruído — é normal que os pontos não formem uma reta perfeita, e é uma boa prática rodar cada medição algumas vezes e usar a média ou a mediana.

---

## 6. Como Projetar um Algoritmo do Zero

As seções anteriores ensinam a **analisar** um algoritmo que já existe: provar que está correto, calcular sua complexidade, medir seu tempo. Mas boa parte da lista pede algo diferente: **criar** o algoritmo antes de analisar qualquer coisa. Isso é uma habilidade separada — mais parecida com resolver um quebra-cabeça do que com aplicar uma fórmula — mas existem estratégias recorrentes que resolvem a maioria dos problemas de uma lista introdutória.

### 6.1 Antes de tudo: entenda o problema por completo

Antes de pensar em como resolver, tenha clareza absoluta sobre:
- **O que exatamente é a entrada** (um vetor de inteiros? um número natural? de que tamanho, com que restrições?).
- **O que exatamente é a saída esperada** (um índice? um valor? um booleano? uma contagem?).
- **Casos de borda:** o que acontece com entrada vazia, com um único elemento, com valores repetidos, com números negativos? Um algoritmo que "parece certo" mas quebra em um caso de borda não está pronto.

Fazer alguns exemplos manuais pequenos (à mão, no papel) antes de escrever qualquer pseudocódigo ajuda a enxergar o padrão da solução.

### 6.2 Estratégia 1 — Força bruta

A solução mais óbvia e ingênua: testar **todas** as possibilidades e escolher/contar as que satisfazem a condição pedida.

- Quase sempre é fácil de justificar que está **correta** (você literalmente verificou tudo).
- Costuma ser **lenta** (frequentemente Θ(n²) ou Θ(n³)), mas é um ótimo ponto de partida — e em vários exercícios da lista (ex.: contar ternos, achar a moda por comparação par a par) força bruta já é uma resposta válida, mesmo que não seja a mais eficiente.

**Como pensar:** "quais são todas as combinações possíveis de elementos/valores que eu preciso considerar?" e monte laços aninhados que cobrem exatamente essas combinações, sem repetir e sem faltar nenhuma.

### 6.3 Estratégia 2 — Varredura única (uma passada só)

Muitos problemas não precisam comparar tudo com tudo — dá para percorrer a entrada **uma única vez**, mantendo alguma informação parcial atualizada a cada passo.

**Pergunta-chave:** "que informação eu preciso guardar sobre o que já vi até agora, para decidir o que fazer com o próximo elemento?"

Esse é exatamente o padrão do algoritmo do menor elemento (Seção 2.3): a cada posição, só precisamos lembrar do menor valor visto até ali — não precisamos comparar todos os pares. Esse tipo de solução costuma ser Θ(n), bem mais eficiente que força bruta.

### 6.4 Estratégia 3 — Redução a um problema já resolvido

Às vezes o jeito mais simples de resolver um problema novo é transformá-lo em um problema que você já sabe resolver.

**Exemplo de raciocínio:** para achar a moda de um vetor (valor mais frequente), comparar cada elemento com todos os outros é força bruta Θ(n²). Mas se você **ordenar o vetor primeiro**, elementos iguais ficam agrupados lado a lado, e contar a maior sequência de repetidos vira uma varredura única — bem mais simples de raciocinar e, dependendo do algoritmo de ordenação usado, potencialmente mais eficiente no total.

Sempre vale perguntar: "isso fica mais fácil se eu ordenar primeiro? Se eu usar uma estrutura auxiliar (um vetor de contagem, por exemplo)?"

### 6.5 Estratégia 4 — Explorar uma propriedade matemática que corta trabalho

Às vezes existe uma característica matemática do problema que permite parar de testar muito antes do "óbvio".

**Exemplo clássico — testar se `n` é primo:** a solução ingênua testa todos os divisores de 2 até `n-1`. Mas repare: se `n = a × b` com `a ≤ b`, então necessariamente `a ≤ √n` (porque se ambos os fatores fossem maiores que `√n`, o produto seria maior que `n`). Ou seja, **basta testar divisores até √n** — se nenhum divide `n`, nenhum dos maiores vai dividir também. Isso reduz o algoritmo de Θ(n) para Θ(√n) sem mudar a lógica de fundo, só aproveitando essa observação.

Esse tipo de "sacada" costuma vir de examinar a estrutura matemática do problema, não de truques de programação.

### 6.6 Estratégia 5 — Busca binária quando existe monotonicidade

Se você percebe que uma condição é **monótona** (verdadeira até certo ponto e depois sempre falsa, ou vice-versa), não precisa testar valor por valor — pode cortar o espaço de busca pela metade a cada tentativa.

**Exemplo — raiz quadrada inteira de `n`:** queremos o maior `m` tal que `m² ≤ n`. A condição `m² ≤ n` é verdadeira para `m` pequeno e falsa para `m` grande — é monótona. Em vez de testar `m = 0, 1, 2, 3...` um por um (o que seria Θ(√n) testes), dá para fazer busca binária no intervalo `[0, n]`, testando o meio, decidindo para qual lado continuar, e chegando à resposta em Θ(log n) testes.

**Como reconhecer quando usar:** sempre que a resposta for "o maior/menor valor que satisfaz uma condição", e essa condição só "vira" de verdadeira para falsa (ou o contrário) uma única vez ao longo da faixa de valores possíveis, busca binária é candidata forte.

### 6.7 Roteiro prático para atacar uma questão de projeto

1. Entenda a entrada, a saída e os casos de borda (Seção 6.1).
2. Pense primeiro na força bruta — mesmo que não seja a resposta final, ela te dá confiança de que você entendeu o problema e serve de base de comparação.
3. Pergunte-se: dá pra resolver com uma única passada (6.3)? Ordenar ajuda (6.4)? Existe uma propriedade matemática que corta o espaço de busca (6.5)? A condição é monótona, permitindo busca binária (6.6)?
4. Escreva o pseudocódigo da solução escolhida.
5. **Só depois** de ter o algoritmo, aplique as ferramentas das seções anteriores: defina o invariante e prove a corretude (Seção 2), conte as operações e classifique a complexidade (Seção 4), e, se o exercício pedir, implemente e meça o tempo de execução (Seção 5).

## 7. Mapa: qual seção usar em cada questão da Lista 1

| Questão | Do que se trata | Seção deste material |
|---|---|---|
| Q1, Q2, Q3, Q4 | Provas de somatórios | Seção 1 (indução — siga o roteiro de 6 passos) |
| Q5, Q6 | Provas de desigualdades | Seção 1.4 |
| Q7 | Projetar + provar invariante para achar o menor elemento | Seção 6.3 (varredura única) para projetar, Seção 2 (checklist 2.4, exemplo 2.3) para provar |
| Q8 | Projetar solução de partição + implementação + medição de tempo + gráfico | Seção 6.2/6.3 para projetar, Seção 5 (análise empírica) para medir |
| Q9 | Projetar algoritmo de ternos + analisar complexidade + sensibilidade à entrada | Seção 6.2 (força bruta) para projetar, Seção 4 (laços aninhados) + 4.4 para analisar |
| Q10 | Projetar raiz quadrada inteira com restrição de operações | Seção 6.6 (busca binária — condição monótona) |
| Q11 | Projetar algoritmo de moda + complexidade | Seção 6.4 (redução — ordenar primeiro) + Seção 4 para analisar |
| Q12 | Projetar primalidade (ingênuo e O(√n)) + complexidade | Seção 6.5 (propriedade matemática do √n) + Seção 4 |
| Q13 | Puzzle da ponte | Não é conteúdo de complexidade — projeto de estratégia por tentativa e erro lógico, fora do escopo das seções técnicas |
| Q14 | Projetar gerador de vetor + contagem de ciclos + operação mais relevante | Seção 6.3 (varredura) para projetar, Seção 4.3 para contar a operação dominante |
| Q15 | Interpretar tabela de tempos → achar classe de complexidade | Seção 5 (use a "regra da razão" ou a fórmula de `b`) |
| Q16 | Analisar incrementos de variável, melhor/pior caso | Seção 4.4 |
| Q17 | Multiplicações no `eval`/`pwr` e implementar a regra de Horner | Seção 4.3 (análise) + Seção 6.4/6.3 (para implementar Horner) |

---

*Dica final 1: sempre que uma questão pedir "prove", primeiro identifique se é uma prova por indução pura (Seção 1) ou uma prova de invariante de laço (Seção 2) — são a mesma ideia lógica, mas aplicadas em contextos diferentes.*

*Dica final 2: sempre que uma questão pedir "projete" ou "construa um algoritmo", resista ao impulso de já sair analisando complexidade — primeiro resolva o problema em si usando o roteiro da Seção 6, e só depois volte às seções de prova e análise para o algoritmo que você criou.*