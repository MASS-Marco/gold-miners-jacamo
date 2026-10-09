# Alterações e limitações do tutorial

Registro de 09/10/2026. A origem e os hashes dos arquivos recebidos estão em `origem-do-tutorial.json`. O ZIP integral permanece no acervo acadêmico.

## Alterações realizadas

1. Corrigido `dummy.as l` para `dummy.asl` no arquivo inicial `.jcm`.
2. Preparado build com JaCaMo 1.3.0, Java 21 e Gradle 8.10, compatível com o ambiente já usado na disciplina.
3. Adicionada a solução oficial `solutions/miner1.asl` como `miner-coleta.asl`, mantendo créditos. O agente inicial de exploração foi preservado.
4. Acrescentadas propriedades de processo para executar o ambiente sem janela e controlar a espera artificial entre operações.
5. Protegidas as atualizações da visualização quando não há interface gráfica.
6. Corrigida a atualização de `cell`: as percepções anteriores são removidas uma vez antes de reconstruir a vizinhança, em vez de serem removidas repetidamente durante cada célula.
7. Configurado registro no console, com saídas UTF-8 e perfil Java dentro de `build`, para execução controlada no Windows.
8. Criados lançador, configuração e verificações de modelo e integração. Sessões têm prazo máximo, configuração preservada e saídas próprias.

Foram trazidos do ZIP somente os arquivos necessários à base de estudo. Caches, arquivos de macOS, documentação duplicada e exemplos de postagem em serviços externos não integram este laboratório.

## Verificação realizada

Dez verificações do modelo cobrem obstáculo, ocupação, coleta, remoção do recurso, capacidade unitária, devolução fora do depósito, nova coleta, depósito, tentativa vazia e conservação. A integração executa um percurso concreto e confere o estado do mundo. Uma sessão de 15 segundos com quatro mineradores foi executada sem erro detectado.

Esses testes não demonstram correção para todas as sequências concorrentes. Uma campanha de competição exigirá outras propriedades e testes específicos.

## Diferenças ainda abertas

- O mundo contém um total global de ouro depositado; não há separação em duas equipes.
- A execução não possui uma barreira de passos comum aos agentes. A espera artificial não é um protocolo de turnos.
- `jia.get_direction` acessa `WorldModel.get()` e consulta o mapa global. A política deve passar a usar conhecimento permitido antes da comparação MAPC.
- O agente de coleta referencia o depósito 0,0 diretamente; o lançador limita esse modo aos cenários 1–3.
- Marcas, geração de ouro, distorção da percepção, falhas aleatórias e regras completas de uso do depósito do cenário de 2006 não estão implementadas.
- Os recursos são representados por presença/ausência na célula. A tentativa de devolver uma carga sobre ouro já existente precisa de regra e teste de conservação, antes de qualquer adaptação competitiva.
- A inicialização compartilha estado estático entre artefatos; deve ser centralizada na nova arquitetura de partidas. Não está preparada para duas partidas simultâneas na mesma JVM.
- Reservas, identificadores de missão, organização Moise e política de recuperação constam somente do desenho proposto.

## Leitura de um aviso conhecido

O Jason pode anunciar que os caminhos do JAR na configuração e no classpath diferem por representação de caminho do Windows. O perfil é local e a biblioteca carregada é a versão resolvida pelo build. As verificações conferem a execução efetiva; não foi alterada configuração global para ocultar o aviso.
