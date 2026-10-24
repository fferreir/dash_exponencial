import os
import flask
import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import numpy as np
from scipy.integrate import solve_ivp
import plotly.graph_objects as go

# =============================================================================
# CONFIGURAÇÃO DE ROTA E PREFIXO (Suporte para dev local e proxy reverso de deploy)
# =============================================================================
prefix = os.getenv('DASH_REQUESTS_PATHNAME_PREFIX', '/dash_exponencial/')
if not prefix.startswith('/'):
    prefix = '/' + prefix
if not prefix.endswith('/'):
    prefix = prefix + '/'

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.LUMEN, dbc.icons.FONT_AWESOME],
    requests_pathname_prefix=prefix,
    routes_pathname_prefix=prefix,
    suppress_callback_exceptions=True
)
server = app.server

# Redirecionamento da raiz '/' para o prefixo da aplicação em desenvolvimento local
if prefix != '/':
    @server.route('/')
    def root_redirect():
        return flask.redirect(prefix)


# =============================================================================
# SISTEMA DE EQUAÇÕES DIFERENCIAIS ORDINÁRIAS (MODELO EXPONENCIAL)
# =============================================================================
def ode_sys(t, state, a, b, c):
    """
    Sistema de crescimento/decaimento exponencial populacional.
    dN/dt = (a - b - c) * N = r * N
    
    Estado:
      state[0]: Tamanho populacional N
      
    Parâmetros:
      a: Taxa intrínseca per capita de natalidade (ano^-1)
      b: Taxa intrínseca per capita de mortalidade natural (ano^-1)
      c: Taxa per capita de mortalidade adicional (ano^-1, ex.: caça predatória)
    """
    n = max(0.0, float(state[0]))
    r = float(a) - float(b) - float(c)
    dn_dt = r * n
    return [dn_dt]


def solucao_analitica(t_arr, n0, a, b, c):
    """
    Solução analítica exata da equação diferencial exponencial:
    N(t) = N0 * exp((a - b - c) * t) = N0 * exp(r * t)
    """
    r = float(a) - float(b) - float(c)
    n0_eff = max(0.0, float(n0))
    # Proteção contra overflow em exponenciais muito elevadas
    expoente = np.clip(r * t_arr, -100.0, 100.0)
    return n0_eff * np.exp(expoente)


# =============================================================================
# CABEÇALHO DO DASHBOARD (HERO HEADER)
# =============================================================================
cabecalho = html.Div(
    [
        html.Div(
            [
                html.H1(
                    [
                        html.I(className="fa-solid fa-arrow-trend-up me-2"),
                        "Modelo de Crescimento Exponencial de Populações"
                    ],
                    className="display-6 mb-1"
                ),
                html.P(
                    "Simulador dinâmico de crescimento malthusiano, decaimento populacional e análise de tempos de duplicação e extinção.",
                    className="lead fs-6 mb-0 opacity-75"
                ),
            ],
            className="hero-header p-3 mb-3"
        )
    ]
)


# =============================================================================
# DOCUMENTAÇÃO TEÓRICA E PERGUNTAS PEDAGÓGICAS (ACCORDION)
# =============================================================================
descricao = html.Div([
    dcc.Markdown(
        r'''
        O **modelo de crescimento exponencial** (também denominado *modelo malthusiano*) foi formulado originalmente pelo economista britânico **Thomas Robert Malthus** em seu célebre *An Essay on the Principle of Population* (1798).

        Representa a forma mais elementar e fundamental de modelagem matemática de populações biológicas, assumindo que os recursos ambientais (alimento, espaço, refúgio) são ilimitados e que cada indivíduo contribui proporcionalmente e de forma constante para a taxa de variação da população.

        A taxa líquida per capita de variação populacional resulta do balanço direto entre as taxas instantâneas de **natalidade ($$a$$)**, **mortalidade natural ($$b$$)** e eventual **mortalidade adicional ($$c$$)** (por exemplo, caça predatória, pesca, exploração de recursos ou catástrofes ambientais).
        ''', mathjax=True
    ),
    dcc.Markdown(
        r'''
        ### Formulação Matemática e Dedução da EDO:
        $$\frac{dN}{dt} = \text{Nascimentos} - \text{Mortes Naturais} - \text{Mortalidade Adicional}$$
        $$\frac{dN}{dt} = aN - bN - cN = (a - b - c)N$$

        Definindo a **taxa intrínseca líquida de crescimento per capita** como $$r = a - b - c$$:
        $$\frac{dN}{dt} = r N$$

        Integrando por separação de variáveis a partir da condição inicial $$N(0) = N_0$$:
        $$\int_{N_0}^{N(t)} \frac{dN}{N} = \int_{0}^{t} r \, dt \implies \ln\left(\frac{N(t)}{N_0}\right) = r t$$
        $$N(t) = N_0 e^{r t} = N_0 e^{(a - b - c)t}$$

        ### Comportamentos Qualitativos Fundamentais:
        * **Crescimento Exponencial ($$r > 0 \iff a > b + c$$):** A natalidade supera as perdas globais. A população cresce aceleradamente com concavidade positiva, tendendo ao infinito ($$N(t) \to \infty$$).
        * **Equilíbrio Populacional ($$r = 0 \iff a = b + c$$):** Geração nula de novos indivíduos líquidos. A população permanece perenemente inalterada no patamar inicial ($$N(t) = N_0$$).
        * **Decaimento Exponencial e Extinção ($$r < 0 \iff a < b + c$$):** A mortalidade agregada excede a natalidade. A população colapsa assintoticamente em direção a zero ($$N(t) \to 0$$), atingindo o limiar crítico de extinção biológica ($$N < 1$$ indivíduo).

        ### Linearização Semi-Logarítmica:
        Tomando o logaritmo natural em ambos os lados da solução exata:
        $$\ln(N(t)) = \ln(N_0) + r t$$
        Em escala semi-logarítmica ($\log_{10}$ ou $\ln$), a trajetória exponencial transforma-se em uma **linha reta**, cujo coeficiente angular (inclinação) é estritamente proporcional à taxa de crescimento $$r$$.
        ''', mathjax=True
    )
])

