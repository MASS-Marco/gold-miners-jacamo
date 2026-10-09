"""Explicacoes de leitura para o nucleo do laboratorio, sem modificar suas fontes."""
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]

PURPOSES={
 'miner.asl':'Explora o mapa e escolhe destinos. Comece pelos planos de free, near e next_step; esta versão não faz a entrega de ouro.',
 'miner-coleta.asl':'Acrescenta memória das descobertas, escolha de alvo, coleta e depósito. O depósito 0,0 e a consulta global de caminhos ainda são limitações do exemplo.',
 'dummy.asl':'Mantém um participante sem estratégia ativa de mineração. Ajuda a estudar um minerador de cada vez.',
 'leader.asl':'Mantém um placar baseado em mensagens dropped. Os mineradores desta versão ainda não enviam essas mensagens; o total do ambiente é uma informação diferente.',
 'MiningPlanet.java':'Liga ações dos agentes ao mundo por CArtAgO. Expõe posição, carga e células percebidas; não é ainda um coordenador de duas equipes.',
 'WorldModel.java':'Guarda o estado do mundo e aplica movimento, coleta e depósito. A segunda metade constrói seis mapas por coordenadas; cada posição faz parte da instância.',
 'WorldView.java':'Desenha o mapa e oferece controles visuais. A interface foi preservada, mas as verificações registradas usaram execução sem janela.',
 'get_direction.java':'Usa A* para escolher um primeiro movimento. Consulta o modelo global; esse acesso deverá mudar para uma competição com informação local.',
 'random.java':'Gera números aleatórios como ação interna Jason. O limite de nextInt é exclusivo; isso deve ser considerado ao passar dimensões do mapa.',
 'random_direction.java':'Alternativa antiga não usada pelos mineradores executados. As coordenadas candidatas começam em -1 e não são reinicializadas por tentativa; revisar antes de usar.',
 'dist.java':'Converte coordenadas do AgentSpeak e devolve a distância calculada por Location. Distância geométrica não demonstra que exista caminho livre.',
 'neighbour.java':'Verifica proximidade usando a classe Location e devolve verdadeiro ou falso para o contexto do plano.',
 'ModelChecks.java':'Verifica situações pequenas do modelo, como ocupação, capacidade, devolução e conservação. Falhas levantam um erro, em vez de apenas imprimir uma mensagem.',
 'ValidationProbe.java':'Observador usado somente no teste. Confere o estado real após a entrega, sem orientar a escolha de ações dos mineradores.',
 'verificacao.asl':'Percorre uma coleta conhecida. Espera perceber cada efeito antes de avançar e pede uma conferência independente ao final.',
 'laboratorio.py':'Prepara dependências, usa o Java adequado, compila e controla processos com prazo máximo. Distingue estudo, verificação e futura competição.',
 'indicadores.py':'Calcula eficiência, eficácia e diferença de resultado útil a partir de registros informados. Conserva a identificação de números ilustrativos.',
 'verificar_indicadores.py':'Verifica fórmulas e entradas problemáticas. Inclui zero ações, prazo excedido, números inválidos e pares não comparáveis.',
 'build.gradle':'Declara ferramentas, dependências, pastas de código e tarefas Java. O lançador obtém search.jar antes de chamar o Gradle.',
 'settings.gradle':'Define o nome do projeto usado pelo Gradle.',
 'gold_miners.jcm':'Cria o conjunto inicial: líder, um minerador e três agentes inativos, cada minerador com seu artefato de percepção.',
 'verificacao.jcm':'Cria um agente e dois artefatos para conferir uma única entrega. Não configura uma partida competitiva.',
 'laboratorio.cmd':'Atalho Windows. Entra na pasta correta, escolhe o Python local quando disponível e repassa os argumentos.',
 'devcontainer.json':'Prepara Java e Python para um ambiente de desenvolvimento. A configuração foi incluída, mas o contêiner ainda não foi executado.',
 'logging.properties':'Direciona os registros ao console. O lançador guarda as saídas em arquivos específicos de cada sessão.'
}

