"""Kit Web: acha, no catálogo, bibliotecas, referências e ferramentas para projetos web, e guia a escolha por etapa e seção.

Uso (Python 3.9+, só biblioteca padrão; funciona em qualquer IA ou terminal):
  python kitweb.py briefing projeto.json [--trilha site|software]   cria o briefing da trilha
  python kitweb.py entrevista --briefing projeto.json              o que falta perguntar
  python kitweb.py ux [--trilha site|software]                     fundamentos de UX/UI (o piso de todo projeto)
  python kitweb.py recriar ID                                      componente pago: só referência, recriar limpo
  python kitweb.py guia --briefing projeto.json [--secao hero]     roteiro da trilha, ou atalhos de uma seção
  python kitweb.py buscar fundo animado [--stack vue] [--categoria componentes] [--gratis] [--n 8]
  python kitweb.py listar [--categoria referencia]
  python kitweb.py ver reactbits
  python kitweb.py categorias | secoes
  python kitweb.py adicionar --id x --nome X --url https://... --categoria componentes [--stack react,tailwind]
                   [--acesso gratis] [--licenca MIT] [--tags hero,cards] [--resumo "..."] [--cuidado "..."]
  python kitweb.py checar          confere se cada URL ainda responde
  python kitweb.py teste           autoteste do catálogo e da busca
Qualquer comando de leitura aceita --json (saída para outra IA).
Palavras: site, landing page, sistema, painel, app, software, projeto web, componentes, biblioteca de UI, animação, referência de design, shader.
"""
import argparse
import json
import re
import sys
import unicodedata
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

CATALOGO = Path(__file__).resolve().parent / "catalogo.json"
ACESSOS = {"gratis", "gratis+pro", "freemium", "pago", "conferir"}
ORDEM_ACESSO = {"gratis": 0, "gratis+pro": 1, "freemium": 2, "conferir": 3, "pago": 4}


def carregar():
    return json.loads(CATALOGO.read_text(encoding="utf-8"))


