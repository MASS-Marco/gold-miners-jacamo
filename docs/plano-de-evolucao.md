# Plano de evolução

Projeto individual. Todos os itens abaixo, exceto a preparação, são planejados.

| Etapa | Critério para considerar pronta |
|---|---|
| P0 Preparação concluída | Compilar; verificar regras; executar coleta e depósito; preservar fontes e evidências. |
| P1 Competição local | Duas equipes de quatro agentes, placar separado, início e fim de partida, passos e conflitos definidos. |
| P2 Informação e invariantes | Remover acesso global da política; validar percepção por equipe, conservação, capacidade, ocupação e contagem única de entrega. |
| P3 S0 e S1 | Executar políticas independente e coordenada no mesmo ambiente, com reservas atômicas e regras de liberação. |
| P4 Campanha inicial | Controlar sementes e ordem das ações; trocar lados; registrar dados de todas as partidas. |
| P5 S2 | Representar papéis e missões com Moise/ORA4MAS, mantendo os critérios de S1 para uma comparação justa. |
| P6 Adendo | Implementar um caso de recuperação, conservar a identidade do recurso e confirmar conclusão por evento do ambiente. Comparar políticas equivalentes. |
| P7 Extensões do enunciado | Experimentar minerais de valores diferentes e múltiplos depósitos em configurações comuns às equipes. |
| P8 Bônus | Avaliar mistura de AOP ou LLM somente com núcleo estável e tempo disponível. |

## Decisões de desenho que devem preceder a campanha

1. Definir quais diferenças do cenário 2006 serão reproduzidas e registrar cada simplificação.
2. Definir a ordem de resolução de movimentos, disputas e depósitos por passo; não favorecer sempre o mesmo identificador.
3. Manter no máximo um portador por recurso e uma identidade nova quando surgir um recurso na mesma célula.
4. Determinar como o ambiente conhece a equipe responsável pela entrega e rejeita eventos duplicados.
5. Tornar explícita a informação permitida aos agentes e aos artefatos de equipe.
6. Confirmar em aula eventual exigência de interoperabilidade entre projetos. O plano atual usa competição local, sem adaptador XML/TCP histórico.

## Relação com trabalhos anteriores

O Contract Net e os leilões oferecem alternativas futuras de alocação, mas a reserva simples vem primeiro. BPMN documenta o processo; Moise explicita compromissos. O artefato do ambiente confirma o resultado físico. Os modelos em `docs/modelos` são propostas de análise; não são componentes executados pelo lançador.
