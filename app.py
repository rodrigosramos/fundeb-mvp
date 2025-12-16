"""
FUNDEB Fácil - Sistema Inteligente para Projeção de Complementações Orçamentárias
MVP para Prêmio SOF 2025
"""
import streamlit as st
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from calculadora import CalculadoraFUNDEB, formatar_moeda, formatar_numero
from chat_agent import ChatAgentFUNDEB


# Configuração da página
st.set_page_config(
    page_title="FUNDEB Fácil",
    page_icon="📚",
    layout="wide"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 0.25rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 0.25rem;
        margin: 1rem 0;
    }
    /* Reduzir padding entre colunas */
    [data-testid="column"] {
        padding: 0 10px;
    }
    /* Melhorar scroll do chat */
    .stChatMessage {
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def carregar_municipios():
    """Carrega dados dos municípios"""
    with open('dados/municipios.json', 'r', encoding='utf-8') as f:
        return json.load(f)


@st.cache_resource
def inicializar_calculadora():
    """Inicializa calculadora (cached)"""
    return CalculadoraFUNDEB()


@st.cache_data
def obter_lista_ufs(municipios):
    """Retorna lista única de UFs ordenada"""
    return sorted(list(set([m['uf'] for m in municipios])))


@st.cache_data
def filtrar_municipios_por_uf(municipios, uf):
    """Filtra municípios de uma UF específica"""
    return [m for m in municipios if m['uf'] == uf]


def inicializar_chat_agent():
    """Inicializa agente de chat - APENAS via Secrets"""
    try:
        api_key = st.secrets.get("ANTHROPIC_API_KEY")
        if api_key:
            return ChatAgentFUNDEB(api_key=api_key)
    except Exception:
        pass
    return None


def main():
    """Função principal do app"""

    # Header
    st.markdown('<div class="main-header">📚 FUNDEB Fácil</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">Sistema Inteligente para Compreensão e Projeção de Complementações VAAT/VAAF</div>',
        unsafe_allow_html=True
    )

    # Carrega dados
    municipios = carregar_municipios()
    calculadora = inicializar_calculadora()

    # Layout side-by-side: Calculadora (65%) | Chat (35%)
    col_calc, col_chat = st.columns([65, 35], gap="large")

    # ========== COLUNA ESQUERDA: CALCULADORA ==========
    with col_calc:
        st.markdown("### 🧮 Calculadora VAAT/VAAF")

        # Filtro UF → Município
        st.markdown("#### 📍 Selecione o Município")

        lista_ufs = obter_lista_ufs(municipios)

        col_uf, col_mun = st.columns(2)

        with col_uf:
            # Detectar UF padrão (primeira com municípios)
            uf_default = lista_ufs[0] if lista_ufs else "PR"
            uf_selecionada = st.selectbox(
                "Estado (UF)",
                options=lista_ufs,
                index=lista_ufs.index(uf_default) if uf_default in lista_ufs else 0
            )

        with col_mun:
            municipios_filtrados = filtrar_municipios_por_uf(municipios, uf_selecionada)
            opcoes_mun = {m['nome']: m for m in municipios_filtrados}

            municipio_nome = st.selectbox(
                "Município",
                options=list(opcoes_mun.keys())
            )

            municipio_data = opcoes_mun[municipio_nome].copy()

        st.markdown("---")

        # Informações do Município em colunas compactas
        col_info1, col_info2, col_info3 = st.columns(3)

        with col_info1:
            st.metric("População", f"{municipio_data['populacao']:,}")

        with col_info2:
            st.metric("NSE", f"{municipio_data['nse']:.1f}")

        with col_info3:
            st.metric("DRec", f"{municipio_data['drec']:.3f}")

        st.markdown("---")

        # Modo de simulação
        st.markdown("#### 🎯 Modo de Simulação")
        modo_simulacao = st.radio(
            "Escolha o modo:",
            ["Dados Atuais", "Simular Cenário"],
            help="Use 'Simular Cenário' para projetar impacto de mudanças nas matrículas"
        )

        # Edição de matrículas (se modo simulação)
        if modo_simulacao == "Simular Cenário":
            st.markdown("**✏️ Edite as Matrículas**")

            with st.expander("📝 Editar Matrículas", expanded=True):
                for etapa, valor in municipio_data['matriculas'].items():
                    etapa_label = etapa.replace('_', ' ').title()
                    novo_valor = st.number_input(
                        etapa_label,
                        min_value=0,
                        value=valor,
                        step=10,
                        key=f"input_{etapa}"
                    )
                    municipio_data['matriculas'][etapa] = novo_valor

        st.markdown("---")

        # Botão calcular e resultados
        st.markdown("#### 💰 Resultados do Cálculo")

        # Botão calcular
        if st.button("🔢 Calcular Complementações", type="primary", use_container_width=True):
            with st.spinner("Calculando..."):
                # Calcula
                resultado = calculadora.calcular_ambas_complementacoes(municipio_data)

                # Salva em session_state
                st.session_state['ultimo_resultado'] = resultado

        # Exibe resultados se disponível
        if 'ultimo_resultado' in st.session_state:
            resultado = st.session_state['ultimo_resultado']

            # Métricas principais
            col_m1, col_m2, col_m3 = st.columns(3)

            with col_m1:
                st.metric(
                    "💵 VAAT",
                    formatar_moeda(resultado['vaat']['valor_total']),
                    delta="Elegível" if resultado['vaat']['elegivel'] else "Não elegível"
                )

            with col_m2:
                st.metric(
                    "💵 VAAF",
                    formatar_moeda(resultado['vaaf']['valor_total']),
                    delta="Elegível" if resultado['vaaf']['elegivel'] else "Não elegível"
                )

            with col_m3:
                st.metric(
                    "💰 Total",
                    formatar_moeda(resultado['total_complementacoes'])
                )

            st.markdown("---")

            # Detalhamento por etapa
            st.markdown("**📊 Detalhamento por Etapa Educacional**")

            tab_vaat, tab_vaaf = st.tabs(["VAAT", "VAAF"])

            with tab_vaat:
                if resultado['vaat']['elegivel']:
                    df_vaat = pd.DataFrame.from_dict(
                        resultado['vaat']['detalhamento'],
                        orient='index'
                    )
                    df_vaat.index.name = 'Etapa'
                    df_vaat = df_vaat.reset_index()
                    df_vaat['Etapa'] = df_vaat['Etapa'].str.replace('_', ' ').str.title()

                    # Tabela
                    st.dataframe(
                        df_vaat.style.format({
                            'matriculas_brutas': '{:.0f}',
                            'matriculas_ajustadas': '{:.2f}',
                            'valor_complementacao': 'R$ {:,.2f}',
                            'ponderador_efetivo': '{:.3f}'
                        }),
                        use_container_width=True,
                        hide_index=True
                    )

                    # Gráfico
                    fig = px.bar(
                        df_vaat,
                        x='Etapa',
                        y='valor_complementacao',
                        title='Contribuição de Cada Etapa para VAAT',
                        labels={'valor_complementacao': 'Valor (R$)', 'Etapa': 'Etapa Educacional'}
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Município não elegível para VAAT")

            with tab_vaaf:
                if resultado['vaaf']['elegivel']:
                    df_vaaf = pd.DataFrame.from_dict(
                        resultado['vaaf']['detalhamento'],
                        orient='index'
                    )
                    df_vaaf.index.name = 'Etapa'
                    df_vaaf = df_vaaf.reset_index()
                    df_vaaf['Etapa'] = df_vaaf['Etapa'].str.replace('_', ' ').str.title()

                    # Tabela
                    st.dataframe(
                        df_vaaf.style.format({
                            'matriculas_brutas': '{:.0f}',
                            'matriculas_ajustadas': '{:.2f}',
                            'valor_complementacao': 'R$ {:,.2f}',
                            'ponderador_efetivo': '{:.3f}'
                        }),
                        use_container_width=True,
                        hide_index=True
                    )

                    # Gráfico
                    fig = px.bar(
                        df_vaaf,
                        x='Etapa',
                        y='valor_complementacao',
                        title='Contribuição de Cada Etapa para VAAF',
                        labels={'valor_complementacao': 'Valor (R$)', 'Etapa': 'Etapa Educacional'}
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Município não elegível para VAAF")

    # ========== COLUNA DIREITA: CHAT ==========
    with col_chat:
        st.markdown("### 💬 Assistente Conversacional FUNDEB")

        # Verifica se API está configurada (session_state ou secrets)
        chat_agent = inicializar_chat_agent()

        if not chat_agent:
            st.info("⚠️ Chat indisponível. Configure ANTHROPIC_API_KEY nos Secrets do Streamlit Cloud para ativar o assistente conversacional.")
        else:
            # Inicializa histórico
            if 'chat_history' not in st.session_state:
                st.session_state['chat_history'] = []

            # Container com altura fixa para histórico
            chat_container = st.container(height=500)

            with chat_container:
                # Exibe histórico
                for msg in st.session_state['chat_history']:
                    with st.chat_message(msg['role']):
                        st.markdown(msg['content'])

            # Input do usuário (fora do container - fica fixo)
            if prompt := st.chat_input("Faça uma pergunta sobre FUNDEB..."):
                # Adiciona mensagem do usuário
                st.session_state['chat_history'].append({
                    'role': 'user',
                    'content': prompt
                })

                # Gera resposta
                with st.spinner("Pensando..."):
                    contexto = st.session_state.get('ultimo_resultado')

                    resposta = chat_agent.gerar_resposta(
                        prompt,
                        contexto_municipio=contexto,
                        historico=[
                            {"role": m['role'], "content": m['content']}
                            for m in st.session_state['chat_history'][:-1]
                        ]
                    )

                    # Adiciona ao histórico
                    st.session_state['chat_history'].append({
                        'role': 'assistant',
                        'content': resposta
                    })

                # Força rerun para mostrar novas mensagens
                st.rerun()

            # Botão limpar histórico
            if st.button("🗑️ Limpar Histórico"):
                st.session_state['chat_history'] = []
                st.rerun()


if __name__ == "__main__":
    main()