METHODS={
 'environment':'selecionar o Java e as variáveis somente para o processo do laboratório',
 'prepare_search_library':'obter a biblioteca do tutorial e conferir sua integridade',
 'compile_project':'compilar as fontes e registrar o classpath',
 'folder':'criar uma pasta exclusiva para os registros da execução',
 'java_command':'montar os argumentos Java e o perfil local de execução',
 'run_java':'iniciar o processo e encerrá-lo ao alcançar o limite de tempo',
 'validate':'conferir o modelo e uma entrega, preservando evidências',
 'execute':'gerar a configuração de uma sessão de estudo e acompanhar sua saída',
 'main':'interpretar o comando informado e encaminhá-lo à operação correspondente',
 'numero':'rejeitar valores que não servem como medidas não negativas',
 'avaliar':'calcular os indicadores de uma equipe em um registro',
 'comparar':'conferir os pares e calcular diferenças entre referência e candidata',
 'move':'tentar mudar a posição conforme a direção e a ocupação da célula',
 'pick':'retirar ouro do mapa e registrar a carga quando as condições permitem',
 'drop':'devolver a carga ao mapa ou contabilizar sua entrega no depósito',
 'initWorld':'escolher o cenário e preparar as propriedades percebidas',
 'updateAgPercept':'atualizar as informações observáveis do minerador',
 'updateAgPerceptCell':'expor o conteúdo de uma célula da vizinhança',
 'create':'criar a instância compartilhada do modelo quando ela ainda não existe',
 'get':'fornecer acesso à instância compartilhada do modelo',
 'destroy':'liberar a referência estática ao modelo',
 'getDepot':'consultar a posição do depósito',
 'getGoldsInDepot':'consultar o total de entregas contabilizado pelo mundo',
 'getInitialNbGolds':'consultar a quantidade inicial registrada para o cenário',
 'isCarryingGold':'verificar se o identificador está no conjunto de portadores',
 'isAllGoldsCollected':'comparar o total depositado com a quantidade inicial registrada',
 'setDepot':'definir a célula que representa o depósito',
 'setAgCarryingGold':'incluir o agente no conjunto de portadores',
 'setAgNotCarryingGold':'retirar o agente do conjunto de portadores',
 'setInitialNbGolds':'registrar o total inicial usado nas conferências',
 'setId':'atribuir um nome ao cenário',
 'getId':'consultar o nome do cenário',
 'init':'inicializar o artefato com os parâmetros do projeto',
 'validateDelivery':'conferir depósito, carga e conservação após o percurso de teste',
 'check':'interromper a verificação quando uma condição esperada não é satisfeita',
 'custo':'informar o custo de uma transição na busca',
 'ehMeta':'verificar se a posição do estado coincide com o destino',
 'h':'estimar a distância restante até o destino',
 'sucessores':'construir estados candidatos para os quatro movimentos',
 'suc':'adicionar um sucessor quando a regra de ocupação permite',
 'equals':'comparar estados pela posição representada',
 'hashCode':'produzir o código de dispersão compatível com a posição',
 'toString':'produzir uma representação textual do objeto',
 'initComponents':'montar painéis, rótulos, controle de velocidade e eventos da interface',
 'udpateCollectedGolds':'atualizar o rótulo visual com o total depositado e o total inicial',
 'draw':'escolher como desenhar cada tipo de objeto',
 'drawAgent':'desenhar o agente com indicação visual de carga',
 'drawDepot':'desenhar o depósito na célula correspondente',
 'drawGold':'desenhar o símbolo do ouro',
 'drawEnemy':'desenhar o símbolo de outro agente segundo a convenção visual',
 'mouseClicked':'transformar um clique no mapa em inclusão de ouro para estudo',
 'mouseMoved':'mostrar a célula sobre a qual o cursor está',
 'stateChanged':'aplicar a velocidade escolhida no controle visual',
 'next':'produzir um novo resultado aleatório com uma cópia do unificador',
 'hasNext':'verificar se ainda pode ser produzido outro resultado',
 'setEnv':'associar a visualização ao artefato do ambiente',
 'setSleep':'alterar a espera artificial entre operações',
 'getSimId':'consultar o identificador do cenário',
 'endSimulation':'sinalizar o fim e liberar o modelo',
 'up':'solicitar o movimento para cima','down':'solicitar o movimento para baixo',
 'left':'solicitar o movimento para a esquerda','right':'solicitar o movimento para a direita',
 'skip':'aguardar sem deslocar e atualizar a percepção',
 'getDescricao':'fornecer a descrição textual do problema de busca'
}

