# gestor_notas.py

import random  
from colorama import init, Fore, Style  # [VOLUNTARIO: Uso de librería externa colorama]

# Inicializamos colorama para que el color vuelva a la normalidad automáticamente
init(autoreset=True)

def mostrar_menu():
    # Imprime las opciones del menú principal en pantalla con colores.
    print(Fore.CYAN + Style.BRIGHT + "\n--- MENÚ PRINCIPAL ---")
    print(Fore.CYAN + "1. Añadir una nota.")
    print(Fore.CYAN + "2. Ver todas las notas.")
    print(Fore.CYAN + "3. Buscar una nota por palabra clave.")
    print(Fore.CYAN + "4. Eliminar una nota.")
    # [VOLUNTARIO: Opción extra para filtrar categorías]
    print(Fore.CYAN + "5. Filtrar notas por categoría. " + Fore.YELLOW + "(¡Mejora!)") 
    print(Fore.CYAN + "6. Salir.")

# [Opción 1 - Añadir una nota]
# Pide los datos al usuario y añade la nota a la lista, controlando duplicados.
def añadir_nota(notas):
    
    print(Fore.YELLOW + Style.BRIGHT + "\n--- AÑADIR NUEVA NOTA ---")
    
    titulo = input("Introduce el título de la nota: ").strip()
    
    # Comprobamos si el título ya existe en la lista de notas
    indice_existente = -1
    for i, nota in enumerate(notas):
        # Ignoramos mayúsculas/minúsculas usando .lower()
        if nota['titulo'].lower() == titulo.lower():
            indice_existente = i  
            break  
            
    if indice_existente != -1:
        print(Fore.RED + "⚠️ Atención: Ya existe una nota con ese título.")
        # Preguntamos si se quiere sobreescribir 
        sobreescribir = input("¿Quieres sobreescribirla? (s/n): ").strip().lower()
        if sobreescribir != 's':
            print(Fore.RED + "❌ Operación cancelada. No se ha modificado la nota.")
            return  
            
    contenido = input("Introduce el contenido de la nota: ").strip()
    
    # [VOLUNTARIO: Añadir categorías a las notas]
    categoria = input("Introduce una categoría (ej: estudio, personal, trabajo): ").strip()
    if not categoria: 
        categoria = "General"
        
    # [VOLUNTARIO: Asignamos colores aleatorios a las diferentes categorias sin usar el blanco porque contrasta mal con el fondo]
    color_categoria = None
    for nota_guardada in notas:
        if nota_guardada.get('categoria', '').lower() == categoria.lower():
            color_categoria = nota_guardada.get('color')
            break
            
    if not color_categoria:
        colores_disponibles = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
        color_categoria = random.choice(colores_disponibles)

    # Pedimos la confirmación final antes de guardar la nota
    confirmacion = input("¿Guardar esta nota? (s/n): ").strip().lower()
    
    if confirmacion == 's':
        # Guardamos la nota como un diccionario con título, contenido, categoría y color
        nueva_nota = {
            "titulo": titulo, 
            "contenido": contenido, 
            "categoria": categoria, 
            "color": color_categoria
        }
        
        # Usamos if/else para sobreescribir o añadir una nota
        if indice_existente != -1:
            notas[indice_existente] = nueva_nota
            print(Fore.GREEN + "✅ Nota sobreescrita con éxito.")
        else:
            notas.append(nueva_nota) # Las añadimos a la lista usando .append()
            print(Fore.GREEN + "✅ Nota guardada con éxito.")
    else:
        print(Fore.RED + "❌ Operación cancelada. La nota no se ha guardado.")
 
# [Opción 2 - Ver todas las notas]
# Muestra todas las notas guardadas y numeradas. Puede filtrar y mostrar estadísticas
def ver_notas(notas, filtro_categoria=None):
   
     # [VOLUNTARIO: Filtrar notas por categoría]
    if filtro_categoria:
       
        notas_a_mostrar = [n for n in notas if n['categoria'].lower() == filtro_categoria.lower()]
        print(Fore.YELLOW + Style.BRIGHT + f"\n--- NOTAS DE LA CATEGORÍA: {filtro_categoria.upper()} ---")
    else:
        notas_a_mostrar = notas
        print(Fore.YELLOW + Style.BRIGHT + "\n--- TUS NOTAS ---")
        
    # Mostramos un mensaje si la lista está vacía
    if len(notas_a_mostrar) == 0:
        print(Fore.CYAN + "ℹ️ No hay notas para mostrar aquí.")
    else:
        # Mostramos las notas numeradas usando start=1 para que empiece desde 1 en lugar de 0
        for indice, nota in enumerate(notas_a_mostrar, start=1):
            color_cat = nota.get('color', Fore.RESET)
            print(Fore.GREEN + f"[{indice}] {nota['titulo']} " + color_cat + f"({nota['categoria']})")
            print(f"    {nota['contenido']}")
            
        # [VOLUNTARIO: Mostrar las estadísticas de las notas]
        total_notas = len(notas_a_mostrar)
        longitud_total = sum(len(nota['contenido']) for nota in notas_a_mostrar)
        media_caracteres = longitud_total / total_notas
        
        print(Fore.BLUE + Style.BRIGHT + "\n📊 --- ESTADÍSTICAS ---")
        print(Fore.BLUE + f"Total de notas mostradas: {total_notas}")
        print(Fore.BLUE + f"Longitud media del contenido: {media_caracteres:.1f} caracteres")

