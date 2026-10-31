#!/usr/bin/env python3
"""Checks Chapter 2: offline-safe, counting table complete, unchecked cells marked, links resolve."""
import re, os, sys
d=os.path.dirname(os.path.abspath(__file__))
t=open(os.path.join(d,'ch02-five-languages.html'),encoding='utf-8').read()
ok=True
def check(n,c):
    global ok
    print(('PASS ' if c else 'FAIL ')+n); ok&=bool(c)
check('no outside resources',not re.search(r'<link\b|<script\b|<img\b|url\(',t))
tbl=t.split('Lesson 1.')[1].split('Lesson 2.')[0]
rows=re.findall(r'<tr><td>(\d+)\. ',tbl)
check('counting table has rows 1..10',rows==[str(i) for i in range(1,11)])
cells=re.findall(r'<tr><td>\d+\. .*?</tr>',tbl)
check('every row has 6 language cells',all(len(re.findall(r'<td',c))==6 for c in cells))
check('Nepali and Tibetan cells carry lang tags and romanization',all('lang="ne"' in c and 'lang="bo"' in c and c.count('class="rom"')==2+('lang="yrl"' in c) for c in cells))
check('Dzongkha cells are blank prompts, not filled in',all(re.search(r'<td lang="dz"><span class="blank">find out',c) for c in cells))
check('Tupi-Guarani: only sourced iepé and mukui filled, rest blank prompts',[c.count('find out') for c in cells]==[1,1]+[2]*8 and 'iep' in cells[0] and 'mukui' in cells[1] and sum('lang="yrl"' in c for c in cells)==2)
sk=t.split('Lesson 4.')[1].split('What comes next')[0]
skrows=re.findall(r'<tr><td>(\d+)</td>(.*?)</tr>',sk,re.S)
check('Sanskrit table has rows 1..10 with 5 cells each',[r[0] for r in skrows]==[str(i) for i in range(1,11)] and all(len(re.findall(r'<td',"<td>"+r[1]))==5 for r in skrows))
check('Panini facts sourced (3,983 sutras, eight chapters, dating uncertain)','3,983' in sk and 'eight chapters' in sk and 'uncertain' in sk)
check('Sanskrit numerals marked to confirm','to confirm with a Sanskrit speaker' in sk)
check('UN box sourced and scoped (A/RES/71/178, 2022-2032, Plan not opened)','A/RES/71/178' in t and '2022&ndash;2032' in t and 'Global Action Plan document itself was not opened' in t)
check('Brazil proposal sourced, not claimed as adopted','Carta de Bel' in t and 'nothing saying the government has adopted' in t)
check('Amondawa box sourced, with the narrower claim and the unchecked Hopi/Pirahã flagged','Amondawa' in t and 'not what the authors say' in t and 'I have not checked them here' in t and 'full paper was not read' in t)
check('Oral-traditions box: consent stated, practice marked as author proposal','Oral traditions' in t and 'speakers decide' in t and 'not drawn from a guideline' in t)
check('unchecked Tibetan sentence is marked, not invented','for a Tibetan speaker to write' in t)
check('to-confirm box present','To confirm' in t)
check('Portuguese blocks present','lang="pt"' in t)
for h in re.findall(r'href="([^"#]+)"',t):
    if not h.startswith('http'): check('link '+h,os.path.exists(os.path.join(d,h)))
# controls: a table row missing a language cell, or an outside <link>, must be caught
check('control: short row caught',len(re.findall(r'<td','<tr><td>1. one</td><td>um</td></tr>'))!=6)
check('control: outside link caught',bool(re.search(r'<link\b','<link href=x>')))
sys.exit(0 if ok else 1)
