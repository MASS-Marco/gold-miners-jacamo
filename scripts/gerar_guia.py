"""Gera guia e leitura por linha em HTML/PDF a partir das fontes locais."""
from pathlib import Path
import hashlib
import html
import json
import os
import re
import unicodedata
import mistune
import pymupdf
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from explicar_codigo import ROOT, PURPOSES, annotated, source_files

DEST=ROOT/'guia'
URL='https://github.com/MASS-Marco/gold-miners-jacamo'
MD=mistune.create_markdown(escape=False,plugins=['table'])

def norm(value):
    return re.sub(r'\s+','',unicodedata.normalize('NFKC',value)).replace('\u00ad','').casefold()

def frame(title,content,css,extra=''):
    return f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>{css}</style></head><body><header class="toolbar"><div class="toolbar-inner"><nav><a href="Guia-do-Laboratorio.html">Guia</a><a href="Codigo-Comentado.html">Código por linha</a><a href="{URL}">GitHub</a></nav><div class="controls"><button id="font" type="button" aria-pressed="false">Aumentar fonte</button><button id="print" type="button">Imprimir</button></div></div></header><main>{content}</main><script>document.querySelector('#print').onclick=()=>window.print();document.querySelector('#font').onclick=function(){{const b=this.getAttribute('aria-pressed')!=='true';document.documentElement.style.setProperty('--scale',b?'1.12':'1');this.setAttribute('aria-pressed',String(b));}};{extra}</script></body></html>'''

def main():
    css=(DEST/'estilo.css').read_text(encoding='utf-8')
    raw=(DEST/'Guia-do-Laboratorio.md').read_text(encoding='utf-8')
    parts=re.split(r'(?=^## )',raw,flags=re.M)
    intro=MD(parts[0]);sections=[]
    for i,part in enumerate(parts[1:],1):
        sections.append(f'<section class="sheet" id="parte-{i}">'+(f'<header class="intro">{intro}</header>' if i==1 else '')+MD(part)+'</section>')
    guide=frame('Guia do laboratório Gold Miners',''.join(sections),css)
    (DEST/'Guia-do-Laboratorio.html').write_text(guide,encoding='utf-8')
    report={'data':'2026-10-09','arquivos':[],'pdfs':{}}
    file_sections=[];links=[];active=0;total=0;manifest=[]
    for i,path in enumerate(source_files(),1):
        relative=path.relative_to(ROOT).as_posix();rows=annotated(path);anchor=f'arquivo-{i}'
        links.append(f'<li><a href="#{anchor}">{html.escape(relative)}</a></li>')
        body=[]
        for row in rows:
            total+=1;active+=row['kind']=='code'
            code=html.escape(row['code']);note=html.escape(row['explanation'])
            body.append(f'<tr class="{row["kind"]}" id="{anchor}-L{row["line"]}"><td class="ln"><a href="#{anchor}-L{row["line"]}">{row["line"]}</a></td><td class="source"><code>{code or " "}</code></td><td class="explanation">{note}</td></tr>')
        file_sections.append(f'<section class="sheet code-file" id="{anchor}"><h2>{html.escape(relative)}</h2><p>{PURPOSES.get(path.name,"Configuração de apoio ao laboratório.")}</p><p class="credit"><a href="../{relative}">Abrir arquivo original</a> · {len(rows)} linhas · numeração da cópia documentada</p><table class="code-table"><thead><tr><th>Linha</th><th>Código</th><th>Como ler</th></tr></thead><tbody>'+''.join(body)+'</tbody></table></section>')
        digest=hashlib.sha256(path.read_text(encoding='utf-8').encode()).hexdigest()
        manifest.append({'arquivo':relative,'sha256_texto_lf':digest,'linhas':rows})
        report['arquivos'].append({'arquivo':relative,'linhas':len(rows),'linhas_ativas':sum(r['kind']=='code' for r in rows),'sha256_texto_lf':digest})
    toc='<section class="sheet"><p class="eyebrow">Gold Miners · leitura acompanhada</p><h1>Código explicado linha por linha</h1><p>Use este apêndice como uma conversa ao lado do editor. Comece pelo arquivo que você está estudando, acompanhe o trecho original e leia a explicação na mesma linha.</p><p>As linhas de decisão explicam o comportamento. As de estrutura explicam a sintaxe e a rotina em que aparecem. Os comentários originais preservam os créditos e observações do tutorial; na tela, podem ser mostrados pelo controle abaixo. Na impressão, eles ficam ocultos para concentrar a consulta nas linhas ativas.</p><p>O núcleo documentado inclui agentes, ambiente, ações internas, testes, lançador e configurações. Bibliotecas, Gradle Wrapper, arquivos gerados e geradores editoriais não fazem parte desta leitura por linha.</p><p><a href="Guia-do-Laboratorio.pdf">Guia introdutório em PDF</a> · <a href="Codigo-Comentado.pdf">Este apêndice em PDF</a> · <a href="'+URL+'">Laboratório no GitHub</a></p><div class="filters"><label>Pesquisar código ou explicação <input id="search" type="search" placeholder="Exemplo: carrying_gold"></label><label><input id="comments" type="checkbox"> Mostrar comentários e linhas vazias</label><p id="count" aria-live="polite"></p></div><ol class="file-list">'+''.join(links)+'</ol></section>'
    script="""const all=[...document.querySelectorAll('.code-table tbody tr')];function filter(){const q=document.querySelector('#search').value.toLocaleLowerCase('pt-BR');const origin=document.querySelector('#comments').checked;let n=0;for(const row of all){const visible=(origin||row.classList.contains('code'))&&row.textContent.toLocaleLowerCase('pt-BR').includes(q);row.hidden=!visible;n+=visible;}document.querySelector('#count').textContent=n+' linhas visíveis';}document.querySelector('#search').oninput=filter;document.querySelector('#comments').onchange=filter;filter();"""
    extra_css=''' .filters{background:#eef6f5;padding:14px;border-radius:8px}.filters label{display:block;margin:7px 0}.filters input[type=search]{display:block;width:100%;padding:10px;font:inherit;border:1px solid #a9c4ca;border-radius:5px}.file-list{columns:2;font-size:14px}.code-file h2{overflow-wrap:anywhere;font-size:23px}.code-table{font-size:14px;line-height:1.55}.code-table th:first-child,.code-table td:first-child{width:8%;text-align:right}.code-table th:nth-child(2){width:43%}.code-table td{padding:9px 8px}.code-table code{background:none;padding:0;white-space:pre-wrap;overflow-wrap:anywhere;font-size:12px}.code-table .ln{color:#657e89}.comment,.blank{color:#657e89}.code-table tr[hidden]{display:none}.code-file{scroll-margin-top:130px}@media(max-width:700px){.file-list{columns:1}.code-table thead{display:none}.code-table,.code-table tbody{display:block}.code-table tr{display:grid;grid-template-columns:40px 1fr;border:1px solid #d3e2e6;margin:10px 0}.code-table td:first-child{width:auto;grid-row:1/3;grid-column:1;text-align:left}.code-table td{border:0}.code-table .source{grid-column:2}.code-table .explanation{grid-column:2}.code-table tr[hidden]{display:none}}@media print{.filters{display:none}.file-list{font-size:8pt;line-height:1.35}.file-list li{margin:3px 0}.code-file h2{font-size:15pt}.code-table{font-size:8.5pt;line-height:1.3;break-inside:auto}.code-table code{font-size:7.6pt;line-height:1.3}.code-table td,.code-table th{padding:6px 6px}.code-table tr.code,.code-table tr.code[hidden]{display:table-row!important}.code-table tr.comment,.code-table tr.blank{display:none!important}.code-table tr{break-inside:avoid}}'''
    extra_css+='@media print{.code-file{break-before:auto;padding-top:6mm}.code-file h2{break-after:avoid}.code-table td,.code-table th{padding:5px 6px}}'
    code_html=frame('Código comentado Gold Miners',toc+''.join(file_sections),css+extra_css,script)
    (DEST/'Codigo-Comentado.html').write_text(code_html,encoding='utf-8')
    (DEST/'comentarios-por-linha.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    with sync_playwright() as p:
        browser=p.chromium.launch(channel='msedge' if os.name=='nt' else None,headless=True)
        context=browser.new_context(offline=True,locale='pt-BR')
        for stem,markup in [('Guia-do-Laboratorio',guide),('Codigo-Comentado',code_html)]:
            page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
            page.goto((DEST/(stem+'.html')).as_uri(),wait_until='load')
            widths=[]
            for width in [390,768,1440]:
                page.set_viewport_size({'width':width,'height':1000})
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(stem,width)
                widths.append(width)
            page.locator('#font').click()
            assert page.locator('#font').get_attribute('aria-pressed')=='true'
            page.locator('#font').click()
            if stem=='Codigo-Comentado':
                page.locator('#search').fill('carrying_gold')
                assert page.locator('.code-table tr.code:visible').count()>0
                page.locator('#search').fill('')
                page.locator('#comments').check()
                assert page.locator('.comment:visible').count()>0
                page.locator('#comments').uncheck()
            page.set_viewport_size({'width':1440,'height':1000});page.emulate_media(media='print')
            page.pdf(path=str(DEST/(stem+'.pdf')),format='A4',prefer_css_page_size=True,print_background=True,display_header_footer=True,header_template='<span></span>',footer_template='<div style="width:100%;margin:0 17mm;font:8px Arial;color:#526b78;display:flex;justify-content:space-between"><span>Gold Miners · guia do laboratório · 09/10/2026</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>',tagged=True,outline=True)
            assert not errors,errors
            document=pymupdf.open(DEST/(stem+'.pdf'));whole=norm(' '.join(q.get_text() for q in document))
            soup=BeautifulSoup(markup,'html.parser')
            if stem=='Guia-do-Laboratorio':
                blocks=[t.get_text(' ',strip=True) for t in soup.select('main p,main h1,main h2,main h3,main td,main th,main li')]
            else:
                blocks=[t.get_text(' ',strip=True) for t in soup.select('tr.code .source,tr.code .explanation')]
            missing=[b for b in blocks if norm(b) not in whole]
            assert not missing,(stem,missing[:4])
            for q in document:
                assert all(-1<=w[0]<w[2]<=q.rect.width+1 and -1<=w[1]<w[3]<=q.rect.height+1 for w in q.get_text('words'))
            report['pdfs'][stem]={'paginas':len(document),'blocos_conferidos':len(blocks),'ausentes':missing,'viewports_offline':widths,'erros_javascript':errors}
            document.close();page.close()
        browser.close()
    report['total_linhas']=total;report['linhas_ativas_com_explicacao']=active
    (DEST/'conferencia.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'arquivos':len(manifest),'linhas_ativas':active,'pdfs':report['pdfs']},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