def salvar(dados):
    CATALOGO.write_text(json.dumps(dados, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def plano(texto):
    return "".join(c for c in unicodedata.normalize("NFD", str(texto).casefold()) if unicodedata.category(c) != "Mn")


def termos(texto):
    return [t for t in re.findall(r"[a-z0-9+.-]+", plano(texto)) if len(t) >= 2]


FRAMEWORKS = {"react", "vue", "svelte", "next", "nuxt"}
BASE_DO_FRAMEWORK = {"next": "react", "nuxt": "vue"}


def serve_na_stack(item, stack):
    """Serve se cita a stack (ou a base dela), se é 'qualquer' ou se não depende de framework (js, css, html)."""
    proprias = set(item["stack"])
    return bool(proprias & {stack, BASE_DO_FRAMEWORK.get(stack, stack), "qualquer"}) or not proprias & FRAMEWORKS


def filtrar(itens, stack=None, categoria=None, gratis=False):
    out = []
    for i in itens:
        if categoria and i["categoria"] != categoria:
            continue
        if stack and not serve_na_stack(i, stack):
            continue
        if gratis and i["acesso"] not in ("gratis", "gratis+pro"):
            continue
        out.append(i)
    return out


def pontuar(item, busca):
    campos = {"nome": 4, "tags": 3, "categoria": 2, "resumo": 1, "stack": 1}
    total = 0
    for t in busca:
        raiz = t[:5]
        for campo, peso in campos.items():
            valor = item.get(campo, "")
            texto = " ".join(valor) if isinstance(valor, list) else valor
            if any(p.startswith(raiz) for p in termos(texto)):
                total += peso
    return total


def ordenar(itens, pontos=None):
    pontos = pontos or {}
    return sorted(itens, key=lambda i: (-pontos.get(i["id"], 0), not i.get("em_uso"), ORDEM_ACESSO.get(i["acesso"], 9), i["nome"].casefold()))


RECRIAVEIS = ("componentes", "comunidade", "animacao", "shaders-3d", "graficos", "experimento")


def recriavel(i):
    """Componente pago (ou com parte Pro): entra só como referência e é recriado limpo."""
    return i["categoria"] in RECRIAVEIS and i["acesso"] in ("pago", "gratis+pro", "freemium")


def linha(i):
    uso = " [em uso]" if i.get("em_uso") else ""
    aviso = "  ! " + i["cuidado"] if i.get("cuidado") else ""
    if recriavel(i):
        aviso += "\n  >> %s: só referência; recrie limpo com as skills: python kitweb.py recriar %s" % (
            "Pago" if i["acesso"] == "pago" else "Parte paga", i["id"])
    return "- %s (%s)%s — %s | %s | %s\n  %s%s" % (i["nome"], i["id"], uso, i["acesso"], i["licenca"], ", ".join(i["stack"]), i["url"], ("\n  " + i["resumo"]) + aviso if i.get("resumo") else aviso)


def mostrar(itens, como_json):
    if como_json:
        print(json.dumps(itens, ensure_ascii=False, indent=2))
    elif not itens:
        print("Nada encontrado. Tente outro termo, tire filtros ou rode `secoes`/`categorias`.")
    else:
        print("\n".join(linha(i) for i in itens))


def cmd_buscar(a, d):
    busca = termos(" ".join(a.termos))
    base = filtrar(d["itens"], a.stack, a.categoria, a.gratis)
    pontos = {i["id"]: pontuar(i, busca) for i in base}
    achados = [i for i in ordenar(base, pontos) if pontos[i["id"]] > 0][: a.n]
    mostrar(achados, a.json)


def cmd_listar(a, d):
    itens = ordenar(filtrar(d["itens"], a.stack, a.categoria, a.gratis))
    if a.json:
        return mostrar(itens, True)
    for cat, desc in d["categorias"].items():
        grupo = [i for i in itens if i["categoria"] == cat]
        if grupo:
            print("\n## %s — %s\n%s" % (cat, desc, "\n".join(linha(i) for i in grupo)))


def cmd_ver(a, d):
    item = next((i for i in d["itens"] if i["id"] == a.id), None)
    if not item:
        sys.exit("Item '%s' não existe. Use buscar." % a.id)
    print(json.dumps(item, ensure_ascii=False, indent=2) if a.json else linha(item))


def por_tags(itens, tags, n):
    pontos = {i["id"]: len(set(i["tags"]) & set(tags)) for i in itens}
    return [i for i in ordenar(itens, pontos) if pontos[i["id"]] > 0][:n]


NAO_COMPONENTE = ("referencia", "skill-ia", "design-md", "geracao-ia", "servico")
INTENSOS = {"shader", "3d", "particulas"}


def ler_briefing(caminho):
    if not caminho:
        return {}
    try:
        return json.loads(Path(caminho).read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        sys.exit("Briefing ilegível (%s): %s" % (caminho, e))


def vazio(v):
    return v is None or (isinstance(v, (str, list, dict)) and not (v.strip() if isinstance(v, str) else v))


def como_lista(v):
    return [plano(x).strip() for x in (v if isinstance(v, list) else str(v or "").split(",")) if str(x).strip()]


TRILHAS = ("site", "software")


def trilha_de(d, b, pedida=None):
    """Trilha do projeto: a pedida na linha de comando, a do briefing, a do tipo de projeto ou 'site'."""
    for t in (pedida, b.get("trilha"), d.get("trilha_do_tipo", {}).get(plano(b.get("tipo", "")).strip())):
        if t and plano(t).strip() in TRILHAS:
            return plano(t).strip()
    return "site"


def da_trilha(lista, trilha):
    return [x for x in lista if trilha in x.get("trilhas", TRILHAS)]


def pendentes(d, b, trilha=None):
    out = []
    trilha = trilha or trilha_de(d, b)
    for q in da_trilha(d["entrevista"], trilha):
        v = b.get(q["id"])
        if q["id"] == "referencias":
            minimo = q.get("minimo", 3)
            v = referencias(b)
            if len(v) < minimo:
                out.append({**q, "situacao": "tem %d de %d" % (len(v), minimo)})
            elif any(vazio(r.get("olhar")) for r in v):
                out.append({**q, "situacao": "falta dizer o que olhar em cada uma"})
        elif vazio(v):
            out.append({**q, "situacao": "sem resposta"})
    for q in out:
        if "%s" in q["pergunta"]:
            q["pergunta"] = q["pergunta"] % ", ".join(d["tipos"])
    return sorted(out, key=lambda q: not q["obrigatoria"])


def referencias(b):
    """Referências do briefing como dicionários, só as que têm URL (texto solto vira {'url': texto})."""
    refs = [r if isinstance(r, dict) else {"url": str(r)} for r in (b.get("referencias") or [])]
    return [r for r in refs if not vazio(r.get("url"))]


def sem_estudo(b):
    """Referências do briefing que ainda não foram estudadas (abertas, roladas e descritas em 'estudo')."""
    return [r["url"] for r in referencias(b) if vazio(r.get("estudo"))]


def sem_conceito(b, secoes):
    """O que falta no conceito: a metáfora e o papel de cada seção dentro dela."""
    c = b.get("conceito") or {}
    if vazio(c.get("metafora")):
        return ["metafora"]
    mapa = {plano(k).strip(): v for k, v in (c.get("secoes") or {}).items()}
    return [s for s in secoes if vazio(mapa.get(s))]


CAMPOS_ARTE = ("fundo", "elemento", "passagem", "microinteracoes", "pequenos_elementos")
GERAL_ARTE = {"site": ("mundo", "paleta", "materiais", "luz", "camera", "ritmo"),
              "software": ("tokens", "densidade", "tipografia", "icones", "modo")}


def sem_direcao(b, por_secao=True, secoes=()):
    """O que falta na direção de arte: cada campo do plano geral e, em site, o plano de cada seção do briefing
    (fundo, elemento, passagem, microinterações e pequenos elementos)."""
    da = b.get("direcao_arte") or {}
    geral = da.get("geral")
    falta = []
    if vazio(geral) or (isinstance(geral, dict) and all(vazio(x) for x in geral.values())):
        falta.append("geral")
    elif isinstance(geral, dict):
        buracos = [c for c in GERAL_ARTE["site" if por_secao else "software"] if vazio(geral.get(c))]
        if buracos:
            falta.append("geral (%s)" % ", ".join(buracos))
    if not por_secao:
        return falta
    planos = da.get("secoes") or {}
    if not planos:
        return falta + ["secoes"]
    for nome, plano_s in planos.items():
        buracos = [c for c in CAMPOS_ARTE if vazio((plano_s or {}).get(c))]
        if buracos:
            falta.append("%s (%s)" % (nome, ", ".join(buracos)))
    planejadas = {plano(k).strip() for k in planos}
    return falta + ["%s (sem plano)" % s for s in secoes if s not in planejadas]


CAMPOS_TELA = ("objetivo", "acoes", "estados")


def sem_telas(b):
    """Software: telas planejadas com objetivo, ações e estados."""
    telas = b.get("telas") or {}
    if not telas:
        return ["telas"]
    return ["%s (%s)" % (n, ", ".join(c for c in CAMPOS_TELA if vazio((p or {}).get(c))))
            for n, p in telas.items() if any(vazio((p or {}).get(c)) for c in CAMPOS_TELA)]


def papel(b, secao):
    mapa = {plano(k).strip(): v for k, v in ((b.get("conceito") or {}).get("secoes") or {}).items()}
    return mapa.get(secao, "")


def contexto(a, d, b):
    """Junta filtros da linha de comando com o briefing; a linha de comando vence."""
    stacks = {s for i in d["itens"] for s in i["stack"]} - {"qualquer"}
    stack = a.stack or next((t for t in (x.split(".")[0] for x in termos(b.get("stack", ""))) if t in stacks), None)
    gratis = a.gratis or (bool(b) and not plano(b.get("aceita_pago", "")).strip().startswith("sim"))
    secoes = como_lista(b.get("secoes")) or d["tipos"].get(plano(b.get("tipo", "")).strip(), [])
    calmo = plano(b.get("efeitos", "")).startswith("calm")
    return stack, gratis, list(dict.fromkeys(secoes)), calmo


def escolher_secao(d, itens, secao, n, calmo):
    """Componentes para a seção: pelas tags do atalho do catálogo ou, em seção de nome livre, pela busca do nome."""
    base = [i for i in itens if i["categoria"] not in NAO_COMPONENTE and not (calmo and INTENSOS & set(i["tags"]))]
    if secao in d["secoes"]:
        return por_tags(base, d["secoes"][secao], n)
    pontos = {i["id"]: pontuar(i, termos(secao)) for i in base}
    return [i for i in ordenar(base, pontos) if pontos[i["id"]] > 0][:n]


def skills_da(etapa, trilha):
    """Skills obrigatórias da etapa; 'nome@site' vale só na trilha site."""
    return [s.split("@")[0] for s in etapa.get("skills", []) if "@" not in s or s.split("@")[1] == trilha]


def sem_ux(d, b, trilha):
    feitas = set(b.get("ux_aplicado") or {})
    todas = dict.fromkeys(s for e in da_trilha(d["etapas"], trilha) for s in skills_da(e, trilha))
    return [s for s in todas if s not in feitas]


def cmd_recriar(a, d):
    item = next((i for i in d["itens"] if i["id"] == a.id), None) if a.id else None
    if a.id and not item:
        sys.exit("Item '%s' não existe. Use buscar." % a.id)
    r = d["recriar"]
    if a.json:
        return print(json.dumps({"item": item, **r}, ensure_ascii=False, indent=2))
    if item:
        print("# Recriar limpo a partir de %s (%s)\nReferência: %s\n" % (item["nome"], item["acesso"], item["url"]))
    print(r["regra"] + "\n")
    print("\n".join("%d. %s" % (n, p.replace("<id>", item["id"] if item else "<id>")) for n, p in enumerate(r["passos"], 1)))
    print("\nSkills: " + ", ".join(r["skills"]))


def fundamentos(d, trilha=None):
    return [g for g in d["fundamentos"]["grupos"] if not trilha or trilha in g.get("trilhas", TRILHAS)]


def mostrar_fundamentos(grupos):
    for g in grupos:
        print("### %s" % g["grupo"])
        print("\n".join("- " + r for r in g["regras"]))


def cmd_ux(a, d):
    trilha = plano(a.trilha).strip() if a.trilha else None
    grupos = fundamentos(d, trilha)
    if a.json:
        return print(json.dumps({"sobre": d["fundamentos"]["_sobre"], "grupos": grupos,
                                 "fontes": [i for i in d["itens"] if i["categoria"] == "ux-base"]}, ensure_ascii=False, indent=2))
    print("# Fundamentos de UX/UI%s\n%s\n" % (" (trilha %s)" % trilha if trilha else "", d["fundamentos"]["_sobre"]))
    mostrar_fundamentos(grupos)
    print("\nFontes e skills (categoria ux-base):\n" + "\n".join(linha(i) for i in ordenar([i for i in d["itens"] if i["categoria"] == "ux-base"])))


POR_SECAO = 5  # opções por seção no roteiro; as etapas mostram tudo do catálogo, salvo --n


def cmd_guia(a, d):
    b = ler_briefing(a.briefing)
    stack, gratis, secoes, calmo = contexto(a, d, b)
    # pagos recriáveis ficam no guia como referência (marcados por linha()); o resto pago sai se não aceita pago
    itens = [i for i in filtrar(d["itens"], stack) if not gratis or i["acesso"] in ("gratis", "gratis+pro") or recriavel(i)]
    if a.secao:
        secao = plano(a.secao)
        if secao not in d["secoes"]:
            sys.exit("Seção desconhecida. Opções: " + ", ".join(d["secoes"]))
        achados = escolher_secao(d, itens, secao, a.n or 8, calmo)
        if a.json:
            return mostrar(achados, True)
        print("Seção %s (tags: %s)%s:" % (secao, ", ".join(d["secoes"][secao]), " stack " + stack if stack else ""))
        return mostrar(achados, False)
    trilha = trilha_de(d, b, getattr(a, "trilha", None))
    falta = pendentes(d, b, trilha) if b else []
    roteiro = []
    for n, etapa in enumerate(da_trilha(d["etapas"], trilha), 1):
        etapa = {**etapa, "titulo": "%d. %s" % (n, etapa["titulo"])}
        e = {**etapa, "itens": []}
        if etapa.get("por_secao"):
            e["secoes"] = {s: escolher_secao(d, itens, s, a.n or POR_SECAO, calmo) for s in secoes}
        elif etapa.get("so_se_pedido"):
            pedido = termos(" ".join(como_lista(b.get("servicos"))))
            cands = [i for i in itens if i["categoria"] in etapa["categorias"]]
            e["itens"] = [i for i in ordenar(cands) if pedido and pontuar(i, pedido) > 0][: a.n]
        else:
            e["itens"] = ordenar([i for i in itens if i["categoria"] in etapa["categorias"]])[: a.n]
        if etapa["categorias"] == ["referencia"] and b:
            e["do_briefing"] = referencias(b)
        if (etapa.get("direcao") or etapa.get("direcao_sistema")) and b:
            e["estudos"] = [r for r in referencias(b) if not vazio(r.get("estudo"))]
        if etapa.get("fundamentos"):
            e["regras"] = fundamentos(d, trilha)
        e["skills"] = skills_da(etapa, trilha)
        roteiro.append(e)
    ux_falta = sem_ux(d, b, trilha) if b else []
    estudar = sem_estudo(b)
    site = trilha == "site"
    conceito_falta = sem_conceito(b, secoes) if b and site else []
    arte_falta = sem_direcao(b, por_secao=site, secoes=secoes) if b else []
    telas_falta = sem_telas(b) if b and not site else []
    if a.json:
        return print(json.dumps({"pendentes": falta, "sem_estudo": estudar, "conceito": b.get("conceito"), "sem_conceito": conceito_falta, "direcao_arte": b.get("direcao_arte"), "sem_direcao_arte": arte_falta, "telas": b.get("telas"), "sem_telas": telas_falta, "sem_skills_ux": ux_falta, "recriar": d["recriar"], "trilha": trilha, "stack": stack, "so_gratis": gratis, "secoes": secoes, "roteiro": roteiro}, ensure_ascii=False, indent=2))
    if b:
        obrig = [q for q in falta if q["obrigatoria"]]
        print("# %s — %s | trilha %s | stack %s | %s | seções: %s" % (b.get("nome") or "projeto sem nome", b.get("tipo") or "tipo ?", trilha, stack or "?",
              "pagos só como referência (recriar limpo)" if gratis else "pago liberado; componente pago ainda se recria limpo", ", ".join(secoes) or "?"))
        if obrig:
            print("! Entreviste antes: %d pergunta(s) obrigatória(s) sem resposta (%s). Rode `entrevista --briefing`."
                  % (len(obrig), ", ".join(q["id"] for q in obrig)))
        if conceito_falta:
            print("! Defina o conceito antes de construir: %s" % (
                "falta a metáfora" if conceito_falta == ["metafora"] else "seções sem papel no conceito: " + ", ".join(conceito_falta)))
        if arte_falta:
            print("! Planeje a direção %s antes de construir: falta %s" % ("de arte" if site else "visual do sistema", "; ".join(arte_falta)))
        if telas_falta:
            print("! Planeje tarefas e telas antes de construir: falta %s" % "; ".join(telas_falta))
        if ux_falta:
            print("! Skills de UI/UX ainda não aplicadas (%d): %s. Aplique cada uma na sua etapa e grave em ux_aplicado.<skill> o que ela mudou; não entregue com pendência."
                  % (len(ux_falta), ", ".join(ux_falta)))
        if estudar:
            print("! Estude antes de construir (pesa mais que Impeccable e Taste): %d referência(s) sem 'estudo': %s"
                  % (len(estudar), ", ".join(estudar)))
    for e in roteiro:
        print("\n## %s\n%s" % (e["titulo"], e["dica"]))
        if e["skills"]:
            feitas = set((b.get("ux_aplicado") or {}) if b else ())
            print("Aplicar (obrigatório): " + ", ".join(s + (" [feito]" if s in feitas else "") for s in e["skills"]))
        if e.get("regras"):
            mostrar_fundamentos(e["regras"])
            print("Para aprofundar e revisar:")
        if "do_briefing" in e:
            refs = e["do_briefing"]
            print("Do briefing (%d):" % len(refs))
            for r in refs:
                print("  * %s — %s\n    estudo: %s" % (r["url"], r.get("olhar") or "o que olhar?", r.get("estudo") or "(falta estudar)"))
            print("Onde buscar mais:")
        if e.get("conceito") and b:
            c = b.get("conceito") or {}
            print("Conceito: %s" % (c.get("metafora") or "(não definido)"))
            if c.get("por_que"):
                print("Por quê: %s" % c["por_que"])
            for s in secoes:
                print("  * %s: %s" % (s, papel(b, s) or "(sem papel definido)"))
        if e.get("telas") and b:
            for nome, pt in (b.get("telas") or {}).items():
                print("  ### %s" % nome)
                for c, val in (pt or {}).items():
                    print("    %s: %s" % (c, val if not isinstance(val, list) else "; ".join(map(str, val))))
        if (e.get("direcao") or e.get("direcao_sistema")) and b:
            print("Tire a direção dos estudos das referências (%d de %d estudadas):" % (len(e["estudos"]), len(referencias(b))))
            for r in e["estudos"]:
                print("  * %s — %s" % (r["url"], r["estudo"]))
            da = b.get("direcao_arte") or {}
            geral = da.get("geral") or {}
            for k, val in (geral.items() if isinstance(geral, dict) else [("geral", geral)]):
                print("  %s: %s" % (k, val if not isinstance(val, list) else "; ".join(map(str, val))))
            for nome, plano_s in ((da.get("secoes") or {}).items() if e.get("direcao") else []):
                print("  ### %s" % nome)
                for c in CAMPOS_ARTE + tuple(k for k in (plano_s or {}) if k not in CAMPOS_ARTE):
                    if (plano_s or {}).get(c):
                        print("    %s: %s" % (c, plano_s[c]))
        if "secoes" in e:
            if not e["secoes"]:
                print("(sem seções: passe --briefing com tipo/secoes, ou use --secao)")
            for s, grupo in e["secoes"].items():
                print("\n### %s" % s)
                if papel(b, s):
                    print("Papel no conceito: %s" % papel(b, s))
                print("\n".join(linha(i) for i in grupo) or "(sem atalho no catálogo para esta seção; tente `buscar` com outro termo)")
        elif e.get("so_se_pedido") and not e["itens"]:
            print("(nada no catálogo para: %s)" % b["servicos"] if b.get("servicos") else "(nada pedido em 'servicos' no briefing)")
        if e["itens"]:
            print("\n".join(linha(i) for i in e["itens"]))
        if e.get("so_se_pedido") and b.get("midia"):
            n = sum(s.get("status", "planejado") == "planejado" for s in b["midia"])
            print("Mídia: %d espaço(s), %d ainda por gerar. Prompts prontos: python kitweb.py midia --briefing <arquivo>" % (len(b["midia"]), n))
    if not b:
        print("\nSem briefing o guia é genérico. Comece por: python kitweb.py briefing projeto.json && python kitweb.py entrevista --briefing projeto.json")


def cmd_briefing(a, d):
    destino = Path(a.arquivo)
    if destino.exists():
        sys.exit("%s já existe; edite ou rode entrevista --briefing nele." % destino)
    trilha = plano(a.trilha or "site").strip()
    modelo = {"trilha": trilha} | {q["id"]: ([] if q["id"] == "referencias" else "") for q in da_trilha(d["entrevista"], trilha)}
    modelo["referencias"] = [{"url": "", "olhar": "", "estudo": ""}]
    modelo["ux_aplicado"] = {}
    if trilha == "site":
        modelo["conceito"] = {"metafora": "", "por_que": "", "opcoes": {"literais": [], "nao_literais": []}, "secoes": {}}
        modelo["direcao_arte"] = {"geral": {"mundo": "", "paleta": "", "materiais": "", "luz": "", "camera": "", "ritmo": "", "modelos": []},
                                  "secoes": {"Hero": {c: "" for c in CAMPOS_ARTE} | {"pequenos_elementos": ""}}}
    else:
        modelo["telas"] = {"Tela principal": {"objetivo": "", "dados": "", "acoes": "", "estados": "vazio, carregando, erro, sucesso, sem permissão"}}
        modelo["direcao_arte"] = {"geral": {"tokens": "", "densidade": "", "tipografia": "", "icones": "", "modo": ""}}
    destino.write_text(json.dumps(modelo, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Briefing criado em %s. Agora: python kitweb.py entrevista --briefing %s" % (destino, destino))


STATUS_MIDIA = ("planejado", "gerado", "aplicado")


def cmd_midia(a, d):
    b = ler_briefing(a.briefing)
    slots = b.setdefault("midia", [])
    if a.marcar:
        sid, status = a.marcar
        slot = next((s for s in slots if s.get("id") == sid), None)
        if not slot or status not in STATUS_MIDIA:
            sys.exit("Use --marcar <id existente> <%s>" % "|".join(STATUS_MIDIA))
        slot["status"] = status
        if a.arquivo:
            slot["arquivo"] = a.arquivo
        Path(a.briefing).write_text(json.dumps(b, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return print("%s: %s%s. %s" % (sid, status, " (" + a.arquivo + ")" if a.arquivo else "",
                     "Agora troque no código o marcador data-midia=\"%s\" pelo arquivo e marque como aplicado." % sid if status == "gerado" else ""))
    tipos = {s.get("tipo", "video") for s in slots}
    geradores = ordenar([i for i in d["itens"] if i["categoria"] == "geracao-ia" and tipos & set(i["tags"])])
    if a.json:
        return print(json.dumps({"slots": slots, "geradores": geradores, "regras": d["midia"]}, ensure_ascii=False, indent=2))
    if not slots:
        return print("Nenhuma mídia planejada. Campos de cada item em 'midia' no briefing: %s\n%s" % (d["midia"]["campos"], d["midia"]["marcador"]))
    for st in STATUS_MIDIA:
        grupo = [s for s in slots if s.get("status", "planejado") == st]
        if grupo:
            print("\n## %s (%d)" % (st, len(grupo)))
        for s in grupo:
            print("- %s — seção %s, %s, %s%s\n  prompt: %s" % (s.get("id"), s.get("secao", "?"), s.get("tipo", "video"), s.get("formato", "formato ?"),
                  " → " + s["arquivo"] if s.get("arquivo") else "", s.get("prompt") or "(falta escrever o prompt)"))
    if geradores:
        print("\nGeradores no catálogo (cole o prompt e salve o arquivo na pasta do projeto):\n" + "\n".join(linha(i) for i in geradores))


def cmd_entrevista(a, d):
    b = ler_briefing(a.briefing)
    falta = pendentes(d, b, trilha_de(d, b, a.trilha))
    if a.json:
        return print(json.dumps(falta, ensure_ascii=False, indent=2))
    if not falta:
        return print("Briefing completo. Siga com: python kitweb.py guia --briefing %s" % a.briefing)
    obrig = sum(q["obrigatoria"] for q in falta)
    print("Faltam %d resposta(s), %d obrigatória(s). Pergunte uma por vez, nesta ordem, e grave no briefing:\n" % (len(falta), obrig))
    for q in falta:
        extra = "".join("\n    %s: %s" % (r, q[k]) for k, r in (("por_que", "por quê"), ("exemplo", "ex.")) if q.get(k))
        print("- [%s] %s: %s (%s)%s" % ("obrigatória" if q["obrigatoria"] else "opcional", q["id"], q["pergunta"], q["situacao"], extra))
    if any(q["id"] == "referencias" for q in falta):
        tipo = plano(b.get("tipo", ""))
        refs = [i for i in d["itens"] if i["categoria"] == "referencia"]
        print("\nPara ajudar com referências, ofereça:\n" + "\n".join(linha(i) for i in (por_tags(refs, [tipo, "landing"], 4) or refs[:4])))


def cmd_categorias(a, d):
    for cat, desc in d["categorias"].items():
        print("%-12s %3d  %s" % (cat, sum(i["categoria"] == cat for i in d["itens"]), desc))


def cmd_secoes(a, d):
    for s, tags in d["secoes"].items():
        print("%-12s %s" % (s, ", ".join(tags)))


def lista(texto):
    return [plano(t).strip() for t in (texto or "").split(",") if t.strip()]


def cmd_adicionar(a, d):
    if a.categoria not in d["categorias"]:
        sys.exit("Categoria inválida. Opções: " + ", ".join(d["categorias"]))
    if a.acesso not in ACESSOS:
        sys.exit("Acesso inválido. Opções: " + ", ".join(sorted(ACESSOS)))
    if not re.match(r"^https?://", a.url):
        sys.exit("URL precisa começar com http(s)://")
    url = a.url.rstrip("/").casefold()
    for i in d["itens"]:
        if i["id"] == a.id or i["url"].rstrip("/").casefold() == url:
            sys.exit("Já existe: %s (%s). Edite o catalogo.json se quiser mudar." % (i["nome"], i["id"]))
    item = {"id": a.id, "nome": a.nome, "url": a.url, "categoria": a.categoria, "stack": lista(a.stack) or ["qualquer"],
            "acesso": a.acesso, "licenca": a.licenca, "tags": lista(a.tags), "resumo": a.resumo, "cuidado": a.cuidado,
            "em_uso": False, "adicionado": date.today().isoformat()}
    d["itens"].append(item)
    salvar(d)
    print("Adicionado:\n" + linha(item))


def responde(url):
    pedido = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 kitweb-checar"})
    try:
        with urllib.request.urlopen(pedido, timeout=15) as r:
            return url, r.status
    except Exception as e:  # noqa: BLE001 — só relatório
        return url, getattr(e, "code", None) or type(e).__name__


def cmd_checar(a, d):
    with ThreadPoolExecutor(8) as pool:
        resultados = list(pool.map(responde, [i["url"] for i in d["itens"]]))
    ruins = [(u, s) for u, s in resultados if not (isinstance(s, int) and 200 <= s < 300)]
    # ponytail: 403 costuma ser bloqueio de robô (Cloudflare), não site morto; confira no navegador antes de remover
    for u, s in ruins:
        print("%s  %s" % (s, u))
    print("%d de %d responderam." %(len(resultados) - len(ruins), len(resultados)))


def cmd_teste(a, d):
    ids = [i["id"] for i in d["itens"]]
    assert len(ids) == len(set(ids)), "id repetido"
    for i in d["itens"]:
        assert i["categoria"] in d["categorias"], i["id"]
        assert i["acesso"] in ACESSOS, i["id"]
        assert i["url"].startswith("http"), i["id"]
    for e in d["etapas"]:
        assert all(c in d["categorias"] for c in e["categorias"]), e["titulo"]
        assert e.get("trilhas") and set(e["trilhas"]) <= set(TRILHAS), e["titulo"]
    assert set(d["trilha_do_tipo"]) == set(d["tipos"]), "tipo sem trilha"
    assert trilha_de(d, {"tipo": "dashboard"}) == "software" and trilha_de(d, {"tipo": "landing"}) == "site"
    assert trilha_de(d, {"tipo": "landing", "trilha": "software"}) == "software"
    assert not any(e.get("conceito") for e in da_trilha(d["etapas"], "software"))
    assert not any(e.get("telas") for e in da_trilha(d["etapas"], "site"))
    assert any(q["id"] == "usuarios" for q in pendentes(d, {"tipo": "sistema"}))
    assert not any(q["id"] == "usuarios" for q in pendentes(d, {"tipo": "landing"}))
    assert sem_telas({}) == ["telas"] and sem_telas({"telas": {"Chamados": {"objetivo": "a", "acoes": "b"}}}) == ["Chamados (estados)"]
    assert sem_direcao({"direcao_arte": {"geral": dict.fromkeys(GERAL_ARTE["software"], "x")}}, por_secao=False) == []
    assert sem_direcao({"direcao_arte": {"geral": {"tokens": "x"}}}, por_secao=False) == ["geral (densidade, tipografia, icones, modo)"]
    assert sem_direcao({"direcao_arte": {"geral": {"tokens": "", "modo": ""}}}, por_secao=False) == ["geral"]
    base = filtrar(d["itens"], "react")
    achados = [i for i in base if pontuar(i, termos("fundo background hero")) > 0]
    assert achados, "busca sem resultado"
    assert all(serve_na_stack(i, "react") for i in base) and not any("vue" in i["stack"] and "react" not in i["stack"] for i in base)
    assert serve_na_stack({"stack": ["js", "threejs"]}, "react") and serve_na_stack({"stack": ["react"]}, "next")
    assert not serve_na_stack({"stack": ["vue", "nuxt"]}, "react")
    assert por_tags(d["itens"], d["secoes"]["hero"], 5), "seção hero vazia"
    assert plano("Animação") == "animacao"
    assert all(s in d["secoes"] for t in d["tipos"].values() for s in t), "tipo com seção inexistente"
    assert len(pendentes(d, {})) == len(da_trilha(d["entrevista"], "site"))
    b = {"tipo": "institucional", "stack": "React + Vite", "aceita_pago": "nao", "efeitos": "calmo",
         "referencias": [{"url": "https://a", "olhar": "x"}] * 3}
    stack, gratis, secoes, calmo = contexto(argparse.Namespace(stack=None, gratis=False), d, b)
    assert (stack, gratis, calmo) == ("react", True, True) and secoes == d["tipos"]["institucional"]
    assert not any(q["id"] == "referencias" for q in pendentes(d, b))
    assert sem_direcao({}) == ["geral", "secoes"]
    geral = dict.fromkeys(GERAL_ARTE["site"], "x")
    hero = dict.fromkeys(CAMPOS_ARTE, "x")
    assert sem_direcao({"direcao_arte": {"geral": {"paleta": "x"}, "secoes": {"Hero": {"fundo": "a", "elemento": "b", "passagem": "c"}}}}) == [
        "geral (mundo, materiais, luz, camera, ritmo)", "Hero (microinteracoes, pequenos_elementos)"]
    assert sem_direcao({"direcao_arte": {"geral": geral, "secoes": {"Hero": hero}}}, secoes=["hero", "sobre"]) == ["sobre (sem plano)"]
    assert sem_direcao({"direcao_arte": {"geral": geral, "secoes": {"Hero": hero, "Sobre": hero}}}, secoes=["hero", "sobre"]) == []
    livre = contexto(argparse.Namespace(stack=None, gratis=False), d, {"secoes": "Hero, Sobre nós, Rodapé", "stack": "Next.js"})
    assert livre[0] == "next" and livre[2] == ["hero", "sobre nos", "rodape"], "seção livre do briefing não pode sumir"
    assert escolher_secao(d, d["itens"], "hero", 5, False)
    assert len(pendentes(d, {"referencias": [{"url": "", "olhar": "", "estudo": ""}]})) == len(da_trilha(d["entrevista"], "site"))
    assert any(q["id"] == "referencias" for q in pendentes(d, {"referencias": ["https://a", "https://b", "https://c"]})), "texto solto não diz o que olhar"
    assert sem_estudo({"referencias": [{"url": ""}, "https://a"]}) == ["https://a"]
    assert sem_conceito({}, ["hero"]) == ["metafora"]
    assert sem_conceito({"conceito": {"metafora": "gravidade", "secoes": {"Hero": "o centro aparece"}}}, ["hero", "cards"]) == ["cards"]
    assert len(sem_estudo(b)) == 3 and not sem_estudo({"referencias": [{"url": "x", "estudo": "hero com objeto central"}]})
    assert not contexto(argparse.Namespace(stack=None, gratis=False), d, {"aceita_pago": "Sim (uso próprio)"})[1]
    assert not any(INTENSOS & set(i["tags"]) for i in escolher_secao(d, d["itens"], "hero", 10, True))
    for t in TRILHAS:
        etapas_t = da_trilha(d["etapas"], t)
        assert etapas_t[0].get("fundamentos"), "fundamentos têm que ser a 1ª etapa de " + t
        assert any(e["titulo"].startswith("Checklist de UX") for e in etapas_t), "falta checklist em " + t
        assert fundamentos(d, t) and all(g["regras"] for g in fundamentos(d, t))
    assert not any(g["grupo"].startswith("Conversão") for g in fundamentos(d, "software"))
    assert any(i["categoria"] == "ux-base" for i in d["itens"])
    for t in TRILHAS:
        falta = sem_ux(d, {}, t)
        assert "ux-heuristics" in falta and "accessibility-review" in falta, t
        assert not sem_ux(d, {"ux_aplicado": dict.fromkeys(falta, "ok")}, t)
    assert "seo-audit" in sem_ux(d, {}, "site") and "seo-audit" not in sem_ux(d, {}, "software")
    pago = next(i for i in d["itens"] if i["acesso"] == "pago" and i["categoria"] == "componentes")
    assert recriavel(pago) and "recriar " + pago["id"] in linha(pago)
    assert not any(recriavel(i) for i in d["itens"] if i["categoria"] in ("servico", "ux-base", "referencia"))
    assert d["recriar"]["passos"] and d["recriar"]["skills"]
    print("ok: %d itens, %d categorias, %d seções" % (len(ids), len(d["categorias"]), len(d["secoes"])))


def main():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except AttributeError:
            pass
    p = argparse.ArgumentParser(description="Kit Web: catálogo e guia para projetos web.")
    sub = p.add_subparsers(dest="cmd", required=True)

    def filtros(sp, n=8):
        sp.add_argument("--stack")
        sp.add_argument("--categoria")
        sp.add_argument("--gratis", action="store_true", help="só grátis ou com parte grátis")
        sp.add_argument("--n", type=int, default=n)
        sp.add_argument("--json", action="store_true")

    filtros(b := sub.add_parser("buscar"))
    b.add_argument("termos", nargs="+")
    filtros(sub.add_parser("listar"), 999)
    v = sub.add_parser("ver")
    v.add_argument("id")
    v.add_argument("--json", action="store_true")
    filtros(g := sub.add_parser("guia"), None)
    g.add_argument("--secao")
    g.add_argument("--briefing", help="arquivo JSON do projeto (crie com `briefing`)")
    g.add_argument("--trilha", choices=TRILHAS, help="site ou software (padrão: do briefing ou do tipo)")
    br = sub.add_parser("briefing")
    br.add_argument("arquivo")
    br.add_argument("--trilha", choices=TRILHAS, default="site")
    md = sub.add_parser("midia")
    md.add_argument("--briefing", required=True)
    md.add_argument("--marcar", nargs=2, metavar=("ID", "STATUS"))
    md.add_argument("--arquivo")
    md.add_argument("--json", action="store_true")
    en = sub.add_parser("entrevista")
    en.add_argument("--briefing", help="sem arquivo, lista todas as perguntas")
    en.add_argument("--trilha", choices=TRILHAS)
    en.add_argument("--json", action="store_true")
    ux = sub.add_parser("ux", help="fundamentos de UX/UI: o piso de todo projeto")
    ux.add_argument("--trilha", choices=TRILHAS)
    ux.add_argument("--json", action="store_true")
    rc = sub.add_parser("recriar", help="recriar limpo um componente pago, usando-o só de referência")
    rc.add_argument("id", nargs="?")
    rc.add_argument("--json", action="store_true")
    sub.add_parser("categorias")
    sub.add_parser("secoes")
    ad = sub.add_parser("adicionar")
    for campo in ("id", "nome", "url", "categoria"):
        ad.add_argument("--" + campo, required=True)
    ad.add_argument("--stack", default="")
    ad.add_argument("--acesso", default="conferir")
    ad.add_argument("--licenca", default="conferir")
    ad.add_argument("--tags", default="")
    ad.add_argument("--resumo", default="")
    ad.add_argument("--cuidado", default="")
    sub.add_parser("checar")
    sub.add_parser("teste")
    a = p.parse_args()
    if getattr(a, "stack", None):
        a.stack = plano(a.stack)
    globals()["cmd_" + a.cmd](a, carregar())


if __name__ == "__main__":
    main()
