# Laboratório Gold Miners

Projeto individual de **Marco Aurélio Santos de Souza**, na disciplina de Sistemas Multiagentes com o Prof. Jomi F. Hübner, UFSC, 2026.2.

Preparação inicial em 09/10/2026. O laboratório parte do tutorial oficial JaCaMo e está pronto para estudo e desenvolvimento. A disputa entre duas equipes e as estratégias comparativas ainda não foram implementadas.

[![Abrir no GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/MASS-Marco/gold-miners-jacamo?quickstart=1)

[Código e instruções no GitHub](https://github.com/MASS-Marco/gold-miners-jacamo). O Dev Container segue a configuração dos trabalhos anteriores e oferece Java 21 e Python. A execução desta preparação foi validada localmente em Windows; o contêiner ainda não foi executado. No terminal Linux, usar `python3 scripts/laboratorio.py validar`. Abrir o Codespaces depende de uma conta GitHub e da disponibilidade de uso da conta.

## Começar

Para acompanhar com explicações e pequenos exercícios, abra o [guia do laboratório](guia/Guia-do-Laboratorio.md). Há versões em [HTML](guia/Guia-do-Laboratorio.html) e [PDF](guia/Guia-do-Laboratorio.pdf), além do [código explicado linha por linha](guia/Codigo-Comentado.html) e seu [PDF de consulta](guia/Codigo-Comentado.pdf). Para visualizar HTML baixado do GitHub, use o arquivo local no navegador; o GitHub apresenta seu código-fonte. O PDF abre no próprio repositório.

No terminal desta pasta, em Windows:

```powershell
.\laboratorio.cmd diagnosticar
.\laboratorio.cmd validar
.\laboratorio.cmd executar --modo coletar --cenario 3 --segundos 15
```

O lançador utiliza o Python local de `C:\MestradoUFSC\.venv-documentos`, quando disponível, e o JDK 21 isolado do laboratório JaCaMo. Também pode ser chamado por `python -X utf8 scripts/laboratorio.py validar`. Em outra máquina, preparar Python 3.10 ou superior e Java 21; as dependências Java são obtidas pelo Gradle Wrapper na primeira compilação. A execução foi conferida em Windows, com Python 3.14, Java 21, JaCaMo 1.3.0 e Gradle 8.10.

`validar` verifica dez condições do modelo e uma sequência completa de percepção, movimento, coleta e depósito, com conferência do estado final. O observador de teste acessa o estado do mundo somente para verificar o resultado; ele não decide a estratégia dos mineradores.

`executar` recompila e inicia uma sessão por tempo limitado. O limite encerra o processo iniciado pelo comando; não significa que todo o ouro foi coletado. Para visualizar o mundo, acrescentar `--interface`. A interface foi preservada, mas a verificação desta preparação foi feita sem janela. Para a introdução, usar `--modo explorar --cenario 1`.

## O que está pronto

- Tutorial de exploração e solução oficial inicial de coleta, com créditos e origem preservados.
- Compilação, lançador e perfil Java local; registros por sessão.
- Dez verificações do modelo e uma integração Jason–CArtAgO, aprovadas.
- Sessão de 15 segundos com quatro mineradores, sem erro de execução detectado.
- Controle de versão Git, documentação de diferenças, plano de evolução e protocolo de experimentos ainda planejado.
- Modelo BPMN de análise e contrato proposto de missões, associados ao adendo acadêmico.
- Guia em HTML/PDF, código explicado por linha e exercícios para outros interessados.
- Módulo de eficiência, eficácia e efetividade simulada, com exemplos identificados como didáticos e verificações dos cálculos.

Para estudar os indicadores:

```text
python scripts/indicadores.py experimentos/exemplo-indicadores.json
python scripts/verificar_indicadores.py
```

O módulo calcula indicadores sobre registros de entrada; a instrumentação automática do simulador ainda será desenvolvida. Ele distingue números ilustrativos de registros observados e rejeita pares que divergem nos parâmetros de comparação conferidos. Os critérios e as limitações estão no guia.

As evidências selecionadas estão em [experimentos/evidencias](experimentos/evidencias). O encerramento intencional da sessão por tempo pode produzir código 1 no processo Java em Windows; o comando de estudo distingue esse encerramento de um erro encontrado nos registros.

## Organização

| Caminho | Conteúdo |
|---|---|
| `src/agt` | Agentes AgentSpeak e ações internas Java |
| `src/env/mining` | Artefato, modelo e visualização do ambiente |
| `src/test` | Verificações de regras e agente de integração |
| `configuracoes/verificacao.jcm` | Cenário controlado de verificação |
| `scripts/laboratorio.py` | Compilação e execução controlada |
| `docs` | Origem, alterações, evolução e modelos propostos |
| `experimentos/protocolo.json` | Planejamento da campanha; sem resultados comparativos |
| `experimentos/execucoes` | Registros locais de cada execução; fora do Git |

## Limites que orientam a próxima etapa

O tutorial possui quatro mineradores de um mesmo conjunto, placar global e execução assíncrona. Ainda não representa as duas equipes do MAPC 2006. A ação `jia.get_direction` consulta o mapa global; esse acesso deve ser substituído antes de comparar estratégias sob percepção local. O agente de coleta usa depósito em 0,0, por isso o lançador aceita cenários 1 a 3 nesse modo.

Outras diferenças estão em [alterações e limitações](docs/alteracoes-do-tutorial.md) e no [plano de evolução](docs/plano-de-evolucao.md). O BPMN tem estrutura validada pelos esquemas da OMG e é não executável. Moise/ORA4MAS, eventos de missão e recuperação ainda não estão integrados ao programa.

## Materiais acadêmicos

O enunciado, a proposta em HTML/PDF, quatro cadernos e o adendo permanecem no acervo acadêmico pessoal. Os modelos técnicos propostos no adendo estão em `docs/modelos` para apoiar o desenvolvimento.

Prazos do PDF recebido: proposta **05/11/2026**; apresentação **04/12/2026**; relatório final **11/12/2026**. Laboratório inicial para estudo, com execução individual confirmada; a entrega acadêmica ainda será preparada.

## Fontes e autoria

[Tutorial JaCaMo](https://jacamo-lang.github.io/jacamo/tutorials/gold-miners/readme.html) · [Cenário MAPC 2006](https://multiagentcontest.org/2006/) · [Créditos e componentes](NOTICE.md) · [Manifesto de origem](docs/origem-do-tutorial.json).

O código do tutorial não é apresentado como criação original do estudante. A preparação local acrescenta infraestrutura de execução, verificações, correções delimitadas e um plano de investigação. O Git registra essa base para permitir comparar as próximas alterações.
