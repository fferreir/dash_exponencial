"""
=============================================================================
Testes unitários para o modelo matemático exponencial (Malthus).
=============================================================================
"""

import pytest
import numpy as np

from src.model import (
    ode_sys,
    solucao_analitica,
    calcular_taxa_liquida,
    calcular_cinetica,
    calcular_populacao_final,
    calcular_limiar_extincao_expansao,
    simular_modelo
)


def test_ode_sys_zero_population():
    """Se a população for zero, a taxa de variação deve ser nula."""
    deriv = ode_sys(0.0, [0.0], a=0.10, b=0.05, c=0.0)
    assert deriv == [0.0]


def test_ode_sys_derivative_calculation():
    """Testa dN/dt = (a - b - c) * N para crescimento e declínio."""
    # Crescimento: (0.10 - 0.05 - 0.0) * 100 = 5.0
    deriv_pos = ode_sys(0.0, [100.0], a=0.10, b=0.05, c=0.0)
    assert pytest.approx(deriv_pos[0], 1e-6) == 5.0

    # Declínio: (0.10 - 0.15 - 0.10) * 100 = -15.0
    deriv_neg = ode_sys(0.0, [100.0], a=0.10, b=0.15, c=0.10)
    assert pytest.approx(deriv_neg[0], 1e-6) == -15.0


def test_solucao_analitica_exactness():
    """Valida a solução exata N(t) = N0 * exp(r * t)."""
    t = np.array([0.0, 10.0, 20.0])
    n0 = 10.0
    a, b, c = 0.10, 0.05, 0.0  # r = 0.05
    n_expected = 10.0 * np.exp(0.05 * t)
    n_calc = solucao_analitica(t, n0, a, b, c)
    assert np.allclose(n_calc, n_expected, rtol=1e-5)


def test_numerical_analytical_agreement():
    """Valida a concordância da integração numérica RK45 com a solução analítica."""
    t_eval, n_analitica, dn_dt, n_ode = simular_modelo(
        a=0.10, b=0.05, c=0.0, n0=10.0, t_end=50.0, t_nsamples=500
    )
    # A diferença relativa entre RK45 e a solução analítica deve ser muito pequena (< 0.1%)
    assert np.allclose(n_ode, n_analitica, rtol=1e-3)
    # Verifica dN/dt = r * N
    r = 0.10 - 0.05 - 0.0
    assert np.allclose(dn_dt, r * n_analitica, rtol=1e-5)


def test_taxa_liquida():
    """Verifica o cálculo da taxa intrínseca líquida r = a - b - c."""
    assert pytest.approx(calcular_taxa_liquida(0.10, 0.05, 0.0), 1e-6) == 0.05
    assert pytest.approx(calcular_taxa_liquida(0.10, 0.10, 0.0), 1e-6) == 0.00
    assert pytest.approx(calcular_taxa_liquida(0.10, 0.15, 0.05), 1e-6) == -0.10


def test_calcular_cinetica_duplicacao():
    """Para r > 0, td = ln(2) / r."""
    r = 0.05
    val, sub = calcular_cinetica(r)
    expected_td = np.log(2.0) / 0.05  # ~13.86
    assert f"{expected_td:.2f} anos" == val
    assert "duplicação" in sub


def test_calcular_cinetica_meia_vida():
    """Para r < 0, t1/2 = ln(2) / |r|."""
    r = -0.10
    val, sub = calcular_cinetica(r)
    expected_thalf = np.log(2.0) / 0.10  # ~6.93
    assert f"{expected_thalf:.2f} anos" == val
    assert "meia-vida" in sub


def test_calcular_cinetica_estabilidade():
    """Para r == 0, a cinética deve reportar estabilidade."""
    val, sub = calcular_cinetica(0.0)
    assert val == "Estável"
    assert "constante" in sub


def test_calcular_limiar_expansao():
    """Para r > 0, calcula tempo para 10x N0."""
    r = 0.05
    n0 = 10.0
    titulo, val, sub, card_class, icon = calcular_limiar_extincao_expansao(r, n0)
    expected_10x = np.log(10.0) / 0.05  # ~46.05
    assert "Expansão (10× N₀)" == titulo
    assert f"{expected_10x:.2f} anos" == val
    assert "fa-rocket" in icon


def test_calcular_limiar_extincao():
    """Para r < 0, calcula tempo de extinção (N < 1)."""
    r = -0.05
    n0 = 1000.0
    titulo, val, sub, card_class, icon = calcular_limiar_extincao_expansao(r, n0)
    expected_text = np.log(1000.0) / 0.05  # ~138.16
    assert "Tempo até a Extinção" == titulo
    assert f"{expected_text:.2f} anos" == val
    assert "fa-skull-crossbones" in icon


def test_calcular_populacao_final_formatacao():
    """Verifica a formatação de números grandes, médios e decimais."""
    # População extinta (< 1)
    val, sub = calcular_populacao_final(0.05, 100.0, 70.0)
    assert val == "0.050"
    assert "extinta" in sub

    # População muito grande (>= 1e7)
    val_big, _ = calcular_populacao_final(1.5e8, 10.0, 50.0)
    assert "e+" in val_big


def test_overflow_protection():
    """Verifica proteção contra overflow em exponenciais elevadas."""
    t_large = np.array([1000.0])
    # r = 10.0 * 1000.0 geraria overflow sem np.clip
    res = solucao_analitica(t_large, n0=1.0, a=10.0, b=0.0, c=0.0)
    assert not np.isnan(res).any()
    assert not np.isinf(res).any()
