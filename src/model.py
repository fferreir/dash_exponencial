"""
=============================================================================
Módulo Matemático e Numérico: Modelo de Crescimento Exponencial de Populações
=============================================================================
Modelo Malthusiano clássico com natalidade, mortalidade natural e adicional:
  dN/dt = (a - b - c) * N = r * N
"""

import numpy as np
from scipy.integrate import solve_ivp


def ode_sys(t, state, a, b, c):
    """
    Sistema de crescimento/decaimento exponencial populacional.
    dN/dt = (a - b - c) * N = r * N

    Estado:
      state[0]: Tamanho populacional N

    Parâmetros:
      t: Tempo
      state: Vetor de estado [N]
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
    expoente = np.clip(r * np.asarray(t_arr, dtype=float), -100.0, 100.0)
    return n0_eff * np.exp(expoente)


def calcular_taxa_liquida(a, b, c):
    """
    Calcula a taxa intrínseca líquida per capita r = a - b - c.
    """
    return float(a) - float(b) - float(c)


def calcular_cinetica(r):
    """
    Calcula a cinética populacional: tempo de duplicação (td) se r > 0,
    tempo de meia-vida (t1/2) se r < 0, ou estabilidade se r == 0.

    Retorna:
      (kpi_kin_val, kpi_kin_sub)
    """
    if r > 1e-5:
        td = np.log(2.0) / r
        return f"{td:.2f} anos", "Tempo de duplicação: td = ln(2)/r"
    elif r < -1e-5:
        thalf = np.log(2.0) / abs(r)
        return f"{thalf:.2f} anos", "Tempo de meia-vida: t₁/₂ = ln(2)/|r|"
    else:
        return "Estável", "População constante ao longo do tempo"


def calcular_populacao_final(pop_final, n0, t_end):
    """
    Formata e calcula as métricas de população final N(t_final) e variação percentual.

    Retorna:
      (kpi_pop_val, kpi_pop_sub)
    """
    pop_final = float(pop_final)
    n0 = float(n0)
    t_end = float(t_end)

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

    return kpi_pop_val, kpi_pop_sub


def calcular_limiar_extincao_expansao(r, n0):
    """
    Calcula o tempo para decuplicar (10x N0) se r > 0, ou tempo de extinção
    biológica efetiva (N < 1) se r < 0, ou estabilidade se r == 0.

    Retorna:
      (titulo, valor, subtitulo, card_class, icon_class)
    """
    r = float(r)
    n0 = float(n0)

    if r > 1e-5:
        t_10x = np.log(10.0) / r
        return (
            "Expansão (10× N₀)",
            f"{t_10x:.2f} anos",
            "Tempo para decuplicar (10× o tamanho inicial)",
            "kpi-card kpi-vaccine",
            "fa-solid fa-rocket kpi-icon"
        )
    elif r < -1e-5:
        titulo = "Tempo até a Extinção"
        card_class = "kpi-card kpi-deaths"
        icon_class = "fa-solid fa-skull-crossbones kpi-icon"
        if n0 > 1.0:
            t_ext = np.log(n0) / abs(r)
            return (
                titulo,
                f"{t_ext:.2f} anos",
                "Tempo até restar menos de 1 indivíduo (N < 1)",
                card_class,
                icon_class
            )
        else:
            return (
                titulo,
                "< 1 ano",
                "N₀ já está no limiar crítico de extinção (N ≤ 1)",
                card_class,
                icon_class
            )
    else:
        return (
            "Equilíbrio Demográfico",
            "Estável",
            "Equilíbrio perpétuo (dN/dt = 0, sem extinção)",
            "kpi-card kpi-peak",
            "fa-solid fa-scale-balanced kpi-icon"
        )


def simular_modelo(a, b, c, n0, t_end, t_nsamples=1000):
    """
    Executa a simulação numérica e analítica do modelo exponencial.

    Retorna:
      t_eval: Vetor temporal de avaliação
      n_analitica: Solução analítica exata N(t)
      dn_dt: Taxa instantânea absoluta dN/dt
      n_ode: Solução numérica calculada via solve_ivp (RK45)
    """
    a = float(a)
    b = float(b)
    c = float(c)
    n0 = float(n0)
    t_end = float(t_end)

    r = a - b - c
    t_eval = np.linspace(0.0, t_end, t_nsamples)

    # Solução por EDO (solve_ivp com método RK45)
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

    return t_eval, n_analitica, dn_dt, n_ode
