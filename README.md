<div align="center">

# Kit Web

**Um guia de bolso para projetos web.** Bibliotecas de componentes, animação, shaders, referências de design,
skills de IA e serviços: organizados, pesquisáveis e com o cuidado de licença já anotado.

![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-3776AB?logo=python&logoColor=white)
![Zero dependências](https://img.shields.io/badge/depend%C3%AAncias-zero-2ea44f)
![Itens](https://img.shields.io/badge/cat%C3%A1logo-51%20itens-8957e5)
![Feito para IA](https://img.shields.io/badge/feito%20para-humanos%20%2B%20IAs-f97316)

</div>

---

## Por que existe

Shadcn, Aceternity, Magic UI, React Bits, Untitled UI, HeroUI, 21st.dev, Skiper, Shaders, Dribbble, Mobbin,
Refero… o problema nunca é falta de opção, é **excesso**. O Kit Web transforma essa pilha de favoritos num roteiro:
o que olhar primeiro, o que usar em cada seção e o que **não** pode ir para o cliente sem pagar.

- **Entrevista antes de sugerir:** um briefing do projeto; o kit pergunta o que falta (público, ação, referências,
  orçamento para itens pagos) e insiste quando há pouca referência.
- **Guia por etapa:** das referências até a checagem de licença, em 7 passos, filtrado pelo briefing.
- **Vídeos com prompt pronto:** cada espaço de vídeo ou imagem gerada por IA nasce marcado no código, com o prompt
  escrito no briefing; gerar depois é colar no gerador e entregar o arquivo.
- **Atalho por seção:** hero, cards, fundo, rolagem, preços, dashboard, login…
- **Licença visível:** grátis, grátis com parte Pro, freemium ou pago, mais a licença de cada item.
- **Funciona com qualquer IA:** `SKILL.md` com as instruções e `--json` em todo comando de leitura.
- **Cresce com o uso:** achou uma biblioteca nova? Um comando e ela entra no catálogo.

## Começando

```bash
git clone <url-do-repositorio> kit-web
cd kit-web
python kitweb.py briefing meu-site.json          # cria o briefing em branco
python kitweb.py entrevista --briefing meu-site.json  # o que falta responder
python kitweb.py guia --briefing meu-site.json        # roteiro sob medida
```

Só precisa de Python 3.9 ou mais novo. Nada para instalar. Com pressa? `python kitweb.py guia --stack react` dá o
roteiro genérico.

## Comandos

| Comando | O que faz |
| --- | --- |
| `briefing arquivo.json` | Cria o briefing do projeto em branco |
| `entrevista --briefing arquivo.json` | Perguntas que faltam, obrigatórias primeiro |
| `guia --briefing arquivo.json` | Roteiro sob medida: stack, seções do tipo, só grátis se não houver orçamento |
| `midia --briefing arquivo.json` | Vídeos e imagens planejados, com prompts prontos e geradores |
| `midia --briefing … --marcar <id> gerado --arquivo …` | Registra o arquivo gerado para a IA aplicar no código |
| `guia [--stack react]` | Roteiro genérico, sem briefing |
| `guia --secao hero` | Opções para uma seção específica (veja `secoes`) |
| `buscar fundo animado --gratis` | Busca livre, com filtros `--stack`, `--categoria`, `--gratis`, `--n` |
| `ver reactbits` | Ficha completa de um item |
| `listar [--categoria referencia]` | Catálogo inteiro, agrupado |
| `categorias` · `secoes` | O que existe para filtrar |
| `adicionar --id … --nome … --url … --categoria …` | Guarda um item novo (recusa duplicado) |
| `checar` | Confere se todas as URLs ainda respondem |
| `teste` | Autoteste do catálogo e da busca |

Exemplo:

```text
$ python kitweb.py guia --secao cards --stack react --n 2
Seção cards (tags: cards, bento, scroll) stack react:
- Aceternity UI (aceternity) — gratis+pro | gratuitos liberados; Pro proprietário | react, tailwind, motion
  https://ui.aceternity.com/components
  Componentes de impacto: spotlight, cards 3D, paralaxe, revelação ao rolar, fundos animados.
  ! Templates e blocos Pro são pagos. Fácil de exagerar: um por tela.
- Skiper UI (skiper-ui) — gratis+pro | gratuitos livres; Premium US$ 129 único | react, tailwind, motion
  https://skiper-ui.com/
  Componentes autorais com animação caprichada.
  ! 106+ componentes Premium pagos; conferir quais são grátis.
```

## O roteiro

| Etapa | Foco |
| --- | --- |
| 1. Referências reais | 3 a 5 telas reais do mesmo tipo de projeto antes de qualquer componente |
| 2. Direção visual | Tipografia, cores e tom num `DESIGN.md`; skill de gosto para fugir da “cara de IA” |
| 3. Base de componentes | Uma base só, de preferência a que o projeto já usa |
| 4. Efeitos por seção | Um efeito forte por tela; o resto calmo |
| 5. Movimento | Só `transform` e `opacity`, respeitando `prefers-reduced-motion` |
| 6. Serviços e mídia | Login, pagamento e imagens prontos; segredos só em variável de ambiente |
| 7. Licença | Conferir cada item usado e registrar no projeto |

## O catálogo

| Categoria | Itens | O que tem |
| --- | ---: | --- |
| `componentes` | 16 | Bibliotecas organizadas (shadcn/ui, Magic UI, Aceternity, React Bits, HeroUI, daisyUI…) |
| `comunidade` | 7 | Coleções soltas de vários autores (21st.dev, Skiper, FreeFrontend…) |
| `referencia` | 9 | Inspiração real (Dribbble, Mobbin, Refero, Godly, SaaS Landing Page…) |
| `geracao-ia` | 4 | Imagem, vídeo e telas por IA |
| `animacao` | 3 | Anime.js, Motion, Transitions.dev |
| `shaders-3d` | 3 | Shaders, partículas e WebGL |
| `skill-ia` | 3 | Taste Skill, Impeccable, reanimate |
| `graficos` | 2 | Recharts, Bklit |
| `design-md` | 2 | Sistemas de design em texto para a IA |
| `servico` · `experimento` | 2 | Clerk; demo de cena 3D em várias janelas |

## Licença e venda: leia antes de entregar

| Marcação | Significa |
| --- | --- |
| `gratis` | Livre para usar (confira a licença indicada) |
| `gratis+pro` | Só a parte gratuita entra sem compra; o resto exige licença paga |
| `freemium` | Serviço com plano grátis limitado |
| `pago` | Só com licença comprada |
| `conferir` | Ainda não verificado: verifique antes de usar |
| `MIT + Commons Clause` | Pode usar no site ou app; **não** pode revender o componente em si |
| `por componente` | Cada item tem autor e licença próprios |

As informações de preço e licença foram conferidas nos sites quando cada item entrou, e podem mudar. A palavra final é
sempre a do site oficial.

## Usando com uma IA

Aponte o agente para o [`SKILL.md`](SKILL.md): ele explica quando usar o kit e as regras de escolha. No Claude Code,
Codex ou similares, copie a pasta para o diretório de skills, ou peça à IA para rodar `python kitweb.py guia --json`.

## Contribuindo com o catálogo

```bash
python kitweb.py adicionar --id nova-lib --nome "Nova Lib" --url https://exemplo.dev \
  --categoria componentes --stack react,tailwind --acesso gratis --licenca MIT \
  --tags hero,cards --resumo "O que ela faz bem." --cuidado "O que observar."
python kitweb.py teste
```

Categorias, seções e etapas do guia vivem no `catalogo.json`; ajuste lá, sem mexer no código.

## Estrutura

```text
kit-web/
├── kitweb.py       # CLI (só biblioteca padrão)
├── catalogo.json   # itens, categorias, seções e etapas do guia
└── SKILL.md        # instruções para agentes de IA
```
