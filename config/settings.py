# config/settings.py
"""
Configurações centralizadas da aplicação.
Todas as constantes e parâmetros configuráveis devem estar aqui.
"""

from pathlib import Path
from typing import Final

# ============================================================================
# Limites de processamento
# ============================================================================
MAX_ROWS: Final[int] = 10_000_000  # Limite de linhas para processar
MAX_FILE_SIZE_MB: Final[int] = 1000  # Limite de 1GB

# ============================================================================
# Configurações de análise
# ============================================================================
FUZZY_THRESHOLD: Final[int] = 88  # Limiar de similaridade fuzzy (0-100)
SEMANTIC_THRESHOLD: Final[float] = 0.8  # Limiar de similaridade semântica (0-1)
MAX_TERMS_FUZZY: Final[int] = 500  # Máximo de termos para análise fuzzy
MAX_TOP_CATEGORIES: Final[int] = 100  # Máximo de categorias top exibidas

# ============================================================================
# Stopwords padrão (português)
# ============================================================================
DEFAULT_STOPWORDS: Final[list[str]] = [
    "de",
    "a",
    "mas",
    "por",
    "e",
    "do",
    "da",
    "os",
    "as",
    "em",
    "um",
    "uma",
    "para",
    "com",
    "sem",
    "no",
    "na",
    "nos",
    "nas",
    "o",
    "à",
    "ao",
    "se",
    "que",
    "ou",
    "é",
    "foi",
    "são",
    "está",
    "ser",
    "ter",
    "seu",
    "sua",
    "seus",
    "suas",
    "ele",
    "ela",
    "eles",
    "elas",
    "isso",
    "isto",
    "aquilo",
    "este",
    "esta",
    "esse",
    "essa",
    "aquele",
    "aquela",
    "qual",
    "quais",
]

# ============================================================================
# Caminhos padrão
# ============================================================================
BASE_DIR: Final[Path] = Path(__file__).resolve().parent.parent
OUTPUT_DIR: Final[Path] = BASE_DIR / "output"
LOGS_DIR: Final[Path] = BASE_DIR / "logs"

# ============================================================================
# Servidor web (Dash)
# ============================================================================
DASH_HOST: Final[str] = "127.0.0.1"
DASH_PORT: Final[int] = 8050
DASH_DEBUG: Final[bool] = False

# ============================================================================
# Modelos NLP
# ============================================================================
EMBEDDING_MODEL: Final[str] = "paraphrase-multilingual-MiniLM-L12-v2"

# ============================================================================
# Formatos suportados
# ============================================================================
SUPPORTED_EXTENSIONS: Final[tuple[str, ...]] = (".csv", ".xlsx", ".xls")
