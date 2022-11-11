import json

"""
this function updates registros.json with registry numbers in case nombres_to_scrape.json contains that entry
"""


def update_jsons():
    with open('../Data/nombres_to_scrape.json', 'r') as json_file:
        data_to_scrape = json.load(json_file)

    with open('../Data/registros.json', 'r') as file:
        registros = json.load(file)
        names_without_numero_de_registro = []
        indexes = []
        for idx, obj in enumerate(registros):
            if obj['numero_de_registro'] == '-':
                names_without_numero_de_registro.append(obj['nombre_o_razon_social'])
                indexes.append(idx)
        updates = 0
        for data in data_to_scrape:
            if data['name'] in names_without_numero_de_registro:
                updates += 1
                name_index = names_without_numero_de_registro.index(data['name'])
                index_to_change = indexes[name_index]
                registros[index_to_change]['numero_de_registro'] = data['registro']
                index_to_pop = data_to_scrape.index(data)
                data_to_scrape.pop(index_to_pop)

    print('--------------------------------------------')
    print('Adding numero_de_registro to entries if possible:')
    print(f'jsons updated:  {updates} entries changed')
    print('--------------------------------------------')

    json_object1 = json.dumps(data_to_scrape, indent=4)
    with open('../Data/nombres_to_scrape.json', 'w') as outfile:
        outfile.write(json_object1)

    json_object2 = json.dumps(registros, indent=4)
    with open('../Data/registros.json', 'w') as outfile:
        outfile.write(json_object2)


if __name__ == "__main__":
    update_jsons()