parametros = dcc.Markdown(
    r'''
    * **$$a$$ (Taxa intrínseca de natalidade):** Expressa em $$ano^{-1}$$. Representa a taxa per capita média anual de nascimentos na população.
    * **$$b$$ (Taxa intrínseca de mortalidade natural):** Expressa em $$ano^{-1}$$. Representa a taxa per capita média anual de óbitos por causas naturais (senescência, patógenos basais).
    * **$$c$$ (Taxa de mortalidade adicional):** Expressa em $$ano^{-1}$$. Representa o impacto per capita anual de intervenções externas (caça desportiva ou comercial, predação invasora, secas ou desastres).
    * **$$r$$ (Taxa intrínseca líquida de crescimento per capita):** $$r = a - b - c$$ ($$ano^{-1}$$). Parâmetro central que dita se a população expande ($$r > 0$$), estagna ($$r = 0$$) ou contrai ($$r < 0$$).
    * **$$N_0$$ (População inicial):** Número de indivíduos no instante $$t = 0$$.
    * **$$t_d$$ (Tempo de duplicação):** Válido para $$r > 0$$. Tempo necessário para que o tamanho populacional dobre ($$N = 2 N_0$$):
      $$t_d = \frac{\ln(2)}{r} = \frac{\ln(2)}{a - b - c} \approx \frac{0.6931}{r} \text{ anos}$$
    * **$$t_{k\times}$$ (Tempo para multiplicar por $$k$$ vezes):** Tempo necessário para a população crescer $$k$$ vezes ($$N = k N_0$$):
      $$t_{k\times} = \frac{\ln(k)}{r}$$
    * **$$t_{1/2}$$ (Tempo de meia-vida):** Válido para $$r < 0$$. Intervalo de tempo para a população ser reduzida à metade ($$N = N_0 / 2$$):
      $$t_{1/2} = \frac{\ln(2)}{|r|} = \frac{\ln(2)}{b + c - a} \text{ anos}$$
    * **$$t_{ext}$$ (Tempo até a extinção biológica efetiva):** Válido para $$r < 0$$ e $$N_0 > 1$$. Tempo até que a população atinja menos de 1 indivíduo ($$N(t) < 1$$):
      $$N_0 e^{r t_{ext}} = 1 \implies t_{ext} = \frac{\ln(N_0)}{|r|} = \frac{\ln(N_0)}{b + c - a} \text{ anos}$$
    ''', mathjax=True
)

cond_inicial = html.Div([
    dcc.Markdown(
        r'''
        ### Síntese dos Cenários Notáveis do Modelo Exponencial:

        A tabela abaixo resume os parâmetros típicos de estudo demográfico e os cenários pedagógicos explorados neste simulador:
        ''', mathjax=True
    ),
    dbc.Table(
        [
            html.Thead(
                html.Tr([
                    html.Th("Cenário Demográfico"),
                    html.Th("N₀"),
                    html.Th("Natalidade a"),
                    html.Th("Mort. Nat. b"),
                    html.Th("Mort. Adic. c"),
                    html.Th("Taxa Líquida r"),
                    html.Th("Comportamento Esperado")
                ])
            ),
            html.Tbody([
                html.Tr([
                    html.Td("1. Expansão Exponencial"),
                    html.Td("1 a 10"),
                    html.Td("0.10 ano⁻¹"),
                    html.Td("0.05 ano⁻¹"),
                    html.Td("0.00 ano⁻¹"),
                    html.Td(html.Span("+0.05 ano⁻¹", className="text-success fw-bold")),
                    html.Td("Duplica a cada ~13.86 anos; atinge 10× em ~46.05 anos.")
                ]),
                html.Tr([
                    html.Td("2. Decaimento e Extinção"),
                    html.Td("1.000"),
                    html.Td("0.10 ano⁻¹"),
                    html.Td("0.15 a 0.50 ano⁻¹"),
                    html.Td("0.00 ano⁻¹"),
                    html.Td(html.Span("-0.05 a -0.40 ano⁻¹", className="text-danger fw-bold")),
                    html.Td("Extinção (N < 1) ocorre entre ~17.3 e ~138.2 anos.")
                ]),
                html.Tr([
                    html.Td("3. Caça Predatória em Equilíbrio"),
                    html.Td("10.000"),
                    html.Td("0.10 ano⁻¹"),
                    html.Td("0.10 ano⁻¹"),
                    html.Td("0.10 ano⁻¹"),
                    html.Td(html.Span("-0.10 ano⁻¹", className="text-danger fw-bold")),
                    html.Td("População em equilíbrio natural desaba e extingue-se em ~92.1 anos.")
                ]),
                html.Tr([
                    html.Td("4. Equilíbrio Neutro Estático"),
                    html.Td("Qualquer"),
                    html.Td("0.10 ano⁻¹"),
                    html.Td("0.10 ano⁻¹"),
                    html.Td("0.00 ano⁻¹"),
                    html.Td(html.Span("0.00 ano⁻¹", className="text-primary fw-bold")),
                    html.Td("População perene mantida em N(t) = N₀.")
                ]),
            ])
        ],
        bordered=True,
        hover=True,
        size="sm",
        className="table-data mt-2"
    )
])

