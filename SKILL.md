---
name: kit-web
description: "Fundamentos de UX/UI (princípios, leis, heurísticas, acessibilidade e checklists) como base de todo projeto, mais guia e catálogo de bibliotecas de componentes, animação, shaders, referências de design, skills de design e serviços para projetos web (sites, landing pages, painéis, apps web). Use sempre que for criar ou melhorar um projeto web, escolher componentes ou efeitos, procurar referência visual, ou quando aparecer uma biblioteca ou site de design novo para guardar."
---

# Kit Web

Ferramenta autônoma: uma pasta com `kitweb.py` (Python 3.9+, só biblioteca padrão) e `catalogo.json`.
Funciona com qualquer IA ou pessoa no terminal; não depende de outro sistema. Rode os comandos a partir desta pasta.

## A base: fundamentos de UX/UI

Todo projeto, site ou software, começa e termina pela mesma base, sem precisar ditar regra por regra:

- **Primeira etapa das duas trilhas:** `python kitweb.py ux --trilha site|software` (ou a etapa 1 do `guia`) traz os
  fundamentos: objetivo e tarefa, hierarquia, Gestalt, carga cognitiva, feedback, estados, navegação, formulários,
  consistência, acessibilidade WCAG AA, texto, responsivo e desempenho, ética e, por trilha, conversão ou uso diário.
  São o piso: nenhuma referência, skill ou efeito passa por cima deles. Ordem: **fundamentos (piso) > estudo das
  referências (caráter) > Impeccable > Taste (refino)**.
- **Skills de UX (categoria `ux-base`)**, instale uma vez:
  - Claude Code: `/plugin marketplace add wondelai/skills`, depois `/plugin install ux-design@wondelai-skills` e
    `/plugin install metaskills@wondelai-skills`. Outras IAs: `npx skills add wondelai/skills/<nome> --global`.
  - uxuiprinciples: copie o `SKILL.md` de `vibe-coding-advisor`, `uxui-evaluator` e `interface-auditor` para a pasta de
    skills (ou use o MCP grátis `@uxuiprinciples/mcp-server`). Rode o `vibe-coding-advisor` antes de gerar componentes.
  - Laws of UX: só consulta (licença CC BY-NC-ND: não copie o texto).
- **Penúltima etapa, Checklist de UX antes de entregar:** para cada página e componente, o checklist dele no
  Checklist Design, item por item; depois `ux-heuristics` (severidade 0 a 4), `uxui-evaluator`, `design:accessibility-review`,
  `design:design-critique` e, em site, `marketing:seo-audit`. Severidade 3 e 4 se corrige antes de entregar.
- Skill não instalada? Os fundamentos do `catalogo.json` valem sozinhos; nunca pule a base por falta de skill.

## Skills de UI/UX são obrigatórias, etapa por etapa

Cada etapa do `guia` traz uma linha **Aplicar (obrigatório)** com as skills daquela etapa. Rode cada uma no que a etapa
produziu e grave no briefing, em `ux_aplicado.<skill>`, o que ela mudou (uma frase basta). O guia lista no topo toda
skill ainda não aplicada; **não entregue com pendência**. Sem a skill instalada, aplique o método dela pelos fundamentos e
registre "sem a skill, aplicado pelos fundamentos".

| Skill | Etapas | Onde instalar |
| --- | --- | --- |
| `vibe-coding-advisor`, `uxui-evaluator`, `interface-auditor` | fundamentos, base, checklist | uxuiprinciples/agent-skills |
| `ux-heuristics`, `design-everyday-things`, `refactoring-ui`, `web-typography`, `microinteractions`, `top-design` | telas, direção, estados, efeitos, movimento, checklist | wondelai/skills, coleção `ux-design` |
| `impeccable`, `design-taste-frontend` | direção | itens `impeccable` e `tasteskill` |
| `ux-copy`, `accessibility-review`, `design-critique` | estados, acessibilidade, checklist | plugin `design` do Claude |
| `seo-audit` (só site) | checklist | plugin `marketing` do Claude |

## Componente pago: só referência, recriado limpo

Biblioteca paga, ou a parte Pro de uma `gratis+pro`, **não entra no projeto**. O guia mostra esses itens marcados com
`>>` e `python kitweb.py recriar <id>` dá o processo: especificar por observação da demo pública (capturas, medidas,
tempos, estados), sem abrir nem copiar o código-fonte nem usar assets, nome ou texto do original; implementar só a partir
da especificação, de preferência em outra sessão; aplicar as skills (`vibe-coding-advisor`, `refactoring-ui`,
`web-typography`, `microinteractions`, `reanimate`, `impeccable`, `design-taste-frontend`, `accessibility-review`); comparar
lado a lado; registrar como "recriado a partir de referência visual, código próprio".

## Duas trilhas