GOALS={
 'near':'chegar à vizinhança do destino ou tratar uma rota não encontrada',
 'go_near':'iniciar a exploração em direção a um destino escolhido',
 'next_step':'escolher e executar um único movimento',
 'pos':'chegar exatamente à posição informada',
 'init_handle':'preparar a intenção de coleta e abandonar a exploração incompatível',
 'handle':'acompanhar o ciclo de coleta e depósito do alvo',
 'ensure':'executar a operação de coleta ou depósito e conferir sua condição',
 'choose_gold':'escolher outro ouro conhecido ou voltar à exploração',
 'calc_gold_distance':'montar a lista de distâncias dos alvos conhecidos',
 'verificar':'percorrer e conferir a entrega do teste',
 'posicao':'esperar que a posição pretendida apareça na percepção',
 'com_carga':'esperar a confirmação da carga','sem_carga':'esperar a confirmação de carga vazia'
}

EXACT={
 'WorldModel model = WorldModel.get();':'Obtém o mundo compartilhado. Numa política competitiva, esse acesso global precisa ser substituído por conhecimento permitido.',
 'goldsInDepot++;':'Conta mais uma unidade entregue. O tutorial ainda mantém esse contador global, sem separação por equipe.',
 'return true;':'Devolve verdadeiro à chamada que está sendo atendida; seu significado depende do método.',
 'return false;':'Devolve falso para indicar que a condição ou tentativa não foi satisfeita.',
 'free.':'Crença inicial de disponibilidade para explorar ou assumir uma coleta.',
 'last_dir(null).':'Crença inicial: ainda não há uma última direção executada.',
 '+cell(X,Y,gold) <- +gold(X,Y).':'Transforma a percepção de ouro em memória própria. Assim a descoberta não some apenas por sair do campo de visão, mas pode ficar desatualizada.',
 '-free;':'Retira a crença de disponibilidade enquanto o agente trata a coleta.',
 '?carrying_gold;':'Confere a crença de carga após a coleta. Se ela não puder ser satisfeita, o plano falha.',
 '!pos(0,0);':'Solicita retorno ao depósito fixo em 0,0. Este é um dos pontos a generalizar para outros cenários.',
 'D.':'Executa como ação a direção que foi unificada com a variável D.',
 'return 1;':'Atribui custo unitário ao estado/transição usado pela busca do exemplo.',
 'return pos.distance(to);':'Usa a distância de Location como estimativa. Ela não incorpora, por si só, todos os desvios por obstáculos.',
 'return pos.equals(to);':'Reconhece a meta quando a posição coincide com o destino.',
 'return pos.hashCode();':'Usa a posição para organizar estados em estruturas de busca que dependem de hash.',
 'return agWithGold.contains(ag);':'Consulta se o agente aparece no conjunto de quem carrega ouro.',
 'return goldsInDepot == initialNbGolds;':'Compara o total depositado com a quantidade inicial registrada. A interpretação muda se houver geração dinâmica de recursos.',
 'model = null;':'Remove a referência compartilhada. Isso permite criar outro mundo numa inicialização posterior.',
 'agWithGold = new HashSet<Integer>();':'Cria um conjunto sem identificadores repetidos para registrar quem carrega ouro.',
 'data[x][y] = DEPOT;':'Marca a célula como depósito, substituindo seu conteúdo representado neste vetor.',
 'setAgCarryingGold(ag);':'Registra que o agente passou a carregar a peça retirada do mapa.',
 'setAgNotCarryingGold(ag);':'Registra que o agente deixou de carregar ouro após a operação.',
 'agWithGold.add(ag);':'Inclui o identificador do agente no conjunto de portadores.',
 'agWithGold.remove(ag);':'Retira o identificador do conjunto de portadores.',
 'break;':'Encerra este ramo do switch; evita continuar pelo caso seguinte.',
 'try {':'Abre um trecho cujo erro será tratado pelos blocos catch seguintes.',
 '@Override':'Indica que o método redefine um comportamento previsto na classe ou interface de origem.',
 'pass':'Neste ramo Python não é necessário fazer outra operação; a exceção esperada já foi reconhecida.',
 '@echo off':'Evita repetir cada comando do atalho Windows na tela.',
 'setlocal':'Mantém as variáveis do atalho restritas a esta execução.',
 'exit /b %errorlevel%':'Devolve ao terminal o código de encerramento do comando executado.',
 'cd /d "%~dp0"':'Entra na pasta do próprio atalho, inclusive quando ela está em outra unidade.',
 "env.pop('JASON_HOME',None)":"Retira JASON_HOME da cópia das variáveis do processo para evitar seleção de uma instalação externa.",
 "expired = False":"Começa assumindo que o processo ainda não atingiu o limite de tempo.",
 "expired = True":"Registra que o encerramento foi provocado pelo prazo máximo da sessão.",
 'process.terminate()':'Pede o encerramento apenas do processo Java iniciado por esta chamada.',
 'process.kill(); code = process.wait(timeout=5)':'Força o fim do processo iniciado se ele não terminar e recolhe seu código de saída.',
 'model.pick(agId);':'Pede ao modelo a coleta para este agente. A atualização posterior da percepção informa o efeito.',
 'model.drop(agId);':'Pede ao modelo a devolução ou depósito da carga, conforme a posição.',
 'model.move(m, agId);':'Pede o movimento ao modelo. A posição percebida depois informa se houve deslocamento.',
 'while(hasObsProperty("cell")) removeObsProperty("cell");':'Retira as células percebidas anteriormente antes de reconstruir a vizinhança. Isso evita manter dados locais antigos.'
}

