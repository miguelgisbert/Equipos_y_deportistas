from datetime import datetime
import sqlite3
import os

# Comprovar si el fitxer de la base de dades ja existeix
db_exists = os.path.exists('reto1.db')

# Conexión a la base de datos
conn = sqlite3.connect('reto1.db')
cur = conn.cursor()

# Crear las tablas si no existen
cur.execute('CREATE TABLE IF NOT EXISTS equipos (id INTEGER PRIMARY KEY, nombre TEXT)')
cur.execute('CREATE TABLE IF NOT EXISTS deportistas (id INTEGER PRIMARY KEY, nombre TEXT, altura REAL, peso REAL, fecha_nacimiento TEXT, equipo_id INTEGER, FOREIGN KEY(equipo_id) REFERENCES equipos(id))')

# Comprovar si les taules estan buides
cur.execute('SELECT COUNT(*) FROM equipos')
if cur.fetchone()[0] == 0:
    # Diccionario inicial de equipos y sus deportistas
    equipos = {
        "Infantil A": [
            {"nombre": "Miguel", "altura": 1.75, "peso": 68, "fecha_nacimiento": "2005-04-12"},
            {"nombre": "Biel", "altura": 1.68, "peso": 60, "fecha_nacimiento": "2006-06-23"},
            {"nombre": "Xavi", "altura": 1.70, "peso": 65, "fecha_nacimiento": "2005-11-30"}
        ],
        "Infantil B": [
            {"nombre": "Arnau", "altura": 1.72, "peso": 62, "fecha_nacimiento": "2006-01-15"},
            {"nombre": "Albert", "altura": 1.74, "peso": 64, "fecha_nacimiento": "2005-09-10"},
            {"nombre": "Ricardo", "altura": 1.69, "peso": 63, "fecha_nacimiento": "2006-03-05"}
        ],
    }

    # Insertar equipos en la base de datos
    for equipo, deportistas in equipos.items():
        cur.execute('INSERT INTO equipos (nombre) VALUES (?)', (equipo,))
        equipo_id = cur.lastrowid  # Obtener el ID del equipo recién insertado

        # Insertar deportistas en la base de datos
        for deportista in deportistas:
            cur.execute('INSERT INTO deportistas (nombre, altura, peso, fecha_nacimiento, equipo_id) VALUES (?, ?, ?, ?, ?)',
                        (deportista['nombre'], deportista['altura'], deportista['peso'], deportista['fecha_nacimiento'], equipo_id))

    # Confirmar los cambios
    conn.commit()

def obtener_opcion():
    """
    Solicita al usuario que elija una opción del menú y valida que sea un número entero.
    """
    while True:
        try:
            return int(input("\033[1;36m\nElige una opción: \033[0m"))
        except ValueError:
           print("\033[91mEntrada no válida. Por favor, introduce un número entero.\033[0m")

def obtener_float(mensaje):
    """
    Solicita al usuario que introduzca un número flotante y valida que sea correcto.
    Admite tanto punto decimal como coma decimal.
    """
    while True:
        try:
            valor = input(mensaje).replace(',', '.')
            return float(valor)
        except ValueError:
            print("\033[91mEntrada no válida. Por favor, introduce un número válido.\033[0m")

def obtener_fecha(mensaje):
    """
    Solicita al usuario que introduzca una fecha y valida que sea correcta.
    """
    while True:
        try:
            fecha = input(mensaje)
            fecha_dt = datetime.strptime(fecha, "%Y-%m-%d")
            if fecha_dt >= datetime.today():
                print("\033[91mLa fecha debe ser anterior al día actual. Por favor, introduce una fecha válida.\033[0m")
            else:
                return fecha
        except ValueError:
            print("\033[91mEntrada no válida. Por favor, introduce una fecha válida en el formato YYYY-MM-DD.\033[0m")

def calcular_edad(fecha_nacimiento):
    """
    Calcula la edad a partir de la fecha de nacimiento.
    """
    fecha_nacimiento = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
    hoy = datetime.today()
    edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    return edad

