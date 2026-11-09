import csv,pickle,collections as C
F=['First_Arraign_Date','Court_Type','Court_Name','County_Name','Top_Severity_at_Arraign','Top_Arraign_Article_Section','Release Decision at Arraign','Bail_Set_and_Posted_at_Arraign','Bail_Set_and_Not_Posted_at_Arraign','First_Bail_Set_Cash','Disposition_Type','Docket_Status','Days_Arraign_to_Dispo','Days_Arraign_Bail_Set_to_First_Posted','prior_vfo_cnt','prior_nonvfo_cnt','prior_misd_cnt','arr_cycle_id','Disposition_Date']
out=[];flow=C.Counter()
for y in (2023,2024,2025):
  with open(f'NYS_{y}.csv',newline='',encoding='utf-8',errors='replace') as h:
    for r in csv.DictReader(h):
      flow['all rows']+=1;flow[('court',r['Court_Type'])]+=1
      if r['Court_Type']=='Local': flow[('local sev',r['Top_Severity_at_Arraign'].strip())]+=1
      if r['Court_Type']=='Local' and r['Top_Severity_at_Arraign'].strip()=='Misdemeanor': out.append([r[k].strip() for k in F])
pickle.dump((F,out,flow),open('extract.pkl','wb'));print(len(out),flow.most_common())
