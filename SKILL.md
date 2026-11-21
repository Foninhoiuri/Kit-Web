---
name: kit-web
description: "Guia e catálogo de bibliotecas de componentes, animação, shaders, referências de design, skills de design e serviços para projetos web (sites, landing pages, painéis, apps web). Use sempre que for criar ou melhorar um projeto web, escolher componentes ou efeitos, procurar referência visual, ou quando aparecer uma biblioteca ou site de design novo para guardar."
---

# Kit Web

Ferramenta autônoma: uma pasta com `kitweb.py` (Python 3.9+, só biblioteca padrão) e `catalogo.json`.
Funciona com qualquer IA ou pessoa no terminal; não depende de outro sistema. Rode os comandos a partir desta pasta.

## Quando usar

- **Começo de qualquer projeto web:** `python kitweb.py guia --stack <react|vue|html|...>` dá o roteiro em 7 etapas
  (referências, direção visual, base, efeitos por seção, movimento, serviços, licença) com os itens certos de cada uma.
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
