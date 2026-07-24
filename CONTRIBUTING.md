# Como contribuir · How to contribute
### Principia Orthogona — geometry

*Bilíngue PT/EN. Toda seção aparece primeiro em português, depois em inglês.*
*Bilingual PT/EN. Every section appears in Portuguese first, then English.*

---

## Para quem é isto / Who this is for

**PT.** Se você chegou até aqui lendo as provas, os capítulos ou o desenvolvimento
Lean, você já sabe o suficiente para contribuir. Não é preciso ser co-autor nem
saber tudo. Há quatro caminhos, do mais fácil ao mais técnico, e **todos contam
como contribuição real** — inclusive apontar um erro sem consertá-lo.

**EN.** If you got here by reading the proofs, the chapters, or the Lean
development, you already know enough to contribute. You do not need to be a
co-author or to know everything. There are four paths, easiest to most technical,
and **all count as real contributions** — including pointing at an error without
fixing it.

> **A regra que rege tudo / The one rule that governs everything.**
> Nada é "provado", "verificado" ou "fechado" sem uma verificação de núcleo:
> ou o CI está verde, ou o código foi colado num núcleo Lean real e voltou limpo.
> Prosa fluente e confiança não são evidência. — Nothing is "proved,"
> "verified," or "closed" without a kernel check: either CI is green, or the code
> was pasted into a real Lean kernel and came back clean. Fluent prose and
> confidence are not evidence.

---

## Caminho 1 — Auditar (o mais valioso) / Audit (the most valuable)

**PT.** O trabalho mais importante deste repositório não é provar coisas novas —
é encontrar as afirmações falsas que ainda estão marcadas como verdadeiras. Uma
única lema falso já se propagou por vários capítulos (veja
`CLAUDE.md`, seção "KNOWN DEFECT"). Achar o próximo é uma contribuição de primeira
ordem, e você **não precisa saber consertá-lo** — basta abrir uma Issue.

Como caçar (use a *assinatura* do defeito, não o vocabulário):

```bash
# o termo de fronteira δ falsamente afirmado, em qualquer notação
grep -rlE 'δ\(\s*[ηr]\s*[−-]\s*[ηr]' . --include=*.html --include=*.md --include=*.tex
# a dobra pontual + a porta/limiar juntas
grep -ril 'λ|ψ|²ψ' .
grep -ril '\[K,F\]\|\[K, F\]\|commutator lemma' .
```

O padrão a reconhecer: uma derivação que **prova que as duas composições são
iguais** e depois **afirma um δ mesmo assim**. Se encontrar uma que já não esteja
listada em `CLAUDE.md`, abra uma Issue (modelo abaixo). Crédito integral por achar,
mesmo sem consertar.

**EN.** The most important work in this repository is not proving new things — it
is finding the false claims still marked as true. A single false lemma already
propagated across several chapters (see `CLAUDE.md`, "KNOWN DEFECT"). Finding the
next one is a first-order contribution, and you **do not need to know how to fix
it** — just open an Issue.

How to hunt (use the *signature* of the defect, not the vocabulary): the grep
commands above. The pattern to recognise: a derivation that **proves the two
compositions equal** and then **asserts a δ anyway**. If you find one not already
in `CLAUDE.md`, open an Issue (template below). Full credit for finding, even
without fixing.

---

## Caminho 2 — Lean (fechar sorries e problemas abertos) / Lean (close sorries and open problems)

**PT.** Cada capítulo corrigido traz um **exemplo trabalhado** (uma prova pequena,
verificada no núcleo) e um **próximo problema aberto** logo em seguida. O exemplo é
o seu molde; o problema aberto é o seu trabalho. Ganha crédito integral por uma
prova **ou** por uma refutação — mostrar que algo *não* pode ser provado como
enunciado é resultado tão bom quanto prová-lo.

Como verificar o seu trabalho:

1. Núcleo Lean local, se você tem Mathlib compilado:
   ```bash
   lake env lean SeuArquivo.lean
   ```
2. Ou cole no navegador em <https://live.lean-lang.org> (traz Mathlib pronto).
3. **Sempre termine com `#print axioms nome_do_teorema`.** A resposta deve ser
   exatamente `[propext, Classical.choice, Quot.sound]`. Qualquer `sorryAx`
   significa que **não está fechado**, mesmo sem a palavra `sorry` no corpo.

Armadilha aprendida na marra: defina operadores por *pattern match* em `Fin N`,
**nunca** pela notação de vetor `![…]` — as lemas `Matrix.cons_val` do Mathlib não
encadeiam além dos índices baixos num literal `Fin N`, e a forma de vetor falha
silenciosamente em `sorry`. O núcleo pega isso; `#print axioms` é como você fica
sabendo.

Onde começar: Problema Aberto D1-T1′ (cadeia de N sítios, decidível) no capítulo do
riboswitch é o de menor barreira. A partir dele: a generalização D_N de Saturno, a
porta estado-dependente do Cap 18, e o levantamento contínuo do Cap IV.

**EN.** Each repaired chapter carries a **worked example** (a small, kernel-verified
proof) and a **next open problem** right after it. The example is your template;
the open problem is your work. Full credit for a proof **or** a disproof — showing
something *cannot* be proved as stated is as good a result as proving it.