perguntas = dcc.Markdown(
    r'''
    1. **Tempo de Expansão e Multiplicação ($$r > 0$$):**
       * *Condições:* Inicie a simulação com $$N_0 = 1$$, taxa de natalidade $$a = 0.10 \text{ ano}^{-1}$$, mortalidade natural $$b = 0.05 \text{ ano}^{-1}$$ e mortalidade adicional $$c = 0$$.
       * *Questão:* A taxa líquida de crescimento é $$r = a - b = 0.05 \text{ ano}^{-1}$$. Estime qual o tempo necessário (em anos) para que a população aumente duas ($$2\times$$), cinco ($$5\times$$) ou dez ($$10\times$$) vezes em relação a $$N_0$$.
       * *Dica analítica:* Utilize as fórmulas $$t_d = \frac{\ln(2)}{r} \approx 13.86\text{ anos}$$, $$t_{5\times} = \frac{\ln(5)}{r} \approx 32.19\text{ anos}$$ e $$t_{10\times} = \frac{\ln(10)}{r} \approx 46.05\text{ anos}$$. Compare os valores teóricos com os marcadores visuais no gráfico.
    
    2. **Sobremortalidade e Tempo até a Extinção ($$r < 0$$):**
       * *Condições:* Configure uma população inicial com $$N_0 = 1000$$ indivíduos e taxa de natalidade fixa em $$a = 0.10 \text{ ano}^{-1}$$ ($$10\%$$ ao ano), sem mortalidade adicional ($$c = 0$$).
       * *Questão:* Varie a taxa de mortalidade natural $$b$$ entre $$0.15$$ ($$15\%$$ ao ano) e $$0.50 \text{ ano}^{-1}$$ ($$50\%$$ ao ano). Calcule e observe em quanto tempo a população entra em extinção efetiva ($$N < 1$$ indivíduo).
       * *Dica analítica:* O tempo de extinção biológica para $$N_0 > 1$$ é dado por $$t_{ext} = \frac{\ln(N_0)}{b - a}$$. Para $$b = 0.15$$, $$t_{ext} = \frac{\ln(1000)}{0.05} \approx 138.16\text{ anos}$$. Para $$b = 0.50$$, $$t_{ext} = \frac{\ln(1000)}{0.40} \approx 17.27\text{ anos}$$.
    
    3. **Equilíbrio Demográfico Rompido por Caça Predatória ($$c > 0$$):**
       * *Condições:* Suponha uma população inicialmente em equilíbrio natural, onde a natalidade e a mortalidade natural se anulam ($$a = b = 0.10 \text{ ano}^{-1}$$), com população inicial de $$N_0 = 10000$$ animais.
       * *Questão:* Introduza uma taxa de caça predatória ou exploração antrópica $$c = 0.10 \text{ ano}^{-1}$$. Em quanto tempo essa população entrará em colapso e se extinguirá?
       * *Dica analítica:* Como $$a - b = 0$$, a taxa líquida torna-se $$r = -c = -0.10 \text{ ano}^{-1}$$. O tempo até a extinção é $$t_{ext} = \frac{\ln(10000)}{0.10} = \frac{9.2103}{0.10} \approx 92.1\text{ anos}$$.
    
    4. **Comportamento em Escala Semi-Logarítmica:**
       * *Questão:* Alterne a escala do eixo vertical de *"Linear"* para *"Logarítmica (log₁₀)"*. Por que as curvas exponenciais (crescentes ou decrescentes) transformam-se em retas perfeitas? Qual o significado geométrico da inclinação dessas retas?
    ''', mathjax=True
)

textos_descricao = html.Div(
    dbc.Accordion(
        [
            dbc.AccordionItem(descricao, title="📘 Descrição e Formulação Matemática"),
            dbc.AccordionItem(parametros, title="📊 Parâmetros e Métricas do Modelo"),
            dbc.AccordionItem(cond_inicial, title="⚙️ Condições Iniciais e Cenários Típicos"),
            dbc.AccordionItem(perguntas, title="❓ Roteiro de Estudo e Perguntas Pedagógicas"),
        ],
        start_collapsed=True,
        flush=False,
    )
)


