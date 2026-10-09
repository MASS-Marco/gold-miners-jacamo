"""Prepara e verifica o tutorial local. Usa apenas a biblioteca padrao do Python."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import io
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]

def prepare_search_library():
    """Recupera a dependencia original sem redistribuir seu binario no Git."""
    target = ROOT/'lib/search.jar'
    expected = '290e21c7300c74e16f1eb620f92bbed5c3a87adf2f9e6a5d8f595c0b9ae2b34e'
    if not target.exists():
        url = 'https://raw.githubusercontent.com/jacamo-lang/jacamo/main/doc/tutorials/gold-miners/initial-gold-miners.zip'
        print('Obtendo search.jar do pacote oficial JaCaMo...')
        with urllib.request.urlopen(url,timeout=45) as response: data = response.read()
        if hashlib.sha256(data).hexdigest() != 'b5d2e486645cb48571b30d86a0ffcc343c33a5a797a71dbd32fc025f5af66d7c':
            raise RuntimeError('O pacote oficial mudou. Conferir nova versao antes de atualizar a dependencia.')
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            candidates = [name for name in archive.namelist() if name.endswith('/lib/search.jar') and '__MACOSX' not in name]
            if len(candidates)!=1: raise RuntimeError('search.jar nao localizado de forma univoca no pacote.')
            binary = archive.read(candidates[0])
        if hashlib.sha256(binary).hexdigest()!=expected: raise RuntimeError('Integridade de search.jar divergente.')
        target.parent.mkdir(exist_ok=True)
        target.write_bytes(binary)
    if hashlib.sha256(target.read_bytes()).hexdigest()!=expected:
        raise RuntimeError('search.jar local difere da dependencia verificada.')

def environment():
    env = os.environ.copy()
    local = ROOT.parent / 'JaCaMo/00-ambiente-e-instalacao'
    if (local/'jdk-21/bin/java.exe').exists():
        env['JAVA_HOME'] = str(local/'jdk-21')
        env['GRADLE_USER_HOME'] = str(local/'gradle-user-home')
        env['GRADLE_OPTS'] = '-Duser.home="'+str(local/'perfil-isolado')+'"'
    env.pop('JASON_HOME',None)
    binary = 'java.exe' if os.name=='nt' else 'java'
    candidate = Path(env.get('JAVA_HOME',''))/'bin'/binary
    java = str(candidate) if candidate.is_file() else shutil.which(binary)
    if not java:
        raise RuntimeError('Java 21 nao encontrado. Use o laboratorio JaCaMo ou configure JAVA_HOME para o processo.')
    return java,env

def compile_project():
    prepare_search_library()
    _,env = environment()
    wrapper = ROOT/('gradlew.bat' if os.name=='nt' else 'gradlew')
    command = [str(wrapper),'--no-daemon','--console=plain','classes','testClasses','runtimeClasspath']
    if os.name!='nt': command.insert(0,'sh')
    subprocess.run(command,cwd=ROOT,env=env,check=True,timeout=180)

def folder(kind):
    stamp = datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    path = ROOT/'experimentos/execucoes'/f'{stamp}-{kind}'
    path.mkdir(parents=True)
    return path

def java_command(main,args,test=False,gui=False):
    java,env = environment()
    runtime_home = ROOT/'build/perfil-java'
    runtime_home.mkdir(parents=True,exist_ok=True)
    cpfile = ROOT/'build'/('test-runtime-classpath.txt' if test else 'runtime-classpath.txt')
    if not cpfile.exists(): compile_project()
    command = [java,'-Dfile.encoding=UTF-8','-Dstdout.encoding=UTF-8','-Dstderr.encoding=UTF-8','-Dgoldminers.headless='+str(not gui).lower(),
               '-Duser.home='+str(runtime_home),'-Djava.util.logging.config.file=logging.properties',
               '-Djava.awt.headless='+str(not gui).lower(),'-Dgoldminers.delay=20',
               '-cp',cpfile.read_text(encoding='utf-8'),main,*args]
    return command,env

def run_java(main,args,output,test=False,seconds=45,gui=False):
    command,env = java_command(main,args,test,gui)
    with (output/'stdout.log').open('w',encoding='utf-8') as out, (output/'stderr.log').open('w',encoding='utf-8') as err:
        process = subprocess.Popen(command,cwd=ROOT,env=env,stdout=out,stderr=err,
                                   creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' and not gui else 0)
        expired = False
        try: code = process.wait(timeout=seconds)
        except subprocess.TimeoutExpired:
            expired = True
            process.terminate()
            try: code = process.wait(timeout=8)
            except subprocess.TimeoutExpired:
                process.kill(); code = process.wait(timeout=5)
    return code,expired,(output/'stdout.log').read_text(encoding='utf-8')+(output/'stderr.log').read_text(encoding='utf-8')

def validate():
    compile_project()
    destination = folder('verificacao')
    model = destination/'modelo'; model.mkdir()
    code,expired,text = run_java('mining.ModelChecks',[],model,test=True)
    if code!=0 or expired or 'MODEL_CHECKS|passed=10' not in text:
        raise RuntimeError('Falha no modelo. Veja '+str(model))
    integration = destination/'integracao'; integration.mkdir()
    code,expired,text = run_java('jacamo.infra.JaCaMoLauncher',['configuracoes/verificacao.jcm'],integration,test=True)
    required = ['PERCEPTION|gold=1,1','PICK|carrying=true','WORLD_VERIFIED|deposited=1|carrying=false|conservation=ok','END|status=ok']
    missing = [marker for marker in required if marker not in text]
    if code!=0 or expired or missing or 'GOLD_MINERS|FAIL' in text or re.search(r'Exception|SEVERE|Error parsing|Error creating',text):
        raise RuntimeError('Falha de integracao. Marcadores ausentes: '+str(missing)+'. Veja '+str(integration))
    source_files = sorted(list((ROOT/'src').rglob('*.java'))+list((ROOT/'src').rglob('*.asl'))+[ROOT/'build.gradle',ROOT/'configuracoes/verificacao.jcm',ROOT/'logging.properties',Path(__file__)])
    result = {'data_utc':datetime.now(timezone.utc).isoformat(),'status':'aprovado','verificacoes_modelo':10,
              'integracao':'Jason e CArtAgO executaram percepcao, movimento, coleta e deposito; estado conferido por observador de teste.',
              'limite':'Nao e campeonato, comparacao de estrategias nem implementacao MAPC 2006 completa.',
              'marcadores':required,'fontes_sha256':{str(p.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in source_files}}
    (destination/'resultado.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    evidence = ROOT/'experimentos/evidencias'
    (evidence/'verificacao-inicial.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print('VERIFICACAO_GOLD_MINERS_APROVADA | modelo=10 | integracao=1')
    print(destination)

def execute(args):
    agent = 'miner.asl' if args.modo=='explorar' else 'miner-coleta.asl'
    if args.modo=='coletar' and args.cenario not in (1,2,3):
        raise ValueError('A base de coleta usa deposito 0,0. Use cenarios 1 a 3 antes de adaptar o agente.')
    compile_project()
    destination = folder('tutorial')
    generated = ROOT/'configuracoes/geradas'; generated.mkdir(exist_ok=True)
    jcm = generated/(destination.name+'.jcm')
    agents = ['agent leader']
    for i in range(1,5):
        source = agent if args.modo=='coletar' or i==1 else 'dummy.asl'
        agents.append(f'agent miner{i}: {source} {{\n  focus: mining.m{i}view\n}}')
    artifacts = [f'artifact m{i}view: mining.MiningPlanet({args.cenario},{i-1})' for i in range(1,5)]
    jcm.write_text('mas tutorial_gold_miners {\n'+'\n'.join(agents)+'\nworkspace mining {\n'+'\n'.join(artifacts)+'\n}\n}\n',encoding='utf-8')
    shutil.copy2(jcm,destination/'cenario.jcm')
    code,expired,text = run_java('jacamo.infra.JaCaMoLauncher',[jcm.relative_to(ROOT).as_posix()],destination,seconds=args.segundos,gui=args.interface)
    failures = bool(re.search(r'Exception|SEVERE|parse error|Error parsing|Error creating',text))
    result = {'modo':args.modo,'cenario':args.cenario,'duracao_limite_segundos':args.segundos,
              'encerrado_pelo_limite':expired,'codigo_processo':code,'erro_detectado':failures,
              'observacao':'Sessao de estudo; encerramento por tempo nao significa que todo o ouro foi coletado.'}
    (destination/'sessao.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2)); print(destination)
    if failures or (not expired and code!=0): raise RuntimeError('A sessao apresentou falha. Confira os registros.')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command',required=True)
    sub.add_parser('diagnosticar'); sub.add_parser('compilar'); sub.add_parser('validar')
    p = sub.add_parser('executar')
    p.add_argument('--modo',choices=['explorar','coletar'],default='coletar')
    p.add_argument('--cenario',type=int,choices=range(1,7),default=3)
    p.add_argument('--segundos',type=int,default=15)
    p.add_argument('--interface',action='store_true',help='Abre a visualizacao grafica para estudo interativo.')
    args = parser.parse_args()
    if args.command=='diagnosticar':
        java,env = environment()
        print('Java:',java); print('JaCaMo: 1.3.0 | Gradle: 8.10')
        subprocess.run([java,'-version'],env=env,check=True)
    elif args.command=='compilar': compile_project()
    elif args.command=='validar': validate()
    else:
        if not 1<=args.segundos<=3600: parser.error('Use duracao de 1 a 3600 segundos.')
        execute(args)

if __name__=='__main__': main()
