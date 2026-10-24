# 📈 dash_exponencial: Simulador do Modelo de Crescimento Exponencial de Populações

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Dash](https://img.shields.io/badge/Dash-2.18%2B-brightgreen.svg)](https://dash.plotly.com/)
[![Plotly](https://img.shields.io/badge/Plotly-5.24%2B-orange.svg)](https://plotly.com/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)

Aplicação web interativa desenvolvida com **Dash**, **Plotly**, **Bootstrap** e **SciPy** para simulação, exploração teórica e análise demográfica baseadas no clássico **Modelo de Crescimento Exponencial de Malthus (1798)**. Permite investigar o impacto de taxas de natalidade, mortalidade natural e mortalidade adicional (ex.: caça predatória ou colheita) na evolução de populações biológicas, com cálculo em tempo real de tempos de duplicação, meia-vida e tempo até a extinção.

---

## 📌 Sumário
- [Visão Geral](#-visão-geral)
- [Formulação Matemática](#-formulação-matemática)
  - [Dedução da EDO](#dedução-da-edo)
  - [Solução Analítica Exata](#solução-analítica-exata)
  - [Propriedades Notáveis da Dinâmica Exponencial](#propriedades-notáveis-da-dinâmica-exponencial)
  - [Linearização Semi-Logarítmica](#linearização-semi-logarítmica)
- [Parâmetros e Métricas do Modelo](#-parâmetros-e-métricas-do-modelo)
- [Cenários Notáveis de Estudo](#-cenários-notáveis-de-estudo)
- [Principais Funcionalidades](#-principais-funcionalidades)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Instalação e Execução](#-instalação-e-execução)
- [Roteiro de Estudo e Perguntas Pedagógicas](#-roteiro-de-estudo-e-perguntas-pedagógicas)
- [Licença](#-licença)

---

## 🔬 Visão Geral

O **crescimento exponencial** é o ponto de partida fundamental da biologia de populações e da ecologia matemática. Proposto originalmente pelo economista britânico **Thomas Robert Malthus** em sua célebre obra:
> **MALTHUS, T. R.** *An Essay on the Principle of Population.* J. Johnson, Londres, 1798.

O modelo descreve a dinâmica de uma população biológica habitando um meio ideal com recursos essencialmente ilimitados (ausência de densodependência ou escassez de alimento/espaço). Sob essas premissas, a taxa per capita de geração de novos indivíduos e a taxa per capita de perdas permanecem constantes ao longo do tempo.

Este simulador introduz uma partição realista das taxas vitais:
1. **Taxa intrínseca de natalidade ($a$):** nascimentos per capita por ano.
2. **Taxa intrínseca de mortalidade natural ($b$):** mortes basais por senescência ou causas naturais por ano.
3. **Taxa de mortalidade adicional ($c$):** sobremortalidade imposta por intervenções externas constantes (como caça desportiva, pesca comercial ou catástrofes recorrentes).

---

## 📐 Formulação Matemática

### Dedução da EDO

A variação temporal absoluta do número de indivíduos $N(t)$ em um intervalo infinitesimal $dt$ é o balanço entre entradas (nascimentos) e saídas (óbitos):

$$\frac{dN}{dt} = \text{Nascimentos} - \text{Mortes Naturais} - \text{Mortalidade Adicional}$$

$$\frac{dN}{dt} = a N - b N - c N = (a - b - c) N$$

Definindo a **taxa intrínseca líquida de crescimento per capita** como $r = a - b - c$:

$$\frac{dN}{dt} = r N$$

### Solução Analítica Exata

Com a condição inicial $N(0) = N_0$, a equação é separável:

$$\int_{N_0}^{N(t)} \frac{dN}{N} = \int_{0}^{t} r \, dt \implies \ln\left(\frac{N(t)}{N_0}\right) = r t$$

$$N(t) = N_0 e^{r t} = N_0 e^{(a - b - c)t}$$

### Propriedades Notáveis da Dinâmica Exponencial

1. **Regimes Dinâmicos:**
   * **Crescimento Exponencial ($r > 0 \iff a > b + c$):** A natalidade supera a mortalidade total. A população explode matematicamente em direção ao infinito ($N(t) \to \infty$).
   * **Equilíbrio Demográfico Neutro ($r = 0 \iff a = b + c$):** As taxas de ganho e perda se anulam estritamente. A população mantém-se constante em $N(t) = N_0$.
   * **Decaimento Exponencial ($r < 0 \iff a < b + c$):** As perdas superam a reposição reprodutiva. A população declina assintoticamente a zero ($N(t) \to 0$).

2. **Tempo de Duplicação ($t_d$):**
   Válido para $r > 0$. Tempo necessário para que o efetivo dobre de tamanho ($N = 2 N_0$):
   $$2 N_0 = N_0 e^{r t_d} \implies t_d = \frac{\ln(2)}{r} = \frac{\ln(2)}{a - b - c} \approx \frac{0.6931}{r} \text{ anos}$$

3. **Tempos de Multiplicação por $k$ vezes ($t_{k\times}$):**
   Tempo para atingir $k$ vezes a população inicial ($N = k N_0$):
   $$t_{k\times} = \frac{\ln(k)}{r}$$
   * Para dobrar ($k=2$): $t_{2\times} = \frac{\ln(2)}{r}$
   * Para quintuplicar ($k=5$): $t_{5\times} = \frac{\ln(5)}{r} \approx \frac{1.6094}{r}$
   * Para decuplicar ($k=10$): $t_{10\times} = \frac{\ln(10)}{r} \approx \frac{2.3026}{r}$

4. **Tempo de Meia-Vida ($t_{1/2}$):**
   Válido para $r < 0$. Tempo para a população decair a metade ($N = N_0 / 2$):
   $$t_{1/2} = \frac{\ln(2)}{|r|} = \frac{\ln(2)}{b + c - a} \text{ anos}$$

5. **Tempo até a Extinção Biológica Efetiva ($t_{ext}$):**
   Embora matematicamente a solução contínua atinja zero apenas no limite $t \to \infty$, na biologia a extinção ocorre no momento em que a população atinge menos de um único indivíduo remanescente ($N(t_{ext}) = 1$ para $N_0 > 1$):
   $$N_0 e^{r t_{ext}} = 1 \implies r t_{ext} = \ln\left(\frac{1}{N_0}\right) = -\ln(N_0)$$
   $$t_{ext} = \frac{\ln(N_0)}{|r|} = \frac{\ln(N_0)}{b + c - a} \text{ anos}$$

### Linearização Semi-Logarítmica

Tomando o logaritmo natural de $N(t)$:

$$\ln(N(t)) = \ln(N_0) + r t$$

Em um gráfico onde o eixo das ordenadas está em escala logarítmica ($\ln$ ou $\log_{10}$), a curva exponencial transforma-se em uma **reta**. A inclinação dessa reta é diretamente proporcional à taxa líquida $r$, permitindo identificar visualmente se o regime é de aceleração ($r > 0$), estabilidade ($r = 0$) ou declínio ($r < 0$).

---

## 📊 Parâmetros e Métricas do Modelo

| Parâmetro / Métrica | Símbolo | Unidade | Significado Biológico |
| :--- | :---: | :---: | :--- |
| **Taxa intrínseca de natalidade** | $a$ | $\text{ano}^{-1}$ | Nascimentos médios anuais por indivíduo na população. |
| **Taxa de mortalidade natural** | $b$ | $\text{ano}^{-1}$ | Óbitos basais médios anuais decorrentes de senescência/doenças. |
| **Mortalidade adicional / caça** | $c$ | $\text{ano}^{-1}$ | Óbitos anuais per capita causados por pressão externa (caça, catástrofes). |
| **Taxa líquida de crescimento** | $r$ | $\text{ano}^{-1}$ | Balanço líquido per capita anual ($r = a - b - c$). |
| **População inicial** | $N_0$ | Indivíduos | Tamanho do efetivo populacional no instante $t = 0$. |
| **Horizonte temporal** | $t_{\max}$ | Anos | Duração total da janela de simulação. |
| **Tempo de duplicação** | $t_d$ | Anos | Tempo necessário para a população duplicar de tamanho ($r > 0$). |
| **Tempo de meia-vida** | $t_{1/2}$ | Anos | Tempo necessário para a população reduzir-se pela metade ($r < 0$). |
| **Tempo até a extinção** | $t_{ext}$ | Anos | Tempo necessário para que o efetivo caia abaixo de 1 indivíduo ($r < 0$). |

---

## ⚙️ Cenários Notáveis de Estudo

| Cenário Demográfico | $N_0$ | Natalidade $a$ | Mortalidade $b$ | Mortalidade $c$ | Taxa Líquida $r$ | Comportamento Observado |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **1. Expansão Exponencial** | $1$ a $10$ | $0.10 \text{ ano}^{-1}$ | $0.05 \text{ ano}^{-1}$ | $0.00 \text{ ano}^{-1}$ | **$+0.05 \text{ ano}^{-1}$** | Duplica a cada $\approx 13.86$ anos; atinge $10\times$ em $\approx 46.05$ anos. |
| **2. Decaimento e Extinção** | $1.000$ | $0.10 \text{ ano}^{-1}$ | $0.15$ a $0.50 \text{ ano}^{-1}$ | $0.00 \text{ ano}^{-1}$ | **$-0.05$ a $-0.40 \text{ ano}^{-1}$** | Extinção ($N < 1$) ocorre entre $\approx 17.27$ e $\approx 138.16$ anos. |
| **3. Caça em Equilíbrio** | $10.000$ | $0.10 \text{ ano}^{-1}$ | $0.10 \text{ ano}^{-1}$ | $0.10 \text{ ano}^{-1}$ | **$-0.10 \text{ ano}^{-1}$** | População equilibrada colapsa sob caça constante e extingue-se em $\approx 92.10$ anos. |
| **4. Equilíbrio Neutro** | Qualquer | $0.10 \text{ ano}^{-1}$ | $0.10 \text{ ano}^{-1}$ | $0.00 \text{ ano}^{-1}$ | **$0.00 \text{ ano}^{-1}$** | Efetivo perenemente estacionário em $N(t) = N_0$. |

---

## 🚀 Principais Funcionalidades

- **Painel de Controles com Badges:** Sliders interativos com atualização em tempo real para $a$, $b$, $c$, $N_0$ e $t_{\max}$.
- **Botões de Preset para $N_0$:** Seletores rápidos de população inicial (`1`, `10`, `100`, `1.000`, `10.000`) para agilizar os testes dos exercícios.
- **4 Cards de Métricas em Tempo Real (KPIs):**
  1. *Taxa Líquida ($r$):* Valor com sinal, unidade e classificação dinâmica de estado (*Crescimento*, *Equilíbrio* ou *Decaimento/Extinção*).
  2. *Cinética Populacional:* Cálculo automático do tempo de duplicação ($t_d$) ou meia-vida ($t_{1/2}$).
  3. *População Final:* Tamanho populacional em $t_{\max}$ com notação científica automática para números grandes e variação percentual sobre $N_0$.
  4. *Limiar Crítico / Extinção:* Tempo até extinção ($N < 1$) em regimes decrescentes ou tempo para decuplicar ($10\times$) em regimes de crescimento.
- **Controles Avançados do Gráfico:**
  - *Alternância de Variável:* Visualização da População $N(t)$ ou da Taxa Instantânea de Variação $\frac{dN}{dt}$.
  - *Escala do Eixo Vertical:* Escala Linear ou Escala Logarítmica ($\log_{10}$), demonstrando a linearização matemática da exponencial.
  - *Marcadores Didáticos:* Linha de extinção ($N = 1$), marcadores de duplicação ($2\times N_0$), meia-vida ($N_0/2$) e múltiplos ($5\times$ e $10\times N_0$).
- **Documentação Teórica Integrada:** Accordion com formulação matemática detalhada, dedução por separação de variáveis, tabela de parâmetros e roteiro pedagógico de perguntas.
- **Integração Numérica e Analítica:** Solução por EDO via `solve_ivp` (Runge-Kutta de ordem 5(4)) acoplada à solução analítica exata com proteções numéricas contra overflow.
- **Pronto para Deploy:** Suporte transparente à variável de ambiente `DASH_REQUESTS_PATHNAME_PREFIX` e redirecionamento de raiz para subcaminhos de proxy reverso.

---

## 📁 Estrutura do Projeto

```text
dash_exponencial/
├── app.py              # Aplicação principal Dash, callbacks, simulação e visualização
├── assets/
│   └── estilos.css     # Folha de estilos customizada (design system alinhado ao dash-sir)
├── requirements.txt    # Dependências do projeto
├── README.md           # Documentação completa
└── LICENSE             # Licença GNU GPLv3
```

---

## 💻 Instalação e Execução

### 1. Clonar o repositório
```bash
git clone https://github.com/fferreir/dash_exponencial.git
cd dash_exponencial
```

### 2. Criar e ativar o ambiente virtual

Com `uv` (recomendado):
```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

Ou com `python3 -m venv`:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Executar a aplicação
```bash
python app.py
```

O aplicativo estará acessível no navegador em:
- [http://localhost:8050](http://localhost:8050) (com redirecionamento automático para `/dash_exponencial/`)

---

## ❓ Roteiro de Estudo e Perguntas Pedagógicas

### Questão 1: Tempo de Expansão e Multiplicação ($r > 0$)
> Considere uma população com taxa de natalidade superior à de mortalidade. Por exemplo, $a = 0.10 \text{ ano}^{-1}$ e $b = 0.05 \text{ ano}^{-1}$ (com $c = 0$). Estime qual o tempo necessário (em anos) para que o tamanho desta população aumente duas, cinco ou dez vezes. Inicie com a população com um indivíduo ($N_0 = 1$).

* **Resolução Teórica:**
  A taxa líquida é $r = a - b - c = 0.10 - 0.05 - 0.00 = +0.05 \text{ ano}^{-1}$.
  A equação de tempo para multiplicar por um fator $k$ é $t_{k\times} = \frac{\ln(k)}{r}$:
  - **Duas vezes ($2\times$):** $t_{2\times} = \frac{\ln(2)}{0.05} \approx \frac{0.6931}{0.05} = 13.86\text{ anos}$.
  - **Cinco vezes ($5\times$):** $t_{5\times} = \frac{\ln(5)}{0.05} \approx \frac{1.6094}{0.05} = 32.19\text{ anos}$.
  - **Dez vezes ($10\times$):** $t_{10\times} = \frac{\ln(10)}{0.05} \approx \frac{2.3026}{0.05} = 46.05\text{ anos}$.
* **No Simulador:**
  Selecione $N_0 = 1$ no botão rápido, configure $a = 0.10$, $b = 0.05$, $c = 0.00$. Observe os marcadores verdes, cianos e roxos no gráfico correspondentes aos instantes de multiplicação.

---

### Questão 2: Sobremortalidade e Extinção Populacional ($r < 0$)
> Para uma situação em que a taxa de mortalidade seja maior que a taxa de natalidade, calcule qual o tempo até a extinção da população. Por exemplo, para uma população com 1000 indivíduos e taxa de natalidade de $10\%$ por ano ($a = 0.10$), estime o tempo até a extinção, variando a taxa de mortalidade entre $15\%$ e $50\%$ por ano ($b \in [0.15, 0.50]$, com $c = 0$).

* **Resolução Teórica:**
  A taxa líquida de contração é $r = a - b < 0$. O tempo até que reste menos de 1 indivíduo ($N(t_{ext}) = 1$) a partir de $N_0 = 1000$ é:
  $$t_{ext} = \frac{\ln(1000)}{b - a} = \frac{6.9078}{b - 0.10}$$
  - Para $b = 0.15 \text{ ano}^{-1}$ ($r = -0.05 \text{ ano}^{-1}$): $t_{ext} = \frac{6.9078}{0.05} \approx 138.16\text{ anos}$.
  - Para $b = 0.25 \text{ ano}^{-1}$ ($r = -0.15 \text{ ano}^{-1}$): $t_{ext} = \frac{6.9078}{0.15} \approx 46.05\text{ anos}$.
  - Para $b = 0.50 \text{ ano}^{-1}$ ($r = -0.40 \text{ ano}^{-1}$): $t_{ext} = \frac{6.9078}{0.40} \approx 17.27\text{ anos}$.
* **No Simulador:**
  Clique no preset `1.000` de $N_0$, mantenha $a = 0.10$ e deslize $b$ de $0.15$ até $0.50$. O quarto card de KPI (*Limiar Crítico / Extinção*) e o marcador no gráfico atualizam-se instantaneamente indicando o ano exato do colapso populacional.

---

### Questão 3: Equilíbrio Rompido por Caça Predatória ($c > 0$)
> Supondo uma situação em que a taxa de natalidade e a de mortalidade natural sejam iguais (população em equilíbrio), verifique em quanto tempo pode se extinguir uma população com 10000 animais quando sujeita à caça predatória com taxa $c = 0.10$ por ano.

* **Resolução Teórica:**
  Em equilíbrio natural, $a = b \implies a - b = 0$. Sob caça com taxa $c = 0.10 \text{ ano}^{-1}$:
  $$r = a - b - c = -c = -0.10\text{ ano}^{-1}$$
  O tempo até a extinção biológica ($N < 1$) a partir de $N_0 = 10000$ indivíduos é:
  $$t_{ext} = \frac{\ln(10000)}{0.10} = \frac{9.2103}{0.10} \approx 92.10\text{ anos}$$
* **No Simulador:**
  Selecione o preset `10.000` de $N_0$, configure $a = 0.10$, $b = 0.10$, $c = 0.10$ e aumente o horizonte de tempo para $100$ anos. Observe a trajetória de declínio e o ponto exato de cruzamento com a linha tracejada vermelha de extinção em $t \approx 92.1$ anos.

---

### Questão 4: Análise em Escala Logarítmica
> Alterne a visualização para a escala logarítmica ($\log_{10}$). O que você observa a respeito da forma geométrica das trajetórias populacionais?

* **Explicação Didática:**
  Como $\ln(N(t)) = \ln(N_0) + r t$, o gráfico semi-logarítmico converte qualquer dinâmica exponencial em uma reta de equação $y = mx + d$, onde a inclinação $m$ corresponde à taxa $r$. Curvas crescentes têm inclinação positiva, curvas decrescentes têm inclinação negativa, e o equilíbrio populacional é uma reta estritamente horizontal ($m = 0$). Isso facilita a detecção visual e a comparação entre diferentes taxas de crescimento na literatura biológica.

---

## 📄 Licença

Distribuído sob a licença GNU General Public License v3.0 (GPLv3). Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.