# =============================================================================
# COMPONENTES DE CONTROLE (CARDS COM SLIDERS E BADGES)
# =============================================================================
ajuste_parametros_demo = html.Div(
    [
        html.Div(
            [
                html.I(className="fa-solid fa-dna me-2 text-success"),
                "Parâmetros Demográficos"
            ],
            className="card-header"
        ),
        html.Div(
            [
                html.Div([
                    dbc.Label(dcc.Markdown(r'Taxa de natalidade ($$a$$):', mathjax=True), className="mb-0"),
                    html.Span(id="badge_a", className="slider-val-badge")
                ], className="slider-label"),
                dcc.Slider(
                    id="a",
                    min=0.00,
                    max=0.50,
                    step=0.01,
                    value=0.10,
                    tooltip={"placement": "bottom", "always_visible": False}
                ),
            ],
            className="slider-group",
        ),
        html.Div(
            [
                html.Div([
                    dbc.Label(dcc.Markdown(r'Taxa de mortalidade natural ($$b$$):', mathjax=True), className="mb-0"),
                    html.Span(id="badge_b", className="slider-val-badge badge-danger")
                ], className="slider-label"),
                dcc.Slider(
                    id="b",
                    min=0.00,
                    max=0.50,
                    step=0.01,
                    value=0.05,
                    tooltip={"placement": "bottom", "always_visible": False}
                ),
            ],
            className="slider-group",
        ),
        html.Div(
            [
                html.Div([
                    dbc.Label(dcc.Markdown(r'Mortalidade adicional / caça ($$c$$):', mathjax=True), className="mb-0"),
                    html.Span(id="badge_c", className="slider-val-badge badge-warning")
                ], className="slider-label"),
                dcc.Slider(
                    id="c",
                    min=0.00,
                    max=0.30,
                    step=0.01,
                    value=0.00,
                    tooltip={"placement": "bottom", "always_visible": False}
                ),
            ],
            className="slider-group",
        ),
    ],
    className="card-control mb-3",
)

ajuste_condicoes = html.Div(
    [
        html.Div(
            [
                html.I(className="fa-solid fa-users me-2 text-primary"),
                "Condições Iniciais e Horizonte"
            ],
            className="card-header"
        ),
        html.Div(
            [
                html.Div([
                    dbc.Label(dcc.Markdown(r'População inicial ($$N_0$$):', mathjax=True), className="mb-0"),
                    html.Span(id="badge_n0", className="slider-val-badge badge-info")
                ], className="slider-label"),
                # Botões rápidos de preset para os valores dos exercícios
                html.Div(
                    [
                        dbc.Button("1", id="btn_preset_1", size="sm", outline=True, color="primary", className="btn-preset me-1"),
                        dbc.Button("10", id="btn_preset_10", size="sm", outline=True, color="primary", className="btn-preset me-1"),
                        dbc.Button("100", id="btn_preset_100", size="sm", outline=True, color="primary", className="btn-preset me-1"),
                        dbc.Button("1.000", id="btn_preset_1000", size="sm", outline=True, color="primary", className="btn-preset me-1"),
                        dbc.Button("10.000", id="btn_preset_10000", size="sm", outline=True, color="primary", className="btn-preset"),
                    ],
                    className="d-flex mb-2"
                ),
                dcc.Slider(
                    id="n0",
                    min=1,
                    max=10000,
                    step=1,
                    value=1,
                    tooltip={"placement": "bottom", "always_visible": False}
                ),
            ],
            className="slider-group",
        ),
        html.Div(
            [
                html.Div([
                    dbc.Label("Horizonte de Tempo (anos):", className="mb-0"),
                    html.Span(id="badge_t_max", className="slider-val-badge badge-neutral")
                ], className="slider-label"),
                dcc.Slider(
                    id="t_max",
                    min=10,
                    max=200,
                    step=5,
                    value=70,
                    tooltip={"placement": "bottom", "always_visible": False}
                ),
            ],
            className="slider-group",
        ),
    ],
    className="card-control mb-3",
)

ajuste_opcoes_grafico = html.Div(
    [
        html.Div(
            [
                html.I(className="fa-solid fa-sliders me-2 text-secondary"),
                "Opções de Visualização e Referências"
            ],
            className="card-header"
        ),
        html.Div(
            [
                dbc.Label("Variável Exibida:", className="fw-semibold small text-muted mb-1"),
                dbc.RadioItems(
                    id="modo_grafico",
                    options=[
                        {"label": " População N(t)", "value": "pop"},
                        {"label": " Taxa de Variação dN/dt", "value": "deriv"},
                    ],
                    value="pop",
                    inline=True,
                    className="small"
                ),
            ],
            className="slider-group",
        ),
        html.Div(
            [
                dbc.Label("Escala do Eixo Vertical:", className="fw-semibold small text-muted mb-1"),
                dbc.RadioItems(
                    id="escala_y",
                    options=[
                        {"label": " Escala Linear", "value": "linear"},
                        {"label": " Escala Logarítmica (log₁₀)", "value": "log"},
                    ],
                    value="linear",
                    inline=True,
                    className="small"
                ),
            ],
            className="slider-group",
        ),
        html.Div(
            [
                dbc.Label("Elementos de Referência Didáticos:", className="fw-semibold small text-muted mb-1"),
                dbc.Checklist(
                    id="opcoes_referencia",
                    options=[
                        {"label": " Linha de Extinção (N = 1 indivíduo)", "value": "extincao"},
                        {"label": " Marcadores de Duplicação (2×) e Meia-Vida", "value": "duplicacao"},
                        {"label": " Marcadores de Múltiplos (5× e 10× N₀)", "value": "multiplos"},
                    ],
                    value=["extincao", "duplicacao", "multiplos"],
                    className="small"
                ),
            ],
            className="slider-group",
        ),
    ],
    className="card-control mb-3",
)