- **site:** sites e páginas (institucional, landing, portfólio, e-commerce). Etapas: fundamentos de UX/UI, estudo, conceito,
  direção de arte por seção, base, efeitos por seção, movimento, serviços e mídia, checklist de UX, licença.
- **software:** sistemas e apps (painéis, SaaS, sistemas internos, apps de IA). Etapas: fundamentos de UX/UI, estudo, tarefas
  e telas, direção visual do sistema, base, estados e dados, movimento funcional, serviços, acessibilidade e uso diário,
  checklist de UX, licença.

A trilha sai do `tipo` do briefing (ou de `trilha` no briefing, ou de `--trilha`). Os passos 5 e 6 abaixo são da trilha site;
na trilha software, no lugar deles: **tarefas e telas** (`telas`: objetivo, dados, ações e estados de cada tela) e **direção
visual do sistema** (`direcao_arte.geral`: tokens, densidade, tipografia, ícones, modo). O dia a dia é com componentes React;
3D (e Blender, padrão para modelar) só quando o projeto pedir.

## Fluxo de um projeto novo

1. `python kitweb.py briefing projeto.json [--trilha software]` cria o briefing em branco da trilha (guarde na pasta do projeto).
2. **Antes de perguntar, procure:** preencha o que já estiver nos arquivos, notas ou código do projeto.
3. `python kitweb.py entrevista --briefing projeto.json` lista o que falta, obrigatórias primeiro.
   Entreviste a pessoa **uma pergunta por vez**, oferecendo o que você achou como sugestão, e grave cada resposta no JSON.
   Com poucas referências (menos de 3, ou sem dizer o que olhar em cada uma), a entrevista insiste nelas e oferece onde buscar.
4. **Estude cada referência antes de construir** (pesa mais que qualquer skill): abra no navegador, espere carregar,
   role a página inteira, capture telas em vários pontos e grave em `referencias[].estudo` o que ocupa o centro do hero,
   o que preenche e move a tela, como reage a rolagem e mouse, a ordem das seções e o que copiar como ideia.
   Ordem de peso: **estudo das referências > Impeccable > Taste**. As skills refinam o que o estudo mostrou; não o substituem.
   O guia avisa enquanto houver referência sem estudo.
5. **Conceito, antes de qualquer seção:** leia a identidade da empresa (propósito, visão, valores, nome, jeito de atuar),
   não o que ela vende. Levante opções das **duas linhas, sempre** (principalmente em serviço, cuja entrega não se vê):
   **literais** (o resultado como ele é, no mundo do cliente) e **não literais** (metáforas), pelo menos 3 de cada; nunca a ferramenta
   como se fosse a solução. Mostre ao cliente com a leitura de cada uma e deixe ele escolher ou combinar. Exemplos do cliente são exemplos: capte a ideia.
   Grave em `conceito`: `metafora`, `por_que`, `opcoes` e `secoes` (o que cada seção deve fazer o visitante entender ou sentir
   dentro da metáfora). O guia avisa enquanto faltar a metáfora ou o papel de alguma seção.
6. **Direção de arte, geral e por seção, antes de codar:** geral (mundo, paleta, materiais, luz, câmera, ritmo, modelos a
   produzir) e, para cada seção, `fundo`, `elemento`, `passagem` (como chega e como vai para a próxima), `microinteracoes` e
   `pequenos_elementos`. Grave em `direcao_arte`. Modelos melhores: Blender ou Spline, ou bancos com licença clara (Poly Haven CC0).
   O guia avisa enquanto faltar qualquer campo do plano geral, algum campo de seção ou o plano de alguma seção do
   briefing, e mostra na etapa os estudos das referências: a direção sai deles, não do gosto da IA.
7. `python kitweb.py guia --briefing projeto.json` dá o roteiro da trilha já filtrado: stack, componentes pagos só como
   referência para recriar (serviços pagos saem se `aceita_pago` não for "sim"), seções do tipo de projeto, sem shaders/3D
   se `efeitos` for "calmo", e as skills de UI/UX que faltam aplicar. Cada etapa lista **todas** as bibliotecas do
   catálogo que servem na stack (limite só com `--n`); toda seção do briefing aparece, mesmo de nome livre ("Sobre",
   "Rodapé"), com até 5 opções. Biblioteca sem framework (js, css, html) serve em qualquer stack; `next` inclui as de React.
   Se ainda faltar pergunta obrigatória, o guia avisa no topo; não comece a construir antes de responder.

## Vídeos e imagens geradas por IA

**Código primeiro:** interface, ícones, texto, formas abstratas, luz, vidro, partículas e aberturas são feitos em código
(CSS, SVG, shader, Three.js): ficam nítidos, leves e reagem a mouse e scroll. Vídeo ou imagem gerada só para o que código
não faz bem: objetos 3D realistas, pessoas, lugares, produto filmado. Cada item diz em `por_que_video` por que não dá em código.

Não precisam estar prontos para começar. Durante a entrevista e a produção:

