import json
import pandas as pd
import warnings


def registros_to_excel():
    print('////////////////////////////////////////')
    with open('../Data/registros.json', 'r') as file:
        registros = json.load(file)

    # Sort entries alphabetically
    registros = sorted(registros, key=lambda d: d['nombre_o_razon_social'])
    print(f'{len(registros)} TOTAL entries')

    # Complete entries
    registros_with_number = [obj for obj in registros if obj['numero_de_registro'] != '-']
    print(f'{len(registros_with_number)} WITH number')

    # Incomplete entries
    registros_without_number = [obj for obj in registros if obj['numero_de_registro'] == '-']
    print(f'{len(registros_without_number)} WITHOUT number')

    # Append complete with incomplete
    registros = registros_with_number + registros_without_number

    # Convert list to pandas DataFrame
    registros = pd.DataFrame(registros)

    # Writing to Excel file (If "ModuleNotFoundError: No module named openpyxl", install and import openpyxl)
    print('Writing to ../Data/Registros_REPSE.xlsx, please stand by...')
    writer = pd.ExcelWriter('../Data/Registros_REPSE.xlsx')
    registros.to_excel(writer, sheet_name='Registros', index=False, na_rep='NaN')

    # Auto adjust column width
    for index, column in enumerate(registros):
        if index != 5:
            column_width = max(registros[column].astype(str).map(len).max(), len(column))
        else:
            column_width = 20
        col_idx = registros.columns.get_loc(column)
        writer.sheets['Registros'].set_column(col_idx, col_idx, column_width)

    warnings.filterwarnings("ignore")
    writer.save()
    print('Excel file updated successfully')
    print('////////////////////////////////////////')


if __name__ == "__main__":
    registros_to_excel()