def mostrar_deportistas(equipo_id=None):
    """
    Muestra la lista de equipos y sus deportistas.
    Si se proporciona un equipo_id, muestra solo los deportistas de ese equipo.
    """
    if equipo_id:
        cur.execute('SELECT nombre FROM equipos WHERE id = ?', (equipo_id,))
        equipo = cur.fetchone()
        if not equipo:
            print(f"\033[91mEl equipo con ID {equipo_id} no existe.\033[0m")
            return
        equipo_nombre = equipo[0]
        cur.execute('SELECT nombre, altura, peso, fecha_nacimiento FROM deportistas WHERE equipo_id = ?', (equipo_id,))
        deportistas = cur.fetchall()
        equipos_a_mostrar = {equipo_nombre: deportistas}
    else:
        cur.execute('SELECT id, nombre FROM equipos')
        equipos = cur.fetchall()
        equipos_a_mostrar = {}
        for equipo in equipos:
            equipo_id, equipo_nombre = equipo
            cur.execute('SELECT nombre, altura, peso, fecha_nacimiento FROM deportistas WHERE equipo_id = ?', (equipo_id,))
            deportistas = cur.fetchall()
            equipos_a_mostrar[equipo_nombre] = deportistas
    if not equipos_a_mostrar:
        print("\033[91mNo hay equipos.\033[0m")
        return
    print("\033[94m\nLista de equipos:\033[0m")
    for equipo, deportistas in equipos_a_mostrar.items():
        print(f"\033[92m\n{equipo}\033[0m - Deportistas ({len(deportistas)}):")
        print(f"\033[33m{'#':<5} {'Nombre':<25} {'Altura':<10} {'Peso':<7} {'Edad':<15}\033[0m")
        print("-" * 65)
        for i, deportista in enumerate(deportistas, start=1):
            nombre, altura, peso, fecha_nacimiento = deportista
            if len(nombre) > 20:
                nombre = nombre[:20] + '(...)'
            altura = f"{altura:.2f}"
            peso = round(peso)
            edad = calcular_edad(fecha_nacimiento)
            print(f"{i:<5} {nombre:<25} {altura:<10} {peso:<7} {edad:<15}")

def gestion_deportistas(equipo_id):
    """
    Submenú para gestionar los deportistas dentro de un equipo específico.
    """
    while True:
        cur.execute('SELECT nombre FROM equipos WHERE id = ?', (equipo_id,))
        equipo = cur.fetchone()
        if not equipo:
            print(f"\033[91mEl equipo con ID {equipo_id} no existe.\033[0m")
            return
        equipo_nombre = equipo[0]

        print(f"\033[94m\n--- Gestión de Deportistas en el equipo {equipo_nombre} ---\033[0m")
        print("0: Volver al menú anterior")
        print("1: Ver deportistas")
        print("2: Añadir deportista")
        print("3: Modificar deportista")
        print("4: Eliminar deportista\n")
        
        opcion = obtener_opcion()
        
        if opcion == 0:
            break
        elif opcion == 1:
            # Ver deportistas
            mostrar_deportistas(equipo_id)
        elif opcion == 2:
            # Añadir deportista
            nombre = input("\033[1;36m\nEscribe el nombre del nuevo deportista: \033[0m")
            altura = obtener_float("\033[1;36m\nEscribe la altura del nuevo deportista (en metros): \033[0m")
            peso = obtener_float("\033[1;36m\nEscribe el peso del nuevo deportista (en kg): \033[0m")
            fecha_nacimiento = obtener_fecha("\033[1;36m\nEscribe la fecha de nacimiento del nuevo deportista (YYYY-MM-DD): \033[0m")
            cur.execute('INSERT INTO deportistas (nombre, altura, peso, fecha_nacimiento, equipo_id) VALUES (?, ?, ?, ?, ?)',
                        (nombre, altura, peso, fecha_nacimiento, equipo_id))
            conn.commit()
            print(f"\033[92m{nombre} ahora está en {equipo_nombre}!\033[0m")
        elif opcion == 3:
            # Modificar deportista
            cur.execute('SELECT id, nombre FROM deportistas WHERE equipo_id = ?', (equipo_id,))
            deportistas = cur.fetchall()
            if not deportistas:
                print("\033[91mNo hay deportistas en el equipo.\033[0m")
                continue
            mostrar_deportistas(equipo_id)
            try:
                num_deportista = int(input("\033[1;36m\nEscribe el número del deportista a modificar: \033[0m")) - 1
                deportista_id = deportistas[num_deportista][0]
                nombre = input("\033[1;36m\nEscribe el nombre del nuevo deportista: \033[0m")
                altura = obtener_float("\033[1;36m\nEscribe la altura del nuevo deportista (en metros): \033[0m")
                peso = obtener_float("\033[1;36m\nEscribe el peso del nuevo deportista (en kg): \033[0m")
                fecha_nacimiento = obtener_fecha("\033[1;36m\nEscribe la fecha de nacimiento del nuevo deportista (YYYY-MM-DD): \033[0m")
                cur.execute('UPDATE deportistas SET nombre = ?, altura = ?, peso = ?, fecha_nacimiento = ? WHERE id = ?',
                            (nombre, altura, peso, fecha_nacimiento, deportista_id))
                conn.commit()
                print(f"\033[92mModificación realizada para {nombre}!\033[0m")
            except (IndexError, ValueError):
                print("\033[91mNúmero no válido. Intenta de nuevo.\033[0m")
        elif opcion == 4:
            # Eliminar deportista
            cur.execute('SELECT id, nombre FROM deportistas WHERE equipo_id = ?', (equipo_id,))
            deportistas = cur.fetchall()
            if not deportistas:
                print("\033[91mNo hay deportistas en el equipo.\033[0m")
                continue
            mostrar_deportistas(equipo_id)
            try:
                num_deportista = int(input("\033[1;36m\nEscribe el número del deportista a eliminar: \033[0m")) - 1
                deportista_id = deportistas[num_deportista][0]
                confirmacion = input("\033[1;36m\nVas a eliminar al deportista: \033[0m" + deportistas[num_deportista][1] + "\033[1;36m\n¿Estás seguro? (Sí (S), No (N)): \033[0m")
                if (confirmacion == 'S' or confirmacion == 's'):
                    cur.execute('DELETE FROM deportistas WHERE id = ?', (deportista_id,))
                    conn.commit()
                    print(f"\033[92mEl deportista ha sido eliminado del equipo {equipo_nombre}.\033[0m")
            except (IndexError, ValueError):
                print("\033[91mEntrada no válida. Intenta de nuevo.\033[0m")
        else:
            print("\033[91mOpción no válida. Intenta de nuevo.\033[0m")

