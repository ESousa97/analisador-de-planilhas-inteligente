# Contribuindo para o Analisador de Planilhas Inteligente

Obrigado pelo interesse em contribuir! Este documento fornece diretrizes para contribuições.

## 📋 Índice

- [Código de Conduta](#código-de-conduta)
- [Como Posso Contribuir?](#como-posso-contribuir)
- [Configuração do Ambiente](#configuração-do-ambiente)
- [Padrões de Código](#padrões-de-código)
- [Processo de Pull Request](#processo-de-pull-request)
- [Conventional Commits](#conventional-commits)

## Código de Conduta

Este projeto adota o [Contributor Covenant](CODE_OF_CONDUCT.md). Ao participar, espera-se que você siga este código.

## Como Posso Contribuir?

### 🐛 Reportando Bugs

- Use o template de [Bug Report](.github/ISSUE_TEMPLATE/bug_report.yml)
- Inclua passos para reproduzir o problema
- Descreva o comportamento esperado vs. atual
- Adicione screenshots se aplicável
- Informe versão do Python e sistema operacional

### ✨ Sugerindo Funcionalidades

- Use o template de [Feature Request](.github/ISSUE_TEMPLATE/feature_request.yml)
- Descreva o problema que a funcionalidade resolve
- Explique a solução proposta
- Considere alternativas

### 💻 Contribuindo com Código

1. Procure issues com label `good first issue` para começar
2. Comente na issue que deseja trabalhar
3. Siga o [Processo de Pull Request](#processo-de-pull-request)

## Configuração do Ambiente

### Pré-requisitos

- Python 3.10 ou superior
- Git

### Setup

```bash
# Clone o repositório
git clone https://github.com/ESousa97/analisador-de-planilhas-inteligente.git
cd analisador-de-planilhas-inteligente

# Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
.\venv\Scripts\activate  # Windows

# Instale dependências de desenvolvimento
pip install -e ".[dev]"

# Configure pre-commit hooks
pre-commit install
```

### Executando Testes

```bash
# Todos os testes
pytest

# Com cobertura
pytest --cov=. --cov-report=html

# Testes específicos
pytest tests/test_loader.py -v
```

### Executando Linter

```bash
# Verificar problemas
ruff check .

# Corrigir automaticamente
ruff check . --fix

# Formatar código
ruff format .
```

## Padrões de Código

### Estilo

- Seguimos [PEP 8](https://pep8.org/) com algumas adaptações
- Linha máxima: 100 caracteres
- Use type hints sempre que possível
- Docstrings no formato Google

### Exemplo de Código

```python
def process_data(
    df: pd.DataFrame,
    column: str,
    threshold: float = 0.8,
) -> dict[str, Any]:
    """
    Processa dados de uma coluna do DataFrame.

    Args:
        df: DataFrame com os dados
        column: Nome da coluna a processar
        threshold: Limiar de similaridade (0-1)

    Returns:
        Dicionário com resultados do processamento

    Raises:
        ValueError: Se a coluna não existir
    """
    if column not in df.columns:
        raise ValueError(f"Coluna '{column}' não encontrada")

    # Implementação...
    return {"status": "success"}
```

### Commits

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

| Tipo | Descrição |
|------|-----------|
| `feat` | Nova funcionalidade |
| `fix` | Correção de bug |
| `docs` | Documentação |
| `style` | Formatação (não afeta código) |
| `refactor` | Refatoração |
| `test` | Testes |
| `chore` | Manutenção |

**Exemplos:**
```
feat: adiciona análise semântica para colunas de texto
fix: corrige detecção de encoding em arquivos CSV
docs: atualiza README com instruções de instalação
test: adiciona testes para módulo loader
```

## Processo de Pull Request

1. **Fork** o repositório
2. **Crie uma branch** a partir de `main`:
   ```bash
   git checkout -b feat/minha-funcionalidade
   ```
3. **Faça commits** seguindo Conventional Commits
4. **Execute testes** e linter:
   ```bash
   pytest
   ruff check .
   ruff format .
   ```
5. **Push** para seu fork:
   ```bash
   git push origin feat/minha-funcionalidade
   ```
6. **Abra um Pull Request** usando o template

### Checklist do PR

- [ ] Código segue os padrões do projeto
- [ ] Testes foram adicionados/atualizados
- [ ] Documentação foi atualizada
- [ ] Todos os testes passam
- [ ] Linter não reporta erros

## 🙏 Agradecimentos

Agradecemos a todos os contribuidores! Cada contribuição, seja código, documentação ou feedback, é valiosa para o projeto.

---

Dúvidas? Abra uma [Discussion](https://github.com/ESousa97/analisador-de-planilhas-inteligente/discussions) ou entre em contato com os maintainers.
