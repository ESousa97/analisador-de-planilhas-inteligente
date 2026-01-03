"""Dashboard Web para visualização de dados analisados."""

import json
import logging

import dash
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, dcc, html
from flask import request

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────────────────────
# 1. Tema + fonte
# ──────────────────────────────────────────────────────────────────────────────
external_stylesheets = [
    dbc.themes.DARKLY,
    dbc.icons.FONT_AWESOME,
    "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap",
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
stored_indicators = None

# ──────────────────────────────────────────────────────────────────────────────
# 2. Paleta & estilos modernos
# ──────────────────────────────────────────────────────────────────────────────
COLORWAY = [
    "#6366F1",  # Indigo
    "#22D3EE",  # Cyan
    "#F59E0B",  # Amber
    "#10B981",  # Emerald
    "#EF4444",  # Red
    "#8B5CF6",  # Violet
    "#EC4899",  # Pink
    "#14B8A6",  # Teal
    "#F97316",  # Orange
    "#84CC16",  # Lime
]

CARD_STYLE = {
    "backgroundColor": "rgba(17, 24, 39, 0.95)",
    "backdropFilter": "blur(12px)",
    "borderRadius": "16px",
    "border": "1px solid rgba(99, 102, 241, 0.2)",
    "boxShadow": "0 4px 24px rgba(0, 0, 0, 0.4)",
    "marginBottom": "24px",
    "transition": "all 0.3s ease",
}

HEADER_STYLE = {
    "background": "linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%)",
    "fontFamily": "Inter, sans-serif",
    "fontWeight": 600,
    "letterSpacing": "0.5px",
    "borderRadius": "16px 16px 0 0",
    "padding": "16px 20px",
}

GRAPH_CONFIG = {
    "displayModeBar": True,
    "displaylogo": False,
    "modeBarButtonsToRemove": ["lasso2d", "select2d"],
    "responsive": True,
}

GRAPH_LAYOUT = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font": {"family": "Inter, sans-serif", "color": "#E5E7EB"},
    "margin": {"l": 60, "r": 40, "t": 50, "b": 60},
    "legend": {"orientation": "h", "yanchor": "bottom", "y": -0.25, "xanchor": "center", "x": 0.5},
}


# ──────────────────────────────────────────────────────────────────────────────
# 3. Componentes de estatísticas
# ──────────────────────────────────────────────────────────────────────────────
def create_stat_card(title: str, value: str, icon: str, color: str) -> dbc.Card:
    """Cria um card de estatística com ícone."""
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    [
                        html.I(className=f"fas {icon} fa-2x", style={"color": color}),
                        html.Div(
                            [
                                html.H4(
                                    value,
                                    className="mb-0",
                                    style={"fontWeight": 700, "color": "#FFF"},
                                ),
                                html.Small(title, style={"color": "#9CA3AF"}),
                            ],
                            className="ms-3",
                        ),
                    ],
                    className="d-flex align-items-center",
                ),
            ],
            style={"padding": "20px"},
        ),
        style={
            **CARD_STYLE,
            "border": f"1px solid {color}30",
            "marginBottom": "16px",
        },
    )


