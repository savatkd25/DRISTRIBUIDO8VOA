import threading
import time
import random

class BankQueue:
    def __init__(self):
        self.queue = [] 
        self.mutex = threading.Lock() 
        self.semaphore = threading.Semaphore(1) 

    def add_person(self, person):
        self.mutex.acquire() 
        self.queue.append(person) 
        print(f"{person.name} se ha unido a la cola.") 
        self.mutex.release() 

    def serve_person(self):
        self.semaphore.acquire()
        self.mutex.acquire() 

        for person in self.queue:
            if person.is_elderly(): 
                self.queue.remove(person)
                self.mutex.release()
                print(f"Se está atendiendo a {person.name}...")
                wait_time = random.randint(2, 4)
                print(f"{person.name} está siendo atendido. ({wait_time} segundos)")
                time.sleep(wait_time)
                person.serve()
                self.semaphore.release() 
                return 

            elif not person.has_been_served():
                self.queue.remove(person)
                self.mutex.release() 
                print(f"Se está atendiendo a {person.name}...")
                wait_time = random.randint(1, 3)
                print(f"{person.name}  está siendo atendido. ({wait_time} segundos)") 
                time.sleep(wait_time)
                person.serve()
                self.semaphore.release()
                return 

        self.mutex.release() 
        self.semaphore.release()

class Person(threading.Thread):
    def __init__(self, name, is_elderly):
        super().__init__() # Inicializamos la clase padre threading.Thread
        self.name = name # Establecemos el nombre de la persona
        self.is_elderly_flag = is_elderly # Indicamos si la persona es de tercera edad o no
        self.served = False # Establecemos que la persona no ha sido atendida todavía

    def is_elderly(self):
        return self.is_elderly_flag # Devolvemos True si la persona es de tercera edad, False en caso contrario

    def serve(self):
        self.served = True

    def has_been_served(self):
        return self.served # Devolvemos True si la persona ha sido atendida, False en caso contrario

    def run(self):
        bank_queue.add_person(self) # Agregamos a la persona a la cola del banco
        while not self.has_been_served(): # Mientras la persona no haya sido atendida todavía
            bank_queue.serve_person() # Intentamos atender a la persona en el banco

def main():
    global bank_queue # Indica que se usará la variable bank_queue definida fuera del ámbito de este archivo
    bank_queue = BankQueue() # Crea una instancia de BankQueue

    person1 = Person("Maria", False) # Crea una instancia 
    person2 = Person("Pedro", True)
    person3 = Person("Dennis", False)
    person4 = Person("Gabriela", False)

    person1.start() 
    person2.start() 
    person3.start() 
    person4.start() 

    person1.join() 
    person2.join() 
    person3.join() 
    person4.join() 

    print("Todos han sido atendidos de manera satisfactorio.") # Imprime un mensaje indicando que todas las personas han sido atendidas


if __name__ == "__main__":
    main()
