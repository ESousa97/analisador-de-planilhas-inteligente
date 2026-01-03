# core/exceptions.py
"""
Exceções customizadas da aplicação.
Centraliza tratamento de erros com mensagens claras.
"""


class AnalyzerError(Exception):
    """Exceção base para erros da aplicação."""

    def __init__(self, message: str, details: str | None = None):
        self.message = message
        self.details = details
        super().__init__(self.message)

    def __str__(self) -> str:
        if self.details:
            return f"{self.message} | Detalhes: {self.details}"
        return self.message


class FileLoadError(AnalyzerError):
    """Erro ao carregar arquivo."""

    def __init__(self, filepath: str, reason: str):
        super().__init__(
            message=f"Erro ao carregar arquivo: {filepath}",
            details=reason,
        )
        self.filepath = filepath


class UnsupportedFormatError(AnalyzerError):
    """Formato de arquivo não suportado."""

    def __init__(self, extension: str):
        supported = [".csv", ".xlsx", ".xls"]
        super().__init__(
            message=f"Formato '{extension}' não suportado",
            details=f"Formatos aceitos: {', '.join(supported)}",
        )
        self.extension = extension


class FileSizeError(AnalyzerError):
    """Arquivo excede o tamanho máximo permitido."""

    def __init__(self, size_mb: float, max_size_mb: float):
        super().__init__(
            message=f"Arquivo muito grande: {size_mb:.1f} MB",
            details=f"Tamanho máximo permitido: {max_size_mb} MB",
        )
        self.size_mb = size_mb
        self.max_size_mb = max_size_mb


class DataValidationError(AnalyzerError):
    """Erro na validação dos dados."""

    def __init__(self, column: str, reason: str):
        super().__init__(
            message=f"Erro de validação na coluna '{column}'",
            details=reason,
        )
        self.column = column


class AnalysisError(AnalyzerError):
    """Erro durante a análise dos dados."""

    def __init__(self, stage: str, reason: str):
        super().__init__(
            message=f"Erro na etapa '{stage}' da análise",
            details=reason,
        )
        self.stage = stage