# =============================================================================
# CARDS DE MÉTRICAS (KPIS)
# =============================================================================
cards_metricas = dbc.Row(
    [
        # KPI 1: Taxa Líquida (r = a - b - c)
        dbc.Col(
            html.Div(
                [
                    html.Div(
                        [
                            html.Div("Taxa Líquida (r)", className="kpi-title"),
                            html.Div(id="kpi_r_val", className="kpi-value"),
                            html.Div(id="kpi_r_sub", className="kpi-subtitle"),
                            html.I(id="kpi_r_icon", className="fa-solid fa-chart-line kpi-icon"),
                        ],
                        className="kpi-card-inner"
                    )
                ],
                id="kpi_r_card",
                className="kpi-card kpi-growth"
            ),
            width=6, sm=6, lg=3, className="mb-2"
        ),
        # KPI 2: Cinética (Duplicação / Meia-Vida)
        dbc.Col(
            html.Div(
                [
                    html.Div(
                        [
                            html.Div("Cinética Populacional", className="kpi-title"),
                            html.Div(id="kpi_kin_val", className="kpi-value"),
                            html.Div(id="kpi_kin_sub", className="kpi-subtitle"),
                            html.I(className="fa-solid fa-stopwatch kpi-icon"),
                        ],
                        className="kpi-card-inner"
                    )
                ],
                className="kpi-card kpi-kinetic"
            ),
            width=6, sm=6, lg=3, className="mb-2"
        ),
        # KPI 3: População Final N(t_max)
        dbc.Col(
            html.Div(
                [
                    html.Div(
                        [
                            html.Div("População Final", className="kpi-title"),
                            html.Div(id="kpi_pop_val", className="kpi-value"),
                            html.Div(id="kpi_pop_sub", className="kpi-subtitle"),
                            html.I(className="fa-solid fa-users kpi-icon"),
                        ],
                        className="kpi-card-inner"
                    )
                ],
                className="kpi-card kpi-population"
            ),
            width=6, sm=6, lg=3, className="mb-2"
        ),
        # KPI 4: Limiar / Extinção / Expansão (Dinâmico)
        dbc.Col(
            html.Div(
                [
                    html.Div(
                        [
                            html.Div("Expansão / Extinção", id="kpi_thresh_title", className="kpi-title"),
                            html.Div(id="kpi_thresh_val", className="kpi-value"),
                            html.Div(id="kpi_thresh_sub", className="kpi-subtitle"),
                            html.I(id="kpi_thresh_icon", className="fa-solid fa-rocket kpi-icon"),
                        ],
                        className="kpi-card-inner"
                    )
                ],
                id="kpi_thresh_card",
                className="kpi-card kpi-threshold"
            ),
            width=6, sm=6, lg=3, className="mb-2"
        ),
    ],
    className="mb-2"
)


# =============================================================================
# LAYOUT PRINCIPAL DO DASHBOARD
# =============================================================================
app.layout = dbc.Container(
    [
        cabecalho,
        dbc.Row(
            [
                # Coluna Esquerda: Controles e Parâmetros (4 colunas)
                dbc.Col(
                    [
                        ajuste_parametros_demo,
                        ajuste_condicoes,
                        ajuste_opcoes_grafico,
                    ],
                    width=12, lg=4
                ),
                
                # Coluna Direita: Métricas, Gráfico e Teoria (8 colunas)
                dbc.Col(
                    [
                        cards_metricas,
                        
                        # Card do Gráfico
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.I(className="fa-solid fa-chart-area me-2 text-success"),
                                                html.Span(
                                                    "Dinâmica Temporal do Crescimento Exponencial",
                                                    id="graph_title_span",
                                                    className="fw-bold text-dark me-3"
                                                ),
                                            ],
                                            className="d-flex align-items-center mb-1 mb-md-0"
                                        ),
                                    ],
                                    className="d-flex flex-wrap justify-content-between align-items-center mb-2 pb-2 border-bottom"
                                ),
                                dcc.Graph(
                                    id='population_chart',
                                    config={
                                        'displayModeBar': True,
                                        'displaylogo': False,
                                        'modeBarButtonsToRemove': ['lasso2d', 'select2d']
                                    },
                                    style={'height': '520px'}
                                ),
                            ],
                            className="graph-card mb-3"
                        ),
                        
                        # Documentação e Roteiro de Perguntas
                        textos_descricao,
                    ],
                    width=12, lg=8
                ),
            ]
        ),
        
        # Rodapé Institucional
        html.Footer(
            html.Div(
                [
                    html.Span("Modelo de Crescimento Exponencial de Populações — Baseado no modelo malthusiano clássico. ", className="text-muted"),
                    html.A("Código-fonte no GitHub", href="https://github.com/fferreir/dash_exponencial", target="_blank", className="text-decoration-none text-success fw-semibold"),
                ],
                className="text-center py-3 border-top mt-4 small"
            )
        )
    ],
    fluid=True,
    className="px-3 py-2"
)


# =============================================================================
# CALLBACKS DE INTERAÇÃO E ATUALIZAÇÃO DE BADGES E PRESETS
# =============================================================================

