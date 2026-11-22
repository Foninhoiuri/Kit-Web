---
name: kit-web
description: "Guia e catálogo de bibliotecas de componentes, animação, shaders, referências de design, skills de design e serviços para projetos web (sites, landing pages, painéis, apps web). Use sempre que for criar ou melhorar um projeto web, escolher componentes ou efeitos, procurar referência visual, ou quando aparecer uma biblioteca ou site de design novo para guardar."
---

# Kit Web

Ferramenta autônoma: uma pasta com `kitweb.py` (Python 3.9+, só biblioteca padrão) e `catalogo.json`.
Funciona com qualquer IA ou pessoa no terminal; não depende de outro sistema. Rode os comandos a partir desta pasta.

## Fluxo de um projeto novo

1. `python kitweb.py briefing projeto.json` cria o briefing em branco (guarde na pasta do projeto).
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
   O guia avisa enquanto faltar o plano geral ou algum campo de seção.
7. `python kitweb.py guia --briefing projeto.json` dá o roteiro em 7 etapas já filtrado: stack, só grátis se
   `aceita_pago` não for "sim", seções do tipo de projeto, sem shaders/3D se `efeitos` for "calmo".
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

## Quando usar

- **Começo de qualquer projeto web:** o fluxo acima. Sem briefing, `python kitweb.py guia --stack react` dá o roteiro genérico.
- **Escolher uma seção:** `python kitweb.py guia --secao hero --stack react` (veja `secoes`).
- **Procurar algo:** `python kitweb.py buscar fundo animado --stack react --gratis`.
- **Detalhe de um item:** `python kitweb.py ver reactbits`.
- **Achou biblioteca, referência ou ferramenta nova:** guarde na hora com `adicionar` (ela recusa duplicado).
  Confira acesso e licença no site antes; se não conferiu, deixe `conferir`.
- Para outra IA consumir: acrescente `--json`.

## Regras de escolha

1. Comece pelo que o projeto já usa (itens `[em uso]` e dependências do repositório). Uma base de componentes só.
2. Referência real antes de componente. Copie a ideia, nunca código, marca ou identidade de terceiros.
3. Um efeito forte por tela. Anime só `transform`/`opacity`, respeite `prefers-reduced-motion`.
4. **Licença e venda** (o ponto de atenção destas bibliotecas):
   - `gratis+pro`: só a parte gratuita entra sem compra; o que estiver marcado Pro exige licença.
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
