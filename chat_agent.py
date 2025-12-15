"""
Agente de chat para explicações sobre FUNDEB
"""
import os
from anthropic import Anthropic


class ChatAgentFUNDEB:
    """Agente conversacional para explicações sobre FUNDEB"""

    def __init__(self, api_key: str = None):
        """Inicializa agente Claude"""
        self.client = Anthropic(api_key=api_key or os.getenv('ANTHROPIC_API_KEY'))
        self.model = "claude-sonnet-4-5"

        # Contexto legal embutido (sem RAG para MVP)
        self.contexto_legal = """
        # CONTEXTO LEGAL DO FUNDEB

        ## Lei 14.113/2020 - FUNDEB Permanente

        ### Complementação da União - Modalidades:

        **VAAT (Valor Aluno Ano Total):**
        - Objetivo: Elevar municípios com menores valores/aluno a patamar mínimo nacional
        - Base: Nível Socioeconômico (NSE) dos estudantes e capacidade de arrecadação local
        - Valor 2025: R$ 24,2 bilhões
        - Beneficiários: 2.425 municípios

        **VAAF (Valor Aluno Ano Final):**
        - Objetivo: Complementar fundos estaduais que não atingem valor mínimo nacional
        - Valor 2025: R$ 26,9 bilhões
        - Beneficiários: 10 estados e 1.849 municípios

        ### Ponderadores (multiplicam matrículas no cálculo):

        **VAAT:**
        - Creche integral: 1,90 (mais alto - reflete custo com professores especializados)
        - Creche parcial: 1,50
        - Pré-escola integral: 1,88
        - Pré-escola parcial: 1,45
        - Anos iniciais urbano: 1,00 (base)
        - Anos iniciais rural: 1,15
        - Educação especial: +1,40 (aditivo)

        **VAAF:**
        - Ponderadores menores que VAAT (complementação menos redistributiva)
        - Creche integral: 1,55
        - Pré-escola integral: 1,50

        ### Ajustes Multiplicativos:

        **NSE (Nível Socioeconômico):**
        - Range: 0,95 a 1,05
        - Alunos mais vulneráveis geram fator maior
        - Fórmula: 0,95 + (NSE/1000)

        **DRec (Disponibilidade de Recursos):**
        - Range: 0,965 a 1,035
        - Capacidade fiscal local
        - Menor capacidade = maior fator

        ### Fórmula Completa:
        Matrículas Ajustadas = Matrículas × Ponderador Base × NSE × DRec

        ### Bases Legais:
        - Lei 14.113/2020, Art. 5º (VAAT) e Art. 6º (VAAF)
        - Portaria MEC nº 567/2024 (ponderadores)
        """

    def gerar_resposta(
        self,
        pergunta: str,
        contexto_municipio: dict = None,
        historico: list = None
    ) -> str:
        """
        Gera resposta usando Claude

        Args:
            pergunta: Pergunta do usuário
            contexto_municipio: Dados do município selecionado (opcional)
            historico: Histórico da conversa (opcional)

        Returns:
            Resposta do agente
        """
        # Monta prompt do sistema
        system_prompt = f"""Você é um especialista em financiamento educacional brasileiro,
especialmente no FUNDEB (Fundo de Manutenção e Desenvolvimento da Educação Básica).

Seu papel é:
1. Explicar de forma didática e acessível como funcionam as complementações VAAT e VAAF
2. Responder perguntas sobre legislação do FUNDEB
3. Quando houver dados de um município específico, explicar os cálculos daquele município
4. Sugerir cenários de simulação relevantes

IMPORTANTE:
- Use linguagem clara, sem jargões excessivos
- Cite sempre as bases legais (Lei 14.113/2020, Portarias MEC)
- Explique passo-a-passo quando falar de cálculos
- Seja conciso mas completo

{self.contexto_legal}
"""

        # Adiciona contexto do município se disponível
        if contexto_municipio:
            system_prompt += f"""

MUNICÍPIO SELECIONADO NA CALCULADORA:
{self._formatar_contexto_municipio(contexto_municipio)}
"""

        # Monta mensagens
        messages = []

        # Adiciona histórico se existir
        if historico:
            messages.extend(historico)

        # Adiciona pergunta atual
        messages.append({
            "role": "user",
            "content": pergunta
        })

        # Chama Claude
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            system=system_prompt,
            messages=messages
        )

        return response.content[0].text

    def _formatar_contexto_municipio(self, contexto: dict) -> str:
        """Formata contexto do município para o prompt"""
        if not contexto:
            return ""

        texto = f"""
Nome: {contexto.get('municipio', 'N/A')}
UF: {contexto.get('uf', 'N/A')}
NSE: {contexto.get('nse', 0):.1f}
DRec: {contexto.get('drec', 0):.3f}

VAAT:
- Elegível: {'Sim' if contexto.get('vaat', {}).get('elegivel') else 'Não'}
- Valor Total: R$ {contexto.get('vaat', {}).get('valor_total', 0):,.2f}

VAAF:
- Elegível: {'Sim' if contexto.get('vaaf', {}).get('elegivel') else 'Não'}
- Valor Total: R$ {contexto.get('vaaf', {}).get('valor_total', 0):,.2f}

Total Complementações: R$ {contexto.get('total_complementacoes', 0):,.2f}
Matrículas Totais: {contexto.get('matriculas_totais', 0):,}
"""
        return texto

    def explicar_calculo(self, resultado_calculo: dict) -> str:
        """
        Gera explicação detalhada de um cálculo específico

        Args:
            resultado_calculo: Resultado da calculadora

        Returns:
            Explicação passo-a-passo
        """
        pergunta = f"""
Me explique passo-a-passo como chegamos aos valores calculados para este município.
Detalhe:
1. Como os ponderadores foram aplicados
2. O impacto dos ajustes de NSE e DRec
3. Como cada etapa educacional contribuiu para o total
4. Por que o município é ou não elegível para cada complementação
"""
        return self.gerar_resposta(pergunta, contexto_municipio=resultado_calculo)