How to check your work: the three steps above. **Always end with
`#print axioms yourTheorem`** — the answer must be exactly
`[propext, Classical.choice, Quot.sound]`; any `sorryAx` means it is **not
closed**, even with no `sorry` in the body. Hard-won trap: pattern-match on
`Fin N`, never `![…]` vector notation. Start with Open Problem D1-T1′ (finite,
decidable); then Saturn's D_N, Ch 18's state-dependent gate, Ch IV's continuum
lift.

---

## Caminho 3 — Tradução / Translation

**PT.** A série é bilíngue PT/EN e a qualidade da tradução importa tanto quanto a
matemática. Duas formas de ajudar: (a) **verificar** traduções existentes contra o
original, (b) **traduzir** um capítulo que ainda não é bilíngue.

Regras que evitam os erros mais comuns:

- **Concordância de gênero.** Ao traduzir para o português, escreva nativamente —
  não traduza palavra a palavra do inglês, que não tem gênero e induz o erro.
  Termos-chave já fixados: *a fumaça*, *a tampa*, *a camada* (fem.); *o limiar*,
  *o acoplamento*, *o operador*, *o teorema*, *o dobramento* (masc.).
- **Não invente números nem citações.** Uma tradução copia o que o original diz;
  se o original está errado, isso é uma Issue (Caminho 1), não um conserto na
  tradução.
- **Não remova uma ressalva ao traduzir.** Se o original diz "(volume a confirmar)",
  a tradução também diz. Uma ressalva só sai pela mesma edição que verifica aquilo
  que ela protege — nunca como faxina.

**EN.** The series is bilingual PT/EN and translation quality matters as much as
the mathematics. Two ways to help: (a) **verify** existing translations against the
original, (b) **translate** a chapter that is not yet bilingual. Rules that prevent
the common errors: write PT natively (do not word-translate genderless English);
never invent numbers or citations (a wrong original is an Issue, not a translation
fix); never drop a caveat in translation — a hedge leaves only by the same edit
that verifies what it protects.

---

## Caminho 4 — Issues e PRs (a mecânica) / Issues and PRs (the mechanics)

### Abrir uma Issue / Open an Issue

**PT.** Use uma Issue para: relatar um defeito que achou (Caminho 1), apontar uma
citação suspeita, ou propor um problema aberto novo. Modelo:

```
Título: [AUDIT] possível δ falso em <arquivo>:<linha>
- Arquivo e linha:
- O que a derivação prova (as duas composições são iguais?):
- O que a derivação afirma mesmo assim (o δ?):
- Já está listado em CLAUDE.md? (sim/não)
```

### Abrir um Pull Request / Open a Pull Request

**PT.** Um PR por unidade de trabalho — uma prova, uma tradução, um conserto. No
texto do PR, inclua:

- **Se é Lean:** a saída de `#print axioms` de cada teorema, colada. Sem isso, não
  é revisável.
- **Se é conserto de defeito:** edição *mínima*. Não reescreva um arquivo que
  funciona — leia, conserte a lema específica, e atualize o ledger em `CLAUDE.md`
  na mesma edição.
- **Se renomeia um teorema:** é uma mudança de quatro arquivos (`.lean`, a lista
  `#print axioms` do CI, o `README`, o `index.html`). Todos os quatro, ou nenhum.
- **Se toca uma etiqueta:** nada migra de `[ABERTO]`/`[MODELO]` para `[VERIFICADO]`
  sem a verificação de núcleo no mesmo PR.

**EN.** Use an Issue to report a defect you found, flag a suspicious citation, or
propose a new open problem (template above, translate freely). One PR per unit of
work. Include: for Lean, the pasted `#print axioms` output of every theorem
(without it, it is not reviewable); for a defect fix, a *minimal* edit (read, fix
the specific lemma, update the `CLAUDE.md` ledger in the same edit — do not rewrite
a working file); renaming a theorem is a four-file change (`.lean`, the CI axiom
list, `README`, `index.html`) — all four or none; a status tag moves to
`[VERIFIED]` only with the kernel check in the same PR.

---

## O que NÃO fazer / What NOT to do

- **Não afirme "provado" sem `#print axioms` limpo.** / Do not claim "proved"
  without a clean `#print axioms`.
- **Não reescreva um arquivo que funciona.** Edição mínima. / Do not wholesale-
  rewrite a working file. Minimal edit.
- **Não remova uma ressalva como faxina.** / Do not remove a caveat as tidying.
- **Não invente citações, autores, ou números.** Verifique na fonte primária. /
  Do not invent citations, authors, or numbers. Check the primary source.
- **Não credencie um teorema como "✓ Lean" se ele depende de `sorry` transitivo.**
  / Do not badge a theorem "✓ Lean" if it depends on a transitive `sorry`.

---

## Crédito / Credit

**PT.** Todo caminho conta. Achar um defeito conta. Uma refutação conta tanto
quanto uma prova. Uma tradução verificada conta. Uma Issue bem escrita que outra
pessoa fecha — conta, e a Issue leva o seu nome. O objetivo não é hierarquia; é um
corpo de matemática que ninguém consegue pegar exagerando uma afirmação.

**EN.** Every path counts. Finding a defect counts. A disproof counts as much as a
proof. A verified translation counts. A well-written Issue that someone else closes
counts, and the Issue carries your name. The goal is not hierarchy; it is a body of
mathematics no one can catch overstating a claim.
