# core/id_generator.py
"""Funções para detecção e garantia de colunas de identificação única."""

import uuid

import pandas as pd

# Padrões de nomes que indicam colunas de ID
ID_COLUMN_PATTERNS = [
    "id",
    "codigo",
    "code",
    "identificacao",
    "identificador",
    "key",
    "chave",
    "registro",
    "matricula",
    "numero",
    "num",
    "ref",
    "referencia",
    "index",
    "indice",
    "pk",
    "primary_key",
    "cpf",
    "cnpj",
    "rg",
    "cnh",
    "sku",
    "ean",
    "upc",
    "barcode",
    "serial",
    "nf",
    "nota_fiscal",
    "pedido",
    "order",
    "ticket",
    "protocolo",
    "hash",
]


def detect_native_id_column(df: pd.DataFrame) -> str | None:
    """
    Detecta coluna de identificador único nativo no DataFrame.

    Prioridade:
    1. Coluna com valores 100% únicos e tipo apropriado
    2. Coluna com nome que indica ID
    3. Primeira coluna numérica com valores únicos

    Returns:
        Nome da coluna identificada ou None se não encontrada.
    """
    if df.empty:
        return None

    # 1. Busca por nome de coluna que indica ID
    for col in df.columns:
        col_lower = str(col).lower().strip()
        col_clean = col_lower.replace("_", "").replace("-", "").replace(" ", "")

        for pattern in ID_COLUMN_PATTERNS:
            if col_clean == pattern or col_lower.startswith(pattern + "_") or col_lower.endswith("_" + pattern):
                # Verifica se é realmente única ou quase única (>95%)
                uniqueness = df[col].nunique() / len(df) if len(df) > 0 else 0
                if uniqueness >= 0.95:
                    return col

    # 2. Busca coluna com 100% valores únicos (primeira encontrada)
    for col in df.columns:
        if df[col].is_unique and not df[col].isna().any():
            # Prefere colunas numéricas ou strings curtas
            if pd.api.types.is_numeric_dtype(df[col]):
                return col
            if df[col].dtype == "object":
                avg_len = df[col].astype(str).str.len().mean()
                if avg_len < 50:  # Provavelmente um ID, não um texto longo
                    return col

    return None


def ensure_id_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Garante que o DataFrame tenha uma coluna de identificação única.

    Regras:
    1. Se já existe ID nativo detectado -> usa ele (NÃO cria novo)
    2. Se não existe ID nativo -> cria "_synthetic_id" com UUID

    A coluna de ID é retornada como primeira coluna do DataFrame.
    """
    if df.empty:
        return df

    # Detecta ID nativo existente
    native_id = detect_native_id_column(df)

    if native_id:
        # Usa ID nativo - apenas move para primeira posição se necessário
        if df.columns[0] != native_id:
            cols = [native_id] + [c for c in df.columns if c != native_id]
            df = df[cols]
        return df

    # Só cria ID sintético se realmente não existe ID nativo
    if "_synthetic_id" not in df.columns and "id" not in df.columns:
        df = df.copy()
        df.insert(0, "_synthetic_id", [str(uuid.uuid4()) for _ in range(len(df))])

    return df


def get_id_column_name(df: pd.DataFrame) -> str:
    """
    Retorna o nome da coluna de ID do DataFrame.

    Returns:
        Nome da coluna de ID (nativo ou sintético).
    """
    native_id = detect_native_id_column(df)
    if native_id:
        return native_id
    if "_synthetic_id" in df.columns:
        return "_synthetic_id"
    if "id" in df.columns:
        return "id"
    return df.columns[0]  # Fallback para primeira coluna
