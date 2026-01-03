# Política de Segurança

## Versões Suportadas

| Versão | Suportada          |
| ------ | ------------------ |
| 1.x.x  | :white_check_mark: |

## Reportando Vulnerabilidades

Se você descobrir uma vulnerabilidade de segurança, por favor **NÃO** abra uma issue pública.

### Como Reportar

1. **Email**: Envie um email para [ESousa97] com:
   - Descrição detalhada da vulnerabilidade
   - Passos para reproduzir
   - Impacto potencial
   - Sugestão de correção (se tiver)

2. **Prazo de Resposta**: Você receberá uma resposta inicial em até 48 horas úteis.

3. **Processo**:
   - Confirmaremos o recebimento do relatório
   - Investigaremos e validaremos a vulnerabilidade
   - Desenvolveremos uma correção
   - Lançaremos a correção e daremos crédito ao descobridor (se desejado)

## Escopo de Segurança

### ✅ Em Escopo

- Vulnerabilidades no código da aplicação
- Problemas de validação de entrada
- Vazamento de dados sensíveis
- Dependências com vulnerabilidades conhecidas
- Configurações inseguras

### ❌ Fora de Escopo

- Vulnerabilidades em dependências que já possuem CVE público e correção disponível
- Ataques que requerem acesso físico ao dispositivo
- Engenharia social

## Modelo de Ameaças

### Superfícies de Ataque

| Superfície | Descrição | Controles |
|------------|-----------|-----------|
| **Entrada de Arquivos** | Upload de planilhas CSV/XLSX/XLS | Validação de formato, limite de tamanho, sanitização |
| **API Local** | Endpoint `/update_data` (localhost) | Bind apenas em 127.0.0.1, validação de JSON |
| **Interface Desktop** | Entrada de caminho de arquivo | Validação de extensão, verificação de existência |

### Dados Processados

| Tipo | Sensibilidade | Tratamento |
|------|---------------|------------|
| Planilhas do usuário | Alta | Processamento local, sem transmissão externa |
| Resultados de análise | Média | Armazenado localmente em `output/` |
| Logs | Baixa | Sem dados sensíveis, apenas operações |

### Controles Implementados

1. **Validação de Entrada**
   - Verificação de extensão de arquivo
   - Limite de tamanho de arquivo (1GB)
   - Limite de linhas processadas (10M)
   - Sanitização de strings

2. **Isolamento**
   - Dashboard web bind apenas em localhost (127.0.0.1)
   - Sem conexões externas (exceto download inicial de modelos NLP)
   - Dados processados localmente

3. **Dependências**
   - Auditoria automática com `pip-audit` no CI
   - Dependabot configurado para atualizações automáticas
   - Versões mínimas especificadas no `pyproject.toml`

4. **Código**
   - Análise estática com Ruff (regras de segurança habilitadas)
   - CodeQL para análise de segurança
   - Pre-commit hooks para verificações

## Boas Práticas para Usuários

1. **Não processe planilhas de fontes não confiáveis** sem verificação prévia
2. **Mantenha as dependências atualizadas**: `pip install --upgrade -r requirements.txt`
3. **Verifique a integridade** de arquivos baixados
4. **Use ambiente virtual** para isolar dependências

## Changelog de Segurança

### 2026-01-03
- Implementado sistema de logging estruturado
- Adicionadas exceções customizadas para melhor tratamento de erros
- Configurado CodeQL para análise de segurança
- Adicionado Dependabot para gestão de dependências
- Implementado pre-commit com verificações de segurança

---

Obrigado por ajudar a manter este projeto seguro!
