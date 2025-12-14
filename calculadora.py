"""
Módulo de cálculo de complementações VAAT e VAAF do FUNDEB
"""
import json
from typing import Dict, Tuple


class CalculadoraFUNDEB:
    """Calculadora de complementações VAAT e VAAF"""

    def __init__(self):
        """Inicializa calculadora carregando ponderadores"""
        with open('dados/ponderadores.json', 'r', encoding='utf-8') as f:
            self.ponderadores = json.load(f)

    def calcular_fator_nse(self, nse: float) -> float:
        """
        Calcula fator de ajuste baseado no NSE
        Formula: 0.95 + (NSE / 1000)
        Range: [0.95, 1.05]
        """
        fator = 0.95 + (nse / 1000)
        return max(0.95, min(1.05, fator))

    def calcular_matriculas_ajustadas(
        self,
        matriculas: Dict[str, int],
        tipo_complementacao: str,
        nse: float,
        drec: float
    ) -> Dict[str, float]:
        """
        Calcula matrículas ajustadas aplicando ponderadores

        Args:
            matriculas: Dicionário com matrículas por etapa
            tipo_complementacao: 'vaat' ou 'vaaf'
            nse: Nível Socioeconômico do município
            drec: Disponibilidade de Recursos (capacidade fiscal)

        Returns:
            Dicionário com matrículas ajustadas por etapa
        """
        ponderadores_tipo = self.ponderadores[tipo_complementacao]
        fator_nse = self.calcular_fator_nse(nse)

        matriculas_ajustadas = {}

        for etapa, qtd_matriculas in matriculas.items():
            if etapa in ponderadores_tipo:
                # Ponderador base da etapa
                ponderador_base = ponderadores_tipo[etapa]

                # Aplica ajustes NSE e DRec
                ponderador_final = ponderador_base * fator_nse * drec

                # Calcula matrículas ajustadas
                matriculas_ajustadas[etapa] = qtd_matriculas * ponderador_final

        return matriculas_ajustadas

    def calcular_complementacao(
        self,
        municipio_data: Dict,
        tipo_complementacao: str,
        total_matriculas_ajustadas_nacional: float = None
    ) -> Tuple[float, Dict]:
        """
        Calcula complementação VAAT ou VAAF para um município

        Args:
            municipio_data: Dados do município
            tipo_complementacao: 'vaat' ou 'vaaf'
            total_matriculas_ajustadas_nacional: Total nacional (para cálculo proporcional)

        Returns:
            Tupla (valor_complementacao, detalhamento_por_etapa)
        """
        # Verifica elegibilidade
        elegivel_key = f'elegivel_{tipo_complementacao}'
        if not municipio_data.get(elegivel_key, False):
            return 0.0, {}

        # Calcula matrículas ajustadas
        matriculas_ajustadas = self.calcular_matriculas_ajustadas(
            municipio_data['matriculas'],
            tipo_complementacao,
            municipio_data['nse'],
            municipio_data['drec']
        )

        # Total de matrículas ajustadas do município
        total_ajustado_municipio = sum(matriculas_ajustadas.values())

        # Valor total da complementação nacional
        total_complementacao_nacional = self.ponderadores['complementacao_total'][f'{tipo_complementacao}_2025']

        # Se não fornecido, usa aproximação (5% dos municípios são elegíveis)
        if total_matriculas_ajustadas_nacional is None:
            # Aproximação: assumindo que município representa 0,02% do total elegível
            # (isso é simplificação para MVP - em produção usaríamos soma real)
            total_matriculas_ajustadas_nacional = total_ajustado_municipio * 5000

        # Calcula proporção do município no total
        proporcao = total_ajustado_municipio / total_matriculas_ajustadas_nacional

        # Valor da complementação
        valor_complementacao = total_complementacao_nacional * proporcao

        # Detalhamento por etapa (quanto cada etapa contribuiu)
        detalhamento = {}
        for etapa, matriculas_ajustadas_etapa in matriculas_ajustadas.items():
            proporcao_etapa = matriculas_ajustadas_etapa / total_ajustado_municipio
            valor_etapa = valor_complementacao * proporcao_etapa

            detalhamento[etapa] = {
                'matriculas_brutas': municipio_data['matriculas'][etapa],
                'matriculas_ajustadas': matriculas_ajustadas_etapa,
                'valor_complementacao': valor_etapa,
                'ponderador_efetivo': (
                    matriculas_ajustadas_etapa / municipio_data['matriculas'][etapa]
                    if municipio_data['matriculas'][etapa] > 0 else 0
                )
            }

        return valor_complementacao, detalhamento

    def calcular_ambas_complementacoes(self, municipio_data: Dict) -> Dict:
        """
        Calcula VAAT e VAAF para um município

        Returns:
            Dicionário com resultados completos
        """
        valor_vaat, detalhe_vaat = self.calcular_complementacao(
            municipio_data, 'vaat'
        )

        valor_vaaf, detalhe_vaaf = self.calcular_complementacao(
            municipio_data, 'vaaf'
        )

        return {
            'municipio': municipio_data['nome'],
            'uf': municipio_data['uf'],
            'vaat': {
                'valor_total': valor_vaat,
                'elegivel': municipio_data.get('elegivel_vaat', False),
                'detalhamento': detalhe_vaat
            },
            'vaaf': {
                'valor_total': valor_vaaf,
                'elegivel': municipio_data.get('elegivel_vaaf', False),
                'detalhamento': detalhe_vaaf
            },
            'total_complementacoes': valor_vaat + valor_vaaf,
            'matriculas_totais': sum(municipio_data['matriculas'].values())
        }


def formatar_moeda(valor: float) -> str:
    """Formata valor em reais"""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def formatar_numero(valor: float) -> str:
    """Formata número com separador de milhares"""
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