# ──────────────────────────────────────────────────────────────────────────────
# 4. Layout principal - todos os gráficos empilhados verticalmente
# ──────────────────────────────────────────────────────────────────────────────
app.layout = dbc.Container(
    [
        # Intervalo para auto-refresh
        dcc.Interval(id="interval-refresh", interval=2000, n_intervals=0),
        dcc.Store(id="data-store"),
        # Header
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.H1(
                            [
                                html.I(className="fas fa-chart-line me-3"),
                                "Analisador de Planilhas",
                            ],
                            className="text-center mb-2",
                            style={
                                "fontFamily": "Inter",
                                "fontWeight": 700,
                                "background": "linear-gradient(135deg, #6366F1, #22D3EE)",
                                "WebkitBackgroundClip": "text",
                                "WebkitTextFillColor": "transparent",
                                "fontSize": "2.5rem",
                            },
                        ),
                        html.P(
                            "Dashboard de Visualizacao de Dados",
                            className="text-center text-muted mb-4",
                            style={"fontFamily": "Inter", "fontSize": "1rem"},
                        ),
                    ]
                ),
                width=12,
            )
        ),
        # Cards de estatísticas
        dbc.Row(id="stats-cards", className="mb-4"),
        # Container principal de gráficos (empilhados verticalmente)
        html.Div(
            id="charts-container",
            style={"display": "flex", "flexDirection": "column", "gap": "24px"},
        ),
        # Footer
        dbc.Row(
            dbc.Col(
                html.Footer(
                    [
                        html.Hr(
                            style={
                                "borderColor": "rgba(99, 102, 241, 0.3)",
                                "margin": "32px 0 16px",
                            }
                        ),
                        html.P(
                            [
                                html.I(className="fas fa-code me-2"),
                                "2025 Analisador Inteligente de Planilhas | Jose Enoque",
                            ],
                            className="text-center",
                            style={"color": "#6B7280", "fontFamily": "Inter", "fontSize": "13px"},
                        ),
                    ]
                ),
                width=12,
            )
        ),
    ],
    fluid=True,
    style={"padding": "32px 48px", "minHeight": "100vh", "backgroundColor": "#0F172A"},
)


# ──────────────────────────────────────────────────────────────────────────────
# 5. Rota de recepção de dados
# ──────────────────────────────────────────────────────────────────────────────
@server.route("/update_data", methods=["POST"])
def update_data():
    """Recebe dados do analisador e armazena para visualização."""
    global stored_indicators
    data = request.get_json()
    if not data:
        return {"error": "No data received"}, 400

    # Obtém o nome da coluna de ID nativo (se existir)
    native_id_col = data.get("id_coluna")
    is_synthetic = data.get("id_is_synthetic", False)

    # Processa cada agrupamento mantendo integridade dos dados
    for idx, g in enumerate(data.get("agrupamentos", [])):
        t = g.get("tabela")
        if isinstance(t, str):
            try:
                g["tabela"] = json.loads(t)
            except json.JSONDecodeError:
                g["tabela"] = None

        # Adiciona ID único ao agrupamento (para identificar o grupo, não os dados)
        if "id" not in g:
            g["id"] = f"grp_{idx}"

        # Preserva referência ao ID nativo nos registros
        # NÃO cria _row_id se já existe coluna "ids" com IDs nativos
        if g.get("tabela") and isinstance(g["tabela"], list):
            for row_idx, row in enumerate(g["tabela"]):
                if isinstance(row, dict):
                    # Marca índice de exibição (apenas para ordenação visual)
                    if "_display_order" not in row:
                        row["_display_order"] = row_idx
                    # Referência ao ID nativo usado
                    if "_native_id_col" not in row:
                        row["_native_id_col"] = native_id_col
                    row["_id_is_synthetic"] = is_synthetic

    stored_indicators = data
    return {
        "status": "success",
        "groups": len(data.get("agrupamentos", [])),
        "id_column": native_id_col,
        "id_is_synthetic": is_synthetic,
    }


# ──────────────────────────────────────────────────────────────────────────────
# 6. Funções auxiliares para processamento de dados
# ──────────────────────────────────────────────────────────────────────────────
def normalize_dataframe(
    df: pd.DataFrame, column_name: str, native_id_col: str | None = None
) -> pd.DataFrame:
    """
    Normaliza DataFrame preservando todos os dados e metadados.

    IMPORTANTE: Não cria IDs artificiais se já existir coluna de ID nativa.
    """
    if df.empty:
        return df

    # Sempre trabalha com cópia para não modificar original
    df = df.copy()

    # Verifica se já existe coluna "ids" (referência aos IDs nativos do indicator.py)
    has_native_ids = "ids" in df.columns

    # Adiciona índice de exibição apenas se necessário (para ordenação visual)
    if "_display_order" not in df.columns:
        df["_display_order"] = range(len(df))

    # Adiciona coluna de origem
    if "_source_column" not in df.columns:
        df["_source_column"] = column_name

    # Marca se tem IDs nativos
    df["_has_native_ids"] = has_native_ids
    if native_id_col:
        df["_native_id_col"] = native_id_col

    return df


