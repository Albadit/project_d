import os
import json
from langdetect import detect

def read_json(file_name: str) -> dict:
  with open(file_name, 'r') as file:
    data = json.load(file)

  return data

def write_json(data, file_name: str):
  with open(os.path.join(os.getcwd(), file_name), 'w') as file:
    json.dump(data, file, indent=2)

def check_null(data: dict) -> dict:
  check = {key: False for key in data[0]}

  for row in data:
    for key, value in row.items():
      if check[key] == False:
        if value:
          check[key] = True

def check_total(data: dict) -> dict:
  check = {key: 0 for key in data[0]}

  for row in data:
    for key, value in row.items():
      if value:
        check[key] += 1

def merge_table(actionscopes: dict, service_joborders: dict) -> dict:
  table = []
  for i in actionscopes:
    merge = {}
    for j in service_joborders:
      if i['Code'] == j['Actionscope.Code']:
        merge = i
        merge['Service_joborders'] = j
        table.append(merge)
        break
    # else: 
    #   merge = i
    #   merge['Service_joborders'] = None
    #   table.append(merge)
    else:
      table.append(i)

  return table

def info_table(merge_table: dict) -> dict:
  table = []
  for index, i in enumerate(merge_table):
    row = {
      'Actionscope.Code': i['Code'],
      'actionScopes_serviceDescription': i['Service object.Description'],
      'actionScopes_description': i['Description'],
      'actionScopes_memo': i['Memo'],
      'actionScopes_servicetype': i['Servicetype'],
    }
    
    # if i['Joborders'] and i['Service_joborders']:
    if i['Joborders']:
      print(index)
      print(i['Code'])
      row['jobOrders_serviceDescription'] = i['Service_joborders']['Service object.Description']
      row['jobOrders_description'] = i['Service_joborders']['Description']
      row['jobOrders_memo'] = i['Service_joborders']['Memo']
      row['jobOrders_internalMemo'] = i['Service_joborders']['Internal memo']
      row['jobOrders_problem'] = i['Service_joborders']['Problem (not visible on tablet)']
      row['jobOrders_realizedSolution'] = i['Service_joborders']['Realized solution']
      row['jobOrders_servicetype'] = i['Service_joborders']['Service type']

    table.append(row)

  return table

def check_joborders(merge_table: dict) -> dict:
  pass


if __name__ == '__main__':
  file1 = os.path.join(os.getcwd(), 'output_json\\Service_joborders.json')
  file2 = os.path.join(os.getcwd(), 'output_json\\Actionscopes.json')
  file3 = os.path.join(os.getcwd(), 'analyse\\merge_table.json')

  service_joborders = read_json(file1)
  actionscopes = read_json(file2)
  mergeTable = read_json(file3)

  # null = check_null(service_joborders)
  # total = check_total(service_joborders)
  # print(null)
  # print(total, len(total))

  # merge = merge_table(actionscopes, service_joborders)
  # write_json(merge, 'analyse\\merge_table.json')

  # print(detect("Pos.010 PC11-IV. Automatic pricking robot equipped with 4 grippers"))
  # print(detect("Onderhoud mechanica met inspectie Basis pakket 2017/2018"))
  # print(detect("SPS Ausgang ist kaput und m\u00fcst umprogramiert werden.\n"))

  info = info_table(mergeTable)
  # write_json(info, 'analyse\\info.json')

