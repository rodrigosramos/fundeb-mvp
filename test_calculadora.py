from calculadora import CalculadoraFUNDEB
import json

# Carrega município teste
with open('dados/municipios.json') as f:
    municipios = json.load(f)

calc = CalculadoraFUNDEB()
resultado = calc.calcular_ambas_complementacoes(municipios[0])

print('✅ TESTE DA CALCULADORA - SUCESSO!')
print(f"Município: {resultado['municipio']}")
print(f"VAAT: R$ {resultado['vaat']['valor_total']:,.2f}")
print(f"VAAF: R$ {resultado['vaaf']['valor_total']:,.2f}")
print(f"Total: R$ {resultado['total_complementacoes']:,.2f}")
