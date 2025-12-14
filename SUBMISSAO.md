# 📄 Template de Submissão - Prêmio SOF 2025

## Dados para o Formulário de Inscrição

### Informações Básicas (Item 5.6)

**Dados Pessoais:**
- Nome completo: Rodrigo Santos Ramos
- Email: [seu-email]
- Telefone: [seu-telefone]
- CPF: [seu-cpf]

**Categoria:**
- ☑️ Soluções em dados orçamentários

**Documentos Necessários (Item 5.6.2):**
- [ ] Diploma ou Declaração de Matrícula (PDF)

---

## 📋 Apresentação da Proposta (Item 5.6.3)

**Arquivo PDF a ser enviado** - Conteúdo sugerido:

### 1. DESCRIÇÃO DO PROBLEMA

O FUNDEB movimenta R$ 339 bilhões anuais (R$ 58,8 bi de complementação da União), mas sua complexidade é o principal obstáculo à implementação eficaz:

- **99% dos secretários de educação** não compreendem os cálculos (diagnóstico do Senado Federal, 2025)
- **Impossibilidade de projeção orçamentária**: Gestores não conseguem estimar impacto de mudanças em matrículas
- **Dependência de consultorias externas**: Municípios pobres ficam excluídos (não podem pagar)
- **Comprometimento do planejamento**: PPA, LDO e LOA baseados em "adivinhação"

**Alinhamento com item 2.4.1.4:**
O problema é fundamentalmente sobre **estimativa e visualização de projeções orçamentárias de médio prazo** - exatamente o desafio proposto pelo edital.

---

### 2. SOLUÇÃO COMPLETA SUGERIDA

**FUNDEB Fácil** é uma aplicação web que transforma complexidade em compreensão através de:

#### 2.1. Calculadora VAAT/VAAF
- Aplica ponderadores oficiais em múltiplas camadas (etapa × modalidade × NSE × DRec)
- Calcula complementações para município selecionado
- Detalha contribuição de cada etapa educacional
- Visualizações gráficas interativas (Plotly)

#### 2.2. Simulação de Cenários
- Gestor edita matrículas futuras (creches, integral, etc.)
- Sistema recalcula complementações
- Mostra impacto financeiro da mudança
- **Permite projeções de médio prazo para PPA/LDO/LOA**

#### 2.3. Chat Explicativo com IA
- Claude 3.5 Sonnet para explicações pedagógicas
- Responde perguntas gerais ("O que é VAAT?")
- Explica cálculos específicos do município ("Como chegamos em R$ X?")
- Cita sempre bases legais (Lei 14.113/2020, Portarias MEC)

#### 2.4. Arquitetura Técnica
- **Frontend**: Streamlit (Python) - interface web intuitiva
- **Backend**: Lógica de cálculo com ponderadores oficiais
- **IA**: Anthropic Claude API para chat
- **Dados**: 5 municípios exemplo representativos (MVP)
- **Stack**: 100% open-source, sem dependências proprietárias

---

### 3. IMPACTO ESPERADO

#### 3.1. Quantitativo
- **MVP**: 5 municípios demonstrativos
- **Produção**: Escalável para 5.568 municípios
- **Complementações**: R$ 51,1 bilhões (VAAT + VAAF)
- **Beneficiários diretos**: Gestores de 4.200+ municípios elegíveis
- **Beneficiários finais**: 47 milhões de estudantes

#### 3.2. Qualitativo

**Para Gestores:**
- ✅ Compreensão da metodologia oficial
- ✅ Capacidade de validar repasses
- ✅ **Projeções de médio prazo fundamentadas** (PPA 2-3 anos)
- ✅ Autonomia (elimina dependência de consultorias)

**Para Municípios Pequenos:**
- ✅ Nivelamento de capacidade técnica via IA
- ✅ Acesso democrático (gratuito, sem instalação)
- ✅ Redução de assimetria de informação

**Para Controle Social:**
- ✅ Conselhos do FUNDEB podem fiscalizar com fundamentação
- ✅ Transparência inteligível (não apenas dados brutos)

