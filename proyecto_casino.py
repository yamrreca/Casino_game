from random import randint, choice
from time import sleep
from math import floor
import csv

class Usuario:
	def __init__(self,snom,scont,iedad,ifichas):
		self.nom = snom
		self.cont = scont
		self.edad = iedad
		self.fichas = ifichas


def menujuegos(): #Interfaz del menú de juegos
	print("Elija la opción deseada:")
	print("a) Jugar ruleta")
	print("b) Jugar pachinko")
	print("c) Consultar fichas")
	print("d) Comprar fichas")
	print("e) Cerrar sesión")


def menuprinc(): #El menú principal
		print("\ncasinoYAP v.1.0")
		print("Seleccione iniciar sesión si ya posee una cuenta, o registrarse si es un nuevo usuario")
		print()
		print("a) Iniciar sesión")
		print("b) Registrarse")
		print("c) Salir")
		print()

def pachinko():
	global usuarioactual
	print('Reglas: Se tendrá el siguiente tablero:')
	print("        .")
	print("      .    .")
	print("    .    .    .")
	print("  .    .    .    .")
	print("|2|1|1|||0|0|1|1|||2|\n")
	print('Se tirará una "pelota" que empezará en la parte de arriba y caerá a uno de los hoyos. Si cae en 0 se pierde. Si cae en 1 ni se gana ni se pierde. Si cae en 2 se gana 2 veces lo apostado.')

	while True:

		lusuarios = []

		if usuarioactual.fichas == 0:
			print('\nYa no tiene fichas. Regrese después de haber comprado más.\n')
			break

		print()

		while True:
			try:
				iapuesta = int(input("Introduzca la cantidad a apostar:" + '\n'))
			except ValueError:
				print('Introduzca un número entero.')
			else:
				break

		while True:
			if iapuesta > usuarioactual.fichas:
				print("\nNo tiene suficientes fichas.\n")
				try:
					iapuesta = int(input("Introduzca la cantidad a apostar:" + '\n'))
				except ValueError:
					print('Introduzca un número entero.')
			else:
				break

		###Listas que definen cómo se ve el tablero. lyeqn es la n-ésima fila

		lyeq4 = list("        .")
		lyeq3 = list("      .    .")
		lyeq2 = list("    .    .    .")
		lyeq1 = list("  .    .    .    .")
		lyeq0 = list("|2|1|1|||0|0|1|1|||2|")

		"""
		La siguiente lista de diccionarios contiene las coordenadas de cada
		punto del tablero. La posición i-ésima de la lista es un diccionario
		que contiene la coordenada x que le corresponde al elemento j-ésimo
		de la lista lyeqi, la cual es la fila i-ésima. Ejemplo: 
		lyeq2[7] es un punto en la segunda fila de abajo hacia arriba al que le
		corresponde la coordenada x=0. Entonces listacoord[2]={7:0}.

		El algoritmo que saca el diccionario se basa en que hay una distancia de
		5 unidades entre puntos en la misma fila, y de 2 unidades horizontales 
		entre los puntos más a la izquierda de filas adyacentes. El origen x=0 
		está en el punto de en medio (el de la fila más arriba).
		"""

		diccoord = {}                #El diccionario de las coordenadas x
		listacoord = []              #La lista de los diccionarios anteriores
		listay = [lyeq1,lyeq2,lyeq3,lyeq4] #Lista de renglones

		for i in range(len(listay)): #La coordenada y es y=i+1 porque empieza en 0
			k = -2                   #Contador para la fórmula índice <-> coord. x
			listacoord.append(diccoord)
			diccoord = {}
			for j in range(len(listay[i])): #j es el índice del punto
				if listay[i][j] == ".":
					k += 2
					diccoord[i - 3 + k] = j #Fórmula índice <-> coord. x

		listacoord.append(diccoord)

		###Se invierten los índices de las listas para facilitar los ciclos

		for i in range(floor(len(listacoord)/2)):
			listacoord[i], listacoord[len(listacoord)-1-i] = listacoord[len(listacoord)-1-i], listacoord[i]

		for i in range(floor(len(listay)/2)):
			listay[i], listay[len(listay)-1-i] = listay[len(listay)-1-i], listay[i]

		###Ciclo que calcula a dónde va la bola
		icoordx = 0                          #Donde empieza la bola

		listay[0][listacoord[0][icoordx]] = 'x' #Tablero inicial
		for j in range(len(listay)):
			print("".join(listay[j]))
		print("".join(lyeq0))
		listay[0][listacoord[0][icoordx]] = '.'

		for i in range(1,len(listacoord)-1): #i define al renglón. El último elemento es un dicc vacío.
			sleep(0.5)
			icambiocoord = choice([-1,1])    #Determina a dónde se va la bola
			icoordx += icambiocoord
			listay[i][listacoord[i][icoordx]] = 'x' #Cambia el punto donde cae la bola por una 'x'
			for j in range(len(listay)):     #Impresión del tablero
				print("".join(listay[j]))    #Transforma a cadena
			print("".join(lyeq0))
			listay[i][listacoord[i][icoordx]] = '.'

		###Se decidirá ahora cuál es el premio

		#listapremio = [[3,2,1],[1,1,0]] #Primer índice = coordenada x, segundo = premio si sale +1, tercero = premio si -1

		lcoordpremios = []                   #Lista de listas con información de los hoyos de hasta abajo
		lnum = [str(i) for i in range(3)]
		k = -5

		for i in range(len(lyeq0)):     #i es índice de lyeq0
			for j in range(len(lnum)):               #j es el entero
				if lyeq0[i] == lnum[j]:
					k +=1
					lcoordpremios.append([j,i,(2*k + 1)/2]) #Primera entrada: valor del premio. segunda: índice del entero que se cambia por 'x', tercera: coord. asociada al hoyo donde cae la bola

		icambiocoord = choice([-1/2,1/2])
		icoordx += icambiocoord

		for i in range(len(lcoordpremios)):
			if lcoordpremios[i][2] == icoordx:
				lyeq0[lcoordpremios[i][1]] = 'x'
				ipremio = lcoordpremios[i][0]

		sleep(0.5)

		for j in range(len(listay)):     #Impresión del tablero
			print("".join(listay[j]))    #Transforma a cadena
		print("".join(lyeq0))

		sleep(0.5)
		print()

		if ipremio == 0:
			print('Ha perdido.\n')
			usuarioactual.fichas -= iapuesta
		elif ipremio == 1:
			print('Ni ganó ni perdió.\n')
		else:
			print("¡Enhorabuena! Ha ganado %d veces su apuesta\n"%(ipremio))
			usuarioactual.fichas += ipremio*iapuesta

		with open('usuarios.txt', 'r') as archivu:
			ausuarios = csv.DictReader(archivu)			
			for user in ausuarios:
				if user['nombre'] == usuarioactual.nom:
					user['fichas'] = usuarioactual.fichas
				lusuarios.append(user)

		with open('usuarios.txt', 'w') as archivu:
			categorias = ['nombre','contrasena','edad','fichas']
			ausuarios = csv.DictWriter(archivu,fieldnames = categorias)
			ausuarios.writeheader()
			for user in lusuarios:
				ausuarios.writerow(user)
			

		print('Ahora tiene', usuarioactual.fichas, 'fichas.' + '\n')


		scontinuar = input("¿Jugar de nuevo? (s,n)" + '\n').lower()
		while scontinuar not in ['s','n']:
			print("Escriba s para sí o n para no")
			scontinuar = input("¿Jugar de nuevo? (s,n) ").lower()
		if scontinuar == "n":
			print()
			break


