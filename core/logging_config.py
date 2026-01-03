# core/logging_config.py
"""
Configuração centralizada de logging para a aplicação.
"""

import logging
import sys
from pathlib import Path


def setup_logging(
    level: int = logging.INFO,
    log_file: Path | None = None,
    log_format: str | None = None,
) -> logging.Logger:
    """
    Configura o logging da aplicação de forma centralizada.

    Args:
        level: Nível de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Caminho opcional para arquivo de log
        log_format: Formato customizado do log

    Returns:
        Logger configurado
    """
    if log_format is None:
        log_format = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"

    # Remove handlers existentes para evitar duplicação
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Configuração base
    logging.basicConfig(
        level=level,
        format=log_format,
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[],
    )

    # Handler para console (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(logging.Formatter(log_format, datefmt="%Y-%m-%d %H:%M:%S"))
    root_logger.addHandler(console_handler)

    # Handler para arquivo (opcional)
    if log_file is not None:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(level)
        file_handler.setFormatter(logging.Formatter(log_format, datefmt="%Y-%m-%d %H:%M:%S"))
        root_logger.addHandler(file_handler)

    # Logger específico da aplicação
    logger = logging.getLogger("analyzer")
    logger.setLevel(level)

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Obtém um logger com o nome especificado.

    Args:
        name: Nome do módulo/componente

    Returns:
        Logger configurado
    """
    return logging.getLogger(f"analyzer.{name}")