**Para Gestão Pública:**
- ✅ Economia de centenas de milhões em consultorias
- ✅ Planejamento orçamentário mais robusto
- ✅ Alinhamento com propósito pedagógico do FUNDEB

---

### 4. DEMONSTRAÇÃO PRÁTICA

**URL do Protótipo Funcional:**
- [Será fornecida após deploy no Streamlit Cloud]
- Exemplo: `https://fundeb-facil-express-xxxxx.streamlit.app`

**Vídeo de Demonstração:**
- [Link para YouTube/Vimeo será fornecido]
- Duração: 3-5 minutos
- Conteúdo: Cálculo, simulação, chat explicativo

**Repositório Open-Source:**
- GitHub: `https://github.com/[seu-usuario]/fundeb-facil-express`
- Licença: MIT (permite uso e modificação pela administração pública)

---

### 5. VIABILIDADE E SUSTENTABILIDADE

#### 5.1. Técnica
- Tecnologias maduras e consolidadas (Streamlit, Python)
- Stack 100% open-source
- Código documentado e testado
- Manutenção acessível a desenvolvedores Python júnior/pleno

#### 5.2. Financeira
- **MVP**: R$ 0 (desenvolvimento voluntário)
- **Produção nacional**: R$ 100-180 mil/ano
- **ROI**: Centenas de milhões economizados em consultorias
- **Modelos de sustentação**: Adoção pelo MEC/FNDE, OSC via convênio, ou código aberto

#### 5.3. Operacional
- Zero instalação necessária (navegador web)
- Zero treinamento (interface intuitiva + chat guiado)
- Zero custos para municípios
- Compatível com processos governamentais existentes

---

### 6. ALINHAMENTO COM OBJETIVOS DO PRÊMIO

**Item 1.1 - Expandir fronteiras de conhecimento:**
✅ Inovação: IA aplicada a educação orçamentária (não apenas processamento)
✅ Fronteira: Transparência como problema pedagógico, não computacional

**Item 2.1.2 - Soluções inovadoras, viáveis, com impacto:**
✅ Inovadora: Primeira aplicação de LLM para explicações pedagógicas de cálculos orçamentários
✅ Viável: Stack open-source, baixo custo, sem dependências externas
✅ Impacto social: Democratização de conhecimento técnico, nivelamento de municípios

**Item 2.4.1.4 - Estimar/visualizar projeções orçamentárias:**
✅ **Alinhamento direto**: Gestor simula cenários e estima receitas VAAT/VAAF para 2-3 anos
✅ Variáveis controláveis: Matrículas (gestor decide expansões)
✅ Visualizações: Gráficos interativos, tabelas, comparações

---

### 7. BASES LEGAIS

- Lei 14.113/2020 (FUNDEB permanente)
- Portaria MEC nº 567/2024 (ponderadores 2025)
- Dados: Censo Escolar INEP
- Fundamentação: Audiências Públicas Senado Federal (2025)

---

### 8. PRÓXIMOS PASSOS (se premiado)

1. **Curto prazo** (3 meses):
   - Expandir para todos os 5.568 municípios
   - Implementar RAG sobre base legal completa
   - Adicionar exportação de relatórios PDF

2. **Médio prazo** (6 meses):
   - Arquitetura multiagentes (LangGraph)
   - Integração com SIOPE
   - Dashboard para secretarias estaduais

3. **Longo prazo** (12 meses):
   - Inclusão de VAAR com condicionalidades
   - Canal WhatsApp para acesso massivo
   - Parceria com MEC/FNDE para adoção oficial

---

## 🎯 **CHECKLIST FINAL**

Antes de submeter, confirme:

- [ ] PDF acima preparado e salvo
- [ ] Diploma/declaração de matrícula escaneado
- [ ] App deployado no Streamlit Cloud
- [ ] URL pública testada e funcionando
- [ ] Vídeo gravado e hospedado (YouTube/Vimeo)
- [ ] Repositório GitHub público
- [ ] README.md completo
- [ ] Formulário de inscrição preenchido
- [ ] Prazo: **até 15/12/2025**

---

**Link para inscrição:** https://premiosof.enap.gov.br/ (verificar site oficial)

**Dúvidas:** premios@enap.gov.br
