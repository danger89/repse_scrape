# REPSE Scraper - Documentación y Manual de Uso
## Información General
Se desarrolló un programa en Python que permite la extracción de datos de https://repse.stps.gob.mx/.
Debido a la architectura de la página, para recuperar todos los datos, es necesario emplear dos extracciones:
* Extracción de nombres de registro
* Extracción de datos de cada nombre <br/>
<!-- -->
A continuación, se muestra la estructura de las carpetas a usar:

### Carpetas
![repse_img5](https://user-images.githubusercontent.com/108626360/199153187-9e032976-9c91-412b-b7a7-b5df5f808063.JPG)
* **Data**: Contiene los datos extraídos en formato json y Excel
* **Scrape**: Contiene los códigos que realizan la extracción de datos

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
* **Registros_REPSE.xlsx**: Excel que contiene los datos de cada registro

## Manual de Uso

### Extracción de nombres de registro
Para extraer los nombres de todos los registros, se debe correr "**nombres_scrape.py**". Dentro de este script, se encuentra una función que contiene dos parámetros:
* **keyword**:  Acota los resultados a registros que contengan el keyword
* **direction**: Ejecuta la extracción de nombres en la dirección especificada
  * **"forward"**: Ejecuta la extracción de nombres de ''a'' a ''z''
  * **"backward**: Ejecuta la extracción de nombres de ''z'' a ''a''
  <!-- -->
<!-- -->
![repse_img6](https://user-images.githubusercontent.com/108626360/199155284-f3cfff3c-f6c8-4cb7-aa1f-b361bc9350c0.JPG) <br/> <br/> 
El script ejecutará el programa "**driver.exe**", abriendo un driver de Google Chrome que dará inicio a la extracción de nombres.
<br/> <br/>
Los nombres que aún no han sido extraídos se guardarán en "**nombres.json**" y en "**nombres_to_scrape.json**"
en la carpeta "**Data**". Previo a la divulgación del código, "**nombres.json**" ya cuenta con más de 80,000 nombres únicos, que representa aproximadamente el 62.6% de todos los registros existentes.
<br/> <br/>
```Nota importante``` Es necesario insertar un keyword, ya que la extracción de todos los nombres sin filtro es extremadamente díficl de correr sin problemas. Se recomienda usar keywords de tres o cuatros letras.  

### Extracción de datos de registro
Para extraer los datos de cada registro se debe correr "**registros_scrape.py**". <br/> <br/>
![repse_img7](https://user-images.githubusercontent.com/108626360/199155486-f1fd328c-bb75-4ccc-acc7-3869e315df95.JPG) <br/> <br/>
El script ejecutará el programa "**driver.exe**", abriendo un driver de Google Chrome que dará inicio a la extracción de datos de cada registro, alimentándose de los nombres en "**nombres_to_scrape.json**".
<br/> <br/>
Al extraer los datos de un registro exitosamente, el nombre del registro será borrado automáticamente de "**nombres_to_scrape.json**" y los datos serán guardados en "**registros.json**" y en el archivo Excel "**Registros_REPSE.xlsx**". Si por alguna razón, el nombre no contiene datos o ya están sus datos en "**registros.json**", será borrado de "**nombres_to_scrape.json**" sin cambios al excel o a la base de datos.

### Uso de VPN
Debido al reCAPTCHA que está implementado en la página, no se permitirá la extracción de datos después de una cantidad determinada de interacciones automatizadas en ella. Para rodear este problema, se recomienda el uso de un VPN (códigos probados con ExpressVPN).
<br/> <br/>
Si ocurre un bloqueo o no se permite el acceso a los datos (se regresa a la página inicial constantemente), es necesario cambiar a una ubicación distinta utilizando el VPN. <br/> <br/>
<img src="https://user-images.githubusercontent.com/108626360/199156779-3c523670-8d91-4a5d-bc26-a3308ae4a99c.JPG" width = 25%>

## Dependencias
Para el correcto funcionamiento de los scripts de Python, se especifican a continuación los requerimientos:
* fake_useragent==0.1.11
* pandas==1.5.1
* selenium==4.5.0
* webdriver_manager==3.8.4
<!-- -->
Los códigos fueron probados con Python 3.9.

## Posibles Problemas
* Dentro de las funciones que realizan los scrapes, se utiliza el método "**time.sleep()**" antes de oprimir cada botón. Esto se hace para esperar a que el botón   cargue y no se oprima antes de tiempo. En caso de tener una computadora lenta o una mala conexión a internet, es posible que los tiempos de espera establecidos en el código no sean suficientes para que los botones aparezcan a tiempo. Si este es el caso, deberán ajustar el tiempo en el "**time.sleep()**" correspondiente del botón que no carga a tiempo. <br/> <br/>
  <img src="https://user-images.githubusercontent.com/108626360/199157396-ff6845c4-cc40-4408-812a-be69e0642b64.jpg" width = 50%> <br/> <br/>

* En los códigos de extracción de datos, se utiliza la versión de Windows del programa "**driver.exe**". Para correr el código en otro sistema operativo, se requiere reemplazar este programa con la versión correspondiente, que se puede encontrar en [esta liga]. También es necesario nombrar el programa "**driver.exe**" y colocarlo en la carpeta "**Scrape**".
<!-- -->
[esta liga]: https://chromedriver.chromium.org/downloads

## Posibles Mejoras
El cambio de ubicación (IP address) utilizando un VPN es un proceso manual y debe realizarse siempre que haya un bloqueo por el reCAPTCHA. Este proceso se podría automatizar en Python utilizando un wrapper de ExpressVPN (o cualquier otro VPN) y cambiando la ubicación desde Python cuando se cumplan ciertos criterios. Desafortunadamente, no se encontró suficiente información acerca del tema para su implementación en Windows. No obstante, es algo que vale la pena investigar si se busca correr el código por un tiempo indefinido.

## Alternativa
En caso de tener dificultades mayores para correr los códigos, me puedo ofrecer personalmente para llevar a cabo la extracción y generar el documento Excel. Actualmente tengo la capacidad para extraer 3000-5000 registros al día utilizando los códigos. 

## Contacto
Para cualquier información adicional o problemas con los códigos, estoy a su disposición en el siguiente medio de contacto:
* Correo: marcelovillarrealx@outlook.com



 