def eliminar_equipo():
    """
    Elimina un equipo y todos sus deportistas.
    """
    mostrar_deportistas()
    try:
        nombre_equipo = input("\033[1;36m\nEscribe el nombre del equipo a eliminar: \033[0m")
        cur.execute('SELECT id FROM equipos WHERE nombre = ?', (nombre_equipo,))
        equipo = cur.fetchone()
        if equipo:
            equipo_id = equipo[0]
            confirmacion = input("\033[1;36m\nVas a eliminar al equipo: \033[0m" + nombre_equipo + "\033[1;36m\n¿Estás seguro? (Sí (S), No (N)): \033[0m")
            if (confirmacion == 'S' or confirmacion == 's'):
                cur.execute('DELETE FROM deportistas WHERE equipo_id = ?', (equipo_id,))
                cur.execute('DELETE FROM equipos WHERE id = ?', (equipo_id,))
                conn.commit()
                print(f"\033[92mEl equipo {nombre_equipo} y todos sus deportistas han sido eliminados.\033[0m")
        else:
            print("\033[91mEl equipo no existe.\033[0m")
    except (IndexError, ValueError):
        print("\033[91mEntrada no válida. Intenta de nuevo.\033[0m")

def gestion_equipos():
    """
    Submenú de gestión de equipos en el club.
    """
    while True:
        print("\033[94m\n--- Gestión de Equipos ---\033[0m")
        print("0: Volver al menú principal")
        print("1: Ver todos los equipos y deportistas")
        print("2: Añadir equipo")
        print("3: Seleccionar equipo para gestionar deportistas")
        print("4: Eliminar equipo")
        
        opcion = obtener_opcion()
        
        if opcion == 0:
            break
        elif opcion == 1:
            mostrar_deportistas()
        elif opcion == 2:
            nombre_equipo = input("\033[1;36m\nEscribe el nombre del nuevo equipo: \033[0m")
            cur.execute('INSERT INTO equipos (nombre) VALUES (?)', (nombre_equipo,))
            conn.commit()
            print(f"\033[92mEl equipo {nombre_equipo} ha sido añadido al club.\033[0m")
        elif opcion == 3:
            mostrar_deportistas()
            nombre_equipo = input("\033[1;36m\nEscribe el nombre del equipo a gestionar: \033[0m")
            cur.execute('SELECT id FROM equipos WHERE nombre = ?', (nombre_equipo,))
            equipo = cur.fetchone()
            if equipo:
                equipo_id = equipo[0]
                gestion_deportistas(equipo_id)
            else:
                print("\033[91mEl equipo no existe.\033[0m")
        elif opcion == 4:
            eliminar_equipo()
        else:
            print("\033[91mOpción no válida. Intenta de nuevo.\033[0m")

def menu_principal():
    """
    Menú principal del programa.
    """
    while True:
        print("\033[94m\n--- Menú Principal ---\033[0m")
        print("0: Salir")
        print("1: Gestión de Equipos")
        
        opcion = obtener_opcion()
        
        if opcion == 0:
            print("\033[94mSaliendo del programa.\033[0m")
            break
        elif opcion == 1:
            gestion_equipos()
        else:
            print("\033[91mOpción no válida. Intenta de nuevo.\033[0m")

# Ejecutar el menú principal
if __name__ == "__main__":
    menu_principal()

# Cerrar la conexión al final del programa
conn.close()