1. Cada lugar que vai ter mídia vira um item em `midia` no briefing: `id`, `secao`, `tipo` (video ou imagem),
   `formato`, `prompt` (em inglês, já escrito com o clima do projeto), `status: planejado`.
2. No código, o espaço leva `data-midia="<id>"` e um substituto leve (gradiente ou imagem estática).
3. Para gerar: `python kitweb.py midia --briefing projeto.json` lista os prompts prontos e os geradores do catálogo.
   A pessoa cola o prompt no gerador e salva o arquivo na pasta do projeto.
4. `python kitweb.py midia --briefing projeto.json --marcar <id> gerado --arquivo public/midia/<id>.mp4`; a IA troca o
   marcador `data-midia` pelo arquivo e marca `aplicado`.

## O que cada biblioteca tem por dentro (inventário)

Cada biblioteca (categorias componentes, comunidade, animacao, shaders-3d, graficos) tem `inventario/<id>.json` com a lista
real do que ela oferece: componentes, blocos, efeitos, plugins, por grupo, com `[Pro]` no que é pago. Resumo legível em
`INVENTARIO.md`. **Antes de escolher ou gerar um componente, olhe o inventário: não invente nome de componente.**

- `python kitweb.py ver <id>`: ficha mais tudo o que a biblioteca tem dentro.
- `python kitweb.py componente marquee [--stack react] [--gratis]`: acha a peça pelo nome em todas as bibliotecas
  (nomes originais, em inglês; as seções em português são traduzidas pela tabela `sinonimos` do catálogo).
- `guia` e `buscar` mostram, em cada biblioteca, a linha **Dentro:** com as peças que servem àquela seção ou busca, e
  quem tem peças da seção sobe na lista. Use essas peças pelo nome; peça `[Pro]` só como referência (`recriar`).
- `python kitweb.py inventario` mostra o que foi levantado, quando e se está completo ou parcial; `--md` regenera o
  `INVENTARIO.md` depois de editar os JSONs.
- Biblioteca nova: levante no site (ordem: `/llms.txt`, registry shadcn `/r/registry.json`, `/sitemap.xml`, barra lateral
  dos docs, repositório) e grave o JSON. Formato: `{"id", "situacao", "fontes": [], "total", "grupos": [{"nome", "itens":
  [{"nome", "pro": true|false|null, "obs"}]}], "tambem_tem": [], "acesso_visto", "observacoes", "conferido_em"}`.
  O `teste` falha se faltar inventário de alguma biblioteca.
- Situação "parcial" (Three.js, R3F, Tailwind Plus, Aura...) quer dizer que pode haver mais do que está listado: confira no site.

## Quando usar

- **Começo de qualquer projeto web:** o fluxo acima. Sem briefing, `python kitweb.py guia --stack react` dá o roteiro genérico.
- **Escolher uma seção:** `python kitweb.py guia --secao hero --stack react` (veja `secoes`).
- **Procurar algo:** `python kitweb.py buscar fundo animado --stack react --gratis`.
- **Achar um componente específico:** `python kitweb.py componente pricing --stack react`.
- **Detalhe de um item e tudo o que ele tem:** `python kitweb.py ver reactbits`.
- **Achou biblioteca, referência ou ferramenta nova:** guarde na hora com `adicionar` (ela recusa duplicado).
  Confira acesso e licença no site antes; se não conferiu, deixe `conferir`.
- Para outra IA consumir: acrescente `--json`.

## Regras de escolha

1. Comece pelo que o projeto já usa (itens `[em uso]` e dependências do repositório). Uma base de componentes só.
2. Referência real antes de componente. Copie a ideia, nunca código, marca ou identidade de terceiros.
3. Um efeito forte por tela. Anime só `transform`/`opacity`, respeite `prefers-reduced-motion`.
4. **Licença e venda** (o ponto de atenção destas bibliotecas):
   - `gratis+pro`: só a parte gratuita entra; o que estiver marcado Pro vira referência e é recriado limpo (`recriar`).
   - `pago` (componente): nunca entra; recriado limpo a partir da demo pública.
   - `MIT + Commons Clause` (React Bits): pode usar no site ou app do cliente; não pode revender o componente
     (kit, template, biblioteca própria).
   - `comunidade` e `por componente`: cada item tem autor e licença próprios; confira na origem.
   - `conferir`: ninguém verificou ainda. Verifique antes de entregar e atualize o catálogo.
   - No fim, registre no projeto quais itens entraram e a licença de cada um.
5. Segredos (chaves de Clerk, IA, pagamento) só em variável de ambiente.

## Manutenção

- `python kitweb.py teste` depois de editar o `catalogo.json` à mão.
- `python kitweb.py checar` de tempos em tempos; 403 costuma ser bloqueio de robô, confira no navegador antes de remover.
- Categorias, seções e etapas do guia vivem no próprio `catalogo.json`; mude lá, não no código.
