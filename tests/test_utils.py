# tests/test_utils.py
"""
Testes para o módulo core.utils
"""

import pandas as pd

from core.utils import normalize_cep_column


class TestNormalizeCepColumn:
    """Testes para a função normalize_cep_column."""

    def test_normalize_cep_8_digits(self) -> None:
        """Deve normalizar CEPs com 8 dígitos."""
        df = pd.DataFrame({"cep": ["01310100", "22041080", "30130000"]})
        result = normalize_cep_column(df, cep_cols=["cep"])

        assert result["cep"].tolist() == ["01310100", "22041080", "30130000"]

    def test_normalize_cep_with_dot_zero(self) -> None:
        """Deve remover '.0' de CEPs numéricos."""
        df = pd.DataFrame({"cep": ["1310100.0", "22041080.0", "30130000.0"]})
        result = normalize_cep_column(df, cep_cols=["cep"])

        assert result["cep"].tolist() == ["01310100", "22041080", "30130000"]

    def test_normalize_cep_padding(self) -> None:
        """Deve preencher CEPs com zeros à esquerda."""
        df = pd.DataFrame({"cep": ["1310100", "22041080", "130000"]})
        result = normalize_cep_column(df, cep_cols=["cep"])

        assert result["cep"].tolist() == ["01310100", "22041080", "00130000"]

    def test_normalize_cep_preserves_nan(self) -> None:
        """Deve preservar valores NaN."""
        df = pd.DataFrame({"cep": ["01310100", None, "30130000"]})
        result = normalize_cep_column(df, cep_cols=["cep"])

        assert result["cep"].iloc[0] == "01310100"
        assert pd.isna(result["cep"].iloc[1])
        assert result["cep"].iloc[2] == "30130000"
