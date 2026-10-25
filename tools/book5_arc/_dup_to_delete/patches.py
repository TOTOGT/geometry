# -*- coding: utf-8 -*-
import re
def setblock(ch, fn, idx_pred, newblock, lang_idx):
    for k,c in enumerate(ch):
        if c[0]==fn: blocks=c[lang_idx]; break
    for i,b in enumerate(blocks):
        if idx_pred(b): blocks[i]=newblock; return
    raise Exception('no block '+fn)
def insert_after(blocks, pred, newblock):
    for i,b in enumerate(blocks):
        if pred(b): blocks.insert(i+1,newblock); return
    raise Exception('no insertion point')

LIT_EN = ("p","<strong>What the literature already has.</strong> The mathematical core is standard and not new. The Boothby–Wang construction gives a contact form on a principal circle bundle from a connection whose curvature is symplectic on the base. Hamilton's classification of Boothby–Wang 5-manifolds (arXiv:1001.1953) states it for U(1)-bundles over symplectic 4-manifolds, where “curvature symplectic” means F is nondegenerate, which on a four-dimensional base is the same as F ∧ F ≠ 0. Ding and Geiges (arXiv:1107.4948) treat contact structures on principal circle bundles in general. On the physics side, Goto (arXiv:2310.17925) ties F ∧ F ≠ 0 to symplectic and contact structures for Maxwell fields on three-dimensional slices of Lorentzian four-manifolds with parallel E and B, and Eager, Gary and Roberts (arXiv:1011.5231) write Sasaki–Einstein five-manifolds as U(1) bundles and Kaluza–Klein reduce on them. A delegated search found no source that states the explicit Kaluza–Klein reading, η = dy + κA with contact exactly where E·B ≠ 0, or the Darboux example in Kaluza–Klein language. That search was limited (about eight web searches; abstracts and excerpts, not full papers; Boyer–Galicki and Geiges' textbook not checked), so it is not a claim of novelty. Treat the contact condition as a known fact in new dress.")
LIT_PT = ("p","<strong>O que a literatura já tem.</strong> O núcleo matemático é padrão e não é novo. A construção de Boothby–Wang fornece uma forma de contato num fibrado principal em círculos a partir de uma conexão cuja curvatura é simplética na base. A classificação de Hamilton das 5-variedades de Boothby–Wang (arXiv:1001.1953) enuncia isso para U(1)-fibrados sobre 4-variedades simpléticas, onde “curvatura simplética” significa que F é não degenerada, o que numa base de dimensão quatro equivale a F ∧ F ≠ 0. Ding e Geiges (arXiv:1107.4948) tratam de estruturas de contato em fibrados principais em círculos em geral. Do lado da física, Goto (arXiv:2310.17925) liga F ∧ F ≠ 0 a estruturas simpléticas e de contato para campos de Maxwell em fatias tridimensionais de 4-variedades lorentzianas com E e B paralelos, e Eager, Gary e Roberts (arXiv:1011.5231) escrevem as 5-variedades de Sasaki–Einstein como U(1)-fibrados e fazem a redução de Kaluza–Klein sobre elas. Uma busca delegada não encontrou fonte que enuncie a leitura explícita de Kaluza–Klein, η = dy + κA com contato exatamente onde E·B ≠ 0, nem o exemplo de Darboux em linguagem de Kaluza–Klein. Essa busca foi limitada (cerca de oito buscas na web; resumos e trechos, não artigos completos; Boyer–Galicki e o livro-texto de Geiges não foram consultados); portanto não é uma afirmação de novidade. Trate a condição de contato como um fato conhecido em roupa nova.")
def apply_en(CH):
    L=1+3  # blocks index in tuple
    setblock(CH,'chV-contact-kk.html',lambda b:b[0]=='p' and b[1].startswith('Two careful comparisons'),
      ("p","Grabowska and Grabowski (arXiv:2207.04484) work in contact Hamiltonian mechanics and mention Kaluza–Klein in one sentence of analogy; they do not derive the condition above. Reduction of Kaluza–Klein by a circle gives a magnetic, symplectic coupling; contact reduction uses an R<sup>×</sup> scaling action. They resemble each other without being the same."),4)
    for c in CH:
        if c[0]=='chV-contact-kk.html': insert_after(c[4],lambda b:b[0]=='p' and b[1].startswith('Grabowska'),LIT_EN)
    setblock(CH,'chV-contact-kk.html',lambda b:b[0]=='st' and b[1]=='[NOT DONE]',
      ("st","[NOT DONE]","Not checked in Lean. The literature check found the core to be standard (previous paragraph); the Kaluza–Klein/E·B phrasing was not found stated, but absence of hits is not proof of novelty. The Book 4 jet-space chapter's space, J¹(ℝ, ℝ²), is a different object (a rank-2 Pfaffian system, not a contact manifold; Book 4 Chapter 5 now says so); a true contact 5-manifold in that family is J¹(ℝ², ℝ). Nothing here rescues or confirms the Book 4 construction."),4)
    for c in CH:
        if c[0]=='chV-ledger.html':
            insert_after(c[4],lambda b:b[0]=='p' and b[1].startswith('van Dongen'),("p","Literature check on the contact condition (delegated web search, abstracts and excerpts only, then spot-checked by me against the arXiv abstracts of Hamilton and Goto): Hamilton, arXiv:1001.1953; Ding and Geiges, arXiv:1107.4948; Goto, arXiv:2310.17925; Eager, Gary and Roberts, arXiv:1011.5231; Dahl, arXiv:0811.2002. The Ding–Geiges, Eager–Gary–Roberts and Dahl entries rest on the search agent's report and were not independently opened."))
    setblock(CH,'chV-ledger.html',lambda b:b[0]=='p' and b[1].startswith('The contact condition'),
      ("p","The contact condition η∧(dη)² = κ² dy∧F∧F, the constant-field example, and the Darboux identification of J¹(ℝ²,ℝ). Now known to be a standard Boothby–Wang fact in new dress. One symbolic check of R<sub>(5)</sub> = −κ²B²/2. None of these is formalized in Lean."),4)
    setblock(CH,'chV-ledger.html',lambda b:b[0]=='p' and b[1].startswith('A literature check'),
      ("p","A fuller literature check (Boyer–Galicki, <em>Sasakian Geometry</em>; Geiges, <em>An Introduction to Contact Topology</em>; Lerman); the original Einstein–Bergmann paper; the reconciliation of Klein's 0.8×10⁻³⁰ cm with the ≈23 Planck lengths in modern conventions; the Book 4 Chapter 6 construction (corrected in place, with Theorem T1 not re-examined). The Portuguese edition exists as a machine-assisted draft that has not been reviewed by a native speaker."),4)
