#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""wp137-verify.py -- companion to book6/wp137-reading-newarks-budget.html. Written 2026-10-21 (R6, R24: run BEFORE the page's sentences).
SOURCE FILES (read by pdftotext on 2026-10-21, copied by hand into this script): '2026 UFB Budget - Newark.pdf' (State of NJ Municipal User Friendly
Budget, year 2026, Municode 0714) and '2025_UFB_Template_FINAL - INTRODUCED BUDGET.pdf' (same form, year 2025; its file name says INTRODUCED).
RECOMPUTED: whether each sheet's columns foot; the rate-versus-levy reconciliation; the debt arithmetic; the valuation ratio; the share of the
general budget that the city itself flags as non-recurring; the levy needed to replace flagged items, per average home; a seeded toy simulation.
NOT A SOURCE FOR: Newark's year-end fund balance (not on the form; it is in the audit), whether any figure is adopted or introduced for 2026 (the
2026 file does not say), or any statement that Newark is in fiscal stress. Nothing here is an audit."""
import math, os, sys, random
fails=[]
def check(ok,msg):
    print('    %s  %s'%('PASS' if ok else 'FAIL',msg))
    if not ok: fails.append(msg)
def head(n,t): print('\n'+'='*72+'\n  [%s]  %s\n'%(n,t)+'='*72)
def near(a,b,tol=0.01): return abs(a-b)<=tol

head(1,'2026: does the general-budget column foot, and does it balance?')
rev26=[4106000.00,184788870.00,110017552.00,5108702.00,32838896.96,254880172.43,20493000.00,275401182.48,10454979.57,2410909.50]
ap26=[72488126,1734927,7872319,136659000,287881564,51088935,9387778,11825405,11975000,75334704,13169750,7500000,105773260.48,9095546,100000,73371221,5200000,3476597.50,20351000,4106000]
GBrev26,GBap26=sum(rev26),sum(ap26)
print('    UFB-2 general-budget revenue lines sum %.2f ; UFB-3 general-budget appropriation lines sum %.2f'%(GBrev26,GBap26))
check(near(GBrev26,900500264.94),'revenue lines foot to the printed column total 900,500,264.94')
check(near(GBap26,908391132.98),'appropriation lines foot to the printed column total 908,391,132.98')
check(near(880149264.94+20351000.00,900500264.94),'UFB-1 appropriations before RUT + RUT = the revenue column (UFB-1 balances)')
gap26=GBap26-GBrev26
print('    UFB-3 general column exceeds UFB-2 general column by %.2f (UFB-3 minus UFB-1 summary: %.2f)'%(gap26,GBap26-900500264.94))
check(near(gap26,7890868.04),'the two sheets differ by 7,890,868.04; this script does NOT explain it')


print('    printed all-funds totals 2026: revenue 1,066,000,138.34, appropriations 1,108,746,903.34 -> difference %.2f'%(1066000138.34-1108746903.34))
check(near(1066000138.34-1108746903.34,-42746765.00),'2026 printed all-funds revenue is 42,746,765.00 BELOW printed all-funds appropriations (not explained here)')
print('    printed all-funds totals 2025 (introduced): revenue 1,127,128,648.60, appropriations 1,151,608,648.60 -> difference %.2f'%(1127128648.60-1151608648.60))
check(near(1127128648.60-1151608648.60,-24480000.00),'2025 printed all-funds revenue is 24,480,000.00 below printed appropriations (not explained here)')

head(2,'2025 (introduced file): same test')
rev25=[23850000.00,178708358.00,140017552.00,6255206.00,79933680.40,214764284.99,24840000.00,285637699.92,8910231.68,7263777.28]
ap25=[65939814,1817275,8075630,148126983,270769507,58859881,8821000,10697277,11975000,63866721,12596080,0,108971611,8984644,100000,73025428,2535000,9926798.50,24850000,23850000]
GBrev25,GBap25=sum(rev25),sum(ap25)
print('    revenue lines %.2f ; appropriation lines %.2f'%(GBrev25,GBap25))
check(near(GBrev25,970180790.27),'revenue lines foot to 970,180,790.27')
check(near(945330790.27+24850000.00,970180790.27),'UFB-1 appropriations before RUT + RUT(UFB-3 line 50 = 24,850,000) = revenue column')
print('    UFB-1 header of the 2025 file shows RUT 23,344,000 while its own UFB-3 line 50 shows 24,850,000; the 2026 file calls 23,344,000 the prior-year figure')
check(23344000.00!=24850000.00,'the 2025 introduced file carries two different RUT figures; the 2026 file supports 23,344,000 as the final prior-year value')
print('    general-column appropriation sum minus revenue column (2025): %.2f'%(GBap25-GBrev25))
check(near(GBap25-GBrev25,-56392140.77),'in the 2025 introduced file the UFB-3 general column is 56,392,140.77 BELOW the revenue column (UFB-1 balances); not explained here')

head(3,'surplus drawn against the general budget')
sur=[('2024 (prior col., 2025 file)',43000000.00,None),('2025 (2025 file, introduced; 2026 file prior col. agrees)',23850000.00,GBrev25),('2026',4106000.00,GBrev26)]
for n,s,g in sur: print('    %-58s %14.2f %s'%(n,s,'' if g is None else ' = %.3f%% of general-budget revenue'%(100*s/g)))
check(near(100*23850000/GBrev25,2.458,0.001),'2025 surplus draw is 2.458% of general-budget revenue')
check(near(100*4106000/GBrev26,0.456,0.001),'2026 surplus draw is 0.456% of general-budget revenue')
check(near(4106000/23850000,0.17216,0.0001),'2026 draw is 17.2% of the 2025 draw (-82.78% as printed)')

head(4,'what the city itself flags as non-recurring (UFB-4 list)')
L26={'Surplus':4106000,'Water Utility Fund Balance':10000000,'Sewer Utility Fund Balance':7000000,'Hess Trust Fund':100000,'Community Economic Development Trust Fund':3463045,
 'Sale of Municipal Assets-Group A':7135778,'Sale of Municipal Assets-Group B':22265800,'Sale of Municipal Assets-Group C':32571800,'Sale of Municipal Assets':19400000,
 'Cancellation of Improvement Authorizations':2923510.75,'Cancellation of Outstanding Checks':2346000,'Cancellation of Trusts':1144864.68}
L25={'Surplus':23850000,'Transitional Aid Loan':30000000,'Water Utility Fund Balance':14000000,'Sewer Utility Fund Balance':18800000,'Newark Housing Authority Demolition':4000000,
 'Cancellation of Commitments Payable':1282314.26,'Cancellation of Appropriation Reserves':9980450,'Hess Trust Fund':4500000,'Community Economic Development Trust Fund':3700000}
UT=('Water Utility Fund Balance','Sewer Utility Fund Balance')
t26,t25=sum(L26.values()),sum(L25.values())
g26=sum(v for k,v in L26.items() if k not in UT); g25=sum(v for k,v in L25.items() if k not in UT)
sales26=sum(v for k,v in L26.items() if k.startswith('Sale of Municipal'))
print('    2026 list total %.2f ; excluding the two utility-fund balances %.2f ; asset-sale lines %.2f'%(t26,g26,sales26))
print('    2025 list total %.2f ; excluding the two utility-fund balances %.2f'%(t25,g25))
check(near(t26,112456798.43),'2026 list totals 112,456,798.43')
check(near(g26,95456798.43),'2026 list without utility fund balances 95,456,798.43')
check(near(sales26,81372938.00-0.00+0.0,1.0) or near(sales26,81373378.00,1.0),'2026 asset-sale lines total about 81.37 million (%.2f)'%sales26)
check(near(t25,110112764.26,0.01),'2025 list totals 110,112,764.26')
s26,s25=100*g26/GBrev26,100*g25/GBrev25
print('    flagged general-side items as a share of general-budget revenue: 2025 %.2f%%  2026 %.2f%%'%(s25,s26))
check(s26>s25,'the flagged share ROSE from 2025 to 2026 even though the surplus draw fell by 82.78%')
check(near(s25,7.97,0.01) and near(s26,10.60,0.01),'shares are 7.97% and 10.60%')
check(near(100*sales26/g26,85.25,0.01),'the four asset-sale lines are 85.25%% of the flagged general-side total (%.2f%%)'%(100*sales26/g26))
print('    caution: the UFB-4 lines are the city\'s own tick-box flags; this script does not map them to revenue lines on UFB-2')

head(5,'valuation, rate and levy (UFB-1, 2026)')
val26,eq26=12785121100.00,26763912706.72
check(near(100*val26/eq26,47.77,0.01),'taxable valuation / equalized valuation = 47.77% (printed average ratio 47.77%)')
lev26,lev25=275401182.48,283584246.67
print('    levy / valuation = %.4f per $100 ; printed municipal-purposes rate 2.016'%(100*lev26/val26))
check(near(100*lev26/val26,2.1542,0.0005),'levy / valuation is 2.154 per $100')
check(not near(100*lev26/val26,2.016,0.01),'that does NOT equal the printed 2.016')
print('    levy change %.2f%% ; valuation change (2025 file 12,769,266,100 -> 12,785,121,100) %.2f%% ; implied rate change %.2f%% ; printed rate change %.2f%%'%(
    100*(lev26/lev25-1),100*(val26/12769266100.00-1),100*((lev26/val26)/(lev25/12769266100.00)-1),100*(2.016/2.218-1)))
check(near(100*(lev26/lev25-1),-2.89,0.01),'levy change -2.89% as printed')
check(near(100*(2.016/2.218-1),-9.12,0.02),'printed rate change -9.12%% (the three-decimal rates give %.2f%%; the sheet presumably divides unrounded rates)'%(100*(2.016/2.218-1)))
check(abs(100*((lev26/val26)/(lev25/12769266100.00)-1)-(-9.12))>5,'the levy and valuation figures imply about -3.0%, not -9.12%: unreconciled on the sheet')
print('    average residential payment: 191,563 x 2.016/100 = %.2f (printed 3,861.53)'%(191563*2.016/100))
check(near(191563*2.016/100,3861.53,0.5),'the printed average payment follows the printed rate, not the levy')

head(6,'debt arithmetic (UFB-10, 2026)')
check(near(759701874.59-500565790.65,259136083.94),'gross debt minus deductions = net debt 259,136,083.94')
check(near(100*259136083.94/26999413197.67,0.96,0.005),'net debt is 0.96% of the 3-year average valuation')
check(near(759701874.59/311549,2438.47,0.01),'per-capita gross debt 2,438.47')
check(near(43995319+18666700,62662019),'principal + interest = 62,662,019 debt service')
check(near(100*62662019/1108746903.34,5.65,0.005),'debt service is 5.65% of the 1,108,746,903.34 total budget')

head(7,'what replacing the flagged items from the levy would cost (arithmetic, not a forecast)')
col=0.9624; avg=191563.0
per_m=1e6/col/val26*avg
print('    each $1,000,000 of levy (grossed up by the 96.24%% collection rate used for RUT) costs the average residential assessment ($191,563) $%.2f a year'%per_m)
check(near(per_m,15.57,0.05),'$15.57 per $1 million per average home')
for p in (0,.25,.5,.75,1.0):
    need=p*g26/col; print('    replace %3d%% of the %.2f flagged general-side items: levy +%.2f million = +%.2f%% of the 2026 municipal-purposes levy = +$%.0f per average home'%(p*100,g26/1e6,need/1e6,100*need/lev26,need/val26*avg))
full=g26/col/val26*avg
check(near(full,1486.0,2.0),'full replacement is about $1,486 per average home (constant valuation assumed)')

head(8,'toy simulation: each flagged item independently repeats with probability p (p is an assumption, not data; seed fixed)')
random.seed(137)
items=[v for k,v in L26.items() if k not in UT]
def sim(p,n=20000):
    out=[]
    for _ in range(n):
        lost=sum(v for v in items if random.random()>p)
        out.append(lost/col/val26*avg)
    out.sort(); return sum(out)/n,out[int(.05*n)],out[int(.95*n)]
for p in (.25,.5,.75):
    m,lo,hi=sim(p); print('    p=%.2f : mean +$%.0f per average home, 5-95%% range $%.0f to $%.0f'%(p,m,lo,hi))
m50,_,_=sim(.5)
check(abs(m50-0.5*full)<40,'mean at p=0.5 is close to half of full replacement (expectation is linear: %.0f vs %.0f)'%(m50,.5*full))
print('    the simulation adds only a spread; the mean is already given by the arithmetic in block 7. It models nothing about Newark beyond the 10 flagged lines.')


head('9a','the balance behind the draw: 2021 audit and the 2023 budget\'s Condition of Surplus sheet (OCR / text of the PDFs; read 2026-10-21)')
fb20,use21,ex21,fb21=37296982.41,11700000.00,27791935.91,53388918.32
check(near(fb20-use21+ex21,fb21),'2021 audit: 37,296,982.41 - 11,700,000.00 + 27,791,935.91 = 53,388,918.32 (current-fund balance, 31 Dec 2021)')
a21,a22,u22,u23=53375084.83,77859942.23,25000000.00,60000000.00   # 2023 adopted budget, Condition of Surplus: prior-year and budget-year columns
check(near(a21-u22,28375084.83),'2023 budget sheet: 53,375,084.83 - 25,000,000.00 = 28,375,084.83 remaining (printed)')
check(near(a22-u23,17859942.23),'2023 budget sheet: 77,859,942.23 - 60,000,000.00 = 17,859,942.23 remaining (printed)')
gen22=a22-(a21-u22)
print('    implied surplus added during 2022: %.2f'%gen22)
check(near(gen22,49484857.40),'implied addition to the balance during 2022 is 49,484,857.40')
diff=fb21-a21
print('    audit 2021 balance minus the budget sheet\'s 2021 figure: %.2f'%diff)
check(near(diff,13833.49),'the audit and the 2023 budget sheet differ by 13,833.49 for the same 31 Dec 2021 balance; not explained here')
draws={'2022':25000000.00,'2023':60000000.00,'2024':43000000.00,'2025':23850000.00,'2026':4106000.00}
tot=sum(draws.values()); need=tot-a21
print('    draws 2022-2026 sum %.2f ; minus the 31 Dec 2021 balance %.2f = %.2f ; per year over 2022-2025 (4 operating years): %.2f'%(tot,a21,need,need/4))
check(near(tot,155956000.00),'draws 2022-2026 total 155,956,000.00')
check(near(need,102580915.17),'at least 102,580,915.17 must be added to the balance during 2022-2025 for those draws to be fundable (if each is funded from the balance)')
g23=43000000.00-(a22-u23)
check(near(g23,25140057.77),'to fund the 2024 draw, at least 25,140,057.77 had to be added during 2023 (2024 draw read as 43,000,000 in the 2025 file; 2024 budget not read)')
print('    the 2022 addition (49.48M, from the sheet) and the 2021 operating excess (27.79M, audited) show the balance being refilled each year; the roll-forward after 2022 is an inference, not a reading: no audit after 2021 was provided')

head('8b','2022 adopted legal-line budget (scan; read from the page image of Sheet 11, 2026-10-22): does it agree with the draws used above?')
# Source: '2022 Adopted Legal Line Budget (PDF).pdf', Current Fund - Anticipated Revenues (Continued), Sheet 11, Summary of Revenues, row 1 'Surplus Anticipated (Sheet 4, #1)'.
# Columns as printed: Anticipated 2022 | Anticipated 2021 | Realized in Cash in 2021.  Typed by hand from the image, not from OCR text (OCR misread 816,392 as 816,362).
s22_anticipated, s21_anticipated, s21_realized = 25000000.00, 11700000.00, 11700000.00
tgr22 = 816392337.95
def agrees(v22, v21): return near(v22,25000000.00) and near(v21,11700000.00)
check(agrees(s22_anticipated,s21_anticipated),'2022 adopted budget: surplus anticipated 25,000,000.00 (2022) and 11,700,000.00 (2021), matching the 2023 sheet and the 2021 audit')
check(near(s21_realized,11700000.00),'2022 budget: surplus realized in cash in 2021 = 11,700,000.00 = the amount the 2021 audit says was used')
check(not agrees(24000000.00,11700000.00) and not agrees(25000000.00,12000000.00),'CONTROL: a wrong 2022 draw (24,000,000) or wrong 2021 draw (12,000,000) is rejected by the same test')
print('    2022 budget total general revenues (anticipated, 2022): %.2f ; surplus share %.3f%%  [read from the scan image; not used elsewhere]'%(tgr22,100*s22_anticipated/tgr22))
check(near(100*s22_anticipated/tgr22,3.0623,0.001),'2022 draw is 3.062% of 2022 anticipated total general revenues')

head('8c','Parking Authority 2023 audit (scan; figures read from the page images, 2026-10-22): do the printed schedule and statement foot?')
# Source: Parking Authority of the City of Newark, financial statements for 2023 and 2022 (Withum Smith & Brown), Notes 7, 8 and the statement of net deficit.
# Typed by hand from the page images, not from OCR text (OCR misread 1,670,000 as 4,670,000 and a defeasance figure as 41.687 million).
p23=[0,95000,95000,100000,145000,975000,1670000,2555000,3760000,3030000]
i23=[316237,665763,661013,656263,651263,3133063,2816450,2292763,1483900,339350]
def sched_ok(p,i,tp,ti): return sum(p)==tp and sum(i)==ti and sum(p)+sum(i)==tp+ti
check(sched_ok(p23,i23,12425000,13016065),'Series 2023 schedule foots: principal 12,425,000 + interest 13,016,065 = total debt service 25,441,065 (the issue amount)')
bad=list(p23); bad[6]=4670000
check(not sched_ok(bad,i23,12425000,13016065),'CONTROL: the OCR misread (4,670,000 for 1,670,000) is rejected by the same test')
rev23=[2941192,1473726,479061,891559,475009,12356,160960]
check(sum(rev23)==6433863,'2023 operating revenue lines (read from the statement image) foot to the printed total 6,433,863')
check(sum([4473726 if i==1 else v for i,v in enumerate(rev23)])!=6433863,'CONTROL: the OCR misread of ticket sharing (4,473,726 for 1,473,726) breaks the footing')
check(2092738+682335==2775073,'net deficit: 2,092,738 + 2023 change 682,335 = 2,775,073')
check(not (2092738+682335==2775037),'CONTROL: a transposed net deficit (2,775,037) is rejected')
check(60405<93710 and 12*60405==724860,'monthly rent range 60,405 to 93,710 (read); twelve months at the low end = 724,860 (computed; NOT reconciled to the 479,061 revenue line)')
print('    NOT checked here: the $479,061 City-lease revenue line against Note 7 rent; the 2017 sale price; whether the city guaranteed any Authority bonds.')

head(9,'the page carries these numbers (SKIP if the page is absent)')
page=os.path.join(os.path.dirname(os.path.abspath(__file__)),'wp137-reading-newarks-budget.html')
if os.path.exists(page):
    h=open(page,encoding='utf8').read()
    for s in ('900,500,264.94','908,391,132.98','7,890,868.04','2.458','0.456','112,456,798.43','95,456,798.43','10.60','7.97','47.77','2.154','2.016','-9.12','56,392,140.77','259,136,083.94','15.57','1,486','53,388,918.32','77,859,942.23','13,833.49','49,484,857.40','102,580,915.17','25,140,057.77','155,956,000','85.25','42,746,765','24,480,000','36.02','12,785,121,100','816,392,337.95','3.062','12,425,000','13,016,065','25,441,065','37,386,500','60,405','93,710','2,775,073','479,061','17-1221','11.687'):
        check(s in h,'page contains %s'%s)
else:
    print('    SKIP  page not written yet')

head('HONESTY','what this script establishes and what it does not')
print("""    It checks that the printed columns foot, recomputes ratios and the rate-versus-levy relation from the sheet's own figures, and does
    replacement arithmetic at constant valuation. It does NOT explain the 7.89 million gap between two sheets or the rate that fails to follow
    from the levy; it reports them. It does not say the 2026 file is adopted or introduced (the file does not say). The UFB-4 flags are the city's.
    It uses the 2021 audited fund balance and the 2023 budget's Condition of Surplus sheet; nothing after 2022 is read from a balance sheet. The simulation's probabilities are assumptions. Nothing here is an audit,
    a rating, or a finding that Newark is in fiscal stress.""")
if fails:
    print('\nFAILED: %d'%len(fails)); [print('  -',f) for f in fails]; sys.exit(1)
print('\nAll checks passed.')
