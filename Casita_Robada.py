import random

def rellenarMazo(palos, numeros, mazo):
    for i in range(len(numeros)):
        for j in range(len(palos)):
            carta = numeros[i] + " " + palos[j]
            mazo.append(carta)
    random.shuffle(mazo)
    return mazo

def repartirCartas(barajasJugadores, mazo, carta):
    for i in range(2):
        barajasJugadores.append([])
        for j in range(3):
            carta = mazo[0]
            barajasJugadores[i].append(carta)
            mazo.pop(0)  
    return barajasJugadores, mazo

def rellenarMesa(barajaMesa, mazo, carta):
    cant = 6
    while cant > 0:
        carta = mazo[0]
        barajaMesa.append(carta)
        mazo.pop(0)
        cant = cant - 1 
    return barajaMesa, mazo

def turnoJugador(barajasJugadores, barajaMesa, carta, casitaJugador, casitaMaquina, arch):
    while True:
        try:
            carta = input("Elija una carta de su baraja: ")
            numeroCarta = carta.split()[0]
            assert carta in barajasJugadores[0], "La carta seleccionada no se encuentra en su baraja"
            break
        except AssertionError as mensaje:
            print(mensaje)
            
    while True:
        try:
            accion = int(input("Seleccione: 1 para robar casita - 2 para levantar de la mesa - 3 para tirar: "))
            assert 1 <= accion <= 3, "Seleccion invalida."
            break
        except ValueError:
            print("Seleccion invalida.")
        except AssertionError as mensaje:
            print(mensaje)
    
    #1 Robar casita
    if accion == 1:
        ultimaAcccionJugador = True
        if len(casitaMaquina) != 0:
            if numeroCarta != casitaMaquina[-1].split()[0]:
                print("No se puede robar el mazo rival")
                turnoJugador(barajasJugadores, barajaMesa, carta, casitaJugador, casitaMaquina, arch)
            else:
                arch.write("El jugador roba casita con carta: "+ carta +"\n")
                casitaJugador.extend(casitaMaquina)
                casitaJugador.append(carta)
                casitaMaquina.clear()
                barajasJugadores[0].remove(carta)
        else:
            print("No se puede robar el mazo rival")
            turnoJugador(barajasJugadores, barajaMesa, carta, casitaJugador, casitaMaquina, arch)

    #2 Levantar de la mesa
    if accion == 2:
        ultimaAcccionJugador = True
        cartaMesa = input("Elija una carta de la mesa para levantar: ")
        numeroCartaMesa = cartaMesa.split()[0]
        if cartaMesa in barajaMesa:
            if numeroCartaMesa == numeroCarta:
                arch.write("El jugador levanta de la mesa la carta "+ cartaMesa +" con carta "+ carta +"\n")
                casitaJugador.append(carta)
                casitaJugador.append(cartaMesa)
                barajasJugadores[0].remove(carta)
                barajaMesa.remove(cartaMesa)
            else:
                print("No puede levantar esa carta.")
                turnoJugador(barajasJugadores, barajaMesa, carta, casitaJugador, casitaMaquina, arch)
        else:
            print("La carta seleccionada no se encuentra en la mesa")
            turnoJugador(barajasJugadores, barajaMesa, carta, casitaJugador, casitaMaquina, arch)
    
    #3 Tirar
    if accion == 3:
        arch.write("El jugador tira carta: "+ carta +"\n")
        barajaMesa.append(carta)
        barajasJugadores[0].remove(carta)
    