def purpose(path,name):
    if path.suffix=='.java' and name=='execute':return 'executar a ação interna '+path.stem+' e devolver seu resultado ao Jason'
    if path.suffix=='.java' and name=='main':return 'executar a sequência de verificações do modelo'
    return METHODS.get(name,name or 'preparação deste arquivo')

def explain(path,line,context):
    s=line.strip()
    if s in EXACT:
        if s=='return true;' and path.name=='WorldModel.java' and context=='move':
            return 'O método retorna verdadeiro mesmo se a célula estava bloqueada. Por isso o teste confere a posição, não apenas esse retorno.'
        return EXACT[s]
    if re.fullmatch(r'[{}\[\]();,]+',s):return 'Fecha ou delimita o bloco/estrutura iniciado nas linhas anteriores.'
    if s.startswith('package '):return 'Agrupa a classe no pacote '+s[8:].rstrip(';')+', usado para localizá-la no projeto.'
    if s.startswith(('import ','from ')):return 'Traz o recurso indicado para este arquivo; ele será usado pelas operações abaixo.'
    if s.startswith('def '):
        name=re.findall(r'def (\w+)',s)[0]
        return 'Define a função para '+METHODS.get(name,'organizar esta etapa de execução')+'. Os parâmetros são os dados que a chamada recebe.'
    if 'class ' in s and not s.startswith('mainClass'):
        return 'Define uma classe e, quando indicado por extends ou implements, relaciona seu comportamento à base ou às interfaces utilizadas.'
    if re.match(r'(public|private|protected|static|synchronized|boolean|void|int) ',s) and '(' in s and s.endswith('{') and '=' not in s:
        names=re.findall(r'(\w+)\s*\(',s)
        name=names[-1] if names else context
        description='preparar o cenário '+name[-1] if re.fullmatch(r'world\d',name) else purpose(path,name)
        return 'Inicia o método para '+description+'.'
    if s.startswith('@OPERATION'):return 'Expõe uma operação do artefato aos agentes; as condições e o efeito ficam no corpo indicado.'
    if s.startswith('@'):return 'Identifica ou configura o plano/método. Em planos atomic, a atomicidade é local ao agente, sem garantir exclusão entre mineradores.'
    if s.startswith(('+!','-!')):
        name=re.findall(r'[-+]!(\w+)',s)[0]
        return ('Trata a falha do objetivo de ' if s.startswith('-!') else 'Oferece um plano para ')+GOALS.get(name,name)+('. O trecho após os dois-pontos é o contexto de seleção.' if ':' in s else '.')
    if path.suffix=='.asl':
        a=s.removeprefix('<-').strip()
        if '.print(' in a:return 'Registra uma mensagem para acompanhar a execução. Leia-a junto às percepções e ao estado do mundo para entender o que foi confirmado.'
        if a.startswith(':'):return 'Exige este contexto para selecionar o plano; & combina condições e not consulta a ausência de uma solução na base de crenças.'
        if a.startswith('!!'):return 'Inicia o objetivo indicado numa intenção separada, permitindo sair da preparação atômica da coleta.'
        if a.startswith('!'):
            name=re.findall(r'!(\w+)',a)[0]
            return 'Solicita o subobjetivo de '+GOALS.get(name,name)+'. O ponto e vírgula liga a próxima etapa do corpo.'
        if a.startswith('?'):return 'Consulta a base de crenças e exige que a condição indicada seja satisfeita para continuar.'
        if '.drop_desire' in a:return 'Abandona o objetivo indicado e suas intenções, abrindo espaço para a tarefa de coleta.'
        if '.drop_all_desires' in a:return 'Abandona os objetivos ativos ao receber o encerramento da simulação.'
        if '.abolish(' in a:return 'Remove as crenças que correspondem ao padrão, inclusive quando possuem anotações de origem.'
        if '.findall(' in a:return 'Reúne todos os alvos conhecidos que satisfazem a consulta numa lista para comparação.'
        if '.min(' in a:return 'Seleciona o menor termo da lista ordenável de distâncias, obtendo o próximo alvo.'
        if '.length(' in a:return 'Obtém o tamanho da lista e verifica se há candidatos antes de selecionar um alvo.'
        if '.wait(' in a:return 'Espera o intervalo indicado antes de repetir a observação. A espera evita uma repetição imediata sem novas percepções.'
        if '.stopMAS' in a:return 'Encerra o sistema do teste após registrar o resultado.'
        if 'jia.get_direction' in a:return 'Pede à ação interna uma direção para o alvo. A implementação usa busca A* e ainda consulta o mapa global.'
        if 'jia.dist(' in a:return 'Calcula a distância entre as coordenadas para comparar os alvos conhecidos.'
        if a.startswith('-+'):return 'Substitui a crença indicada por seu novo valor, gerando o evento correspondente à atualização.'
        if a.startswith('-'):return 'Retira a crença indicada, porque ela deixou de representar a situação que o agente quer manter.'
        if a.startswith('+'):return 'Adiciona uma crença ou define reação à sua chegada. O contexto e o corpo, quando presentes, determinam o comportamento.'
        if 'include(' in a:return 'Inclui os planos comuns de integração Jason–CArtAgO fornecidos pelo JaCaMo.'
        if a.rstrip(';.') in ('up','down','left','right','pick','drop','validateDelivery'):
            return 'Solicita a operação '+a.rstrip(';.')+' ao artefato em foco. Os efeitos serão observados pelo agente.'
        if a.startswith('score('):return 'Inicializa o placar que o líder manterá a partir das mensagens recebidas; ainda não é o placar global do ambiente.'
        return 'Compõe o plano ou a crença deste trecho de AgentSpeak. Leia em conjunto com o evento acima e a condição que permite adotá-lo.'
    coord=re.search(r'\.add\(WorldModel\.(GOLD|OBSTACLE),\s*([^,]+),\s*([^\)]+)\)',s)
    if coord:return 'Coloca '+('ouro' if coord[1]=='GOLD' else 'um obstáculo')+' na célula de coordenadas '+coord[2].strip()+', '+coord[3].strip()+'. Esta linha define parte do mapa do cenário.'
    if '.setAgPos(' in s:return 'Define a posição do agente indicado. Nos cenários, os identificadores começam em zero; durante movimentos, a alteração ocorre após testar a célula.'
    if '.setDepot(' in s:return 'Define as coordenadas do depósito deste cenário.'
    if 'WorldModel.create(' in s:return 'Cria o mundo com largura, altura e quantidade de agentes indicadas nos argumentos.'
    if '.setId(' in s:return 'Atribui um nome ao cenário para identificá-lo nos registros e na interface.'
    if '.setInitialNbGolds(' in s:return 'Registra a quantidade de recursos usada como referência; na interface, o valor também pode ser atualizado após um clique.'
    if 'defineObsProperty(' in s:return 'Cria uma propriedade observável do artefato. Os agentes em foco recebem a informação correspondente pela integração com Jason.'
    if 'removeObsProperty' in s:return 'Retira uma propriedade observável que deixou de representar a percepção atual.'
    if 'getObsProperty(' in s:return 'Obtém a propriedade observável existente para atualizá-la ou consultá-la.'
    if '.updateValue(' in s:return 'Atualiza um argumento da propriedade observável; o primeiro número identifica a posição desse argumento.'
    if 'updateAgPercept' in s:return 'Atualiza a percepção do agente ou de uma célula da sua vizinhança após observar o mundo.'
    if 'view != null' in s:return 'Só atualiza a janela se ela foi criada; isso permite executar o laboratório sem interface gráfica.'
    if 'await_time(' in s:return 'Aplica a espera artificial configurada entre ações; isso não constitui um protocolo de turnos entre equipes.'
    if 'System.out.print' in s or 'print(' in s or 'logger.' in s:return 'Escreve uma informação no registro de execução. No teste, os marcadores são lidos pelo lançador para conferir o percurso.'
    if 'throw ' in s or s.startswith('raise '):return 'Interrompe este caminho com um erro explícito, evitando apresentar a condição inválida como sucesso.'
    if s.startswith(('assert ','check(')):return 'Exige que a condição descrita na expressão seja verdadeira. A falha interrompe a verificação e indica o que precisa ser revisto.'
    if s.startswith(('if ','if(', 'if (','elif ')):return 'Só executa este ramo se a condição indicada for satisfeita. O contexto desta rotina é '+purpose(path,context)+'.'
    if s.startswith(('else','} else')):return 'Trata a alternativa em que a condição anterior não foi satisfeita.'
    if s.startswith(('catch','} catch','except ')):return 'Trata o erro indicado. O corpo abaixo define se ele será registrado, convertido em falha ou propagado.'
    if s.startswith(('while ','while(', 'while (')):return 'Repete o trecho enquanto a condição continuar verdadeira. Observe o que muda a cada repetição para entender quando ela termina.'
    if s.startswith(('for ','for(', 'for (')):return 'Percorre os elementos ou índices indicados, repetindo as operações do corpo para cada um.'
    if s.startswith(('switch ','switch(')):return 'Escolhe um ramo de execução de acordo com o valor indicado.'
    if s.startswith('case '):return 'Trata especificamente este valor da seleção. O break, quando presente, encerra o ramo.'
    if s.startswith('default:'):return 'Trata valores que não coincidiram com os casos anteriores.'
    if s.startswith('return '):return 'Entrega este resultado a quem chamou a rotina de '+purpose(path,context)+'.'
    if 'unifies(' in s:return 'Unifica o resultado Java com o argumento AgentSpeak, preenchendo a variável de saída quando houver correspondência.'
    if '.solve()' in s:return 'Avalia o termo numérico recebido do agente e o converte para o tipo Java usado no cálculo.'
    if 'searchAlg.busca' in s:return 'Executa a busca a partir da posição atual até o destino representado pelo estado inicial.'
    if 'new AEstrela' in s:return 'Escolhe A* como algoritmo de busca para calcular a direção do próximo movimento.'
    if 'root.getPai' in s:return 'Volta ao estado pai para percorrer a solução da busca em direção à sua origem.'
    if 'root.getEstado' in s:return 'Obtém o estado deste nó do caminho encontrado pela busca.'
    if 'new GridState' in s:return 'Constrói um estado da busca com posição, origem, destino, modelo e ação associada.'
    if '.getAgPos(' in s:return 'Consulta a posição do agente no modelo do mundo.'
    if 'remove(WorldModel.GOLD' in s:return 'Retira o ouro da célula ao efetivar a coleta.'
    if 'add(WorldModel.GOLD' in s:return 'Devolve ouro à célula atual. A regra para uma célula que já contém ouro ainda precisa de revisão antes da competição.'
    if s.startswith('suc('):return 'Propõe um dos movimentos vizinhos para a busca; a rotina suc decide se o estado pode entrar na lista.'
    if 'rnd.nextInt' in s or 'random.nextInt' in s:return 'Sorteia um inteiro abaixo do limite informado. O valor do limite não é incluído no sorteio.'
    if 'subprocess.' in s:return 'Executa ou configura um processo externo. Os argumentos, ambiente, captura de saída e prazo aparecem nesta chamada.'
    if 'hashlib.sha256' in s:return 'Calcula o resumo SHA-256 para identificar exatamente os bytes verificados, sem interpretar o conteúdo como código.'
    if 'json.loads' in s:return 'Lê a estrutura JSON de entrada para trabalhar com os seus campos.'
    if 'json.dumps' in s:return 'Converte a estrutura de dados para JSON legível, preservando a identificação da origem dos números.'
    if '.write_text(' in s or '.write_bytes(' in s:return 'Grava o conteúdo no arquivo indicado. O caminho e a codificação definem onde o registro ficará disponível.'
    if '.read_text(' in s or '.read_bytes(' in s:return 'Lê o conteúdo do arquivo indicado para conferir, calcular ou preparar a próxima etapa.'
    if '.mkdir(' in s:return 'Cria a pasta de trabalho ou de registros antes de gravar os arquivos.'
    if '.copy2(' in s:return 'Preserva uma cópia do arquivo indicado, vinculando a configuração à execução.'
    if s.startswith('with '):return 'Abre um recurso dentro de um bloco que cuida de fechá-lo ao terminar, inclusive se houver erro.'
    if 'argparse.' in s or '.add_argument(' in s or '.add_parser(' in s:return 'Define um comando ou uma opção do terminal, com tipo, padrão ou valores aceitos.'
    if '.parse_args(' in s:return 'Lê os argumentos do terminal conforme as opções declaradas acima.'
    if path.name=='build.gradle':
        if 'implementation' in s:return 'Adiciona a dependência indicada ao programa Java. A biblioteca local é obtida pelo lançador antes da compilação.'
        if 'srcDirs' in s:return 'Informa em quais pastas o Gradle deve procurar as fontes desta parte do projeto.'
        if 'dependsOn' in s:return 'Exige que a tarefa indicada termine antes de executar esta etapa.'
        if 'systemProperty' in s:return 'Passa uma propriedade ao processo Java para configurar codificação ou visualização.'
        return 'Configura esta propriedade ou tarefa do Gradle: '+s.rstrip('{').strip()+'.'
    if path.suffix=='.jcm':
        if s.startswith('agent '):return 'Cria o agente indicado e associa seu programa AgentSpeak, quando especificado.'
        if s.startswith('artifact '):return 'Cria o artefato da classe indicada. Os parâmetros selecionam cenário e identificador do minerador quando usados por MiningPlanet.'
        if s.startswith('focus:'):return 'Coloca o agente em foco nos artefatos listados para perceber propriedades e executar operações.'
        if s.startswith('workspace '):return 'Abre o espaço de trabalho que reúne os artefatos do ambiente.'
        return 'Declara ou delimita a configuração inicial do sistema multiagente.'
    if path.name=='logging.properties':return 'Configura o registro Java. Linhas sem # são propriedades ativas; os nomes identificam manipulador, formato ou nível.'
    if path.name=='devcontainer.json':return 'Define a opção do contêiner indicada pela chave: nome, imagem, recurso Python, comando de preparação ou usuário de desenvolvimento.'
    if path.suffix=='.cmd':return 'Escolhe o interpretador Python e repassa os argumentos do usuário; o atalho termina com o código devolvido pela execução.'
    if path.name=='WorldView.java':return 'Configura ou desenha um elemento da interface nesta rotina de '+METHODS.get(context,context or 'visualização')+'. A lógica do mundo permanece no modelo.'
    if '=' in s:
        left=s.split('=',1)[0].strip().rstrip(':')
        return 'Define ou atualiza '+left+' com a expressão à direita. Essa informação participa da rotina de '+purpose(path,context)+'.'
    if s.endswith(';') or '(' in s:return 'Executa a chamada indicada como parte da rotina de '+purpose(path,context)+'. Seus argumentos indicam os dados usados nesta etapa.'
    if s.endswith((':',',')):return 'Continua a estrutura de dados ou de parâmetros iniciada acima; o significado do valor é dado pela chave correspondente.'
    return 'Continuação da expressão ou estrutura iniciada acima. Leia-a junto à linha anterior para acompanhar a operação completa.'

