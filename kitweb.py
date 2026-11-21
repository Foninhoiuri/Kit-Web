"""Kit Web: acha, no catálogo, bibliotecas, referências e ferramentas para projetos web, e guia a escolha por etapa e seção.

Uso (Python 3.9+, só biblioteca padrão; funciona em qualquer IA ou terminal):
  python kitweb.py guia [--stack react] [--secao hero]       roteiro do projeto, ou atalhos de uma seção
  python kitweb.py buscar fundo animado [--stack vue] [--categoria componentes] [--gratis] [--n 8]
  python kitweb.py listar [--categoria referencia]
  python kitweb.py ver reactbits
  python kitweb.py categorias | secoes
  python kitweb.py adicionar --id x --nome X --url https://... --categoria componentes [--stack react,tailwind]
                   [--acesso gratis] [--licenca MIT] [--tags hero,cards] [--resumo "..."] [--cuidado "..."]
  python kitweb.py checar          confere se cada URL ainda responde
  python kitweb.py teste           autoteste do catálogo e da busca
Qualquer comando de leitura aceita --json (saída para outra IA).
Palavras: site, landing page, projeto web, componentes, biblioteca de UI, animação, referência de design, shader.
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


def filtrar(itens, stack=None, categoria=None, gratis=False):
    out = []
    for i in itens:
        if categoria and i["categoria"] != categoria:
            continue
        if stack and stack not in i["stack"] and "qualquer" not in i["stack"]:
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


def linha(i):
    uso = " [em uso]" if i.get("em_uso") else ""
    aviso = "  ! " + i["cuidado"] if i.get("cuidado") else ""
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


def cmd_guia(a, d):
    itens = filtrar(d["itens"], a.stack, None, a.gratis)
    if a.secao:
        tags = d["secoes"].get(plano(a.secao))
        if not tags:
            sys.exit("Seção desconhecida. Opções: " + ", ".join(d["secoes"]))
        achados = por_tags([i for i in itens if i["categoria"] not in ("referencia", "skill-ia", "design-md")], tags, a.n)
        if a.json:
            return mostrar(achados, True)
        print("Seção %s (tags: %s)%s:" % (a.secao, ", ".join(tags), " stack " + a.stack if a.stack else ""))
        return mostrar(achados, False)
    roteiro = []
    for etapa in d["etapas"]:
        grupo = ordenar([i for i in itens if i["categoria"] in etapa["categorias"]])[: a.n]
        roteiro.append({**etapa, "itens": grupo})
    if a.json:
        return print(json.dumps(roteiro, ensure_ascii=False, indent=2))
    for e in roteiro:
        print("\n## %s\n%s" % (e["titulo"], e["dica"]))
        if e["itens"]:
            print("\n".join(linha(i) for i in e["itens"]))
    print("\nPor seção: python kitweb.py guia --secao <%s>" % "|".join(d["secoes"]))


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
    base = filtrar(d["itens"], "react")
    achados = [i for i in base if pontuar(i, termos("fundo background hero")) > 0]
    assert achados, "busca sem resultado"
    assert all("react" in i["stack"] or "qualquer" in i["stack"] for i in base)
    assert por_tags(d["itens"], d["secoes"]["hero"], 5), "seção hero vazia"
    assert plano("Animação") == "animacao"
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
    filtros(g := sub.add_parser("guia"), 4)
    g.add_argument("--secao")
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