def ruleta():
	global usuarioactual
	print("Reglas: La ruleta caerá en un número entre el 0 y el 36. Se puede apostar sencillo o docena:")
	print("Sencillo: se apuesta por un número cualquiera entre 0 y 36. Si acierta, la ganancia será de 35 veces la apuesta.")
	print("Docena: se apuesta por un número cualquiera entre 0 y 36, y gana si el número de la ruleta está a una distancia de 1 del que escogió. Si acierta, la ganancia será de 17 veces la apuesta.")

	while True:

		lusuarios = []

		if usuarioactual.fichas == 0:
			print('\nYa no tiene fichas. Regrese después de haber comprado más.\n')
			break

		ipago = int
		suffichas = False
		print()
		smodoapu = input("¿Quiere apostar sencillo o docena?" + "\n").lower()

		while smodoapu not in ['sencillo','docena']:
			print()
			print("Escriba una opción existente.")
			smodoapu = input("¿Quiere apostar sencillo o docena? " + "\n").lower()

		print()

		while True:
			try:
				iapuesta = int(input("Introduzca la cantidad a apostar:" + '\n'))
			except ValueError:
				print('Introduzca un número entero.')
			else:
				break

		while True:
			if iapuesta > usuarioactual.fichas:
				print("No tiene suficientes fichas.")
				try:
					iapuesta = int(input("Introduzca la cantidad a apostar:" + '\n'))
				except ValueError:
					print('Introduzca un número entero.')
			else:
				break

		print()

		while True:
			try:
				inumelecc = int(input("Elija un número del 0 al 36:" + '\n'))
			except ValueError:
				print('Introduzca un número entero.')
			else:
				break

		while True:
			if inumelecc < 0 or inumelecc > 36:
				try:
					print('Número fuera del intervalo aceptado.')
					inumelecc = int(input("Elija un número del 0 al 36:" + '\n'))
				except ValueError:
					print('Introduzca un número entero.')
			else:
				break

		print()
		print("Ha elegido", inumelecc)
		print("Girando la ruleta...")
		sleep(2) #¿Qué es un juego de apuestas sin algo de tensión?
		iganador = randint(0,36)
		print("La ruleta se detuvo en", iganador)
		print()

		if smodoapu == "sencillo":
			if inumelecc == iganador:
				ipago = iapuesta*35
				usuarioactual.fichas += ipago
				print("¡Enhorabuena! Ha ganado", ipago, "fichas." + '\n')
			else:
				print("No ha acertado." + '\n')
				usuarioactual.fichas -= iapuesta
		elif smodoapu == "docena":
			if inumelecc in [iganador, iganador + 1, iganador - 1]:
				ipago = iapuesta*17
				usuarioactual.fichas += ipago
				print("¡Enhorabuena! Ha ganado", ipago, "fichas." + '\n')
			else:
				print("No ha acertado." + '\n')
				usuarioactual.fichas -= iapuesta

		with open('usuarios.txt', 'r') as archivu:
			ausuarios = csv.DictReader(archivu)			
			for user in ausuarios:
				if user['nombre'] == usuarioactual.nom:
					user['fichas'] = usuarioactual.fichas
				lusuarios.append(user)

		with open('usuarios.txt', 'w') as archivu:
			categorias = ['nombre','contrasena','edad','fichas']
			ausuarios = csv.DictWriter(archivu,fieldnames = categorias)
			ausuarios.writeheader()
			for user in lusuarios:
				ausuarios.writerow(user)

		print('Ahora tiene', usuarioactual.fichas, 'fichas.' + '\n')

		scontinuar = input("¿Jugar de nuevo? (s,n)").lower()
		while scontinuar not in ['s','n']:
			print("Escriba s para sí o n para no")
			scontinuar = input("¿Jugar de nuevo? (s,n) ").lower()
		if scontinuar == "n":
			print()
			break