def annotated(path):
    rows=[];block=False;context='';python_doc=False
    for n,line in enumerate(path.read_text(encoding='utf-8').splitlines(),1):
        s=line.strip();kind='code'
        if not s:kind='blank'
        elif block:
            kind='comment'
            if '*/' in s:block=False
        elif s.startswith('/*'):
            kind='comment';block='*/' not in s
        elif s.startswith(('//','#','rem ')) or s.startswith('"""'):
            kind='comment'
        if kind=='code':
            if s.startswith('def '):context=re.findall(r'def (\w+)',s)[0]
            elif path.suffix=='.java' and '(' in s and s.endswith('{') and '=' not in s and re.match(r'(public|private|protected|static|synchronized|boolean|void|int)\b',s):
                names=re.findall(r'(\w+)\s*\(',s)
                if names:context=names[-1]
            text=explain(path,line,context)
        elif kind=='blank':text='Espaço para separar visualmente as etapas.'
        else:text='Comentário original ou documentação; não executa uma ação. A explicação do comportamento está nas linhas ativas correspondentes.'
        rows.append({'line':n,'code':line,'explanation':text,'kind':kind})
    return rows

def source_files():
    sources=sorted((ROOT/'src').rglob('*.asl'))+sorted((ROOT/'src').rglob('*.java'))
    sources += [ROOT/p for p in ['scripts/laboratorio.py','scripts/indicadores.py','scripts/verificar_indicadores.py','build.gradle','settings.gradle','gold_miners.jcm','configuracoes/verificacao.jcm','laboratorio.cmd','.devcontainer/devcontainer.json','logging.properties']]
    return sources