def get_dataframe_info(df: pd.DataFrame, column_name: str = "") -> dict:
    """Extrai informações do DataFrame usando nomes originais das colunas."""
    # Colunas originais (excluindo metadados internos)
    original_cols = [c for c in df.columns if not c.startswith("_")]

    # Detecta coluna de IDs nativos (do indicator.py)
    native_ids_col = "ids" if "ids" in df.columns else None

    # Detecta coluna de label (termo/categoria) - usa nome original
    label_candidates = ["termo_base", "termo", "categoria", "nome", "label", "item", "descricao"]
    label_col = next((c for c in label_candidates if c in df.columns), None)

    # Se não encontrou, usa primeira coluna categórica
    if not label_col:
        cat_cols = df.select_dtypes(include=["object", "category"]).columns
        cat_cols = [c for c in cat_cols if not c.startswith("_")]
        label_col = cat_cols[0] if len(cat_cols) > 0 else None

    # Detecta coluna de frequência
    freq_col = next(
        (c for c in ["frequencia", "freq", "count", "contagem", "qtd"] if c in df.columns), None
    )

    # Detecta coluna de valor numérico
    val_candidates = ["valor", "valor_medio", "media", "total", "soma", "amount", "value"]
    val_col = next((c for c in val_candidates if c in df.columns), None)

    # Todas colunas numéricas (excluindo metadados)
    num_cols = [c for c in df.select_dtypes(include=[np.number]).columns if not c.startswith("_")]

    # Todas colunas categóricas (excluindo metadados)
    cat_cols = [
        c for c in df.select_dtypes(include=["object", "category"]).columns if not c.startswith("_")
    ]

    return {
        "label_col": label_col,
        "freq_col": freq_col,
        "val_col": val_col,
        "num_cols": num_cols,
        "cat_cols": cat_cols,
        "original_cols": original_cols,
        "total_rows": len(df),
        "source": column_name,
        "native_ids_col": native_ids_col,  # ID nativo detectado (se houver)
    }


def get_display_name(col_name: str | None) -> str:
    """Converte nome de coluna para exibição amigável."""
    if col_name is None:
        return "Valor"
    return str(col_name).replace("_", " ").title()


# ──────────────────────────────────────────────────────────────────────────────
# 7. Funções de criação de gráficos (preservam todos os dados)
# ──────────────────────────────────────────────────────────────────────────────
def create_frequency_bar_chart(df: pd.DataFrame, info: dict, title: str) -> go.Figure | None:
    """Gráfico de barras horizontais mostrando TODOS os dados ordenados."""
    if not info["freq_col"] or not info["label_col"]:
        return None

    # Usa todos os dados, ordenados por frequência
    plot_df = df.sort_values(info["freq_col"], ascending=True).copy()
    label_name = get_display_name(info["label_col"])

    fig = px.bar(
        plot_df,
        y=info["label_col"],
        x=info["freq_col"],
        orientation="h",
        color=info["freq_col"],
        color_continuous_scale="Viridis",
        template="plotly_dark",
        custom_data=["_row_id"] if "_row_id" in plot_df.columns else None,
        labels={info["label_col"]: label_name, info["freq_col"]: "Frequencia"},
    )
    fig.update_layout(
        **GRAPH_LAYOUT,
        title={
            "text": f"Frequencias - {title} ({len(plot_df)} itens)",
            "x": 0.5,
            "font": {"size": 16},
        },
        yaxis={"title": label_name, "autorange": "reversed"},
        xaxis={"title": "Frequencia", "gridcolor": "rgba(99,102,241,0.1)"},
        coloraxis_showscale=False,
        height=max(400, len(plot_df) * 25),  # Altura dinâmica baseada na quantidade
    )
    fig.update_traces(
        marker_line_width=0,
        hovertemplate=f"<b>%{{y}}</b><br>{get_display_name(info['freq_col'])}: %{{x}}<extra></extra>",
    )
    return fig