# Atualização dos botões de preset para N0
@app.callback(
    Output("n0", "value"),
    [
        Input("btn_preset_1", "n_clicks"),
        Input("btn_preset_10", "n_clicks"),
        Input("btn_preset_100", "n_clicks"),
        Input("btn_preset_1000", "n_clicks"),
        Input("btn_preset_10000", "n_clicks"),
    ],
    prevent_initial_call=True
)
def aplicar_preset_n0(c1, c10, c100, c1000, c10000):
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update
    btn_id = ctx.triggered[0]["prop_id"].split(".")[0]
    preset_map = {
        "btn_preset_1": 1,
        "btn_preset_10": 10,
        "btn_preset_100": 100,
        "btn_preset_1000": 1000,
        "btn_preset_10000": 10000,
    }
    return preset_map.get(btn_id, dash.no_update)


# Atualização dinâmica dos badges de valores dos sliders
@app.callback(
    [
        Output("badge_a", "children"),
        Output("badge_b", "children"),
        Output("badge_c", "children"),
        Output("badge_n0", "children"),
        Output("badge_t_max", "children"),
    ],
    [
        Input("a", "value"),
        Input("b", "value"),
        Input("c", "value"),
        Input("n0", "value"),
        Input("t_max", "value"),
    ]
)
def update_badges(a_val, b_val, c_val, n0_val, t_max_val):
    return (
        f"{float(a_val):.2f} ano⁻¹",
        f"{float(b_val):.2f} ano⁻¹",
        f"{float(c_val):.2f} ano⁻¹",
        f"{int(n0_val):,} ind.",
        f"{int(t_max_val)} anos",
    )


