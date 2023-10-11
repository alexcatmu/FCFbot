# FCFbot

Para hacerlo funcionar:

<br><br>
Paso 1:

Seguir los pasos de [AQUI](https://console.cloud.google.com/apis/credentials?authuser=2&hl=es-419&project=fedecatfut), hasta ***configura la muestra*** (esta parte ya no hay que hacerla)

<br>

Paso 2:

Crear un calendario en el usuario que hemos creado las credenciales y poner el calendarID en la siguiente línea.
```
service.events().insert(calendarId="92968a2bc13b4fc5ad0e75294650004ef1e069449440914adbb80892626d18f5@group.calendar.google.com", body=event).execute()
```

<br>
Paso 3:

Cambiar las siguientes partes del código.
```
    game_line = soup.find(lambda tag: tag.text == 'RAYO VILADECANS, ASSOC. DEPORT.  A').parent.parent
```
Donde pone ***RAYO VILADECANS, ASSOC. DEPORT.  A*** cambiarlo por el nombre del equipo que queramos hacer el calendario.

```
    url = 'https://www.fcf.cat/resultats/2324/futbol-11/quarta-catalana/grup-23/jornada-'
    all_urls = []
    for i in range(1,27):
```

En la url poner el grupo donde se encuentre el equipo del cual queremos copiar el calendario<br>
En la parte de (1,27) cambiar el 27 por la cantidad de jornadas + 1

<br>
Paso 4:

Hacer run a main.py y esperar a que cree todos los eventos. Una vez finalizada la ejecución se habrá añadido el calendario a tu google calendar.


<br><br>
### **Posibles mejoras:**

Añadir las variables a un fichero aparte (nombre de equipo, grupo/categoria, num de jornadas, calendarId).

Crear directamente el calendario y eliminar el calendarId.

Crear una web con un buscador de equipo.