def create_distribution_pie(df: pd.DataFrame, info: dict, title: str) -> go.Figure | None:
    """Gráfico de pizza com todos os dados (agrupa menores em 'Outros')."""
    if not info["label_col"]:
        return None

    value_col = info["freq_col"] or info["val_col"]
    if not value_col:
        return None

    # Ordena por valor
    sorted_df = df.sort_values(value_col, ascending=False).copy()

    # Se muitos itens, agrupa os menores em "Outros"
    if len(sorted_df) > 8:
        top_df = sorted_df.head(7).copy()
        others_sum = sorted_df.iloc[7:][value_col].sum()
        others_count = len(sorted_df) - 7
        others_row = pd.DataFrame(
            {
                info["label_col"]: [f"Outros ({others_count} itens)"],
                value_col: [others_sum],
            }
        )
        plot_df = pd.concat([top_df[[info["label_col"], value_col]], others_row], ignore_index=True)
    else:
        plot_df = sorted_df[[info["label_col"], value_col]].copy()

    fig = px.pie(
        plot_df,
        names=info["label_col"],
        values=value_col,
        template="plotly_dark",
        color_discrete_sequence=COLORWAY,
        hole=0.4,
    )
    fig.update_layout(
        **GRAPH_LAYOUT,
        title={
            "text": f"Distribuicao - {title} (Total: {len(df)} itens)",
            "x": 0.5,
            "font": {"size": 16},
        },
        height=450,
        showlegend=True,
        legend={"font": {"size": 11}},
    )
    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        marker={"line": {"color": "#1F2937", "width": 2}},
        hovertemplate=f"<b>%{{label}}</b><br>{get_display_name(value_col)}: %{{value:,.0f}}<br>Percentual: %{{percent}}<extra></extra>",
    )
    return fig


def create_treemap(df: pd.DataFrame, info: dict, title: str) -> go.Figure | None:
    """Treemap mostrando proporções de todos os itens."""
    if not info["freq_col"] or not info["label_col"]:
        return None

    # Usa todos os dados
    plot_df = df.copy()

    fig = px.treemap(
        plot_df,
        path=[info["label_col"]],
        values=info["freq_col"],
        color=info["freq_col"],
        color_continuous_scale="RdYlGn",
        template="plotly_dark",
    )
    fig.update_layout(
        **GRAPH_LAYOUT,
        title={
            "text": f"Mapa de Proporcoes - {title} ({len(plot_df)} itens)",
            "x": 0.5,
            "font": {"size": 16},
        },
        height=500,
        coloraxis_showscale=True,
        coloraxis_colorbar={"title": "Freq."},
    )
    fig.update_traces(
        hovertemplate="<b>%{label}</b><br>Frequencia: %{value:,.0f}<br>Percentual: %{percentRoot:.1%}<extra></extra>",
        textinfo="label+value+percent root",
    )
    return fig


def create_histogram(df: pd.DataFrame, info: dict, _title: str) -> go.Figure | None:
    """Histograma para distribuição de valores numéricos."""
    if not info["num_cols"]:
        return None

    col = info["val_col"] or info["freq_col"] or info["num_cols"][0]
    col_name = get_display_name(col)

    fig = px.histogram(
        df,
        x=col,
        nbins=min(30, len(df)),  # Bins dinâmicos baseados na quantidade de dados
        template="plotly_dark",
        color_discrete_sequence=["#6366F1"],
        labels={col: col_name},
    )
    fig.update_layout(
        **GRAPH_LAYOUT,
        title={
            "text": f"Distribuicao - {col_name} ({len(df)} registros)",
            "x": 0.5,
            "font": {"size": 16},
        },
        xaxis={"title": col_name, "gridcolor": "rgba(99,102,241,0.1)"},
        yaxis={"title": "Contagem", "gridcolor": "rgba(99,102,241,0.1)"},
        height=350,
        bargap=0.05,
    )
    fig.update_traces(
        marker_line_width=1,
        marker_line_color="#4F46E5",
        hovertemplate=f"{col_name}: %{{x}}<br>Contagem: %{{y}}<extra></extra>",
    )
    return fig


