# tests/test_stopwords.py
"""
Testes para o módulo analysis.stopwords
"""

from analysis.stopwords import clean_text, remove_stopwords


class TestCleanText:
    """Testes para a função clean_text."""

    def test_lowercase(self) -> None:
        """Deve converter para minúsculas."""
        assert clean_text("TESTE") == "teste"

    def test_remove_accents(self) -> None:
        """Deve remover acentos."""
        assert clean_text("São Paulo") == "sao paulo"

    def test_strip_whitespace(self) -> None:
        """Deve remover espaços extras."""
        assert clean_text("  teste  ") == "teste"

    def test_handle_non_string(self) -> None:
        """Deve converter não-strings para string."""
        assert clean_text(123) == "123"
        assert clean_text(None) == "none"


class TestRemoveStopwords:
    """Testes para a função remove_stopwords."""

    def test_remove_default_stopwords(self) -> None:
        """Deve remover stopwords padrão."""
        words = ["o", "gato", "e", "o", "cachorro"]
        result = remove_stopwords(words)

        assert "o" not in result
        assert "e" not in result
        assert "gato" in result
        assert "cachorro" in result

    def test_remove_custom_stopwords(self) -> None:
        """Deve remover stopwords customizadas."""
        words = ["gato", "cachorro", "papagaio"]
        result = remove_stopwords(words, custom_stopwords=["papagaio"])

        assert "papagaio" not in result
        assert "gato" in result
        assert "cachorro" in result

    def test_remove_single_char_words(self) -> None:
        """Deve remover palavras de um caractere."""
        words = ["a", "gato", "e", "cachorro"]
        result = remove_stopwords(words)

        # Palavras de 1 caractere são removidas
        for word in result:
            assert len(word) > 1
