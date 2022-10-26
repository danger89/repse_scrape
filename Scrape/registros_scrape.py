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
import pprint as pp


def register_scrape():
    # ----------------------------- Setting up Register Scrape ----------------------------- #
    print('Setting up scrape...')

    # Open nombres_to_scrape.json
    with open('../Data/nombres_to_scrape.json') as json_file:
        nombres_to_scrape = json.load(json_file)
    try:
        nombres_to_scrape_copy = copy.deepcopy(nombres_to_scrape[0:4000])
    except:
        nombres_to_scrape_copy = copy.deepcopy(nombres_to_scrape[0:-1])

    # Set up chrome driver options
    ua = UserAgent()
    user_agent = ua.random
    options = webdriver.ChromeOptions()
    # options.add_argument(f'user-agent={user_agent}')
    # options.add_argument("--incognito")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")

    # proxy = "proxy.soax.com:9000"
    # options.add_argument('--proxy-server=%s' % proxy)
    # proxy = "rotating.proxyempire.io:9000"
    # options.add_argument('--proxy-server=%s' % proxy)

    # options.add_argument("--headless")  # Comment this line to see script running in Chrome.
    options.add_experimental_option("detach", True)

    # Locate driver in path and input options parameters
    chrome_driver_path = 'driver2.exe'
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.delete_cookie('_GRECAPTCHA')

    # Define URL and input into driver
    url = 'https://repse.stps.gob.mx'
    driver.get(url)
    time.sleep(1)

    # Identify and click "Consulta" button
    buttons = driver.find_elements(By.CSS_SELECTOR, '.btn-blanco')
    time.sleep(1)
    buttons[1].click()
    time.sleep(2)

    # Identify and click "Consultar" button
    continue_button = driver.find_element(By.CSS_SELECTOR, '.btn-continue')
    continue_button.click()
    time.sleep(2)

    # ---------------------------------- Register Scrape ---------------------------------- #
    print('--------------------------------------------')

    for idx, nombre in enumerate(nombres_to_scrape_copy):
        # Identify search bar and input current name
        search_bar = driver.find_element(By.CSS_SELECTOR, '#rsoc')
        search_bar.send_keys(Keys.CONTROL, 'a')
        search_bar.send_keys(Keys.BACKSPACE)
        search_bar.send_keys(nombre)

        # Identify and click search button
        search_button = driver.find_element(By.CSS_SELECTOR, '#bnt_busqueda')
        search_button.click()
        time.sleep(2.1)

        # Identify and click select button
        selection_buttons = driver.find_elements(By.CSS_SELECTOR, '.g-recaptcha')
        try:
            selection_button = selection_buttons[1]
            selection_button.click()
            time.sleep(1)
        except IndexError:
            try:
                CAPTCHA_check = driver.find_element(By.CSS_SELECTOR, '.text-uppercase')
                if 'CAPCHA' and 'INCORRECTA' in CAPTCHA_check.text:
                    print('Incorrect CAPTCHA')
                elif "NO" and 'DATOS' in CAPTCHA_check.text:
                    print('No entry detected')
                    index_to_pop = nombres_to_scrape.index(nombre)
                    nombres_to_scrape.pop(index_to_pop)
                    json_object = json.dumps(nombres_to_scrape, indent=4)
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
        def get_data():
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
                'entidad_municipio': entidad_municipio,
                'aviso_de_registro': aviso_de_registro,
                'fecha_de_registro': fecha_de_registro,
                'servicios_ofrecidos': servicios
            }
            print(nombre)
            return r
        try:
            registro = get_data()
        except IndexError:
            try:
                time.sleep(2)
                registro = get_data()
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

        # Append data to registros.json
        with open('../Data/registros.json', 'r+') as file:
            # First we load existing data into a dict.
            registros_existentes = json.load(file)
            # Join new_data with existing data inside emp_details
            if registro not in registros_existentes:
                print('Entry added to registros.json')
                registros_existentes.append(registro)
            else:
                print(f'Entry already in registros.json')

            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(registros_existentes, file, indent=4)

        json_object = json.dumps(nombres_to_scrape, indent=4)

        # Updating input_data json
        with open('../Data/registros.json') as json_file:
            registros = json.load(json_file)
        registros = sorted(registros, key=lambda d: d['nombre_o_razon_social'])

        for obj in registros:
            if nombre in obj["nombre_o_razon_social"]:
                index_to_pop = nombres_to_scrape.index(nombre)
                nombres_to_scrape.pop(index_to_pop)

        print('Deleting entry from nombres_to_scrape.json')
        print('--------------------------------------------')
        with open('../Data/nombres_to_scrape.json', 'w') as outfile:
            outfile.write(json_object)

        # Identify and click return button
        return_button = driver.find_element(By.CSS_SELECTOR, '.btn-secondary')
        try:
            return_button.click()
        except:
            time.sleep(0.1)
            return_button.click()
        time.sleep(2.1)

        # Convert list to pandas DataFrame
        registros = pd.DataFrame(registros)

        # Writing to Excel file (If "ModuleNotFoundError: No module named openpyxl", install and import openpyxl)
        writer = pd.ExcelWriter('../Data/Registros_REPSE.xlsx')
        registros.to_excel(writer, sheet_name='Registros', index=False, na_rep='NaN')

        # Auto adjust column width
        for index, column in enumerate(registros):
            if index != 4:
                column_width = max(registros[column].astype(str).map(len).max(), len(column))
            else:
                column_width = 20
            col_idx = registros.columns.get_loc(column)
            writer.sheets['Registros'].set_column(col_idx, col_idx, column_width)

        warnings.filterwarnings("ignore")
        writer.save()


register_scrape()