def create_box_plot(df: pd.DataFrame, info: dict, title: str) -> go.Figure | None:
    """Box plot para análise estatística completa."""
    val = info["val_col"] or info["freq_col"]
    if not val:
        return None

    val_name = get_display_name(val)

    if info["label_col"] and df[info["label_col"]].nunique() <= 10:
        fig = px.box(
            df,
            x=info["label_col"],
            y=val,
            template="plotly_dark",
            color_discrete_sequence=COLORWAY,
            labels={info["label_col"]: get_display_name(info["label_col"]), val: val_name},
            points="outliers",  # Mostra outliers
        )
    else:
        fig = px.box(
            df,
            y=val,
            template="plotly_dark",
            color_discrete_sequence=["#22D3EE"],
            labels={val: val_name},
            points="outliers",
        )

    fig.update_layout(
        **GRAPH_LAYOUT,
        title={
            "text": f"Analise Estatistica - {title} ({len(df)} registros)",
            "x": 0.5,
            "font": {"size": 16},
        },
        height=350,
        xaxis={"gridcolor": "rgba(99,102,241,0.1)"},
        yaxis={"gridcolor": "rgba(99,102,241,0.1)"},
    )
    return fig


def create_complete_data_table(df: pd.DataFrame, _info: dict, title: str) -> dbc.Card:
    """Tabela completa com TODOS os dados originais (paginada)."""
    # Remove colunas internas de metadados para exibição
    display_cols = [c for c in df.columns if not c.startswith("_")]
    display_df = df[display_cols].copy()

    # Limita exibição inicial a 50 linhas, mas mostra total
    max_display = 50
    total_rows = len(display_df)
    show_df = display_df.head(max_display) if total_rows > max_display else display_df

    # Cabeçalho com nomes originais formatados
    table_header = [
        html.Thead(
            html.Tr(
                [
                    html.Th(get_display_name(c), style={"whiteSpace": "nowrap"})
                    for c in show_df.columns
                ]
            )
        )
    ]

    # Corpo da tabela
    rows = []
    for _, row in show_df.iterrows():
        cells = []
        for col in show_df.columns:
            val = row[col]
            if pd.isna(val):
                cells.append(html.Td("-", style={"color": "#6B7280"}))
            elif isinstance(val, float):
                cells.append(html.Td(f"{val:,.2f}"))
            else:
                cells.append(html.Td(str(val)))
        rows.append(html.Tr(cells))
    table_body = [html.Tbody(rows)]

    # Indicador de dados truncados
    truncation_notice = None
    if total_rows > max_display:
        truncation_notice = html.Div(
            f"Exibindo {max_display} de {total_rows} registros",
            className="text-center mt-2",
            style={"color": "#F59E0B", "fontSize": "12px"},
        )

    return dbc.Card(
        [
            dbc.CardHeader(
                [
                    html.I(className="fas fa-table me-2"),
                    f"Dados Completos - {title} ({total_rows} registros)",
                ],
                style=HEADER_STYLE,
            ),
            dbc.CardBody(
                [
                    html.Div(
                        dbc.Table(
                            table_header + table_body,
                            bordered=True,
                            hover=True,
                            responsive=True,
                            striped=True,
                            className="mb-0",
                            style={"fontSize": "13px"},
                        ),
                        style={"maxHeight": "400px", "overflowY": "auto"},
                    ),
                    truncation_notice,
                ],
                style={"padding": "16px", "backgroundColor": "rgba(17,24,39,0.8)"},
            ),
        ],
        style=CARD_STYLE,
    )


def create_summary_stats(df: pd.DataFrame, info: dict, title: str) -> dbc.Card | None:
    """Card com estatísticas resumidas."""
    if not info["num_cols"]:
        return None

    stats_data = []
    for col in info["num_cols"][:4]:  # Máximo 4 colunas numéricas
        col_data = df[col].dropna()
        if len(col_data) == 0:
            continue
        stats_data.append(
            {
                "Coluna": get_display_name(col),
                "Min": f"{col_data.min():,.2f}",
                "Max": f"{col_data.max():,.2f}",
                "Media": f"{col_data.mean():,.2f}",
                "Mediana": f"{col_data.median():,.2f}",
                "Desvio": f"{col_data.std():,.2f}",
            }
        )

    if not stats_data:
        return None

    table_header = [html.Thead(html.Tr([html.Th(k) for k in stats_data[0]]))]
    rows = [html.Tr([html.Td(v) for v in row.values()]) for row in stats_data]
    table_body = [html.Tbody(rows)]

    return dbc.Card(
        [
            dbc.CardHeader(
                [html.I(className="fas fa-calculator me-2"), f"Estatisticas - {title}"],
                style=HEADER_STYLE,
            ),
            dbc.CardBody(
                dbc.Table(
                    table_header + table_body,
                    bordered=True,
                    hover=True,
                    responsive=True,
                    striped=True,
                    className="mb-0",
                    style={"fontSize": "13px"},
                ),
                style={"padding": "16px", "backgroundColor": "rgba(17,24,39,0.8)"},
            ),
        ],
        style=CARD_STYLE,
    )


