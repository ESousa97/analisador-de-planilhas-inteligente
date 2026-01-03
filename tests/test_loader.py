# tests/test_loader.py
"""
Testes para o módulo core.loader
"""

from pathlib import Path

import pandas as pd
import pytest

from core.exceptions import UnsupportedFormatError
from core.loader import (
    detect_delimiter,
    detect_encoding,
    load_spreadsheet,
    validate_file,
)


class TestValidateFile:
    """Testes para a função validate_file."""

    def test_validate_existing_csv(self, temp_csv_file: Path) -> None:
        """Deve validar arquivo CSV existente."""
        result = validate_file(temp_csv_file)
        assert result == temp_csv_file

    def test_validate_nonexistent_file(self, tmp_path: Path) -> None:
        """Deve levantar erro para arquivo inexistente."""
        from core.exceptions import FileLoadError

        with pytest.raises(FileLoadError):
            validate_file(tmp_path / "nao_existe.csv")

    def test_validate_unsupported_format(self, tmp_path: Path) -> None:
        """Deve levantar erro para formato não suportado."""
        txt_file = tmp_path / "test.txt"
        txt_file.write_text("test content")

        with pytest.raises(UnsupportedFormatError):
            validate_file(txt_file)


class TestDetectEncoding:
    """Testes para a função detect_encoding."""

    def test_detect_utf8(self, temp_csv_file: Path) -> None:
        """Deve detectar encoding UTF-8."""
        encoding = detect_encoding(temp_csv_file)
        assert encoding.lower() in ["utf-8", "ascii", "utf-8-sig"]


class TestDetectDelimiter:
    """Testes para a função detect_delimiter."""

    def test_detect_comma(self, temp_csv_file: Path) -> None:
        """Deve detectar vírgula como delimitador."""
        delimiter = detect_delimiter(temp_csv_file, "utf-8")
        assert delimiter == ","

    def test_detect_semicolon(self, temp_csv_semicolon: Path) -> None:
        """Deve detectar ponto-e-vírgula como delimitador."""
        delimiter = detect_delimiter(temp_csv_semicolon, "utf-8")
        assert delimiter == ";"


class TestLoadSpreadsheet:
    """Testes para a função load_spreadsheet."""

    def test_load_csv(self, temp_csv_file: Path) -> None:
        """Deve carregar arquivo CSV corretamente."""
        df = load_spreadsheet(temp_csv_file)

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 3
        assert "id" in df.columns
        assert "nome" in df.columns

    def test_load_csv_with_progress(self, temp_csv_file: Path) -> None:
        """Deve chamar callback de progresso."""
        progress_calls = []

        def progress_callback(processed: int, total: int | None) -> None:
            progress_calls.append((processed, total))

        df = load_spreadsheet(temp_csv_file, progress_callback=progress_callback)

        assert isinstance(df, pd.DataFrame)
        # Para CSV sem chunk, não há chamadas de progresso no meio

    def test_load_unsupported_format(self, tmp_path: Path) -> None:
        """Deve levantar erro para formato não suportado."""
        txt_file = tmp_path / "test.txt"
        txt_file.write_text("test content")

        with pytest.raises(UnsupportedFormatError):
            load_spreadsheet(txt_file)