def turnoMaquina(barajasJugadores, barajaMesa, carta, casitaJugador, casitaMaquina, arch):
    a = False
    vecNumeroMaquina = []
    vecNumeroMesaMaquina = []
    for i in range(len(barajasJugadores[1])):
        numeroCarta = barajasJugadores[1][i].split()[0]
        vecNumeroMaquina.append(numeroCarta)
    for i in range(len(barajaMesa)):
        numeroCarta = barajaMesa[i].split()[0]
        vecNumeroMesaMaquina.append(numeroCarta)    

    #1 Intenta robar casita
    if len(casitaJugador) != 0:
        for i in range(len(vecNumeroMaquina)):
            if vecNumeroMaquina[i] == casitaJugador[-1].split()[0]:
                ultimaAcccionJugador = False
                print("---------------------------------")
                print("IA - Roba casita usando: ", barajasJugadores[1][i])
                print("---------------------------------")
                arch.write("IA roba casita con carta: "+ barajasJugadores[1][i] +"\n")
                casitaMaquina.extend(casitaJugador)
                casitaMaquina.append(barajasJugadores[1][i])
                barajasJugadores[1].remove(barajasJugadores[1][i])
                vecNumeroMaquina.remove(vecNumeroMaquina[i])
                casitaJugador.clear()
                return
    
    #2 Intenta levantar de la mesa
    for i in range(len(vecNumeroMaquina)):
        for j in range(len(vecNumeroMesaMaquina)):  
            if vecNumeroMaquina[i] == vecNumeroMesaMaquina[j] and a == False:
                ultimaAcccionJugador = False
                print("---------------------------------")
                print("IA - Levanta de la mesa: ", barajaMesa[j] , ", usando: ", barajasJugadores[1][i])
                print("---------------------------------")
                arch.write("IA levanta de la mesa la carta "+ barajaMesa[j] +" con carta "+ barajasJugadores[1][i] +"\n")
                casitaMaquina.append(barajaMesa[j])
                casitaMaquina.append(barajasJugadores[1][i])
                barajasJugadores[1].remove(barajasJugadores[1][i])
                vecNumeroMaquina.remove(vecNumeroMaquina[i])
                barajaMesa.remove(barajaMesa[j])
                vecNumeroMesaMaquina.remove(vecNumeroMesaMaquina[j])
                return

    #3 Ultima opción: tirar
    print("---------------------------------")
    print("IA - Tira: ", barajasJugadores[1][-1])
    print("---------------------------------")
    arch.write("IA tira carta: "+ barajasJugadores[1][-1] +"\n")
    barajaMesa.append(barajasJugadores[1][-1])
    barajasJugadores[1].remove(barajasJugadores[1][-1])
    vecNumeroMaquina.remove(vecNumeroMaquina[-1])


#Imprimir 
def impresion(barajasJugadores, casitaJugador, barajaMesa, casitaMaquina, mostrarBarajaRival):
    print("=================================")
    matriz = [[0] * 16 for i in range (8)]
    for f in range(len(matriz)):
        for c in range(len(matriz[0])):
            if f == 0:
                if c == 0:
                    matriz[f][c] = "Cartas PC:"
                elif len(barajasJugadores[1])>=c:
                    if mostrarBarajaRival == 1:
                        matriz[f][c] = "[" + barajasJugadores[1][c-1] + "]"
                    else:
                        matriz[f][c] = "[ X ]"
                else:
                    matriz[f][c] = " "
            elif f == 1:
                if c == 0:
                    matriz[f][c] = "Casita PC:"
                elif c == 1:
                    ultimamaquina = len(casitaMaquina) - 1
                    if ultimamaquina!=-1:
                        matriz[f][c] = "[" + casitaMaquina[ultimamaquina] + "]"
                    else:
                        matriz[f][c] = " "
                else:
                    matriz[f][c] = " "
            elif f == 2 or f == 4 or f==7:
                matriz[f][c] = " "
            elif f == 3:
                if c == 0:
                    matriz[f][c] = "Cartas en Mesa"
                elif len(barajaMesa)>=c:
                    matriz[f][c] = "[" + barajaMesa[c-1] + "]"
                else:
                    matriz[f][c] = " "
            elif f == 5:
                if c == 0:
                    matriz[f][c] = "Cartas Jugador:"
                elif len(barajasJugadores[0])>=c:
                    matriz[f][c] = "[" + barajasJugadores[0][c-1] + "]"
                else:
                    matriz[f][c] = " "
            else:
                if c == 0:
                    matriz[f][c] = "Casita Jugador:"
                elif c == 1:
                    ultimajugador = len(casitaJugador)-1
                    if ultimajugador !=-1:
                        matriz[f][c] = "[" + casitaJugador[ultimajugador] + "]"
                    else:
                        matriz[f][c] = " "
                else:
                    matriz[f][c] = " "
    filas = len(matriz)
    columnas = len(matriz [0])
    for f in range (filas):
        for c in range (columnas):
            print(matriz[f][c],end ="   ")
        print()

    print("=================================")


