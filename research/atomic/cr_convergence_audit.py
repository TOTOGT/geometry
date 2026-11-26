import sys, json, lsda_scf as L
Ha=27.211386
name=sys.argv[1]; kw=json.loads(sys.argv[2])
un=[({(4,0):1,(3,2):2},{(4,0):1,(3,2):2}),({(4,0):0.5,(3,2):2.5},{(4,0):0.5,(3,2):2.5})]
po=[({(4,0):1,(3,2):4},{(4,0):1}),({(4,0):1,(3,2):5},{})]
E=[L.cr(u,d,**kw) for u,d in un+po]
print(f"{name:34s} unpol dE(4s1d5-4s2d4)={ (E[1]['E']-E[0]['E'])*Ha*1000:8.2f} meV   pol dE={(E[3]['E']-E[2]['E'])*Ha*1000:9.2f} meV  conv={all(e['conv'] for e in E)}  max|N_el-24|={max(abs(sum(e['nel'])-24) for e in E):.1e}")