lusuarios = []

while True:

	lusuarios = []  #Aquí se almacenan los usuarios

	menuprinc()

	while True:
		sopcion = input()
		if sopcion not in ['a','b','c']:
			print('Ingrese una opción correcta\n')
		else:
			break

	if sopcion == "c":
		print("\nEsperamos tenerlo de regreso.")
		exit()

	elif sopcion == "b":
		while True:
			try:
				iedad = int(input("Teclee su edad: "))
			except ValueError:
				print("Ingrese un número entero.")
			else:
				break
		if iedad < 18:
			print("Se debe ser mayor de edad para entrar al casino. Adiós.")
			exit()

		try:
			with open('usuarios.txt', 'r') as archivu:
				ausuarios = csv.DictReader(archivu)			
				for linea in ausuarios:
					lusuarios.append(linea)
		except FileNotFoundError:
			archivu = open('usuarios.txt','w+')
			archivu.close()

		bandera = True

		while bandera:
			snombre = input("Teclee un nombre de usuario: ")
			if lusuarios == []: #Siempre estará disponible el nombre si no hay ningún otro usuario
				break
			for user in lusuarios: #Checa que el nombre esté disponible
				if user['nombre'] == snombre:
					print("Nombre no disponible. Por favor elija otro.")
					break						
				else:
					bandera = False
					

		scont = input("Teclee su contraseña: ")

		with open('usuarios.txt', 'w') as archivu:
			categorias = ['nombre','contrasena','edad','fichas']
			ausuarios = csv.DictWriter(archivu,fieldnames = categorias)
			ausuarios.writeheader()

			for user in lusuarios:
				ausuarios.writerow(user)
			ausuarios.writerow({'nombre':snombre,'contrasena':scont,'edad':iedad,'fichas':100})

		lusuarios = []
		print("Su cuenta se creo exitosamente. Se le obsequian 100 fichas.")

	elif sopcion == "a":
		while sopcion == 'a':
			with open('usuarios.txt', 'r') as archivu:
				ausuarios = csv.DictReader(archivu)			
				for linea in ausuarios:
					lusuarios.append(linea)

			usuarioactual = Usuario(str,str,int,int)
			snombre = input("Teclee su nombre de usuario: ")
			scont = input("Teclee su contraseña: ")

			for user in lusuarios:  #Checa si los datos ingresados están en la lista
				if user['nombre'] == snombre and user['contrasena'] == scont:
					usuarioactual.nom = user['nombre']
					usuarioactual.cont = user['contrasena']
					usuarioactual.edad = int(user['edad'])
					usuarioactual.fichas = int(user['fichas'])
					print()
					print("Bienvenido",usuarioactual.nom + '\n')
					lusuarios = []
					sopcion = str
					break

			if usuarioactual.nom == str:
				print("\n Usuario o contraseña incorrecta.\n")
		
		while True:

###El menú de juegos:

			menujuegos()

			while True:
				sopcion = input()
				if sopcion not in ['a','b','c','d','e']:
					print('Ingrese una opción correcta\n')
				else:
					break

			if sopcion == 'e':
				print('\nVuelva pronto',usuarioactual.nom + '\n')
				break

			if sopcion == 'd':

				lusuarios = []

				try:
					ifichasnuevas = int(input('\nIngrese el número de fichas que desea:' + '\n'))
				except ValueError:
					print('Ingrese un número entero.')
				else:
					usuarioactual.fichas += ifichasnuevas
					with open('usuarios.txt', 'r') as archivu:
						ausuarios = csv.DictReader(archivu)			
						for user in ausuarios:
							if user['nombre'] == usuarioactual.nom:
								user['fichas'] = usuarioactual.fichas
							lusuarios.append(user)
					with open('usuarios.txt', 'w') as archivu:
						categorias = ['nombre','contrasena','edad','fichas']
						ausuarios = csv.DictWriter(archivu,fieldnames = categorias)
						ausuarios.writeheader()
						for user in lusuarios:
							ausuarios.writerow(user)
					print('\n' + 'Transacción completada. Tiene ahora', usuarioactual.fichas, 'fichas.' + '\n')

			if sopcion == 'c':
				print('\nUsted tiene',usuarioactual.fichas,'fichas.' + '\n')

###Pachinko:

			if sopcion == 'b':
				pachinko()

			if sopcion == 'a':
				ruleta()

















		



		



	