def create_chart_card(title: str, icon: str, figure: go.Figure) -> dbc.Card:
    """Cria um card contendo um gráfico."""
    return dbc.Card(
        [
            dbc.CardHeader(
                [html.I(className=f"fas {icon} me-2"), title],
                style=HEADER_STYLE,
            ),
            dbc.CardBody(
                dcc.Graph(figure=figure, config=GRAPH_CONFIG),
                style={"padding": "8px"},
            ),
        ],
        style=CARD_STYLE,
    )


# ──────────────────────────────────────────────────────────────────────────────
# 8. Callbacks principais
# ──────────────────────────────────────────────────────────────────────────────
@app.callback(
    [Output("stats-cards", "children"), Output("charts-container", "children")],
    Input("interval-refresh", "n_intervals"),
)
def render_dashboard(_n_intervals):
    """Renderiza todo o dashboard com gráficos empilhados verticalmente."""
    try:
        if not stored_indicators:
            return [], html.Div(
                [
                    html.I(className="fas fa-inbox fa-4x mb-3", style={"color": "#4B5563"}),
                    html.H4("Aguardando Dados...", style={"color": "#9CA3AF"}),
                    html.P(
                        "Carregue uma planilha no aplicativo desktop para visualizar os graficos.",
                        style={"color": "#6B7280"},
                    ),
                ],
                className="text-center py-5",
            )

        all_charts = []
        total_records = 0
        total_columns = len(stored_indicators.get("agrupamentos", []))
        total_unique_terms = 0
        total_data_points = 0

        # Processa cada agrupamento preservando todos os dados
        for grp in stored_indicators.get("agrupamentos", []):
            try:
                raw_data = grp.get("tabela") or []
                if not raw_data:
                    continue

                # Cria DataFrame com todos os dados
                df = pd.DataFrame(raw_data)
                if df.empty:
                    continue

                # Normaliza mantendo integridade
                title = grp.get("coluna", "Dados")
                df = normalize_dataframe(df, title)
                info = get_dataframe_info(df, title)

                # Contadores para estatísticas globais
                total_records += info["total_rows"]
                total_data_points += info["total_rows"] * len(info["original_cols"])
                if info["label_col"]:
                    total_unique_terms += df[info["label_col"]].nunique()

                # ─────────────────────────────────────────────────────────────────────
                # Seção: Visão Geral do Agrupamento
                # ─────────────────────────────────────────────────────────────────────
                section_header = html.Div(
                    [
                        html.H3(
                            [html.I(className="fas fa-layer-group me-2"), title],
                            style={
                                "color": "#E5E7EB",
                                "fontFamily": "Inter",
                                "fontWeight": 600,
                                "marginBottom": "16px",
                                "paddingBottom": "8px",
                                "borderBottom": "2px solid #6366F1",
                            },
                        ),
                        html.P(
                            f"{info['total_rows']} registros | {len(info['original_cols'])} colunas | ID: {grp.get('id', 'N/A')}",
                            style={"color": "#9CA3AF", "fontSize": "14px", "marginBottom": "20px"},
                        ),
                    ]
                )
                all_charts.append(section_header)

                # Gráficos com tratamento de erro individual
                try:
                    bar_fig = create_frequency_bar_chart(df, info, title)
                    if bar_fig:
                        all_charts.append(
                            create_chart_card(f"Frequencias - {title}", "fa-chart-bar", bar_fig)
                        )
                except Exception:
                    pass  # Gráfico de barras falhou, continua com outros

                try:
                    pie_fig = create_distribution_pie(df, info, title)
                    if pie_fig:
                        all_charts.append(
                            create_chart_card(f"Distribuicao - {title}", "fa-chart-pie", pie_fig)
                        )
                except Exception:
                    pass  # Gráfico de pizza falhou, continua com outros

                try:
                    treemap_fig = create_treemap(df, info, title)
                    if treemap_fig:
                        all_charts.append(
                            create_chart_card(f"Proporcoes - {title}", "fa-th-large", treemap_fig)
                        )
                except Exception:
                    pass  # Treemap falhou, continua com outros

                try:
                    hist_fig = create_histogram(df, info, title)
                    if hist_fig:
                        all_charts.append(
                            create_chart_card(f"Histograma - {title}", "fa-signal", hist_fig)
                        )
                except Exception:
                    pass  # Histograma falhou, continua com outros

                try:
                    box_fig = create_box_plot(df, info, title)
                    if box_fig:
                        all_charts.append(
                            create_chart_card(f"Box Plot - {title}", "fa-boxes-stacked", box_fig)
                        )
                except Exception:
                    pass  # Box plot falhou, continua com outros

                try:
                    stats_card = create_summary_stats(df, info, title)
                    if stats_card:
                        all_charts.append(stats_card)
                except Exception:
                    pass  # Stats card falhou, continua com outros

                try:
                    data_table = create_complete_data_table(df, info, title)
                    if data_table:
                        all_charts.append(data_table)
                except Exception:
                    pass  # Tabela de dados falhou, continua com outros

                # Separador visual entre seções
                all_charts.append(
                    html.Hr(style={"borderColor": "rgba(99,102,241,0.2)", "margin": "32px 0"})
                )

            except Exception:
                logger.exception("Erro ao processar agrupamento")
                continue

        # Remove último separador
        if all_charts and isinstance(all_charts[-1], html.Hr):
            all_charts.pop()

        # Cards de estatísticas no topo
        stats_cards = [
            dbc.Col(
                create_stat_card("Colunas Analisadas", str(total_columns), "fa-columns", "#6366F1"),
                md=3,
            ),
            dbc.Col(
                create_stat_card(
                    "Registros Totais", f"{total_records:,}", "fa-database", "#22D3EE"
                ),
                md=3,
            ),
            dbc.Col(
                create_stat_card(
                    "Termos Unicos", f"{total_unique_terms:,}", "fa-fingerprint", "#10B981"
                ),
                md=3,
            ),
            dbc.Col(
                create_stat_card(
                    "Pontos de Dados", f"{total_data_points:,}", "fa-braille", "#F59E0B"
                ),
                md=3,
            ),
        ]

        return stats_cards, all_charts

    except Exception as e:
        # Retorna erro amigável em caso de falha
        error_msg = html.Div(
            [
                html.I(
                    className="fas fa-exclamation-triangle fa-3x mb-3", style={"color": "#EF4444"}
                ),
                html.H4("Erro ao processar dados", style={"color": "#EF4444"}),
                html.P(str(e), style={"color": "#9CA3AF", "fontSize": "12px"}),
            ],
            className="text-center py-5",
        )
        return [], error_msg


