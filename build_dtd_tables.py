import csv
drugs = [] 
pairs = {} 
#with open("advanced_pair_counts_dtd_scored.csv") as f:
#  next(f)
with open("data/pair_counts_dtd_drugbank_uni_1_2_scored.txt") as f:
  next(f)
  for line in f:
    drug = line.split(',')[1]
    drug = drug.split("#")[1]
    drugs.append(drug)
    targ = line.split(",")[0]
    targ = targ.split("#")[1]
    s = pairs.get(targ,set())
    s.add(drug)
    pairs[targ] = s
print(len(drugs),len(set(drugs)))
drugs = set(drugs)
drug_bank = set()
with open("data/structure_links.csv") as f:
  reader = csv.DictReader(f)
  for d in reader:
    chem = d['ChEMBL ID'].strip()
#    if(chem in drugs):print('HI')
    if(len(chem)>2):
      #print(chem)
      drug_bank.add(chem)

print(len(drugs.intersection(drug_bank)))
      
#diff = drugs.difference(drug_bank)n
inter = drugs.intersection(drug_bank)

cnt=0
papers = {}
scores = {}
with open("data/pair_counts_dtd_drugbank_uni_1_2_scored.txt") as f:
  next(f)
  for line in f:
    drug = line.split(',')[1]
    drug = drug.split("#")[1]
    if(drug in drug_bank):
      cnt+=1
      targ = line.split(",")[0]
      targ = targ.split("#")[1]
      papers[(targ,drug)] = line.strip().split(",")[6:] 
      scores[(targ,drug)] = line.strip().split(",")[5]
      #scores[(targ,drug)] = float(line.strip().split(",")[5]) 
      
print(cnt,'cnt')

bank_ids = set() 
drug_ids = set()
chem_to_bank = {}
print(drug_ids)

with open("data/structure_links.csv") as f:
  #header = next(f)
  reader = csv.DictReader(f)
  for d in reader:
    chem = d['ChEMBL ID'].strip()
    if(chem in inter):
      d_bank = d["DrugBank ID"]
      #bank_ids[chem] = d_bank
      bank_ids.add(d_bank)
      drug_ids.add(chem)
      chem_to_bank[chem] = d_bank

bank_ids_to_uni = {}

for x in bank_ids:
  bank_ids_to_uni[x] = set()

with open("data/uniprot_links.csv") as f:
  reader = csv.DictReader(f)
  for d in reader:
    bank = d["DrugBank ID"]
    if(bank in bank_ids):
      s = bank_ids_to_uni[bank]
      s.add(d["UniProt ID"])
      bank_ids_to_uni[bank] = s

#for x in bank_ids_to_uni:
#  print(x,len(bank_ids_to_uni[x]))
def convertDict(d):
    d2 = {}
    targ = d["Target"]
    drug = d["ChEMBL ID"]

    d2["Target"] = '<a href="https://www.uniprot.org/uniprot/%s">%s</a>' % (targ,targ)
    d_b = d["DrugBank ID"]
    d2["DrugBank ID"] = '<a href="https://www.drugbank.ca/drugs/%s">%s</a>' % (d_b,d_b)
    d2["ChEMBL ID"] = '<a href="https://www.ebi.ac.uk/chembl/compound_report_card/%s">%s</a>' % (d["ChEMBL ID"],d["ChEMBL ID"])
    d2["SMILES"] = d["SMILES"]
    d2["Name"] = d["Name"]
    #d2["Other Targets"] = d["Other Targets"]
    d2["Other Targets"] = '<a href="https://www.drugbank.ca/drugs/%s#targets">%s</a>' % (d_b,d["Other Targets"])
#      "Target","Name","DrugBank ID","ChEMBL ID","SMILES","Other Targets"],extrasaction="ignore")
    li_txt = "<ul>"
    for paper in papers[(targ,drug)]:
      link = "http://35.196.80.123/highlight?paper=%s&term1=CVPROT%%23%s&term2=DRUG%%23%s" % (paper,targ,drug)
      li_txt+='<li><a href="%s">%s</a></li>' %(link,paper)

    li_txt += "</ul>"
    d2["Paper Links"] = li_txt
    d2["Score"] = scores[(targ,drug)]
    return d2


