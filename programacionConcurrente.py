import threading
import time

# Función que simula un proceso intensivo en CPU
def procesoIn(nombre):
    operacion=nombre
    for i in range(5):
        if nombre==1:
            operacion=operacion+2
        elif nombre==2:
            operacion=operacion*2
        print(f'Proceso Hilo {nombre} - Iteración {i} - Valor del calculo {operacion}')
        time.sleep(1)

# Crear dos hilos
hilo1 = threading.Thread(target=procesoIn, args=(1,))
hilo2 = threading.Thread(target=procesoIn, args=(2,))

# Iniciar los hilos
hilo1.start()
hilo2.start()

# Esperar a que ambos hilos terminen
hilo1.join()
hilo2.join()

print('Ambos hilos han terminado.')