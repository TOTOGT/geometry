# Relatório de Invenção — Substrato Nutriente Aperiódico Estruturado

**Minuta de trabalho para agente/advogado de patentes. Não constitui parecer jurídico.** As reivindicações abaixo são esqueletos ilustrativos, a serem revisados, restringidos e redigidos por profissional habilitado (agente da propriedade industrial / advogado). Ver §7 (divulgação/prioridade) — as divulgações públicas já feitas (Zenodo/site/livro) já iniciaram prazos. Referências legais ao **INPI** e à **Lei da Propriedade Industrial (LPI), Lei nº 9.279/1996**; notas para PCT/exterior onde diferem.

**Inventor:** Pablo Nogueira Grossi · G6 LLC, Newark NJ · ORCID 0009-0000-6496-2186
**Relacionado:** Livro 6 · Cap. DE-3 — [*Meios Multiplicadores Aperiódicos* (capítulo ao vivo)](https://totogt.github.io/geometry/book6/ch-aperiodic-multiplying-media.html); Livro 3 Cap. η (DNLS); artigo companheiro de criticalidade (Zenodo 10.5281/zenodo.20077205)

---

## 1. Campo técnico

Substratos nutrientes estruturados, meios de cultura/fermentação, ração animal e enchimentos (packings) de biorreator cuja distribuição de nutrientes é ordenada por uma regra aperiódica (de substituição), a fim de controlar o limiar de criticalidade de crescimento (limiar de persistência / lavagem — *washout*) de uma população biológica.

## 2. O problema técnico

Substratos nutrientes periódicos ou homogêneos apresentam um limiar de criticalidade de crescimento fixado apenas pela composição, que não escala de forma previsível da bancada à planta industrial. Culturas em alimentação pobre ou flutuante tendem à lavagem (*washout*) com pouca margem de projeto.

## 3. A invenção (em uma frase)

Um substrato nutriente no qual os domínios portadores de nutriente são dispostos ao longo de um eixo espacial por uma **regra de substituição primitiva** de ordem de inflação *n* (Fibonacci n=2, tribonacci n=3, …), de modo que o autovalor de inflação λ_PF se torna um **parâmetro de projeto** que fixa o limiar de criticalidade de crescimento — um *n* maior eleva o limiar, conferindo robustez contra flutuação de nutrientes e tornando a criticalidade do biorreator covariante sob inflação (escalonamento previsível).

## 4. O efeito inesperado (âncora de atividade inventiva)

O limiar de autoaprisionamento / persistência sobe com *n* como uma **diferença de regime, não apenas de magnitude**: numericamente λ_c(n) ≈ 0,958·Δ_n + 0,107 (r = 0,989), e um ordenamento tribonacci (η ≈ 1,8393 > φ ≈ 1,6180) mantém uma população localizada coesa sob alimentação mais pobre do que um ordenamento Fibonacci de composição global idêntica. Essa vantagem surpreendente, decorrente apenas da estrutura — mesmos ingredientes, margem de sobrevivência diferente — é a âncora de **atividade inventiva (LPI art. 13)**.

---

## 5. Ativo mais forte — par composição + método de uso

### Reivindicação independente de composição (produto)

> **1.** Substrato nutriente estruturado para suportar crescimento biológico, compreendendo uma matriz sólida ou em gel que define, ao longo de pelo menos um eixo espacial, uma pluralidade de domínios portadores de nutriente separados por regiões intersticiais de transporte, caracterizado por o ordenamento dos domínios portadores de nutriente ao longo do referido eixo seguir uma regra de substituição primitiva cuja matriz de inflação possui um autovalor de Perron–Frobenius λ_PF maior que 1, de modo que o perfil de concentração local de nutriente ao longo do referido eixo seja aperiódico e não periódico, com uma razão característica de comprimento de domínio determinada pela referida regra de substituição.

Reivindicações dependentes (restrições):

> **2.** Substrato de acordo com a reivindicação 1, caracterizado por a regra de substituição ser a regra tribonacci (a→ab, b→ac, c→a), de modo que λ_PF = η seja a raiz real de x³ − x² − x − 1 = 0 em (1,2), η ≈ 1,8393.
>
> **3.** Substrato de acordo com a reivindicação 1, caracterizado por a regra de substituição ser uma regra n-bonacci com n ≥ 3, de modo que λ_PF > φ.
>
> **4.** Substrato de acordo com a reivindicação 1, caracterizado por os domínios portadores de nutriente possuírem comprimentos característicos entre [X] e [Y] micrômetros. *(preencher a partir da concretização)*
>
> **5.** Substrato de acordo com a reivindicação 1, caracterizado por a matriz compreender um dentre: hidrogel reticulado; pélete de ração extrudado; arcabouço (scaffold) fabricado por manufatura aditiva (impressão 3D); multicamada moldada.
>
> **6.** Substrato de acordo com a reivindicação 1, **caracterizado por** um modo de crescimento de meia-banda (mid-gap) suportado pelo substrato apresentar uma razão de participação inversa (IPR) de pelo menos K× a de um substrato ordenado por Fibonacci de composição global idêntica. *(limitação estrutural-funcional que carrega o efeito inesperado; fixar K ≈ 3,5–4 a partir de dados)*
>
> **7.** Substrato de acordo com a reivindicação 1, caracterizado por ser adaptado como arcabouço (scaffold) para células animais cultivadas, para produção de carne cultivada.

### Reivindicação independente de método de uso

> **8.** Método de cultivo de uma população de organismos, compreendendo: fornecer um substrato nutriente estruturado de acordo com a reivindicação 1; inocular o substrato com o organismo; e manter condições de cultivo sob as quais a população se localize preferencialmente sobre os domínios portadores de nutriente; caracterizado por a ordem de inflação *n* da regra de substituição ser selecionada de modo que o limiar de persistência da população — a concentração média crítica de nutriente, ou o contraste crítico entre domínios, abaixo do qual a população é lavada (*washout*) — fique acima de um valor-alvo, conferindo assim robustez do cultivo contra flutuação no suprimento de nutrientes.

Dependentes:

> **9.** Método de acordo com a reivindicação 8, compreendendo selecionar n = 3 em vez de n = 2 para elevar o limiar de persistência.
>
> **10.** Método de acordo com a reivindicação 8, caracterizado por o organismo ser uma cepa de fermentação microbiana, uma cultura probiótica ou uma linhagem de células de mamífero.
>
> **11.** Método de acordo com a reivindicação 8, caracterizado por a seleção da ordem de inflação *n* compreender **fabricar** o substrato com uma sequência física de domínios de ordem de inflação *n*. *(vincula a seleção a um ato físico — ver §6)*

---

## 6. Mantendo as reivindicações de "método de projeto" fora da vedação legal (LPI art. 10)

Uma reivindicação que recite "calcular λ_PF" ou "selecionar n para maximizar um limiar" como etapa isolada é um **método matemático / concepção puramente abstrata**, não considerada invenção (LPI art. 10, I e II; correlato ao *Alice/Mayo* nos EUA e ao art. 52 CPE na Europa). A solução é **nunca reivindicar o cálculo isoladamente** — sempre incorporar a escolha de projeto a uma transformação física com resultado estrutural mensurável:

### Reivindicação independente de processo de fabricação (forma segura do "método de projeto")

> **12.** Processo de fabricação de um substrato nutriente estruturado, compreendendo: determinar uma sequência espacial de domínios a partir de uma regra de substituição primitiva de ordem de inflação *n*; e **depositar material nutriente** para formar domínios portadores de nutriente fisicamente dispostos na referida sequência ao longo de um eixo espacial, por manufatura aditiva, extrusão ou moldagem em camadas, de modo que o substrato resultante apresente um perfil de concentração de nutriente aperiódico cuja razão característica de comprimento de domínio seja fixada por λ_PF.

Aqui "determinar a sequência" é uma limitação sobre a *etapa física de deposição e sobre o artigo resultante*, não um elemento reivindicado isoladamente — a reivindicação depende da fabricação de um objeto real. Esse é o padrão que supera a vedação do art. 10.

### Método de controle de qualidade (combina com calorimetria de bomba)

> **13.** Método de qualificação de uma ração ou substrato, compreendendo: medir uma densidade calórica do substrato por calorimetria de bomba de oxigênio; determinar, por caracterização estrutural, a ordem de inflação *n* da sequência de domínios; e aprovar o substrato quando tanto a densidade calórica quanto a ordem de inflação atenderem à especificação. *(especificação de dois parâmetros: energia + margem de robustez)*

---

## 7. Suficiência descritiva e prioridade — itens de ação

- **Suficiência descritiva (LPI art. 24; correlato §112 EUA).** A concretização em nutrição está atualmente *prevista, não testada*. Antes de um depósito amplo, incluir ao menos um exemplo profético e, idealmente, um ensaio de fermentação/cultivo demonstrando o deslocamento de limiar entre substratos n = 2 e n = 3 de composição global idêntica. Isso converte a limitação K× da reivindicação 6 de afirmação em demonstração.
- **Busca de anterioridades (novidade — LPI art. 11).** Pesquisar estado da técnica sobre: estruturação aperiódica/Fibonacci/quasicristalina de ração, hidrogéis e arcabouços; enchimentos estruturados de biorreator; liberação padronizada de nutrientes; geometria de arcabouço para carne cultivada.
- **Prioridade / período de graça.** O arcabouço teórico já foi divulgado publicamente (preprints no Zenodo, totogt.github.io, capítulo do Livro 6).
  - **Brasil (LPI art. 12):** há **período de graça de 12 meses** contados da primeira divulgação feita pelo próprio inventor.
  - **EUA (35 USC §102(b)):** período de graça de 1 ano da primeira divulgação *da concretização de produto*.
  - **Europa (CPE) e maioria das jurisdições:** **novidade absoluta** — a autodivulgação anterior pode já constituir impedimento.
  - **Ação:** levantar a data exata da primeira publicação de qualquer texto que descreva a *ração/substrato físico* (não apenas a matemática abstrata) e tratar um depósito de prioridade (pedido provisório/depósito INPI) como **urgente**.

## 8. Concretizações comerciais (por prioridade)

1. **Arcabouços para carne cultivada** — arcabouços estruturados de nutriente/oxigênio para agricultura celular; fronteira forte de PI; adjacência direta aos interesses da JBS/Friboi em carne cultivada.
2. **Insumos para fermentação de precisão** — robustez contra flutuação de alimentação em fermentação industrial.
3. **Péletes estruturados de ração animal** — perfil de liberação de nutrientes engenheirado com margem de robustez.
4. **Suportes de biofilme / tratamento de água** — meios suporte aperiódicos para culturas em efluentes.