#Programa Principal
palos = ["Basto", "Espada", "Oro", "Copa"]
numeros = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
carta = 0
cartas = 48
mazo = []
cantManos = 7
cantTurnosPorMano = 3
barajasJugadores = []
barajaMesa = []
casitaMaquina = []
casitaJugador = []
ultimaAcccionJugador = True
asignacionTurnos = True

try:
    arch = open("registro.txt", "at")
    arch.write("Nueva partida." + "\n")

    #Juego
    mazo = rellenarMazo(palos, numeros, mazo)
    barajaMesa, mazo = rellenarMesa(barajaMesa, mazo, carta)
    mostrarBarajaRival = int(input("Selecione: 1 para mostrar el mazo del rival - 2 para no mostrarlo: "))

    while cantManos > 0:
        barajasJugadores, mazo = repartirCartas(barajasJugadores, mazo, carta)
        
        if cantManos == 7 or cantManos == 5 or cantManos == 3 or cantManos == 1:
            asignacionTurnos = True
        else:
            asignacionTurnos = False
        print("Nueva mano. Se reparten las cartas")
        arch.write("---------------" + "\n")
        arch.write("Nueva mano." + "\n")

        while cantTurnosPorMano > 0:
            if asignacionTurnos == True:
                impresion(barajasJugadores, casitaJugador, barajaMesa, casitaMaquina, mostrarBarajaRival)
                turnoJugador(barajasJugadores, barajaMesa, carta, casitaJugador, casitaMaquina, arch)
                turnoMaquina(barajasJugadores, barajaMesa, carta, casitaJugador, casitaMaquina, arch)
            else:
                turnoMaquina(barajasJugadores, barajaMesa, carta, casitaJugador, casitaMaquina, arch)
                impresion(barajasJugadores, casitaJugador, barajaMesa, casitaMaquina, mostrarBarajaRival)
                turnoJugador(barajasJugadores, barajaMesa, carta, casitaJugador, casitaMaquina, arch)

            cantTurnosPorMano = cantTurnosPorMano - 1
        cantManos = cantManos - 1
        cantTurnosPorMano = 3

    if ultimaAcccionJugador == True:
        barajasJugadores[0].extend(barajaMesa)
        barajaMesa.clear()
    else:
        barajasJugadores[1].extend(barajaMesa)
        barajaMesa.clear()

    if len(casitaMaquina) > len(casitaJugador):
        arch.write("---------------" + "\n")
        arch.write("La IA ganó el juego con: " + str(len(casitaMaquina)) + " cartas en su casita" + "\n")
        print("La IA ganó el juego con :", len(casitaMaquina), "cartas en su casita")
    if len(casitaMaquina) < len(casitaJugador):
        arch.write("---------------" + "\n")
        arch.write("El jugador ganó el juego con: " + str(len(casitaJugador)) + " cartas en su casita" + "\n")
        print("¡Ganaste el juego con :", len(casitaJugador), "cartas en tu casita!")
    if len(casitaMaquina) == len(casitaJugador):
        arch.write("---------------" + "\n")
        arch.write("Empate" + "\n")
        print("Empataste con la IA")
    arch.write("=====================" + "\n")

except OSError:
    print("No se puede grabar el archivo.")
finally:
    try:
        arch.close()
    except NameError:
        pass