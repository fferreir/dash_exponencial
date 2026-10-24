"""
=============================================================================
Módulo de Layout: Componentes Visuais e Estrutura da Interface Dash
=============================================================================
"""

from dash import html, dcc
import dash_bootstrap_components as dbc

# =============================================================================
# CABEÇALHO DO DASHBOARD (HERO HEADER)
# =============================================================================
cabecalho = html.Div(
    [
        html.Div(
            [
                html.H1(
                    [
                        html.I(className="fa-solid fa-chart-line me-2"),
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
                html.I(className="fa-solid fa-sliders me-2 text-primary"),
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
                    html.Span(id="badge_b", className="slider-val-badge bg-danger text-white")
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
                    html.Span(id="badge_c", className="slider-val-badge bg-info text-white")
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
                html.I(className="fa-solid fa-users me-2 text-success"),
                "Condições Iniciais e Horizonte"
            ],
            className="card-header"
        ),
        html.Div(
            [
                html.Div([
                    dbc.Label(dcc.Markdown(r'População inicial ($$N_0$$):', mathjax=True), className="mb-0"),
                    html.Span(id="badge_n0", className="slider-val-badge")
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
                    html.Span(id="badge_t_max", className="slider-val-badge")
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
                html.I(className="fa-solid fa-gear me-2 text-info"),
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
                className="kpi-card kpi-alive"
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
                className="kpi-card kpi-peak"
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
                className="kpi-card kpi-vaccine"
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
                className="kpi-card kpi-deaths"
            ),
            width=6, sm=6, lg=3, className="mb-2"
        ),
    ],
    className="mb-2"
)


# =============================================================================
# FUNÇÃO PRINCIPAL DE CONSTRUÇÃO DO LAYOUT
# =============================================================================
def create_layout():
    """
    Constrói e retorna a árvore completa de componentes da interface do Dash.
    """
    return dbc.Container(
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
                                                    html.I(className="fa-solid fa-chart-line me-2 text-primary"),
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
                        html.A("Código-fonte no GitHub", href="https://github.com/fferreir/dash_exponencial", target="_blank", className="text-decoration-none text-primary fw-semibold"),
                    ],
                    className="text-center py-3 border-top mt-4 small"
                )
            )
        ],
        fluid=True,
        className="px-3 py-2"
    )
