"""Calcula indicadores a partir de registros; exemplos nao viram resultados reais."""
from pathlib import Path
import argparse
import json
import math

def numero(dados, nome):
    valor = dados[nome]
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise ValueError(f'{nome} precisa ser numerico.')
    if not math.isfinite(valor) or valor < 0:
        raise ValueError(f'{nome} precisa ser finito e nao negativo.')
    return valor

def avaliar(registro):
    """Resume uma equipe numa partida; nao infere causalidade nem qualidade real."""
    valor = numero(registro, 'valor_confirmado')
    acoes = numero(registro, 'acoes_consumidas')
    meta = numero(registro, 'meta_valor')
    passo = numero(registro, 'passo_final')
    limite = numero(registro, 'limite_passos')
    if meta == 0 or limite == 0:
        raise ValueError('Meta e limite de passos precisam ser maiores que zero.')
    if any(v != int(v) for v in (acoes, passo, limite)):
        raise ValueError('Acoes e passos precisam ser inteiros.')
    if valor > 0 and acoes == 0:
        raise ValueError('Entrega positiva com zero acoes nao e um registro valido deste protocolo.')
    dentro_prazo = passo <= limite
    return {
        'eficiencia_valor_por_acao': valor / acoes if acoes else None,
        'eficacia_fracao_da_meta': min(valor / meta, 1) if dentro_prazo else 0,
        'meta_atingida_no_prazo': valor >= meta and dentro_prazo,
        'valor_confirmado': valor,
        'limite': 'Acoes devem incluir falhas e espera; custo de mensagens e CPU e relatado separadamente.'
    }

def comparar(dados):
    """Compara pares declarados equivalentes e mantem a procedencia dos numeros."""
    origem = dados['origem']
    if origem not in ('ilustrativo', 'observado'):
        raise ValueError('Informe origem ilustrativo ou observado.')
    pares = dados['pares']
    if not pares:
        raise ValueError('Informe pelo menos um par de registros.')
    resultados = []
    for par in pares:
        referencia = par['referencia']
        candidata = par['candidata']
        for chave in ('contexto', 'semente', 'orientacao', 'meta_valor', 'limite_passos'):
            if referencia[chave] != candidata[chave]:
                raise ValueError(f'Par {par["id"]} nao e comparavel no campo {chave}.')
        base = avaliar(referencia)
        nova = avaliar(candidata)
        ganho = nova['valor_confirmado'] - base['valor_confirmado']
        resultados.append({
            'id': par['id'], 'referencia': base, 'candidata': nova,
            'diferenca_valor_confirmado': ganho,
            'variacao_percentual': 100 * ganho / base['valor_confirmado'] if base['valor_confirmado'] else None
        })
    return {
        'origem': origem,
        'pares': resultados,
        'efetividade_simulada': {
            'diferenca_media_valor_confirmado': sum(p['diferenca_valor_confirmado'] for p in resultados) / len(resultados),
            'pares_com_melhora': sum(p['diferenca_valor_confirmado'] > 0 for p in resultados),
            'total_pares': len(resultados),
            'interpretacao': 'Efeito util candidato no cenario declarado; depende de desenho comparavel e evidencia de entrega.',
            'limite': 'Nao demonstra impacto profissional, significancia estatistica ou causalidade apenas pelo calculo.'
        },
        'status': 'EXEMPLO_DIDATICO_SEM_RESULTADO_EXPERIMENTAL' if origem == 'ilustrativo' else 'REGISTROS_INFORMADOS_PARA_ANALISE'
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('entrada', type=Path)
    parser.add_argument('--saida', type=Path)
    args = parser.parse_args()
    dados = json.loads(args.entrada.read_text(encoding='utf-8'))
    resultado = comparar(dados)
    texto = json.dumps(resultado, ensure_ascii=False, indent=2)
    if args.saida:
        args.saida.parent.mkdir(parents=True, exist_ok=True)
        args.saida.write_text(texto, encoding='utf-8')
    print(texto)

if __name__ == '__main__':
    main()
