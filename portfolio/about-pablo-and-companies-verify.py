#!/usr/bin/env python3
"""Checks portfolio/about-pablo-and-companies.html: CNPJ check digits (mod 11), identifier
formats, and that unverified registry status is not asserted."""
import re, os, sys
here=os.path.dirname(os.path.abspath(__file__))
page=open(os.path.join(here,'about-pablo-and-companies.html'),encoding='utf-8').read()
ok=[]
def chk(n,c): ok.append(bool(c)); print(('PASS ' if c else 'FAIL ')+n)
def cnpj_valid(s):
    d=[int(c) for c in re.sub(r'\D','',s)]
    if len(d)!=14 or len(set(d))==1: return False
    def dv(x,w): 
        r=sum(a*b for a,b in zip(x,w))%11
        return 0 if r<2 else 11-r
    w1=[5,4,3,2,9,8,7,6,5,4,3,2]; w2=[6]+w1
    return dv(d[:12],w1)==d[12] and dv(d[:13],w2)==d[13]
m=re.search(r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}',page)
chk('page prints a CNPJ',m is not None)
chk('CNPJ check digits valid (mod 11)',m and cnpj_valid(m.group(0)))
chk('CNPJ is 02.493.678/0001-89',m and m.group(0)=='02.493.678/0001-89')
chk('EIN format NN-NNNNNNN',re.search(r'\b33-2880433\b',page) is not None)
chk('UEI is 12 alphanumerics',re.search(r'\bCHGKT9317LY3\b',page) is not None and len('CHGKT9317LY3')==12)
chk('page says CNPJ status not verified against Receita Federal','not been verified' in page.lower() and 'Receita Federal' in page)
chk('page does not assert the Brazilian company is active','situação cadastral: ativa' not in page.lower() and 'is active' not in page.lower())
print('%d/%d checks passed'%(sum(ok),len(ok))); sys.exit(0 if all(ok) else 1)
