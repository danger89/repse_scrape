# REPSE Scraper - Documentación y Manual de Uso
## Información General
Se desarrolló un programa en Python que permite la extracción de datos de https://repse.stps.gob.mx/.
Debido a la architectura de la página, para recuperar todos los datos, es necesario emplear dos extracciones:
* Extracción de nombres de registro
* Extracción de datos de cada nombre <br/>
<!-- -->
A continuación, se muestra la estructura de las carpetas a usar: <br/> <br/>
![repse_img5](https://user-images.githubusercontent.com/108626360/199153187-9e032976-9c91-412b-b7a7-b5df5f808063.JPG)

### Carpeta "Scrape"
![repse_img4](https://user-images.githubusercontent.com/108626360/199153939-1d231009-bda5-4f8f-af46-f1544a5ea55e.JPG)
* **driver.exe**: Archivo ejecutable que contiene un driver de Google Chrome
* **nombres_scrape.py**: Python script que extrae los nombres de los registros
* **registros_scrape.py**: Python script que extrae los datos de un registro, dado el nombre

### Carpeta "Data"
![repse_img3](https://user-images.githubusercontent.com/108626360/199154149-9e2cbb2c-7f54-4df7-8249-a0679ebb60cc.JPG)
* **nombres.json**: Contiene todos los nombres extraídos
* **nombres_to_scrape.json**: Contiene los nombres cuyos datos no han sido extraídos
* **registros.json**: Contiene los datos extraídos de cada registro
* **Registros_REPSE.xlsx**: Excel que contiene los datos de cada registroe

## Manual de Uso
### Extracción de nombres de registro
Para extraer los nombres de todos los registros, se debe correr "nombres\_scrape.py". Dentro de este script, se encuentra una función que contiene dos parámetros:
* **keyword**:  Acota los resultados a registros que contengan el keyword.
* **direction**: Ejecuta la extracción de nombres en la dirección especificada
  * **"forward"**: Ejecuta la extracción de nombres de ''a'' a ''z''
  * **"backward**: Ejecuta la extracción de nombres de ''z'' a ''a''
  <!-- -->
<!-- -->
![repse_img6](https://user-images.githubusercontent.com/108626360/199155284-f3cfff3c-f6c8-4cb7-aa1f-b361bc9350c0.JPG) <br/> <br/> 
El script ejecutará el programa "driver.exe", abriendo un driver de Google Chrome que dará inicio a la extracción de nombres.
<br/> <br/>
Los nombres que aún no han sido extraídos se guardarán en "nombres.json" y en "nombres_to_scrape.json"
en la carpeta "Data". Previo a la divulgación del código, "nombres.json" ya cuenta con más de 80,000 nombres únicos, que representa aproximadamente el 62.6% de todos los registros existentes.
<br/> <br/>
Nota importante: Es necesario insertar un keyword, ya que la extracción de todos los nombres sin filtro es extremadamente díficl de correr sin problemas. Se recomienda usar keywords de tres o cuatros letras.  


### Extracción de datos de registro
Para extraer los datos de cada registro se debe correr ''registros\_scrape.py''. <br/> <br/>
![repse_img7](https://user-images.githubusercontent.com/108626360/199155486-f1fd328c-bb75-4ccc-acc7-3869e315df95.JPG) <br/> <br/>
El script ejecutará el programa "driver.exe", abriendo un driver de Google Chrome que dará inicio a la extracción de datos de cada registro, alimentándose de los nombres en "nombres\_to\_scrape.json".
<br/> <br/>
Al extraer los datos de un registro exitosamente, el nombre del registro será borrado automáticamente de "nombres_to_scrape.json" y los datos serán guardados en "registros.json" y en el archivo Excel "Registros_REPSE.xlsx". Si por alguna razón, el nombre no contiene datos o ya están sus datos en "registros.json", será borrado de "nombres_to_scrape.json" sin cambios al excel o a la base de datos.
