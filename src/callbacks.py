"""
=============================================================================
Módulo de Callbacks: Interatividade, Simulação e Atualização do Dashboard
=============================================================================
"""

import dash
from dash import Input, Output
import numpy as np
import plotly.graph_objects as go

from src.model import (
    simular_modelo,
    calcular_taxa_liquida,
    calcular_cinetica,
    calcular_populacao_final,
    calcular_limiar_extincao_expansao
)


def register_callbacks(app):
    """
    Registra todos os callbacks interativos na instância da aplicação Dash.
    """

    # =========================================================================
    # 1. BOTÕES DE PRESET PARA N0
    # =========================================================================
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

    # =========================================================================
    # 2. BADGES DINÂMICOS DOS SLIDERS
    # =========================================================================
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

    # =========================================================================
    # 3. CALLBACK PRINCIPAL: SIMULAÇÃO E RENDERIZAÇÃO
    # =========================================================================
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

        # Simulação via módulo numérico/analítico
        t_eval, n_analitica, dn_dt, _ = simular_modelo(a, b, c, n0, t_end)
        r = calcular_taxa_liquida(a, b, c)

        # 1. Taxa Líquida (r)
        sinal = "+" if r > 0 else ""
        kpi_r_val = f"{sinal}{r:.3f} ano⁻¹"
        if r > 1e-5:
            kpi_r_sub = "Crescimento Exponencial (a > b + c)"
            kpi_r_card_class = "kpi-card kpi-alive"
        elif r < -1e-5:
            kpi_r_sub = "Decaimento / Risco de Extinção (a < b + c)"
            kpi_r_card_class = "kpi-card kpi-deaths"
        else:
            kpi_r_sub = "Equilíbrio Demográfico Neutro (a = b + c)"
            kpi_r_card_class = "kpi-card kpi-vaccine"

        # 2. Cinética Populacional (td ou t1/2)
        kpi_kin_val, kpi_kin_sub = calcular_cinetica(r)

        # 3. População Final N(t_final)
        pop_final = float(n_analitica[-1])
        kpi_pop_val, kpi_pop_sub = calcular_populacao_final(pop_final, n0, t_end)

        # 4. Limiar Crítico / Extinção / Expansão
        (
            kpi_thresh_title,
            kpi_thresh_val,
            kpi_thresh_sub,
            kpi_thresh_card_class,
            kpi_thresh_icon
        ) = calcular_limiar_extincao_expansao(r, n0)

        # ==========================
        # CONSTRUÇÃO DO GRÁFICO PLOTLY
        # ==========================
        fig = go.Figure()

        if modo_grafico == "pop":
            y_data = n_analitica
            trace_name = "População N(t)"
            line_color = "#16a34a" if r >= 0 else "#dc2626"
            y_axis_title = "Número de Indivíduos (N)"
            hover_template = "Ano: %{x:.2f}<br>População: %{y:,.2f}<extra></extra>"
        else:
            y_data = dn_dt
            trace_name = "Taxa Absoluta dN/dt"
            line_color = "#2563eb" if r >= 0 else "#dc2626"
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
            # 1. Linha de Extinção (N = 1 indivíduo)
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
                        textfont=dict(size=10, color="#dc2626"),
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
                            marker=dict(color="#16a34a", size=9, symbol="diamond"),
                            text=[f"2× N₀ ({td:.1f}a, {n_dup:,.0f})"],
                            textposition="bottom right",
                            textfont=dict(size=10, color="#16a34a"),
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