# =============================================================================
# CALLBACK PRINCIPAL: SIMULAÇÃO E RENDERIZAÇÃO
# =============================================================================
@app.callback(
    [
        Output("kpi_r_val", "children"),
        Output("kpi_r_sub", "children"),
        Output("kpi_r_card", "className"),
        Output("kpi_kin_val", "children"),
        Output("kpi_kin_sub", "children"),
        Output("kpi_pop_val", "children"),
        Output("kpi_pop_sub", "children"),
        Output("kpi_thresh_title", "children"),
        Output("kpi_thresh_val", "children"),
        Output("kpi_thresh_sub", "children"),
        Output("kpi_thresh_card", "className"),
        Output("kpi_thresh_icon", "className"),
        Output("population_chart", "figure"),
    ],
    [
        Input("a", "value"),
        Input("b", "value"),
        Input("c", "value"),
        Input("n0", "value"),
        Input("t_max", "value"),
        Input("modo_grafico", "value"),
        Input("escala_y", "value"),
        Input("opcoes_referencia", "value"),
    ]
)
def simular_e_renderizar(a_val, b_val, c_val, n0_val, t_max_val, modo_grafico, escala_y, opcoes_ref):
    # Parâmetros com proteções numéricas
    a = float(a_val) if a_val is not None else 0.10
    b = float(b_val) if b_val is not None else 0.05
    c = float(c_val) if c_val is not None else 0.00
    n0 = float(n0_val) if n0_val is not None else 1.0
    t_end = float(t_max_val) if t_max_val is not None else 70.0
    
    opcoes_ref = opcoes_ref or []
    mostrar_extincao = "extincao" in opcoes_ref
    mostrar_duplicacao = "duplicacao" in opcoes_ref
    mostrar_multiplos = "multiplos" in opcoes_ref
    
    # Taxa líquida per capita
    r = a - b - c
    
    # Vetor de tempo de avaliação
    t_nsamples = 1000
    t_eval = np.linspace(0.0, t_end, t_nsamples)
    
    # Solução por EDO (solve_ivp com método RK45 de alta precisão)
    sol = solve_ivp(
        fun=ode_sys,
        t_span=(0.0, t_end),
        y0=[n0],
        args=(a, b, c),
        t_eval=t_eval,
        method='RK45'
    )
    n_ode = sol.y[0]
    
    # Solução analítica exata
    n_analitica = solucao_analitica(t_eval, n0, a, b, c)
    
    # Taxa instantânea absoluta dN/dt
    dn_dt = r * n_analitica
    
    # Métricas finais
    pop_final = float(n_analitica[-1])
    
    # ==========================
    # CÁLCULO DOS KPIS
    # ==========================
    # 1. Taxa Líquida (r)
    sinal = "+" if r > 0 else ""
    kpi_r_val = f"{sinal}{r:.3f} ano⁻¹"
    if r > 1e-5:
        kpi_r_sub = "Crescimento Exponencial (a > b + c)"
        kpi_r_card_class = "kpi-card kpi-growth"
    elif r < -1e-5:
        kpi_r_sub = "Decaimento / Risco de Extinção (a < b + c)"
        kpi_r_card_class = "kpi-card kpi-decay"
    else:
        kpi_r_sub = "Equilíbrio Demográfico Neutro (a = b + c)"
        kpi_r_card_class = "kpi-card kpi-equilibrium"
        
    # 2. Cinética Populacional (td ou t1/2)
    if r > 1e-5:
        td = np.log(2.0) / r
        kpi_kin_val = f"{td:.2f} anos"
        kpi_kin_sub = f"Tempo de duplicação: td = ln(2)/r"
    elif r < -1e-5:
        thalf = np.log(2.0) / abs(r)
        kpi_kin_val = f"{thalf:.2f} anos"
        kpi_kin_sub = f"Tempo de meia-vida: t₁/₂ = ln(2)/|r|"
    else:
        kpi_kin_val = "Estável"
        kpi_kin_sub = "População constante ao longo do tempo"
        
    # 3. População Final N(t_final)
    if pop_final >= 1e7:
        kpi_pop_val = f"{pop_final:.2e}"
    elif pop_final >= 1000:
        kpi_pop_val = f"{pop_final:,.0f}".replace(",", ".")
    elif pop_final >= 1.0:
        kpi_pop_val = f"{pop_final:.1f}"
    else:
        kpi_pop_val = f"{pop_final:.3f}"
        
    var_pct = ((pop_final - n0) / max(n0, 1e-6)) * 100.0
    if pop_final < 1.0 and n0 >= 1.0:
        kpi_pop_sub = f"População extinta em t={t_end:.0f} anos (N < 1)"
    else:
        sinal_var = "+" if var_pct > 0 else ""
        if abs(var_pct) >= 1e6:
            kpi_pop_sub = f"{sinal_var}{var_pct:.1e}% em relação a N₀"
        else:
            kpi_pop_sub = f"{sinal_var}{var_pct:,.1f}% em relação a N₀".replace(",", "X").replace(".", ",").replace("X", ".")

    # 4. Limiar Crítico / Extinção / Expansão (Contextualizado ao sinal de r)
    if r > 1e-5:
        # Quando o crescimento é positivo: NÃO HÁ EXTINÇÃO. Exibimos a métrica de expansão (10x N0)
        t_10x = np.log(10.0) / r
        kpi_thresh_title = "Expansão (10× N₀)"
        kpi_thresh_val = f"{t_10x:.2f} anos"
        kpi_thresh_sub = "Tempo para decuplicar (10× o tamanho inicial)"
        kpi_thresh_card_class = "kpi-card kpi-threshold"
        kpi_thresh_icon = "fa-solid fa-rocket kpi-icon"
    elif r < -1e-5:
        # Quando o crescimento é negativo: HÁ RISCO REAL DE EXTINÇÃO (N < 1)
        kpi_thresh_title = "Tempo até a Extinção"
        kpi_thresh_card_class = "kpi-card kpi-decay"
        kpi_thresh_icon = "fa-solid fa-skull-crossbones kpi-icon"
        if n0 > 1.0:
            t_ext = np.log(n0) / abs(r)
            kpi_thresh_val = f"{t_ext:.2f} anos"
            kpi_thresh_sub = "Tempo até restar menos de 1 indivíduo (N < 1)"
        else:
            kpi_thresh_val = "< 1 ano"
            kpi_thresh_sub = "N₀ já está no limiar crítico de extinção (N ≤ 1)"
    else:
        # População em equilíbrio estático neutro (r = 0)
        kpi_thresh_title = "Equilíbrio Demográfico"
        kpi_thresh_val = "Estável"
        kpi_thresh_sub = "Equilíbrio perpétuo (dN/dt = 0, sem extinção)"
        kpi_thresh_card_class = "kpi-card kpi-equilibrium"
        kpi_thresh_icon = "fa-solid fa-scale-balanced kpi-icon"

    # ==========================
    # CONSTRUÇÃO DO GRÁFICO PLOTLY
    # ==========================
    fig = go.Figure()
    
    # Configuração de variável a exibir
    if modo_grafico == "pop":
        y_data = n_analitica
        trace_name = "População N(t)"
        line_color = "#059669" if r >= 0 else "#dc2626"
        y_axis_title = "Número de Indivíduos (N)"
        hover_template = "Ano: %{x:.2f}<br>População: %{y:,.2f}<extra></extra>"
    else:
        y_data = dn_dt
        trace_name = "Taxa Absoluta dN/dt"
        line_color = "#2563eb" if r >= 0 else "#b91c1c"
        y_axis_title = "Taxa de Variação dN/dt (indivíduos / ano)"
        hover_template = "Ano: %{x:.2f}<br>dN/dt: %{y:,.2f} ind./ano<extra></extra>"

    # Curva principal
    fig.add_trace(go.Scatter(
        x=t_eval,
        y=y_data,
        name=trace_name,
        line=dict(color=line_color, width=3.5),
        hovertemplate=hover_template
    ))

    # Elementos de referência para População N(t)
    if modo_grafico == "pop":
        # 1. Linha de Extinção (N = 1 indivíduo) - exibida com destaque apenas quando em declínio
        if mostrar_extincao:
            if r < -1e-5:
                fig.add_hline(
                    y=1.0,
                    line_dash="dot",
                    line_color="#dc2626",
                    line_width=1.5,
                    annotation_text="<b>Limiar de Extinção (N = 1)</b>",
                    annotation_position="bottom right",
                    annotation_font=dict(size=10, color="#dc2626")
                )
            elif n0 <= 1.0:
                fig.add_hline(
                    y=1.0,
                    line_dash="dot",
                    line_color="#94a3b8",
                    line_width=1.0,
                    annotation_text="Nível Inicial (N₀ = 1)",
                    annotation_position="bottom right",
                    annotation_font=dict(size=9, color="#64748b")
                )

        # 2. Marcador de Extinção no gráfico se r < 0 e t_ext <= t_end
        if r < -1e-5 and n0 > 1.0:
            t_ext = np.log(n0) / abs(r)
            if t_ext <= t_end and mostrar_extincao:
                fig.add_trace(go.Scatter(
                    x=[t_ext],
                    y=[1.0],
                    name="Extinção (N = 1)",
                    mode="markers+text",
                    marker=dict(color="#dc2626", size=10, symbol="x"),
                    text=[f"Extinção ({t_ext:.1f} anos)"],
                    textposition="top right",
                    textfont=dict(size=10, color="#b91c1c"),
                    hovertemplate="Extinção: N=1 em %{x:.2f} anos<extra></extra>"
                ))

        # 3. Marcador de Duplicação ou Meia-Vida
        if mostrar_duplicacao:
            if r > 1e-5:
                td = np.log(2.0) / r
                if td <= t_end:
                    n_dup = 2.0 * n0
                    fig.add_trace(go.Scatter(
                        x=[td],
                        y=[n_dup],
                        name="Duplicação (2× N₀)",
                        mode="markers+text",
                        marker=dict(color="#047857", size=9, symbol="diamond"),
                        text=[f"2× N₀ ({td:.1f}a, {n_dup:,.0f})"],
                        textposition="bottom right",
                        textfont=dict(size=10, color="#047857"),
                        hovertemplate="Duplicação: N=%{y:,.1f} em %{x:.2f} anos<extra></extra>"
                    ))
            elif r < -1e-5:
                thalf = np.log(2.0) / abs(r)
                if thalf <= t_end and n0 > 1.0:
                    n_half = n0 / 2.0
                    fig.add_trace(go.Scatter(
                        x=[thalf],
                        y=[n_half],
                        name="Meia-Vida (N₀/2)",
                        mode="markers+text",
                        marker=dict(color="#f59e0b", size=9, symbol="diamond"),
                        text=[f"Meia-vida ({thalf:.1f}a, {n_half:,.1f})"],
                        textposition="top right",
                        textfont=dict(size=10, color="#b45309"),
                        hovertemplate="Meia-vida: N=%{y:,.1f} em %{x:.2f} anos<extra></extra>"
                    ))

        # 4. Marcadores de Múltiplos (5x e 10x N0) para r > 0
        if mostrar_multiplos and r > 1e-5:
            t_5x = np.log(5.0) / r
            if t_5x <= t_end:
                n_5x = 5.0 * n0
                fig.add_trace(go.Scatter(
                    x=[t_5x],
                    y=[n_5x],
                    name="Quintuplicação (5× N₀)",
                    mode="markers+text",
                    marker=dict(color="#0891b2", size=8, symbol="circle"),
                    text=[f"5× N₀ ({t_5x:.1f}a)"],
                    textposition="top left",
                    textfont=dict(size=9, color="#0e7490"),
                    hovertemplate="5× N₀: N=%{y:,.1f} em %{x:.2f} anos<extra></extra>"
                ))
                
            t_10x = np.log(10.0) / r
            if t_10x <= t_end:
                n_10x = 10.0 * n0
                fig.add_trace(go.Scatter(
                    x=[t_10x],
                    y=[n_10x],
                    name="Decuplicação (10× N₀)",
                    mode="markers+text",
                    marker=dict(color="#7c3aed", size=8, symbol="star"),
                    text=[f"10× N₀ ({t_10x:.1f}a)"],
                    textposition="top left",
                    textfont=dict(size=9, color="#6d28d9"),
                    hovertemplate="10× N₀: N=%{y:,.1f} em %{x:.2f} anos<extra></extra>"
                ))

    # Linha zero de referência para taxa de variação
    if modo_grafico == "deriv":
        fig.add_hline(
            y=0.0,
            line_dash="dash",
            line_color="#94a3b8",
            line_width=1.5,
            annotation_text="dN/dt = 0 (Equilíbrio)",
            annotation_position="bottom right",
            annotation_font=dict(size=10, color="#64748b")
        )

    # Configuração de escala do eixo vertical
    yaxis_type = "log" if escala_y == "log" and modo_grafico == "pop" else "linear"
    
    # Atualização de layout geral do gráfico
    fig.update_layout(
        template="plotly_white",
        title=dict(
            text="<b>Evolução Temporal da População N(t)</b>" if modo_grafico == "pop" else "<b>Taxa Instantânea de Variação dN/dt = (a - b - c)N</b>",
            font=dict(size=14, color="#1e293b"),
            x=0.02,
            xanchor="left",
            y=0.96,
            yref="container",
            yanchor="top"
        ),
        xaxis=dict(
            title="Tempo (anos)",
            range=[0, t_end],
            gridcolor="#f1f5f9",
            zerolinecolor="#cbd5e1"
        ),
        yaxis=dict(
            title=y_axis_title,
            type=yaxis_type,
            gridcolor="#f1f5f9",
            zerolinecolor="#cbd5e1"
        ),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.18,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="#e2e8f0",
            borderwidth=1
        ),
        margin=dict(l=60, r=30, t=55, b=85),
        hovermode="x unified"
    )

    return (
        kpi_r_val, kpi_r_sub, kpi_r_card_class,
        kpi_kin_val, kpi_kin_sub,
        kpi_pop_val, kpi_pop_sub,
        kpi_thresh_title, kpi_thresh_val, kpi_thresh_sub,
        kpi_thresh_card_class, kpi_thresh_icon,
        fig
    )


# =============================================================================
# EXECUÇÃO DO APLICATIVO
# =============================================================================
if __name__ == '__main__':
    port = int(os.getenv('PORT', 8050))
    host = os.getenv('HOST', '0.0.0.0')
    app.run(debug=False, host=host, port=port)