# [Opción 3 - Buscar nota por palabra clave]
# Busca notas por palabra clave en título y contenido.
def buscar_nota(notas):
    
    print(Fore.YELLOW + Style.BRIGHT + "\n--- BUSCAR NOTA ---")
    
    if len(notas) == 0:
        print(Fore.CYAN + "ℹ️ No hay notas guardadas para buscar.")
        return

    palabra_clave = input("Introduce la palabra clave a buscar: ").strip().lower()
    encontrada = False 
    
    print(Fore.YELLOW + "\n--- RESULTADOS DE BÚSQUEDA ---")
    # Usamos bucles FOR para recorrer las notas y buscar la palabra clave en título y contenido, ignorando mayúsculas/minúsculas
    for indice, nota in enumerate(notas, start=1):
        titulo_min = nota['titulo'].lower()
        contenido_min = nota['contenido'].lower()
        
        # Comprobamos si la palabra clave está en el título o en el contenido
        if palabra_clave in titulo_min or palabra_clave in contenido_min:
            color_cat = nota.get('color', Fore.RESET)
            print(Fore.GREEN + f"[{indice}] {nota['titulo']} " + color_cat + f"({nota['categoria']})")
            print(f"    {nota['contenido']}")
            encontrada = True 
            
    if not encontrada:
        print(Fore.RED + f"❌ No se encontró ninguna nota que contenga la palabra '{palabra_clave}'.")

# [Opción 4 - Eliminar una nota]
# Elimina una nota según el número elegido, comprobando posibles errores en la entrada
def eliminar_nota(notas):
    
    print(Fore.YELLOW + Style.BRIGHT + "\n--- ELIMINAR NOTA ---")
    
    if len(notas) == 0:
        print(Fore.CYAN + "ℹ️ No hay notas para eliminar.")
        return
        
    ver_notas(notas) 
    entrada = input("\nIntroduce el número de la nota que quieres eliminar (o 'c' para cancelar): ").strip()
    
    if entrada.lower() == 'c':
        print(Fore.RED + "❌ Operación cancelada.")
        return
        
    # Manejamos errores de entrada que no sean números usando isdigit() para evitar que se rompa el programa
    if not entrada.isdigit():
        print(Fore.RED + "❌ Error: Debes introducir un número válido, no letras.")
        return
        
    numero_nota = int(entrada)
    
    # Comprobamos que el número introducido sea válido (dentro del rango)
    if 1 <= numero_nota <= len(notas):
        indice = numero_nota - 1 
        nota_a_eliminar = notas[indice]
        
        confirmacion = input(Fore.RED + f"⚠️ ¿Seguro que quieres eliminar '{nota_a_eliminar['titulo']}'? (s/n): ").strip().lower()
        if confirmacion == 's':
            # Eliminamos la nota de la lista usando .pop() para eliminar por índice
            notas.pop(indice)
            print(Fore.GREEN + "✅ Nota eliminada correctamente.")
        else:
            print(Fore.RED + "❌ Operación cancelada. La nota no se ha eliminado.")
    else:
        print(Fore.RED + "❌ Error: Ese número de nota no existe.")

# [Función principal MAIN que controla el flujo]
# Es el bucle principal que inicializa los datos y llama al resto de funciones
def main():
    
    print(Fore.GREEN + Style.BRIGHT + "¡Bienvenido al Gestor de Notas Personalizado!")
    
    # Lista principal que guardará las notas (diccionarios) en memoria
    notas = [] 
    
    # Bucle general while que mantiene el programa vivo hasta que el usuario decida salir (Opción 6)
    while True:
        mostrar_menu()
        opcion = input(Fore.CYAN + "\nElige una opción (1-6): ").strip()
        
        if opcion == '1':
            añadir_nota(notas)
        elif opcion == '2':
            ver_notas(notas)
        elif opcion == '3':
            buscar_nota(notas)
        elif opcion == '4':
            eliminar_nota(notas)
        elif opcion == '5': # [VOLUNTARIO: Acceso al filtrado por categoría]
            cat = input("¿Qué categoría quieres filtrar?: ").strip()
            ver_notas(notas, filtro_categoria=cat)
        elif opcion == '6':
            # [Opción 6 - Salir del programa]
            print(Fore.GREEN + Style.BRIGHT + "Saliendo del Gestor de Notas. ¡Hasta pronto!")
            break
        else:
            # Mensaje de error para tolerar entradas incorrectas en el menú principal
            print(Fore.RED + "❌ Opción no válida. Por favor, introduce un número del 1 al 6.")

# Este bloque asegura que main() solo se ejecute si este archivo se ejecuta directamente (no si se importa desde otro archivo Python).
if __name__ == "__main__":
    main()

"""
[Sección 7 - Entrega y evaluación. Comentario final]
---------------------------------------------------------
DATOS DEL ALUMNO Y EXPLICACIÓN DEL CÓDIGO
---------------------------------------------------------
Nombre: Diego Santos Fernández
Fecha: 16/04/2026

Explicación:
Este programa es un gestor de notas estructurado en funciones.
Cumple con todos los requisitos técnicos del PDF usando una 
lista de diccionarios ('notas') para almacenar la información, 
bucles (while y for), y condicionales para validar las entradas 
y evitar que el programa se rompa (ej: isdigit()). 

Además, se han implementado la parte voluntaria: 
1. Las notas tienen categorías y opción de filtrado.
2. Visualización de estadísticas (total de notas y media de caracteres).
3. Interfaz mejorada con 'colorama' y 'random' para asignar 
   colores dinámicos a las categorías (excluyendo el blanco).
---------------------------------------------------------
"""