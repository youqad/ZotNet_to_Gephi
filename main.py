import csv
from io import StringIO
import re
import replit

filename = 'zotnet.vna'

nodes_list, edges_list = [], [["Source", "Target"]]
reading_nodes, reading_edges = True, False

with open(filename) as f:
  next(f, None)
  for line in f:
    line_list = list(csv.reader(StringIO(line.replace("'", '"')), delimiter=' '))[0]

    if reading_nodes:
      reading_nodes = False
      line_list[0] = "Id"
      nodes_list.append(["Label"]+line_list)
      continue
    elif line_list[0] == '*tie':
      reading_edges = True
      next(f, None)
      continue

    if not reading_edges:
      match_date = re.search('\d{4}', line_list[2])
      date = match_date.group(0) if match_date else '?'
      truncated_title = (line_list[3][:12] + '..') if len(line_list[3]) > 12 else line_list[3]
      nodes_list.append([f"{line_list[1]} ({date}) — {truncated_title}"] + line_list)
    else:
      edges_list.append(line_list[:-1])

with open("nodes.csv", "w", newline="") as fn:
    writer = csv.writer(fn)
    writer.writerows(nodes_list)

with open("edges.csv", "w", newline="") as fe:
    writer = csv.writer(fe)
    writer.writerows(edges_list)

replit.clear()
print(nodes_list[:10])
print(edges_list[:10])