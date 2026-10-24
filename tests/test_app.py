"""
=============================================================================
Testes de integração para a interface e inicialização do Dash.
=============================================================================
"""

import pytest
from app import app, server


def test_app_instance():
    """Verifica se a aplicação Dash e o servidor Flask foram inicializados corretamente."""
    assert app is not None
    assert server is not None
    assert app.server == server


def test_app_layout_structure():
    """Verifica se o layout do Dash é gerado com sucesso."""
    layout = app.layout
    assert layout is not None


def test_callbacks_registered():
    """Verifica se os callbacks essenciais foram registrados na aplicação."""
    callback_map = app.callback_map
    assert len(callback_map) >= 3

    # Callback principal do gráfico e KPIs
    assert any("population_chart.figure" in k for k in callback_map.keys())

    # Callback de badges
    assert any("badge_a.children" in k for k in callback_map.keys())

    # Callback de presets de N0
    assert any("n0.value" in k for k in callback_map.keys())
