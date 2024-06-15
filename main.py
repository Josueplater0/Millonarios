# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 22:38:24 2024

@author: Jeaouth
"""
import json
import random
import time
import webbrowser

# Variables globales para seguimiento de comodines
comodines_usados = {
    "amigo": False,
    "50_50": False,
    "publico": False
}

# Guardar estadísticas de juego
estadisticas_juego = {
    "nombre": "",
    "correctas": 0,
    "incorrectas": 0,
    "comodines_usados": 0
}

def cargar_preguntas(archivo):
    try:
        with open(archivo, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error cargando {archivo}: {e}")
        return []

def hacer_pregunta(pregunta):
    tiempo_total = 30
    print("\n" + pregunta["pregunta"])
    for i, opcion in enumerate(pregunta["opciones"], 1):
        print(f"{i}. {opcion}")

    inicio = time.time()
    while True:
        tiempo_restante = tiempo_total - int(time.time() - inicio)
        if tiempo_restante <= 0:
            print("\n¡Tiempo agotado!")
            estadisticas_juego["incorrectas"] += 1
            return False
        
        print(f"\rTiempo restante: {tiempo_restante} segundos", end='', flush=True)
        respuesta = input("\nSelecciona una opción (1, 2, 3, 4, 5, 6, 7): ")
        
        if respuesta == "5" and not comodines_usados["amigo"]:
            usar_comodin_amigo()
            comodines_usados["amigo"] = True
            estadisticas_juego["comodines_usados"] += 1
            continue
        elif respuesta == "6" and not comodines_usados["50_50"]:
            hacer_pregunta_50_50(pregunta)
            comodines_usados["50_50"] = True
            estadisticas_juego["comodines_usados"] += 1
            continue
        elif respuesta == "7" and not comodines_usados["publico"]:
            hacer_pregunta_publico()
            comodines_usados["publico"] = True
            estadisticas_juego["comodines_usados"] += 1
            continue
        elif not respuesta.isdigit():
            estadisticas_juego["incorrectas"] += 1
            return False  # Si la respuesta no es un número, es incorrecta
        
        respuesta_int = int(respuesta)
        if respuesta_int == pregunta["correcta"]:
            estadisticas_juego["correctas"] += 1
            return True
        else:
            estadisticas_juego["incorrectas"] += 1
            return False

def usar_comodin_amigo():
    webbrowser.open("https://www.google.com", new=2)

def hacer_pregunta_50_50(pregunta):
    print("Has elegido el comodín 50/50.")
    opciones_correcta = pregunta["correcta"]
    opciones_incorrectas = [i+1 for i in range(4) if i+1 != opciones_correcta]
    opciones_eliminar = random.sample(opciones_incorrectas, 2)
    print("Opciones restantes:")
    print(f"{opciones_correcta}. {pregunta['opciones'][opciones_correcta - 1]}")
    print(f"{opciones_eliminar[0]}. {pregunta['opciones'][opciones_eliminar[0] - 1]}")

def hacer_pregunta_publico():
    estadistica = random.randint(1, 4)
    print(f"Según mi estadística, la opción {estadistica} puede ser la respuesta correcta.")

def jugar_preguntas(archivo_preguntas):
    preguntas = cargar_preguntas(archivo_preguntas)
    
    if len(preguntas) < 5:
        print("No hay suficientes preguntas para jugar.")
        return False

    preguntas_seleccionadas = random.sample(preguntas, 5)
    correctas = 0

    for i, pregunta in enumerate(preguntas_seleccionadas, 1):
        print(f"\nPregunta {i}:")
        if hacer_pregunta(pregunta):
            print("¡Correcto!")
            correctas += 1
        else:
            print("¡Incorrecto o tiempo agotado!")
            return False  # Si falla una pregunta, no puede avanzar

    if correctas == 5:
        print("¡Has respondido todas las preguntas correctamente!")
        return True  # Solo si responde todas las preguntas correctamente, puede avanzar
    else:
        return False

def mostrar_menu():
    print("=== Menú Principal ===")
    print("1. Jugar")
    print("2. Créditos")
    print("3. Clasificación")
    print("4. Salir")
    print("=====================")

def mostrar_menu_dificultad():
    print("=== Selecciona Dificultad ===")
    print("1. Fácil")
    print("2. Intermedia")
    print("3. Difícil")
    print("4. Volver")
    print("=============================")

def jugar_dificultad(dificultad, estados_dificultades):
    if dificultad == "Fácil":
        if jugar_preguntas('preguntas_facil.json'):
            estados_dificultades["Facil"] = True
    elif dificultad == "Intermedia":
        if estados_dificultades["Facil"]:
            if jugar_preguntas('preguntas_intermedia.json'):
                estados_dificultades["Intermedia"] = True
        else:
            print("Debes completar la dificultad Fácil primero.")
    elif dificultad == "Difícil":
        if estados_dificultades["Intermedia"]:
            jugar_preguntas('preguntas_dificil.json')
        else:
            print("Debes completar la dificultad Intermedia primero.")

def jugar(estados_dificultades):
    global comodines_usados
    estadisticas_juego["nombre"] = input("Ingresa tu nombre: ")
    while True:
        mostrar_menu_dificultad()
        opcion = input("Selecciona una opción (1, 2, 3) o '4' para regresar: ")

        if opcion == "1":
            jugar_dificultad("Fácil", estados_dificultades)
        elif opcion == "2":
            jugar_dificultad("Intermedia", estados_dificultades)
        elif opcion == "3":
            jugar_dificultad("Difícil", estados_dificultades)
        elif opcion == "4":
            break
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")
    
    guardar_estadisticas()
    comodines_usados = {"amigo": False, "50_50": False, "publico": False}

def mostrar_creditos():
    while True:
        print("=== Créditos ===")
        print("Juego desarrollado por:")
        print(" Ángel de Jesús Alfaro Gómez")
        print(" Ángel Ernesto Cornejo Vázquez")
        print(" Jeremy Neftalí Arias Sáenz")
        print(" Josué Salvador Platero Ramírez")
        print("4. Volver al menú principal")
        print("================")
        opcion = input("Selecciona una opción: ")

        if opcion == "4":
            break
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")

def guardar_estadisticas():
    try:
        with open('clasificacion.json', 'r', encoding='utf-8') as file:
            clasificacion = json.load(file)
    except FileNotFoundError:
        clasificacion = []

    clasificacion.append(estadisticas_juego)
    with open('clasificacion.json', 'w', encoding='utf-8') as file:
        json.dump(clasificacion, file, indent=4, ensure_ascii=False)

def mostrar_clasificacion():
    try:
        with open('clasificacion.json', 'r', encoding='utf-8') as file:
            clasificacion = json.load(file)
    except FileNotFoundError:
        print("No hay datos de clasificación disponibles.")
        return

    clasificacion.sort(key=lambda x: x["correctas"] - x["incorrectas"], reverse=True)
    print("\n=== Tabla de Clasificación ===")
    for jugador in clasificacion:
        print(f"Nombre: {jugador['nombre']}, Correctas: {jugador['correctas']}, Incorrectas: {jugador['incorrectas']}, Comodines usados: {jugador['comodines_usados']}")
    print("=============================")
    
    input("Presiona Enter para volver al menú principal.")

def main():
    estados_dificultades = {
        "Facil": False,
        "Intermedia": False,
        "Dificil": False
    }

    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción (1, 2, 3, 4,): ")

        if opcion == "1":
            jugar(estados_dificultades)
        elif opcion == "2":
            mostrar_creditos()
        elif opcion == "3":
            mostrar_clasificacion()
        elif opcion == "4":
            print("¡Gracias por jugar! Adiós.")
            break
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")

if __name__ == "__main__":
    main()