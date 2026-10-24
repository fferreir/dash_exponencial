"""
=============================================================================
Aplicação Dash: Modelo de Crescimento Exponencial de Populações (Malthus)
=============================================================================
"""

import os
import sys
import flask
import dash
import dash_bootstrap_components as dbc

# Garante que o diretório atual está no PYTHONPATH para imports locais e WSGI
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.layout import create_layout
from src.callbacks import register_callbacks

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

# Configuração do Layout e Registro de Callbacks
app.layout = create_layout()
register_callbacks(app)

# =============================================================================
# EXECUÇÃO DO APLICATIVO
# =============================================================================
if __name__ == '__main__':
    port = int(os.getenv('PORT', 8050))
    host = os.getenv('HOST', '0.0.0.0')
    app.run(debug=False, host=host, port=port)
