# Experimentos e evidências

`protocolo.json` descreve uma campanha futura. A proposta inicial é comparar S0 e S1 em três famílias de mapas, dez sementes por família e troca de lados, totalizando 60 partidas. A campanha não foi executada, e seu tamanho poderá ser revisto após o piloto.

`evidencias/verificacao-inicial.json` registra a verificação funcional realmente executada, com data e hashes. `evidencias/sessao-inicial.json` registra a sessão de estudo de 15 segundos. Os marcadores de integração estão em texto, sem saídas auxiliares de servidores de inspeção.

`execucoes` recebe cada rodada de estudo e validação. Essa pasta é ignorada no Git, pois pode crescer rapidamente. Evidências selecionadas para o relatório devem manter configuração, versão e vínculo com os registros completos.

Não há resultados de comparação entre estratégias, competição completa ou execução de Moise nesta preparação.

`exemplo-indicadores.json` e `evidencias/exemplo-indicadores-calculado.json` usam números **ilustrativos**, inventados para explicar eficiência, eficácia e efetividade simulada. A execução do cálculo é real; os números de entregas não foram observados no simulador. `scripts/verificar_indicadores.py` confere as fórmulas e rejeita entradas inválidas.
