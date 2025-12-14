# 🚀 Guia de Deploy - Streamlit Cloud

## Pré-requisitos
- Conta GitHub (gratuita)
- Conta Streamlit Cloud (gratuita - https://streamlit.io/cloud)

## Passo a Passo

### 1. Preparar Repositório GitHub

```bash
# Inicializar git (se ainda não fez)
git init

# Adicionar todos os arquivos
git add .

# Fazer primeiro commit
git commit -m "feat: MVP FUNDEB Fácil para Prêmio SOF 2025"

# Criar repositório no GitHub
# Vá para https://github.com/new
# Nome: fundeb-facil-express
# Descrição: Sistema Inteligente para Projeção de Complementações FUNDEB (Prêmio SOF 2025)
# Público ou Privado (seu choice)

# Adicionar remote
git remote add origin https://github.com/SEU-USUARIO/fundeb-facil-express.git

# Push
git branch -M main
git push -u origin main
```

### 2. Deploy no Streamlit Cloud

1. **Acesse**: https://share.streamlit.io/

2. **Faça login** com sua conta GitHub

3. **Clique em "New app"**

4. **Configure:**
   - Repository: `SEU-USUARIO/fundeb-facil-express`
   - Branch: `main`
   - Main file path: `app.py`

5. **Advanced settings** (opcional):
   - Python version: 3.12

6. **Secrets** (IMPORTANTE para o chat):
   - Clique em "Advanced settings"
   - Em "Secrets" adicione:
   ```toml
   ANTHROPIC_API_KEY = "sua-chave-da-anthropic-aqui"
   ```

7. **Deploy!**
   - Clique em "Deploy"
   - Aguarde 2-5 minutos
   - Você receberá uma URL pública tipo: `https://fundeb-facil-express-xxxxx.streamlit.app`

### 3. Validar Deploy

- [ ] App carrega sem erros
- [ ] Calculadora funciona
- [ ] Gráficos são exibidos
- [ ] Chat responde (se API key configurada)
- [ ] Troca de municípios funciona
- [ ] Simulação funciona

### 4. Usar na Submissão

No formulário do Prêmio SOF (item 5.6.4), você pode:

**Opção 1:** Fornecer a URL pública do Streamlit Cloud

**Opção 2:** Fazer um vídeo de demonstração e incluir a URL na descrição

---

## Troubleshooting

### Erro: "Module not found"
- Verifique se `pyproject.toml` está no repositório
- Streamlit Cloud instala dependências automaticamente do pyproject.toml

### Chat não funciona
- Verifique se adicionou `ANTHROPIC_API_KEY` nos Secrets
- Formato correto: `ANTHROPIC_API_KEY = "sk-ant-..."`

### App não carrega dados
- Verifique se a pasta `dados/` está no repositório
- Confirme que `municipios.json` e `ponderadores.json` foram commitados

---

## 🎥 Gravar Vídeo de Demonstração

Para o Prêmio SOF, grave um vídeo de 3-5 minutos mostrando:

1. **Intro** (30s): O que é o FUNDEB Fácil
2. **Calculadora** (1min): Seleção de município, cálculo, visualização de resultados
3. **Simulação** (1min): Editar matrículas, recalcular, mostrar impacto
4. **Chat** (1min): Fazer 2-3 perguntas sobre FUNDEB
5. **Comparações** (30s): Mostrar tab de comparações
6. **Fechamento** (30s): Resumo do valor da solução

**Ferramentas sugeridas:**
- OBS Studio (grátis, open-source)
- Loom (grátis para vídeos curtos)
- Zoom (gravar sessão)

**Hospedagem:**
- YouTube (não listado)
- Vimeo
- Google Drive (público)
