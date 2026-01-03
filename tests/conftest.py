# tests/conftest.py
"""
Configurações e fixtures compartilhadas para os testes.
"""

from collections.abc import Generator
from pathlib import Path

import pandas as pd
import pytest


@pytest.fixture
def sample_dataframe() -> pd.DataFrame:
    """Cria um DataFrame de exemplo para testes."""
    return pd.DataFrame(
        {
            "id": [1, 2, 3, 4, 5],
            "nome": ["João Silva", "Maria Santos", "João Silva", "Ana Costa", "Maria Santos"],
            "cidade": ["São Paulo", "Sao Paulo", "SP", "Rio de Janeiro", "RJ"],
            "valor": [100.50, 200.75, 150.00, 300.25, 250.00],
            "data": ["2024-01-15", "2024-02-20", "2024-01-15", "2024-03-10", "2024-02-20"],
        }
    )


@pytest.fixture
def temp_csv_file(tmp_path: Path) -> Generator[Path, None, None]:
    """Cria um arquivo CSV temporário para testes."""
    csv_content = """id,nome,cidade,valor
1,João Silva,São Paulo,100.50
2,Maria Santos,Rio de Janeiro,200.75
3,Ana Costa,Belo Horizonte,150.00
"""
    csv_path = tmp_path / "test_data.csv"
    csv_path.write_text(csv_content, encoding="utf-8")
    yield csv_path


@pytest.fixture
def temp_csv_semicolon(tmp_path: Path) -> Generator[Path, None, None]:
    """Cria um arquivo CSV com ponto-e-vírgula como delimitador."""
    csv_content = """id;nome;cidade;valor
1;João Silva;São Paulo;100,50
2;Maria Santos;Rio de Janeiro;200,75
3;Ana Costa;Belo Horizonte;150,00
"""
    csv_path = tmp_path / "test_data_semicolon.csv"
    csv_path.write_text(csv_content, encoding="utf-8")
    yield csv_path