tup_count = 0
with open("dtd_table.html",'w') as f:
  
   f.write('''
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/v/dt/dt-1.10.20/datatables.min.css"/>
      
<script type="text/javascript" src="https://cdn.datatables.net/v/dt/dt-1.10.20/datatables.min.js"></script>

<style>
  table {
    border-collapse: collapse;
  }

  table, th, td {
      border: 1px solid black;
  }
</style>
''')
   for targ in pairs:
      f.write('<section id="%s">' % targ )
      f.write('<a href="https://www.uniprot.org/uniprot/%s">%s</a>:\n' % (targ,targ))
      f.write("<table>\n")
      writer = csv.DictWriter(f,["Target","Name","DrugBank ID","ChEMBL ID","SMILES","Other Targets","Score","Paper Links"],extrasaction="ignore")
      f.write("<thead><tr>")
      for x in ["Target","Name","DrugBank ID","ChEMBL ID","SMILES","Other Targets","Score","Paper Links"]:
         f.write("<th>"+x+"</th>")
      f.write("</tr></thead>\n<tbody>\n")

      with open("data/structure_links_filtered.csv") as f2:
         reader = csv.DictReader(f2)
         for d in reader:
           chem = d['ChEMBL ID'].strip()
           if(chem in pairs[targ]):
             tup_count+=1
             bank = d["DrugBank ID"]
             cnt = d["Targets"]
             smile = d["SMILES"]
             d["Target"] = targ
             d["Other Targets"] = cnt
             d = convertDict(d)
             f.write("<tr>")
             for x in ["Target","Name","DrugBank ID","ChEMBL ID","SMILES","Other Targets","Score","Paper Links"]:
               f.write("<td>"+d[x]+"</td>\n")
             f.write("</tr>\n")
#             writer.writerow(d)
      f.write("</tbody></table>\n")
      f.write("\n\n")
      f.write('</section">')
   f.write('''
   <script>
   //$("table").dataTable()
   $( "table" ).each(function() {
     $( this ).dataTable();
     });
   </script>
   ''')
#   f.write("<table>\n")

print(drug_ids)
drug_ids = list(drug_ids)
drug_ids.sort()
print(tup_count)
exit()

with open("drug_to_targs_table.html",'w') as f:
  
   f.write('''
     <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
     <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/v/dt/dt-1.10.20/datatables.min.css"/>
      
      <script type="text/javascript" src="https://cdn.datatables.net/v/dt/dt-1.10.20/datatables.min.js"></script>

   <style>
  table {
    border-collapse: collapse;
    }

    table, th, td {
      border: 1px solid black;
      }
          </style>
          ''')
   for drug in drug_ids:
      #f.write(targ +":\n")
      #f.write("<tr>"+targ + ":</tr>\n")
      f.write("<table>\n")
      writer = csv.DictWriter(f,["Name","DrugBank ID","ChEMBL ID","SMILES","Targets"],extrasaction="ignore")
      f.write("<thead><tr>")
      for x in ["Name","DrugBank ID","ChEMBL ID","SMILES","Targets"]:
         f.write("<th>"+x+"</th>")
      f.write("</tr></thead>\n<tbody>\n")

      #writer.writeheader()
      with open("structure_links_filtered.csv") as f2:
         reader = csv.DictReader(f2)
         for d in reader:
           chem = d['ChEMBL ID'].strip()
           if(chem in drug_ids):
             bank = d["DrugBank ID"]
             cnt = d["Targets"]
             smile = d["SMILES"]
             d["Target"] = targ
             d["Other Targets"] = cnt
             d = convertDict(d)
             f.write("<tr>")
             for x in ["Target","Name","DrugBank ID","ChEMBL ID","SMILES","Other Targets"]:
               f.write("<td>"+d[x]+"</td>")
             f.write("</tr>\n")
#             writer.writerow(d)
      f.write('''</tbody></table>\n
      <script>
      $("table").dataTable()
      </script>
      ''')
      f.write("\n\n")
print(csv.list_dialects())
