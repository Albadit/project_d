import pandas as pd
import os

def xlsx_to_json(xlsx_path, json_path):
  # Read the Excel file
  df = pd.read_excel(xlsx_path)
  
  # Convert the DataFrame to JSON and save to a file
  df.to_json(json_path, orient='records', indent=2)

def convert_folder_xlsx_to_json(input_folder, output_folder):
  # Ensure output folder exists
  if not os.path.exists(output_folder):
    os.makedirs(output_folder)
  
  # Loop through all files in the input directory
  for filename in os.listdir(input_folder):
    if filename.endswith('.xlsx'):
      # Construct full file path
      xlsx_path = os.path.join(input_folder, filename)
      # Change the file extension from .xlsx to .json for the output file name
      json_filename = os.path.splitext(filename)[0] + '.json'
      json_path = os.path.join(output_folder, json_filename)
      
      # Convert the Excel file to JSON
      xlsx_to_json(xlsx_path, json_path)
      print(f"Converted {filename} to json")

if __name__ == '__main__':
  input_folder = os.path.join(os.getcwd(), 'xlsx')
  output_folder = os.path.join(os.getcwd(), 'output_json')
  convert_folder_xlsx_to_json(input_folder, output_folder)
