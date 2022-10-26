import json

# This code updates the nombres_to_scrape.json file if a name was deleted unintentionally

# Open registros.json
with open('../Data/registros.json') as json_file:
    registros = json.load(json_file)
registros = sorted(registros, key=lambda d: d['nombre_o_razon_social'])

# Open nombres_to_scrape.json
with open('../Data/nombres_to_scrape.json') as json_file:
    nombres_to_scrape = json.load(json_file)
nombres_to_scrape.sort()

# open nombres
with open('../Data/nombres.json') as json_file:
    nombres = json.load(json_file)
nombres.sort()

# Fetch names in registros.json
nombres_registrados = []
for obj in registros:
    nombres_registrados.append(obj['nombre_o_razon_social'])

# Append every name to nombres_to_scrape.json
# as long as it is not already contained nombres_to_scrape.json, and is not already in registros.json
for nombre in nombres:
    if nombre not in nombres_to_scrape and nombre not in nombres_registrados:
        nombres_to_scrape.append(nombre)
nombres_to_scrape.sort()

# Updating nombres_to_scrape.json
json_object = json.dumps(nombres_to_scrape, indent=4)
print('Deleting entry from nombres_to_scrape.json')
print('--------------------------------------------')
with open('../Data/nombres_to_scrape.json', 'w') as outfile:
    outfile.write(json_object)

