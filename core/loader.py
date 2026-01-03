# core/loader.py
"""
Módulo responsável pelo carregamento e limpeza inicial de arquivos de dados.
Suporta CSV, XLSX e XLS com detecção automática de encoding e delimitadores.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import chardet
import pandas as pd

from config.settings import MAX_FILE_SIZE_MB, SUPPORTED_EXTENSIONS
from core.exceptions import FileLoadError, FileSizeError, UnsupportedFormatError
from core.logging_config import get_logger

logger = get_logger("loader")


def validate_file(file_path: str | Path, max_size_mb: int = MAX_FILE_SIZE_MB) -> Path:
    """
    Valida se o arquivo existe e está dentro do tamanho permitido.

    Args:
        file_path: Caminho do arquivo
        max_size_mb: Tamanho máximo em MB

    Returns:
        Path validado

    Raises:
        FileLoadError: Se o arquivo não existir
        FileSizeError: Se exceder o tamanho máximo
        UnsupportedFormatError: Se o formato não for suportado
    """
    path = Path(file_path)

    if not path.exists():
        raise FileLoadError(str(path), "Arquivo não encontrado")

    if not path.is_file():
        raise FileLoadError(str(path), "Caminho não é um arquivo válido")

    ext = path.suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise UnsupportedFormatError(ext)

    size_mb = path.stat().st_size / (1024 * 1024)
    if size_mb > max_size_mb:
        raise FileSizeError(size_mb, max_size_mb)

    logger.debug(f"Arquivo validado: {path.name} ({size_mb:.2f} MB)")
    return path


def load_and_clean_excel(file_path: str | Path) -> pd.DataFrame:
    """
    Carrega arquivo Excel e realiza limpeza básica:
    - Remove linhas e colunas vazias
    - Limpa espaços e caracteres invisíveis em strings
    - Tenta converter colunas de datas
    """
    # Carrega com openpyxl (pode gerar warnings ignorados)
    df = pd.read_excel(file_path, engine="openpyxl")

    # Remove linhas e colunas totalmente vazias
    df.dropna(axis=0, how="all", inplace=True)
    df.dropna(axis=1, how="all", inplace=True)

    # Limpa espaços dos nomes das colunas
    df.columns = df.columns.str.strip()

    # Limpa strings nas colunas do tipo object
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].astype(str).str.strip().str.replace(r"[\x00-\x1F]+", "", regex=True)

    # Tenta converter colunas que parecem datas
    for col in df.columns:
        if "data" in col.lower() or "date" in col.lower():
            df[col] = pd.to_datetime(df[col], errors="coerce")

    logger.debug(f"Excel carregado: {len(df)} linhas, {len(df.columns)} colunas")
    return df


def detect_encoding(file_path: str | Path) -> str:
    """Detecta o encoding de um arquivo de texto."""
    with open(file_path, "rb") as f:
        result = chardet.detect(f.read(2048))
    encoding = result["encoding"] or "utf-8"
    logger.debug(f"Encoding detectado: {encoding}")
    return encoding


def detect_delimiter(file_path: str | Path, encoding: str) -> str:
    """Detecta o delimitador mais provável de um arquivo CSV."""
    with open(file_path, encoding=encoding) as f:
        sample = f.read(4096)
        delimiters = [",", ";", "\t", "|", ":"]
        delimiter_scores = {d: sample.count(d) for d in delimiters}
        delimiter = max(delimiter_scores, key=delimiter_scores.get)
        logger.debug(f"Delimitador detectado: '{delimiter}'")
        return delimiter


def load_spreadsheet(
    file_path: str | Path,
    chunksize: int | None = None,
    progress_callback: Callable[[int, int | None], None] | None = None,
) -> pd.DataFrame:
    """
    Carrega uma planilha (CSV, XLSX, XLS) e retorna um DataFrame.

    Args:
        file_path: Caminho do arquivo
        chunksize: Tamanho dos chunks para leitura incremental (CSV apenas)
        progress_callback: Função de callback para progresso (processed, total)

    Returns:
        DataFrame com os dados carregados

    Raises:
        FileLoadError: Se houver erro no carregamento
        UnsupportedFormatError: Se o formato não for suportado
    """
    path = validate_file(file_path)
    ext = path.suffix.lower()

    logger.info(f"Carregando arquivo: {path.name}")

    try:
        if ext == ".csv":
            encoding = detect_encoding(path)
            delimiter = detect_delimiter(path, encoding)
            if chunksize:
                chunks = []
                total_rows = 0
                for chunk in pd.read_csv(
                    path,
                    encoding=encoding,
                    delimiter=delimiter,
                    chunksize=chunksize,
                    low_memory=False,
                ):
                    chunks.append(chunk)
                    total_rows += len(chunk)
                    if progress_callback:
                        progress_callback(total_rows, None)
                df = pd.concat(chunks, ignore_index=True)
            else:
                df = pd.read_csv(path, encoding=encoding, delimiter=delimiter, low_memory=False)
        elif ext in [".xlsx", ".xls"]:
            df = load_and_clean_excel(path)
            if progress_callback:
                progress_callback(len(df), len(df))
        else:
            raise UnsupportedFormatError(ext)

        logger.info(f"Arquivo carregado: {len(df)} linhas, {len(df.columns)} colunas")
        return df

    except (UnsupportedFormatError, FileSizeError, FileLoadError):
        raise
    except Exception as e:
        logger.error(f"Erro ao carregar arquivo: {e}")
        raise FileLoadError(str(path), str(e)) from e
