# REPSE Scraper - Documentación y Manual de Uso
## Información General
Se desarrolló un programa en Python que permite la extracción de datos de https://repse.stps.gob.mx/.
Debido a la architectura de la página, para recuperar todos los datos, es necesario emplear dos extracciones:
* Extracción de nombres de registro
* Extracción de datos de cada nombre <br/>
<!-- -->
A continuación, se muestra la estructura de las carpetas a usar: <br/> <br/>
![repse_img5](https://user-images.githubusercontent.com/108626360/199153187-9e032976-9c91-412b-b7a7-b5df5f808063.JPG)

#### Carpeta "Scrape"
* driver.exe: Archivo ejecutable que contiene un driver de Google Chrome
* nombres_scrape.py: Python script que extrae los nombres de los registros
* registros_scrape.py: Python script que extrae los datos de un registro, dado el nombre