# ──────────────────────────────────────────────────────────────────────────────
# 9. HTML base customizado
# ──────────────────────────────────────────────────────────────────────────────
app.index_string = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    {%metas%}
    <title>Analisador de Planilhas - Dashboard</title>
    {%favicon%}
    {%css%}
    <style>
        * { box-sizing: border-box; }
        body {
            font-family: "Inter", -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
            min-height: 100vh;
            margin: 0;
        }
        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: #1E293B; }
        ::-webkit-scrollbar-thumb { background: #6366F1; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #818CF8; }
        .card:hover { transform: translateY(-4px); box-shadow: 0 8px 32px rgba(99,102,241,0.3) !important; }
        .dash-table-container { border-radius: 8px; overflow: hidden; }
        .table { color: #E5E7EB !important; }
        .table-striped tbody tr:nth-of-type(odd) { background-color: rgba(99,102,241,0.1) !important; }
        .table-hover tbody tr:hover { background-color: rgba(99,102,241,0.2) !important; }
        .table thead th { background: #374151 !important; border-bottom: 2px solid #6366F1 !important; }
    </style>
</head>
<body>
    {%app_entry%}
    <footer>
        {%config%}
        {%scripts%}
        {%renderer%}
    </footer>
</body>
</html>
"""

# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)
