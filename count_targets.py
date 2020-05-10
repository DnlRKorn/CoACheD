import csv
targs = {}
drug_bank = set()
with open("structure_links.csv") as f:
  reader = csv.DictReader(f)
  for d in reader:
    chem = d['ChEMBL ID'].strip()
#    if(chem in drugs):print('HI')
    if(len(chem)>2):
      #print(chem)
      drug_bank.add(chem)
from tabulate import tabulate


#tabulate([["strings", "numbers"], ["spam", 41.9999], ["eggs", "451.0"]],
#    ...                headers="firstrow", tablefmt="html")


with open("pair_counts_dtd_1_2_scored.txt") as f:
  next(f)
  for line in f:
    l = line.split(',')
    prot = l[0].split("#")[1]
    chem = l[1].split("#")[1]
    if("CHEMBL" not in chem):
      print("BAD",line)
      exit()
    if(chem not in drug_bank):continue
    s = targs.get(prot,set())
    s.add(chem)
    targs[prot] = s 

keys = list(targs.keys())
keys.sort()
for k in keys:
  print(k,len(targs[k]))

def updateDict(d):
  d2 = {}
  for x in d:
    d2[x] = d[x]
  d2["Entry"] = '<a href="https://www.uniprot.org/uniprot/%s">%s</a>' %(d["Entry"],d["Entry"])
#  d2["Entry name"] = '<a href="https://www.uniprot.org/uniprot/%s">%s</a>' %(d["Entry"],d["Entry"])
  return d2

table = []
with  open("target_info.html",'w') as f2:
  csvfile = open("uniprot_targs2.txt")
  reader = csv.DictReader(csvfile,delimiter='|')
  fields = reader.fieldnames
  fields.append("Drug_Count")
  table.append(fields)
  f2.write('''<style>
  table {
    border-collapse: collapse;
    }

    table, th, td {
      border: 1px solid black;
      }
          </style>
          ''')
  f2.write("<table>\n<tr>")
  for x in fields:
    f2.write("<th>%s</th>"%x)
  f2.write("</tr>\n")
#  writer = csv.DictWriter(f2,fields)
#  writer.writeheader()
  for d in reader:
    #cnt = len(targs[d['Entry']])
    cnt = len(targs.get(d['Entry'],[]))
    d['Drug_Count'] = cnt
    if(cnt==0):continue
    d = updateDict(d)
    f2.write("<tr>")
    for x in fields:
      f2.write("<th>%s</th>"%d[x])
    f2.write("</tr>\n")
#    writer.writerow(d)
#  f2.write("\n\n")
  csvfile = open("uniprot_targs2.txt")
  reader = csv.DictReader(csvfile,delimiter='|')
  for d in reader:
    #cnt = len(targs[d['Entry']])
    cnt = len(targs.get(d['Entry'],[]))
    d['Drug_Count'] = cnt
    if(cnt!=0):continue
    d = updateDict(d)
    f2.write("<tr>")
    for x in fields:
      f2.write("<th>%s</th>"%d[x])
    f2.write("</tr>\n")
  f2.write("</table>")

#with open("targets.txt",'w') as f:
#  for x in keys:
#    #f.write(x + ',' + str(targs[x])+ '\n')
#    f.write(x + ',' + str(len(targs[x]))+ '\n')
#    # print(x,len(targs[x]))
