# Guia para estudar o laboratório

[Guia introdutório em HTML](Guia-do-Laboratorio.html) · [PDF](Guia-do-Laboratorio.pdf) · [Código explicado por linha](Codigo-Comentado.html) · [PDF de consulta do código](Codigo-Comentado.pdf).

Comece pelo guia curto e escolha um exercício. O apêndice é para consulta por arquivo e linha; não precisa ser lido inteiro em sequência. A busca no HTML filtra tanto o código quanto as explicações.

O apêndice acompanha 25 arquivos do núcleo de execução, incluindo agentes, ações internas, ambiente, visualização, testes, lançador e configurações. Cada linha mantém o número do arquivo. Comentários originais e espaços podem ser exibidos na tela; a impressão concentra as linhas ativas. Bibliotecas, Gradle Wrapper, geradores editoriais e arquivos gerados estão fora desse recorte.

O texto de cada fonte, normalizado para quebras de linha LF, é identificado por SHA-256 em `conferencia.json`. Os comentários também estão em `comentarios-por-linha.json`. As explicações não alteram o código de origem nem constituem verificação formal de todas as situações possíveis.

Para regenerar após mudar o código, instalar as dependências de `requirements.txt` e executar `python scripts/gerar_guia.py` na raiz. Em Windows, o gerador usa Edge instalado. Em Linux, preparar o Chromium do Playwright com `python -m playwright install chromium`. Essas dependências são apenas editoriais; executar o laboratório usa a biblioteca padrão do Python e as dependências Java do projeto.

Eficiência, eficácia e efetividade simulada são explicadas no guia e no módulo `scripts/indicadores.py`. Os exemplos numéricos são identificados como ilustrativos. A campanha competitiva e a coleta automática de métricas ainda serão implementadas.
