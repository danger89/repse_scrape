import json
import pandas as pd
import warnings

# This code converts registros.json to excel file "Registros_REPSE.xlsx"

with open('../Data/registros.json') as json_file:
    registros = json.load(json_file)
registros = sorted(registros, key=lambda d: d['nombre_o_razon_social'])

# Convert list to pandas DataFrame
registros = pd.DataFrame(registros)

# Writing to Excel file (If "ModuleNotFoundError: No module named openpyxl", install and import openpyxl)
writer = pd.ExcelWriter('../Data/Registros_REPSE.xlsx')
registros.to_excel(writer, sheet_name='Registros', index=False, na_rep='NaN')


# Auto adjust column width
for idx, column in enumerate(registros):
    if idx != 4:
        column_width = max(registros[column].astype(str).map(len).max(), len(column))
    else:
        column_width = 20
    col_idx = registros.columns.get_loc(column)
    writer.sheets['Registros'].set_column(col_idx, col_idx, column_width)

warnings.filterwarnings("ignore")
writer.save()

