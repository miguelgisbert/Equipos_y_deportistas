# Reto 1
Grupo 4. Miguel Gisbert y Biel Tió

## Requisitos

- Python 3.x
- SQLite3

## Instalación

1. Clona el repositorio:
    ```sh
    git clone https://github.com/miguel.gisbert/Equipos_y_deportistas

2. Instala las dependencias
    ```sh
    pip install -r requirements.txt

3. Ejecuta el programa
    ```sh
    python reto1.py

4. Sigue las intrucciones que aparecen en el terminal 

## Explicación del problema y justificación de porqué se ha decidido usar el programa “base” seleccionado

<p>El problema principal que encontramos y el fin con el que hemos decidido crear / adaptar este programa, es la falta de control y gestión tanto de jugadores como de equipos dentro de los clubes amateur. Muchos de estos equipos no tienen una gestión adecuada de estos jugadores y con este programa somos capaces de tener un control de todos nuestros equipos y deportistas, así como ser capaces de añadir información adicional de los mismos.</p>
<p>El programa inicial seleccionado, solamente nos permitía añadir, modificar y eliminar elementos dentro de una lista. En este caso, teníamos una lista de deportes a la cual podíamos añadir deportes nuevos, modificar los nombres de los ya creados, eliminarlos o bien una vez creados los nuevos, reordenarlos alfabéticamente. </p>
<p>Teniendo esta base, hemos ampliado las opciones, hemos creado una lista inicial con subcategorías dentro, donde la lista inicial serían todos los equipos de los que dispone un club y dentro de cada equipo, aparecería una segunda lista, esta segunda lista incluiría a todos los jugadores de ese equipo. Además, hemos creado la opción de añadir información relevante de cada subelemento (jugadores) pudiendo así agregar altura, peso y edad.</p>

## Detalle de qué funcionalidades son necesarias, qué le falta al programa seleccionado.

Las funcionalidades necesarias del programa base que deben seguir en el programa final son las funciones:
-	Crear equipo
-	Modificar equipo
-	Eliminar equipo
-	Crear deportista
-	Modificar deportista
-	Eliminar deportista
-	Visualizar equipos y sus deportistas
-	Visualizar un equipo y sus deportistas

Entre las posibles mejoras al programa estarían: 
-	Generar una forma segura de acceder a los datos SQL desde otras aplicaciones
-	Crear una mejor interfaz de usuario para el manejo de los datos
-	Poder ordenar los datos mostrados según campos, filtrar o mostrar estadísticas

## Explicación del programa final

<p>El programa final inicia conectando a la base de datos o creándola si no existe. Además, comprobamos si existen las tablas “Deportistas” y “Clubes” y en caso de que no existan o estén totalmente vacías las crea con unos datos de ejemplo iniciales. Una vez tenemos esto, el programa solicitará al usuario que opción desea, pudiendo elegir la 0 (Salir del programa) o la 1 (Gestión de equipos).</p>

![Menú principal](/images/menu_principal.png#align)


<p>Si el usuario pulsa 0, el programa finaliza y se apagará. Si por lo contrario pulsa 1, se abrirá un nuevo menú de opciones de las cuales tendrá que elegir nuevamente.</p>

![Gestión de equipos](/images/gestion_equipos.png)

<p>Si el usuario pulsa 1, se generará una tabla con todos los equipos existentes a la base de datos con sus respectivos jugadores y sus edades, alturas y pesos.</p>

![Listado de equipos](/images/lista_equipos.png)

<p>Si el usuario pulsa 2, el programa le pedirá al usuario que escriba el nombre del nuevo equipo, en cuanto este escriba el nombre deseado, el nuevo equipo se creará y se unirá directamente a la base de datos.</p>

![Crear equipo](/images/crear_equipo.png)

<p>Si el usuario pulsa 3, el programa pedirá que se escriba el nombre del equipo que desea gestionar y se desplegará una tabla con todos los equipos y deportistas. Una vez seleccionado el equipo que deseamos modificar, se abrirá un nuevo menú: </p>

![Equipo creado](/images/equipo_creado.png)

<p>Con el 1 se generará una lista con los deportistas de ese equipo y los datos asociados a estos. </p>

<p>Con el 2 el programa le preguntará al usuario el nombre del nuevo jugador, a continuación, su altura, su peso y su fecha de nacimiento, una vez introducidos los datos, si son válidos, aparecerá un mensaje de que el jugador ha sido creado e introducido en el equipo X. </p>

![Crear deportista](/images/crear_deportista.png)

<p>Con el 3 modificaremos el nombre y la información de alguno de los deportistas ya creados, al pulsarlo, el programa nos preguntará el nombre del deportista el cual queremos modificar. Si no existe ningún deportista en ese equipo, aparecerá el mensaje “No hay deportistas en el equipo”. Si existen deportistas, el usuario introducirá el nombre del jugador deseado y posteriormente modificará los datos necesarios.</p>

<p>Con el 4 eliminaremos un deportista. El programa nos preguntará que deportista queremos eliminar y el usuario deberá introducir el número del deportista en cuestión. Si no existe ningún deportista aparecerá el mensaje “No hay deportistas en el equipo.” Si introducimos mal el número, aparecerá el mensaje “Número no válido. Intenta de nuevo”.</p>

<p>Se pedirá una confirmación mostrando el nombre del deportista a la cual habrá que responder ‘s’ o ‘S’ de “Sí” si realmente queremos eliminar ese deportista. </p>

<p>Si el usuario pulsa 4, el programa nos preguntará que equipo deseamos eliminar, para ello el usuario deberá escribir el nombre del equipo que quiere eliminar. Si el nombre introducido no coincide con el de ningún equipo, aparecerá el siguiente mensaje “El equipo no existe”. También habrá mensaje de confirmación para eliminar el equipo. </p>

