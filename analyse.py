import os
import json
from langdetect import detect

# type export: dict or list
def read_json(file_name: str): 
  with open(file_name, 'r') as file:
    data = json.load(file)

  return data

def write_json(data, file_name: str) -> None:
  with open(os.path.join(os.getcwd(), file_name), 'w') as file:
    json.dump(data, file, indent=2)

def check_null(data: dict) -> None:
  check = {key: False for key in data[0]}

  for row in data:
    for key, value in row.items():
      if check[key] == False:
        if value:
          check[key] = True
  
  print(check)

def check_total(data: dict) -> None:
  check = {key: 0 for key in data[0]}

  for row in data:
    for key, value in row.items():
      if value:
        check[key] += 1
  
  print(check)
  print(len(check))

def merge_table(actionscopes: dict, service_joborders: dict) -> list:
  table = []
  for i in actionscopes:
    merge = {}
    for j in service_joborders:
      if i['Code'] == j['Actionscope.Code']:
        merge = i
        merge['Service_joborders'] = j
        table.append(merge)
        break
    else:
      table.append(i)

  return table

def problem_table(merge_table: dict) -> list:
  table = []
  for i in merge_table:
    row = {
      'actionscope_code': i['Code'],
      'actionScopes_serviceDescription': i['Service object.Description'],
      'actionScopes_description': i['Description'],
      'actionScopes_memo': i['Memo'],
      'actionScopes_servicetype': i['Servicetype'],
    }
    
    if i['Joborders'] and 'Service_joborders' in i:
      joborders = {
        'jobOrders_serviceDescription': i['Service_joborders']['Service object.Description'],
        'jobOrders_description': i['Service_joborders']['Description'],
        'jobOrders_memo': i['Service_joborders']['Memo'],
        'jobOrders_internalMemo': i['Service_joborders']['Internal memo'],
        'jobOrders_problem': i['Service_joborders']['Problem (not visible on tablet)'],
        'jobOrders_realizedSolution': i['Service_joborders']['Realized solution'],
        'jobOrders_servicetype': i['Service_joborders']['Service type']
      }
      row.update(joborders)

    table.append(row)

  return table

def check_joborders(merge_table: dict) -> list:
  table = []
  for i in merge_table:
    if i['Joborders'] and not 'Service_joborders' in i:
      table.append(i['Code'])

  print(table)


if __name__ == '__main__':
  file1 = os.path.join(os.getcwd(), 'output_json\\Service_joborders.json')
  file2 = os.path.join(os.getcwd(), 'output_json\\Actionscopes.json')
  file3 = os.path.join(os.getcwd(), 'analyse\\merge_table.json')

  service_joborders = read_json(file1)
  actionscopes = read_json(file2)
  mergeTable = read_json(file3)

  # print(detect("Pos.010 PC11-IV. Automatic pricking robot equipped with 4 grippers"))
  # print(detect("Onderhoud mechanica met inspectie Basis pakket 2017/2018"))
  # print(detect("SPS Ausgang ist kaput und m\u00fcst umprogramiert werden.\n"))

  # check_null(service_joborders)
  # check_total(service_joborders)
  # check_joborders(mergeTable)

  # merge = merge_table(actionscopes, service_joborders)
  # write_json(merge, 'analyse\\merge_table.json')

  info_problem = problem_table(mergeTable)
  write_json(info_problem, 'analyse\\problem_table.json')
