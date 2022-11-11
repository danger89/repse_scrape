from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import copy
import pandas as pd
import warnings
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pprint as pp

from useful_functions import update_incomplete_entries as up


def register_scrape():
    # ----------------------------- Setting up Register Scrape ----------------------------- #
    # Update registros.json and nombres_to_scrape.json with the latest info
    up.update_jsons()
    print('Setting up scrape...')

    # Open nombres_to_scrape.json
    with open('../Data/nombres_to_scrape.json') as json_file:
        data = json.load(json_file)
    try:
        data_copy = copy.deepcopy(data[0:4000])
    except:
        data_copy = copy.deepcopy(data[0:-1])

    # Set up chrome driver options
    ua = UserAgent()
    user_agent = ua.random
    options = webdriver.ChromeOptions()
    options.add_argument(f'user-agent={user_agent}')
    # options.add_argument("--incognito")
    # options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    # options.add_argument("--headless")  # Comment this line to see script running in Chrome.
    options.add_experimental_option("detach", True)

    # Locate driver in path and input options parameters
    chrome_driver_path = 'driver2.exe'
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.delete_cookie('_GRECAPTCHA')

    # Define URL and input into driver
    url = 'https://repse.stps.gob.mx'
    driver.get(url)
    # time.sleep(1.5)

    # Identify and click "Consulta" button
    wait = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-blanco'))
    )
    buttons = driver.find_elements(By.CSS_SELECTOR, '.btn-blanco')
    time.sleep(1)
    buttons[1].click()
    # time.sleep(3)

    # Identify and click "Consultar" button
    wait = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-continue'))
    )
    continue_button = driver.find_element(By.CSS_SELECTOR, '.btn-continue')
    continue_button.click()
    time.sleep(3)

    # ---------------------------------- Register Scrape ---------------------------------- #
    print('--------------------------------------------')
    data_lista = []
    registros_lista = []
    count = 0
    for idx, obj in enumerate(data_copy):
        count += 1

        # Identify search bar and input current name
        search_bar = driver.find_element(By.CSS_SELECTOR, '#rsoc')
        search_bar.send_keys(Keys.CONTROL, 'a')
        search_bar.send_keys(Keys.BACKSPACE)
        search_bar.send_keys(obj['name'])

        # Identify and click search button
        # search_button = driver.find_element(By.CSS_SELECTOR, '#bnt_busqueda')
        search_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '#bnt_busqueda'))
        )
        try:
            search_button.click()
        except:
            time.sleep(1)
            search_button.click()
        # time.sleep(1.8)

        try:
            wait = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'td'))
            )
            time.sleep(1.4)

            # Checking if more than one result appears
            td = driver.find_elements(By.CSS_SELECTOR, 'td')
            results = []
            for idx1, element in enumerate(td):
                if idx1 % 3 == 0:
                    results.append(element.text)
            idx2 = results.index(obj['name'])

            # Identify and click select button
            selection_buttons = driver.find_elements(By.CSS_SELECTOR, '.g-recaptcha')
            selection_button = selection_buttons[idx2+1]
            selection_button.click()

        except:
            try:
                CAPTCHA_check = driver.find_element(By.CSS_SELECTOR, '.text-uppercase')
                if 'CAPCHA' and 'INCORRECTA' in CAPTCHA_check.text:
                    print('Incorrect CAPTCHA')
                elif "NO" and 'DATOS' in CAPTCHA_check.text:
                    print('--------------------------------------------')
                    print(f'No entry detected: {obj["name"]}')
                    index_to_pop = data.index(obj)
                    data.pop(index_to_pop)
                    json_object = json.dumps(data, indent=4)
                    print('Deleting entry from nombres_to_scrape.json')
                    print('--------------------------------------------')
                    with open('../Data/nombres_to_scrape.json', 'w') as outfile:
                        outfile.write(json_object)
                continue
            except:
                print('No entry detected')
                print('--------------------------------------------')
                continue

        # Format data
        def get_data(obje):
            main_data = driver.find_elements(By.CSS_SELECTOR, '.highlightname')
            nombre_o_razon_social = main_data[0].text
            entidad_municipio = main_data[1].text
            AF = main_data[2].text
            aviso_de_registro = AF.split('/')[0][0:-1]
            fecha_de_registro = AF.split('/')[1][1:]

            servicios = []
            servicios_data = driver.find_elements(By.CSS_SELECTOR, 'ul')
            for servicio in servicios_data:
                servicios.append(servicio.text)
            r = {
                'nombre_o_razon_social': nombre_o_razon_social,
                'numero_de_registro': obje['registro'],
                'entidad_municipio': entidad_municipio,
                'aviso_de_registro': aviso_de_registro,
                'fecha_de_registro': fecha_de_registro,
                'servicios_ofrecidos': servicios
            }
            print("Extracting: " + obje['name'])
            return r
        try:
            time.sleep(0.7)
            registro = get_data(obj)
        except IndexError:
            try:
                time.sleep(0.2)
                registro = get_data(obj)
            except:
                # Identify and click "Consulta" button
                time.sleep(3)
                buttons = driver.find_elements(By.CSS_SELECTOR, '.btn-blanco')
                time.sleep(5)
                buttons[1].click()
                time.sleep(3)

                # Identify and click "Consultar" button
                continue_button = driver.find_element(By.CSS_SELECTOR, '.btn-continue')
                continue_button.click()
                time.sleep(5)
                continue

        # Store entry & data
        registros_lista.append(registro)
        data_lista.append(obj)

        # Update registros.json and excel every 25 iterations
        if count > 20:
            # Append data to registros.json
            with open('../Data/registros.json', 'r+') as file:
                registros_existentes = json.load(file)
                entries_added = 0
                entries_already = 0
                for registro in registros_lista:
                    if registro not in registros_existentes:
                        entries_added += 1
                        registros_existentes.append(registro)
                    else:
                        entries_already += 1
                print('--------------------------------------------')
                print(f'{entries_added} entries added to registros.json')
                print(f'{entries_already} already in registros.json')
                print('--------------------------------------------')

                # Sets file's current position at offset.
                file.seek(0)
                # convert back to json.
                json.dump(registros_existentes, file, indent=4)

            # Updating Excel file
            print('//////////////////////////////////////////////////')

            # Open registros.json
            with open('../Data/registros.json') as json_file:
                registros = json.load(json_file)

            # Sort alphabetically
            registros = sorted(registros, key=lambda d: d['nombre_o_razon_social'])
            print(f'TOTAL entries: {len(registros)}')

            # Complete entries
            registros_with_number = [obj for obj in registros if obj['numero_de_registro'] != '-']
            print(f'WITH numero_de_registro: {len(registros_with_number)}')

            # Incomplete entries
            registros_without_number = [obj for obj in registros if obj['numero_de_registro'] == '-']
            print(f'WITHOUT numero_de_registro: {len(registros_without_number)}')

            # Append complete with incomplete
            registros = registros_with_number + registros_without_number

            # Delete data from nombres_to_scrape.json
            for obj1 in data_lista:
                for obj2 in registros:
                    if obj2["nombre_o_razon_social"] == obj1['name']:
                        index_to_pop = data.index(obj1)
                        data.pop(index_to_pop)

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
            print('//////////////////////////////////////////////////')

            # Delete extracted entries from nombres_to_scrape.json
            json_object = json.dumps(data, indent=4)
            print(f'Deleting entries from nombres_to_scrape.json')
            print('--------------------------------------------')
            with open('../Data/nombres_to_scrape.json', 'w') as outfile:
                outfile.write(json_object)

            # Reset stored data
            data_lista = []
            registros_lista = []
            count = 0

        # Identify and click return button
        return_button = driver.find_element(By.CSS_SELECTOR, '.btn-secondary')
        try:
            return_button.click()
        except:
            time.sleep(0.1)
            return_button.click()
        # time.sleep(1.6)


register_scrape()


