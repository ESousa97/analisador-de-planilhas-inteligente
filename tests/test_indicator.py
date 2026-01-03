# tests/test_indicator.py
"""
Testes para o módulo analysis.indicator
"""

import pandas as pd

from analysis.indicator import (
    fuzzy_cluster_terms,
    is_date_candidate,
    is_id_column,
    is_numerical,
    normalize_generic,
)


class TestIsIdColumn:
    """Testes para a função is_id_column."""

    def test_id_column_by_name(self) -> None:
        """Deve identificar coluna 'id' pelo nome."""
        df = pd.DataFrame({"id": [1, 2, 3], "nome": ["a", "b", "c"]})
        assert is_id_column("id", df) is True

    def test_id_column_by_uniqueness(self) -> None:
        """Deve identificar coluna única como ID."""
        df = pd.DataFrame({"codigo": [1, 2, 3], "nome": ["a", "a", "b"]})
        assert is_id_column("codigo", df) is True

    def test_non_id_column(self) -> None:
        """Deve rejeitar coluna não-ID."""
        df = pd.DataFrame({"nome": ["a", "a", "b"]})
        assert is_id_column("nome", df) is False


class TestIsNumerical:
    """Testes para a função is_numerical."""

    def test_numerical_column(self) -> None:
        """Deve identificar coluna numérica."""
        df = pd.DataFrame({"valor": [1.5, 2.5, 3.5]})
        assert is_numerical("valor", df) is True

    def test_non_numerical_column(self) -> None:
        """Deve rejeitar coluna não numérica."""
        df = pd.DataFrame({"nome": ["a", "b", "c"]})
        assert is_numerical("nome", df) is False


class TestIsDateCandidate:
    """Testes para a função is_date_candidate."""

    def test_date_column_pt(self) -> None:
        """Deve identificar coluna com 'data' no nome."""
        assert is_date_candidate("data_nascimento") is True
        assert is_date_candidate("DATA") is True

    def test_date_column_en(self) -> None:
        """Deve identificar coluna com 'date' no nome."""
        assert is_date_candidate("birth_date") is True
        assert is_date_candidate("DATE") is True

    def test_non_date_column(self) -> None:
        """Deve rejeitar colunas sem indicador de data."""
        assert is_date_candidate("nome") is False
        assert is_date_candidate("valor") is False


class TestNormalizeGeneric:
    """Testes para a função normalize_generic."""

    def test_lowercase(self) -> None:
        """Deve converter para minúsculas."""
        assert normalize_generic("TESTE") == "teste"

    def test_remove_accents(self) -> None:
        """Deve remover acentos."""
        assert normalize_generic("São Paulo") == "sao paulo"

    def test_strip_whitespace(self) -> None:
        """Deve remover espaços extras."""
        assert normalize_generic("  teste  ") == "teste"


class TestFuzzyClusterTerms:
    """Testes para a função fuzzy_cluster_terms."""

    def test_cluster_similar_terms(self) -> None:
        """Deve agrupar termos similares."""
        terms = ["apple", "Apple", "applee"]
        clusters = fuzzy_cluster_terms(terms, threshold=80)

        # Termos similares devem ser agrupados
        total_terms_in_clusters = sum(len(c) for c in clusters)
        assert total_terms_in_clusters == 3
        # Com threshold 80, variações próximas devem agrupar
        assert any(len(c) >= 2 for c in clusters)

    def test_separate_different_terms(self) -> None:
        """Deve separar termos diferentes."""
        terms = ["apple", "banana", "orange"]
        clusters = fuzzy_cluster_terms(terms, threshold=90)

        # Cada termo em seu próprio cluster
        assert len(clusters) == 3

    def test_max_terms_limit(self) -> None:
        """Deve respeitar limite de termos."""
        terms = [f"term_{i}" for i in range(600)]
        clusters = fuzzy_cluster_terms(terms, max_terms=500)

        # Quando excede o limite, cada termo vira um cluster individual
        assert len(clusters) == 600
