import csv,pickle
F=['First_Arraign_Date','Court_Name','Judge_Name','Race','Top_Charge_Weight_at_Arraign','Arraign Charge Category','Representation_Type','Release Decision at Arraign','Bail_Set_and_Not_Posted_at_Arraign','Bail_Set_and_Posted_at_Arraign','First_Bail_Set_Cash','Disposition_Type','Days_Arraign_to_Dispo','prior_vfo_cnt','prior_nonvfo_cnt','prior_misd_cnt']
o=[]
for y in (2023,2024,2025):
  with open(f'NYS_{y}.csv',newline='',encoding='utf-8',errors='replace') as h:
    for r in csv.DictReader(h):
      if r['Court_Type']=='Local' and r['Top_Severity_at_Arraign'].strip()=='Misdemeanor': o.append([r[k].strip() for k in F])
pickle.dump((F,o),open('extract2.pkl','wb'));print(len(o))
