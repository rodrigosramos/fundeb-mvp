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
    layout="wide",
    initial_sidebar_state="expanded"
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


def inicializar_chat_agent():
    """Inicializa agente de chat"""
    api_key = st.session_state.get('anthropic_api_key')
    if api_key:
        return ChatAgentFUNDEB(api_key=api_key)
    return None


def main():
    """Função principal do app"""

    # Header
    st.markdown('<div class="main-header">📚 FUNDEB Fácil</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">Sistema Inteligente para Compreensão e Projeção de Complementações VAAT/VAAF</div>',
        unsafe_allow_html=True
    )

    # Sidebar - Configurações
    with st.sidebar:
        st.image("https://via.placeholder.com/150x50/1E88E5/FFFFFF?text=FUNDEB+Fácil", use_container_width=True)

        st.markdown("### ⚙️ Configurações")

        # API Key Anthropic
        api_key = st.text_input(
            "Chave API Anthropic",
            type="password",
            value=st.session_state.get('anthropic_api_key', ''),
            help="Necessária para o chat explicativo"
        )
        if api_key:
            st.session_state['anthropic_api_key'] = api_key
            st.success("✅ API configurada")

        st.markdown("---")

        st.markdown("### 📖 Sobre")
        st.info("""
        **FUNDEB Fácil** é uma solução para transparência inteligível das complementações
        VAAT e VAAF do FUNDEB.

        **Recursos:**
        - 🧮 Calculadora de complementações
        - 📊 Visualizações interativas
        - 🤖 Chat explicativo com IA
        - 🎯 Simulação de cenários
        """)

        st.markdown("---")
        st.caption("Desenvolvido para o Prêmio SOF 2025")

    # Carrega dados
    municipios = carregar_municipios()
    calculadora = inicializar_calculadora()

    # Tabs principais
    tab1, tab2, tab3 = st.tabs(["🧮 Calculadora", "💬 Chat Explicativo", "📊 Comparações"])

    # ========== TAB 1: CALCULADORA ==========
    with tab1:
        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown("### 📍 Selecione o Município")

            # Seleção de município
            municipios_opcoes = {
                f"{m['nome']} - {m['uf']}": m for m in municipios
            }

            municipio_selecionado = st.selectbox(
                "Município",
                options=list(municipios_opcoes.keys()),
                index=0
            )

            municipio_data = municipios_opcoes[municipio_selecionado].copy()

            # Exibe informações do município
            st.markdown("#### Informações do Município")
            st.metric("População", f"{municipio_data['populacao']:,}")
            st.metric("NSE (Nível Socioeconômico)", f"{municipio_data['nse']:.1f}")
            st.metric("DRec (Capacidade Fiscal)", f"{municipio_data['drec']:.3f}")

            st.markdown("---")

            # Modo de simulação
            st.markdown("### 🎯 Modo de Simulação")
            modo_simulacao = st.radio(
                "Escolha o modo:",
                ["Dados Atuais", "Simular Cenário"],
                help="Use 'Simular Cenário' para projetar impacto de mudanças nas matrículas"
            )

            # Edição de matrículas (se modo simulação)
            if modo_simulacao == "Simular Cenário":
                st.markdown("#### ✏️ Edite as Matrículas")

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

        with col2:
            st.markdown("### 💰 Resultados do Cálculo")

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
                st.markdown("#### 📊 Detalhamento por Etapa Educacional")

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

    # ========== TAB 2: CHAT EXPLICATIVO ==========
    with tab2:
        st.markdown("### 💬 Assistente Conversacional FUNDEB")

        # Verifica se API está configurada
        if not st.session_state.get('anthropic_api_key'):
            st.warning("⚠️ Configure sua chave API da Anthropic na barra lateral para usar o chat.")
        else:
            chat_agent = inicializar_chat_agent()

            if chat_agent:
                # Inicializa histórico
                if 'chat_history' not in st.session_state:
                    st.session_state['chat_history'] = []

                # Exibe histórico
                for msg in st.session_state['chat_history']:
                    with st.chat_message(msg['role']):
                        st.markdown(msg['content'])

                # Input do usuário
                if prompt := st.chat_input("Faça uma pergunta sobre FUNDEB..."):
                    # Adiciona mensagem do usuário
                    st.session_state['chat_history'].append({
                        'role': 'user',
                        'content': prompt
                    })

                    with st.chat_message("user"):
                        st.markdown(prompt)

                    # Gera resposta
                    with st.chat_message("assistant"):
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

                            st.markdown(resposta)

                            # Adiciona ao histórico
                            st.session_state['chat_history'].append({
                                'role': 'assistant',
                                'content': resposta
                            })

                # Botão limpar histórico
                if st.button("🗑️ Limpar Histórico"):
                    st.session_state['chat_history'] = []
                    st.rerun()

    # ========== TAB 3: COMPARAÇÕES ==========
    with tab3:
        st.markdown("### 📊 Comparação Entre Municípios")

        st.info("🚧 Recurso em desenvolvimento - MVP focado em cálculo individual e chat explicativo")

        # Preview de comparação simples
        st.markdown("#### Visão Geral dos Municípios")

        # Calcula para todos
        resultados_todos = []
        for mun in municipios:
            res = calculadora.calcular_ambas_complementacoes(mun)
            resultados_todos.append({
                'Município': res['municipio'],
                'UF': res['uf'],
                'VAAT': res['vaat']['valor_total'],
                'VAAF': res['vaaf']['valor_total'],
                'Total': res['total_complementacoes'],
                'Matrículas': res['matriculas_totais']
            })

        df_comparacao = pd.DataFrame(resultados_todos)

        # Gráfico comparativo
        fig = go.Figure()
        fig.add_trace(go.Bar(name='VAAT', x=df_comparacao['Município'], y=df_comparacao['VAAT']))
        fig.add_trace(go.Bar(name='VAAF', x=df_comparacao['Município'], y=df_comparacao['VAAF']))
        fig.update_layout(
            title='Complementações por Município',
            xaxis_title='Município',
            yaxis_title='Valor (R$)',
            barmode='stack'
        )
        st.plotly_chart(fig, use_container_width=True)

        # Tabela
        st.dataframe(
            df_comparacao.style.format({
                'VAAT': 'R$ {:,.2f}',
                'VAAF': 'R$ {:,.2f}',
                'Total': 'R$ {:,.2f}',
                'Matrículas': '{:,.0f}'
            }),
            use_container_width=True,
            hide_index=True
        )


if __name__ == "__main__":
    main()
