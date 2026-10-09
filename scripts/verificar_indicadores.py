"""Confere calculos, casos sem entrega e rejeicao de comparacoes inadequadas."""
import copy
import json
from pathlib import Path
from indicadores import avaliar, comparar

root = Path(__file__).resolve().parents[1]
dados = json.loads((root/'experimentos/exemplo-indicadores.json').read_text(encoding='utf-8'))
resultado = comparar(dados)
assert abs(resultado['pares'][0]['candidata']['eficiencia_valor_por_acao'] - 26/90) < 1e-12
assert resultado['pares'][0]['candidata']['meta_atingida_no_prazo'] is True
assert resultado['pares'][1]['candidata']['meta_atingida_no_prazo'] is False
assert resultado['efetividade_simulada']['diferenca_media_valor_confirmado'] == 6.5
assert resultado['origem'] == 'ilustrativo'
zero = copy.deepcopy(dados['pares'][0]['referencia'])
zero.update(valor_confirmado=0, acoes_consumidas=0)
assert avaliar(zero)['eficiencia_valor_por_acao'] is None
tardio = copy.deepcopy(dados['pares'][0]['candidata'])
tardio['passo_final'] = 101
assert avaliar(tardio)['meta_atingida_no_prazo'] is False
for campo,valor in [('acoes_consumidas',-1),('valor_confirmado',float('nan')),('meta_valor',0),('acoes_consumidas',0)]:
    invalido = copy.deepcopy(dados['pares'][0]['candidata'])
    invalido[campo] = valor
    try:
        avaliar(invalido)
    except ValueError:
        pass
    else:
        raise AssertionError('Registro invalido aceito: '+campo)
desigual = copy.deepcopy(dados)
desigual['pares'][0]['candidata']['semente'] = 999
try:
    comparar(desigual)
except ValueError:
    pass
else:
    raise AssertionError('Par com sementes distintas foi aceito.')
print('INDICADORES_APROVADOS | calculos, prazo, origem, zero e entradas invalidas conferidos')
