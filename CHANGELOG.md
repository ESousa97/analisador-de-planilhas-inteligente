# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [Unreleased]

### Adicionado
- Sistema de logging estruturado (`core/logging_config.py`)
- Exceções customizadas para melhor tratamento de erros (`core/exceptions.py`)
- Configuração moderna com `pyproject.toml`
- Testes automatizados com pytest
- Pre-commit hooks para qualidade de código
- GitHub Actions para CI/CD
- CodeQL para análise de segurança
- Dependabot para gestão de dependências
- Documentação completa (CONTRIBUTING, CODE_OF_CONDUCT, SECURITY)
- Templates de Issue e Pull Request

### Alterado
- Migração de configurações para `config/settings.py` com type hints
- Refatoração do `core/loader.py` com validações e logging
- Atualização do `.gitignore` com padrões modernos

### Segurança
- Adicionada validação de entrada em carregamento de arquivos
- Configurado linter com regras de segurança (Ruff + Bandit)
- Implementada auditoria de dependências no CI

## [1.0.0] - 2024-05-01

### Adicionado
- Interface desktop com PyQt5
- Dashboard web interativo com Dash/Plotly
- Análise fuzzy com RapidFuzz
- Análise semântica com Sentence-Transformers
- Detecção automática de tipos de coluna
- Dicionário com 900+ termos de domínio
- Normalização automática de CEP
- Suporte a CSV, XLSX e XLS
- Detecção automática de encoding e delimitadores
- Exportação de relatórios em CSV e JSON

### Funcionalidades
- 5 tipos de gráficos: Barras, Pizza, Linha, Scatter, Box Plot
- Progress tracking em tempo real
- Arquitetura híbrida Desktop/Web
- Processamento assíncrono com QThread

---

[Unreleased]: https://github.com/ESousa97/analisador-de-planilhas-inteligente/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/ESousa97/analisador-de-planilhas-inteligente/releases/tag/v1.0.0
