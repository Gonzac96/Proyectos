import pyautogui
import time
import keyboard
import random

detener_combinacion = "ctrl+shift+l"  # Definir la combinación de teclas para detener el programa

c = 0

try:
    while True:

        x = random.randint(947, 1218)
        y = random.randint(988, 1018)
        # Definir la posición donde se realizará el clic
        posicion_clic = (x, y)  # Ejemplo de posición, podes ajustar según la necesidad

        t = random.randint(480, 600)
        # Definir el intervalo de tiempo entre clics en segundos
        intervalo_clics = t  # En este caso, entre 480 y 600 segundos(8 a 10 min)

        # Realizar el clic en la posición especificada
        pyautogui.click(posicion_clic)
        print("Clic realizado en", posicion_clic)

        c += 1
        print("Cantidad de listas mandadas: ", c) 
        print("Tiempo de espera hasta la siguiente lista: ", t)
        
        # Esperar el intervalo de tiempo antes de realizar el próximo clic
        time.sleep(intervalo_clics)
        
        # Verificar si se ha presionado la combinación de teclas para detener el programa
        if keyboard.is_pressed(detener_combinacion):
            print("\nPrograma detenido por el usuario.")
            break  # Salir del bucle while si se presiona la combinación de teclas
except KeyboardInterrupt:
    print("\nPrograma detenido por el usuario.")