def apply_pt(P):
    def sb(fn,pred,nb):
        blocks=P[fn][3]
        for i,b in enumerate(blocks):
            if pred(b): blocks[i]=nb; return
        raise Exception(fn)
    sb('chV-contact-kk.html',lambda b:b[0]=='p' and b[1].startswith('Duas comparações'),
      ("p","Grabowska e Grabowski (arXiv:2207.04484) trabalham com mecânica hamiltoniana de contato e mencionam Kaluza–Klein numa frase de analogia; não deduzem a condição acima. A redução de Kaluza–Klein por um círculo dá um acoplamento magnético, simplético; a redução de contato usa uma ação de escala de R<sup>×</sup>. Parecem-se sem serem a mesma coisa."))
    insert_after(P['chV-contact-kk.html'][3],lambda b:b[0]=='p' and b[1].startswith('Grabowska'),LIT_PT)
    sb('chV-contact-kk.html',lambda b:b[0]=='st',
      ("st","[NÃO FEITO]","Não verificado em Lean. A verificação na literatura mostrou que o núcleo é padrão (parágrafo anterior); a formulação em termos de Kaluza–Klein/E·B não foi encontrada enunciada, mas a ausência de resultados não prova novidade. O espaço do capítulo de espaço de jatos do Livro 4, J¹(ℝ, ℝ²), é outro objeto (um sistema de Pfaff de posto 2, não uma variedade de contato; o Capítulo 5 do Livro 4 agora diz isso); uma 5-variedade de contato verdadeira nessa família é J¹(ℝ², ℝ). Nada aqui resgata ou confirma a construção do Livro 4."))
    insert_after(P['chV-ledger.html'][3],lambda b:b[0]=='p' and b[1].startswith('van Dongen'),("p","Verificação na literatura sobre a condição de contato (busca na web delegada, apenas resumos e trechos, depois conferida por mim nos resumos do arXiv de Hamilton e de Goto): Hamilton, arXiv:1001.1953; Ding e Geiges, arXiv:1107.4948; Goto, arXiv:2310.17925; Eager, Gary e Roberts, arXiv:1011.5231; Dahl, arXiv:0811.2002. As entradas de Ding–Geiges, Eager–Gary–Roberts e Dahl baseiam-se no relatório do agente de busca e não foram abertas de forma independente."))
    sb('chV-ledger.html',lambda b:b[0]=='p' and b[1].startswith('A condição de contato'),
      ("p","A condição de contato η∧(dη)² = κ² dy∧F∧F, o exemplo de campo constante e a identificação de Darboux de J¹(ℝ²,ℝ). Agora se sabe que é um fato padrão de Boothby–Wang em roupa nova. Uma verificação simbólica de R<sub>(5)</sub> = −κ²B²/2. Nada disso foi formalizado em Lean."))
    sb('chV-ledger.html',lambda b:b[0]=='p' and b[1].startswith('Uma verificação na literatura'),
      ("p","Uma verificação mais ampla da literatura (Boyer–Galicki, <em>Sasakian Geometry</em>; Geiges, <em>An Introduction to Contact Topology</em>; Lerman); o artigo original de Einstein–Bergmann; a reconciliação dos 0,8×10⁻³⁰ cm de Klein com os ≈23 comprimentos de Planck nas convenções modernas; a construção do Capítulo 6 do Livro 4 (corrigida no local, com o Teorema T1 não reexaminado). A edição em português existe como rascunho assistido por máquina, ainda não revisado por um falante nativo."))
