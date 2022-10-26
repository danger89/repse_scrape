from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import pprint as pp


def name_scrape(keyword, direction):
    if direction != 'forward' and direction != 'backward':
        print('Error: Invalid direction - Allowed directions: forward, backward')
        exit()

    # ----------------------------- Setting up Name Scrape ----------------------------- #
    print('Setting up scrape...')

    # Set up chrome driver options
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    # options.add_argument("--headless")  # Comment this line to see script running in Chrome.
    options.add_experimental_option("detach", True)

    # Locate driver in path and input options parameters
    chrome_driver_path = 'driver.exe'
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Define URL and input into driver
    url = 'https://repse.stps.gob.mx'
    driver.get(url)

    # Locate and click "Consulta" button
    buttons = driver.find_elements(By.CSS_SELECTOR, '.btn-blanco')
    time.sleep(1)
    buttons[1].click()
    time.sleep(1)

    # Identify and click "Consultar" button
    continue_button = driver.find_element(By.CSS_SELECTOR, '.btn-continue')
    continue_button.click()
    time.sleep(2)

    # Identify search bar and input key word
    search_bar = driver.find_element(By.CSS_SELECTOR, '#rsoc')
    search_bar.send_keys(keyword)

    print('--------------------------------------------')
    # Identify and click search button
    search_button = driver.find_element(By.CSS_SELECTOR, '#bnt_busqueda')
    search_button.click()
    time.sleep(2)

    if direction == 'backward':
        selection_buttons = driver.find_elements(By.CSS_SELECTOR, '.g-recaptcha')
        try:
            last_page_button = selection_buttons[-2]
            try:
                last_page_button.click()
            except:
                time.sleep(0.1)
                last_page_button.click()
            time.sleep(2)
        except IndexError:
            print('No more entries detected')
            exit()

    # ---------------------------------- Register Scrape ---------------------------------- #
    # Initialize pagination
    page = 1

    for i in range(500):
        try:
            names = []
            data = driver.find_elements(By.CSS_SELECTOR, 'td')
            for idx, element in enumerate(data):
                if idx % 3 == 0:
                    names.append(element.text)

            new_entries = 0
            entries_already_in_json = 0
            add_names_to_scrape = []

            # Appending output data to names.json
            with open('../Data/nombres.json', 'r+') as file:
                # First we load existing data into a dict.
                existing_names = json.load(file)
                for name in names:
                    # Join new names with existing names inside emp_details
                    if name not in existing_names:
                        new_entries += 1
                        existing_names.append(name)
                        add_names_to_scrape.append(name)
                    else:
                        entries_already_in_json += 1
                print(f'Entries added to nombres.json: {new_entries}')
                # Sets file's current position at offset.
                file.seek(0)
                # convert back to json.
                json.dump(existing_names, file, indent=4)

            # Appending output data to names_to_scrape.json
            with open('../Data/nombres_to_scrape.json', 'r+') as file:
                # First we load existing data into a dict.
                names_to_scrape = json.load(file)
                for name in add_names_to_scrape:
                    # Join new names with existing names inside emp_details
                    names_to_scrape.append(name)
                print(f'Entries added to nombres_to_scrape.json: {new_entries}')
                print(f'Entries already in nombres.json: {entries_already_in_json}')
                print('--------------------------------------------')
                # Sets file's current position at offset.
                file.seek(0)
                # convert back to json.
                json.dump(names_to_scrape, file, indent=4)

            page += 1

            buttons = driver.find_elements(By.CSS_SELECTOR, '.g-recaptcha')
            try:
                CAPTCHA_check = driver.find_element(By.CSS_SELECTOR, '.text-uppercase')
                if 'CAPCHA' and 'INCORRECTA' in CAPTCHA_check.text:
                    print('Incorrect CAPTCHA: Run code again')
            except:
                pass

            if direction == 'forward':
                if len(names) < 15:
                    print('No more entries detected')
                    break
                next_page_button = buttons[-1]
                if next_page_button.text == 'Buscar':
                    print('No more entries detected')
                    break
                try:
                    next_page_button.click()
                except:
                    time.sleep(0.1)
                    next_page_button.click()
                time.sleep(2)
            elif direction == 'backward':
                button_list = []
                for button in buttons:
                    button_list.append(button.text)
                if '‹' not in button_list:
                    print('No more entries detected')
                    break
                next_page_button = ''
                for button in buttons:
                    if button.text == '‹':
                        next_page_button = button
                try:
                    next_page_button.click()
                except:
                    time.sleep(0.1)
                    next_page_button.click()
                time.sleep(2)

        except:
            continue


name_scrape('tom', 'forward')
