# 📚 FUNDEB Fácil

**Sistema Inteligente para Compreensão e Projeção de Complementações Orçamentárias VAAT/VAAF**

Candidato ao **Prêmio SOF 2025** - Categoria "Soluções em dados orçamentários"
Desafio: Item 2.4.1.4 - Estimar ou visualizar projeções orçamentárias de médio prazo

---

## 🎯 O Problema

O FUNDEB movimenta R$ 339 bilhões anuais, mas sua complexidade impede que 99% dos gestores municipais compreendam como são calculadas as complementações. Esta opacidade compromete:

- ❌ Planejamento orçamentário municipal (PPA, LDO, LOA)
- ❌ Validação de repasses
- ❌ Projeções de médio prazo
- ❌ Decisões estratégicas sobre expansão de matrículas

## ✨ A Solução

**FUNDEB Fácil** transforma complexidade em compreensão através de:

- 🧮 **Calculadora VAAT/VAAF**: Cálculos transparentes com ponderadores oficiais
- 📊 **Visualizações Interativas**: Gráficos que revelam impacto de cada etapa educacional
- 🤖 **Chat Explicativo com IA**: Explicações pedagógicas em linguagem natural
- 🎯 **Simulação de Cenários**: Projete impacto de mudanças nas matrículas

## 🚀 Início Rápido

### Pré-requisitos

- Python 3.11+
- uv (gerenciador de pacotes)
- Chave API da Anthropic (para chat)

### Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/fundeb-facil-express.git
cd fundeb-facil-express

# Instale dependências com uv
uv pip install -e .

# Configure sua API key (opcional - apenas para chat)
export ANTHROPIC_API_KEY="sua-chave-aqui"

# Execute o app
streamlit run app.py
```

O app estará disponível em: `http://localhost:8501`

## 📖 Como Usar

### 1. Calculadora

1. Selecione um município na barra lateral
2. Escolha entre "Dados Atuais" ou "Simular Cenário"
3. Se simular, edite as matrículas como desejar
4. Clique em "Calcular Complementações"
5. Veja resultados detalhados por etapa educacional

### 2. Chat Explicativo

1. Configure sua API Key da Anthropic na barra lateral
2. Acesse a aba "Chat Explicativo"
3. Faça perguntas como:
   - "Como é calculado o VAAT?"
   - "Por que creche integral tem ponderador 1,90?"
   - "Explique o cálculo para o município selecionado"

### 3. Comparações

- Visualize todos os municípios lado a lado
- Compare complementações VAAT vs VAAF

## 🏗️ Arquitetura

```
fundeb-facil-express/
├── app.py                 # Interface Streamlit
├── calculadora.py         # Lógica de cálculo VAAT/VAAF
├── chat_agent.py          # Agente Claude para chat
├── dados/
│   ├── municipios.json    # Dados dos municípios
│   └── ponderadores.json  # Ponderadores oficiais
└── .streamlit/
    └── config.toml        # Configuração visual
```

**Stack Técnico:**
- Streamlit (interface)
- Anthropic Claude 3.5 Sonnet (chat IA)
- Pandas (manipulação de dados)
- Plotly (visualizações)

## 📊 Municípios de Exemplo

O MVP inclui 5 municípios reais representativos:

1. **Apucarana-PR**: Município médio, elegível VAAT/VAAF
2. **Acrelândia-AC**: Município pequeno, alta vulnerabilidade
3. **São Paulo-SP**: Capital, não elegível (alta arrecadação)
4. **São Luís-MA**: Capital regional, elegível
5. **Bragança-PA**: Município médio, forte componente rural

## 🎓 Base Legal

- **Lei 14.113/2020**: FUNDEB permanente
- **Portaria MEC nº 567/2024**: Ponderadores 2025
- Dados: Censo Escolar INEP

## 🔮 Roadmap

### MVP (Atual)
- ✅ Calculadora VAAT/VAAF funcional
- ✅ Chat explicativo com Claude
- ✅ Interface Streamlit
- ✅ 5 municípios exemplo

### Versão Completa
- [ ] Todos os 5.568 municípios brasileiros
- [ ] RAG sobre base legal completa
- [ ] Arquitetura multiagentes (LangGraph)
- [ ] Banco SQLite
- [ ] Exportação de relatórios PDF
- [ ] Integração com SIOPE

## 🏆 Prêmio SOF 2025

Este projeto concorre ao **14º Prêmio SOF** na categoria **"Soluções em dados orçamentários"**, endereçando especificamente o desafio:

> **2.4.1.4**: Estimar ou visualizar projeções orçamentárias de médio prazo

**Alinhamento:**
- ✅ Transparência inteligível (não apenas disponibilidade de dados)
- ✅ Inovação (IA aplicada a educação orçamentária)
- ✅ Impacto social (democratização de conhecimento técnico)
- ✅ Viabilidade (tecnologias open-source, baixo custo)

## 📄 Licença

MIT License - Veja [LICENSE](LICENSE) para detalhes

## 👤 Autor

**Rodrigo Santos Ramos**

Desenvolvido para o Prêmio SOF 2025

---

**💡 "Transparência não é apenas publicar dados, é torná-los compreensíveis"**
