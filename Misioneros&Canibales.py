import math
"""
    *
    *   AUTOR: Diego Fernandez Sebastian
    *
    *
    *   Script para el juego de los misioneros y canibales.
    *   Se tiene un rio y en una de las orillas hay 3 misioneros y 3 canibales.
    *   Hay que conseguir que crucen en el menor tiempo posible en una barca
    *   con hueco para dos pasajeros sin que los canibales se coman a los misioneros.
    *   Los canibales se comerán a los misioneros si en una orilla hay más canibales que misioneros.
    *
    *
    *   [M_izq, C_izq, M_dcha, C_dcha, M_t, C_t, orilla, coste_g, coste_h, f, referencia al padre]
    *   Implementación utilizando listas para agilizar el proceso.
    *
"""

# función para el algoritmo A* que implementa la solución


def algoritmo_a_estrella():

    # lista abierta
    lista_abierta = []
    # lista cerrada
    lista_cerrada = []

    # generar un estado inicial
    nodo_raiz = [0, 0, 3, 3, 0, 0, "derecha", 0, 0, 0, None]

    # añadirlo a la lista abierta.
    lista_abierta.append(nodo_raiz)

    anadir = False
    # numero nodos expandidos
    nodos_totales_expandidos = 0

    while len(lista_abierta) > 0:

        # sacar nodo de la lista abierta
        nodo_actual = lista_abierta.pop(0)

        # comprobar si el nodo actual es la solución.
        if comprobar_nodo_final(nodo_actual):
            # si se ha encontrado el estado final se termina devolviendo
            # la solución.
            lista_resultados = []
            # imprimir estadisticas nodos
            print('*' * 30)
            print("Nodos totales expandidos: ", nodos_totales_expandidos)
            print('*' * 30)
            print()
            while nodo_actual is not None:
                lista_resultados.append(nodo_actual)
                nodo_actual = nodo_actual[10]
            return lista_resultados[::-1]

        # comprobación repetidos.
        # comprobar si se encuentra en la lista cerrada
        # si se encuentra habrá que comprobar si tiene mejor función f
        # en el caso de que no tenga una mejor función se descartará.
        # Sino, habrá que actualizarlo.
        for nodo in lista_cerrada:
            if nodo_actual == nodo:
                if nodo_actual[9] < nodo[9]:
                    # el nodo actual tiene una mejor función f. Añadirlo
                    # eliminar nodo antiguo
                    lista_cerrada.remove(nodo)
                    # añadir el nuevo nodo, el valor será su f
                    lista_cerrada.append(nodo_actual)

                    # generar sucesores del nodo.
                    hijos = generar_sucesores(nodo_actual)
                    nodos_totales_expandidos += 1
                    # ESTO ES INEFICIENTE, HAY QUE IMPLEMENTARLO DE OTRA FORMA
                    # NO SE PUEDE HACER UN SORT DE TODA LA LISTA SIEMPRE.
                    # añadir los hijos
                    for hijo in hijos:
                        lista_abierta.append(hijo)

                    # ordenar la lista abierta, para obtener los mejores nodos.
                    lista_abierta.sort(key=ordenar_nodo)

                    anadir = True
                    # salir del bucle for
                    break
                else:
                    # si no es mejor no hacemos nada, por ende
                    # se descarta para que no se expanda.
                    break

        if anadir is False:
            # si no se encontrase en la lista cerrada se tendrá que
            # expandir todos sus sucesores y añadirlo a la lista cerrada
            lista_cerrada.append(nodo_actual)
            hijos = generar_sucesores(nodo_actual)
            nodos_totales_expandidos += 1
            # ESTO ES INEFICIENTE, HAY QUE IMPLEMENTARLO DE OTRA FORMA
            # NO SE PUEDE HACER UN SORT DE TODA LA LISTA SIEMPRE.
            # añadir los hijos
            for hijo in hijos:
                lista_abierta.append(hijo)

            # ordenar la lista abierta, para obtener los mejores nodos.
            lista_abierta.sort(key=ordenar_nodo)

    # si no se ha conseguido solución --> Error
    print("SOLUTION NOT FOUND")
    return None


def imprimir_camino(lista_resultados):
    for resultado in lista_resultados:
        print('*' * 30)
        print()
        print('=' * 30)
        print("Misioneros orilla izquierda: ", resultado[0])
        print("Canibales orilla izquierda: ", resultado[1])
        print('=' * 30)
        print("Orilla: ", resultado[6])
        print("misioneros navegando: ", resultado[4])
        print("canibales navegando: ", resultado[5])
        print('=' * 30)
        print("Misioneros orilla derecha: ", resultado[2])
        print("Canibales orilla orilla derecha: ", resultado[3])
        print('=' * 30)
        print()
        print("g: ", resultado[7])
        print("h: ", resultado[8])
        print("f: ", resultado[9])
        print('*' * 30)


def ordenar_nodo(nodo):
    """
    Función usada para ordenar de menor a mayor los nodos en la lista abierta para coger las mejores aproximaciones.

    """
    return nodo[9]


def calcular_heuristica(nodo):
    """
    La heuristica propuesta consiste en relajar el que los canibales se coman a los misioneros.
    Por cada persona que haya en la orilla contraria al menos tiene que embarcar, navegar y desembarcar.
    Esto supone que:
                3*(M_d + C_d)

    También hay que tener en cuenta a las personas que se encuentran ya embarcadas. Estas necesitan al menos
    desembarcar, por tanto:
                  (M_t + C_t)

    Esto habrá que combinarlo ya que en las últimas etapas no quedarán personas en la orilla contraria haciendo
    que la heuristica no se encuentre tan informada como si se añaden los costes mínimos por ser tripulantes.

    h(n) = 3*(M_d + C_d) + (M_t + C_t)

    """
    nodo[8] = 3*(nodo[2]+nodo[3]) + (nodo[4] + nodo[5])


def actualizar_funcion_f(nodo):
    """
    Funcion para actualizar el numero de pasos total con su heuristica

    """

    nodo[9] = nodo[7] + nodo[8]


def comprobar_operadores(nodo):
    """
    Comprueba los operadores factibles para generar sucesores.
    :param nodo:
    :return:
    """
    # embarcar M, embarcar Ms, embarcar C, embarcar Cs, desembarcar M, desembarcar Ms, desembarcar C, desembarcar Cs,
    # navegar
    # una lista de booleanos. Si es True se podrá realizar el operador deseado.
    operadores = [embarcar_misionero(nodo), embarcar_misioneros(nodo), embarcar_canibal(nodo), embarcar_canibales(nodo),
                  desembarcar_misionero(nodo), desembarcar_misioneros(nodo), desembarcar_canibal(nodo),
                  desembarcar_canibales(nodo), navegar(nodo)]

    # devolver la lista para poder generar los nodos
    return operadores


def generar_sucesores(nodo):
    """
    Devuelve una lista con todos los nodos sucesores hijos.
    :param nodo:
    :return:
    """

    # lista con los hijos del nodo
    hijos = []

    # comprobar operadores
    lista_operadores = comprobar_operadores(nodo)

    # recordatorio posiciones lista de operadores
    # embarcar M, embarcar Ms, embarcar C, embarcar Cs, desembarcar M, desembarcar Ms, desembarcar C, desembarcar Cs,
    # navegar

    if lista_operadores[0]:
        # generar nodo para embarcar misionero
        if nodo[6] == "derecha":
            # embarcar el misionero y restar en misionero derecha.
            hijo = [nodo[0], nodo[1], nodo[2]-1, nodo[3], nodo[4]+1, nodo[5], nodo[6], nodo[7]+1, nodo[8], nodo[9],
                    nodo]
            hijos.append(hijo)
        elif nodo[6] == "izquierda":
            # embarcar el misionero y restar en misionero izquierda.
            hijo = [nodo[0]-1, nodo[1], nodo[2], nodo[3], nodo[4]+1, nodo[5], nodo[6], nodo[7]+1, nodo[8], nodo[9],
                    nodo]
            hijos.append(hijo)

    if lista_operadores[1]:
        # generar nodo para embarcar misioneros.
        if nodo[6] == "derecha":
            # embarcar el misionero y restar en misionero derecha.
            # (M_izq, C_izq, M_dcha, C_dcha, M_t, C_t, orilla, coste_g, coste_h, f, referencia al padre)
            hijo = [nodo[0], nodo[1], nodo[2]-2, nodo[3], nodo[4]+2, nodo[5], nodo[6], nodo[7]+1, nodo[8], nodo[9],
                    nodo]
            hijos.append(hijo)
        elif nodo[6] == "izquierda":
            # embarcar el misionero y restar en misionero izquierda.
            hijo = [nodo[0]-2, nodo[1], nodo[2], nodo[3], nodo[4]+2, nodo[5], nodo[6], nodo[7]+1, nodo[8], nodo[9],
                    nodo]
            hijos.append(hijo)

    if lista_operadores[2]:
        # generar nodo para embarcar canibal
        if nodo[6] == "derecha":
            # embarcar el misionero y restar en misionero derecha.
            hijo = [nodo[0], nodo[1], nodo[2], nodo[3]-1, nodo[4], nodo[5]+1, nodo[6], nodo[7]+1, nodo[8], nodo[9],
                    nodo]
            hijos.append(hijo)
        elif nodo[6] == "izquierda":
            # embarcar el misionero y restar en misionero izquierda.
            hijo = [nodo[0], nodo[1]-1, nodo[2], nodo[3], nodo[4], nodo[5]+1, nodo[6], nodo[7]+1, nodo[8], nodo[9],
                    nodo]
            hijos.append(hijo)

    if lista_operadores[3]:
        # generar nodo para embarcar canibales
        if nodo[6] == "derecha":
            # embarcar el misionero y restar en misionero derecha.
            hijo = [nodo[0], nodo[1], nodo[2], nodo[3]-2, nodo[4], nodo[5]+2, nodo[6], nodo[7]+1, nodo[8], nodo[9],
                    nodo]
            hijos.append(hijo)
        elif nodo[6] == "izquierda":
            # embarcar el misionero y restar en misionero izquierda.
            hijo = [nodo[0], nodo[1]-2, nodo[2], nodo[3], nodo[4], nodo[5]+2, nodo[6], nodo[7]+1, nodo[8], nodo[9],
                    nodo]
            hijos.append(hijo)

    if lista_operadores[4]:
        # generar nodo para desembarcar misionero
        if nodo[6] == "derecha":
            # embarcar el misionero y restar en misionero derecha.
            hijo = [nodo[0], nodo[1], nodo[2]+1, nodo[3], nodo[4]-1, nodo[5], nodo[6], nodo[7]+1, nodo[8], nodo[9],
                    nodo]
            hijos.append(hijo)
        elif nodo[6] == "izquierda":
            # embarcar el misionero y restar en misionero izquierda.
            hijo = [nodo[0]+1, nodo[1], nodo[2], nodo[3], nodo[4]-1, nodo[5], nodo[6], nodo[7]+1, nodo[8], nodo[9],
                    nodo]
            hijos.append(hijo)

    if lista_operadores[5]:
        # generar nodo para desembarcar misioneros
        if nodo[6] == "derecha":
            # embarcar el misionero y restar en misionero derecha.
            hijo = [nodo[0], nodo[1], nodo[2]+2, nodo[3], nodo[4]-2, nodo[5], nodo[6], nodo[7]+1, nodo[8], nodo[9],
                    nodo]
            hijos.append(hijo)
        elif nodo[6] == "izquierda":
            # embarcar el misionero y restar en misionero izquierda.
            hijo = [nodo[0]+2, nodo[1], nodo[2], nodo[3], nodo[4]-2, nodo[5], nodo[6], nodo[7]+1, nodo[8], nodo[9],
                    nodo]
            hijos.append(hijo)

    if lista_operadores[6]:
        # generar nodo para desembarcar canibal
        if nodo[6] == "derecha":
            # embarcar el misionero y restar en misionero derecha.
            hijo = [nodo[0], nodo[1], nodo[2], nodo[3]+1, nodo[4], nodo[5]-1, nodo[6], nodo[7]+1, nodo[8], nodo[9],
                    nodo]
            hijos.append(hijo)
        elif nodo[6] == "izquierda":
            # embarcar el misionero y restar en misionero izquierda.
            hijo = [nodo[0], nodo[1]+1, nodo[2], nodo[3], nodo[4], nodo[5]-1, nodo[6], nodo[7]+1, nodo[8], nodo[9],
                    nodo]
            hijos.append(hijo)

    if lista_operadores[7]:
        # generar nodo para desembarcar canibales
        if nodo[6] == "derecha":
            # embarcar el misionero y restar en misionero derecha.
            hijo = [nodo[0], nodo[1], nodo[2], nodo[3]+2, nodo[4], nodo[5]-2, nodo[6], nodo[7]+1, nodo[8], nodo[9],
                    nodo]
            hijos.append(hijo)
        elif nodo[6] == "izquierda":
            # embarcar el misionero y restar en misionero izquierda.
            hijo = [nodo[0], nodo[1]+2, nodo[2], nodo[3], nodo[4], nodo[5]-2, nodo[6], nodo[7]+1, nodo[8], nodo[9],
                    nodo]
            hijos.append(hijo)

    if lista_operadores[8]:
        # generar nodo para navegar
        if nodo[6] == "derecha":
            # navegar hacia la izquierda
            hijo = [nodo[0], nodo[1], nodo[2], nodo[3], nodo[4], nodo[5], "izquierda", nodo[7]+1, nodo[8], nodo[9],
                    nodo]
            hijos.append(hijo)
        elif nodo[6] == "izquierda":
            # navegar hacia la derecha
            hijo = [nodo[0], nodo[1], nodo[2], nodo[3], nodo[4], nodo[5], "derecha", nodo[7]+1, nodo[8], nodo[9], nodo]
            hijos.append(hijo)

    # una vez han sido generados los nodos hijos
    # calcular su coste heuristico y actualizar su f
    for hijo in hijos:
        calcular_heuristica(hijo)
        actualizar_funcion_f(hijo)

    return hijos


def comprobar_nodo_final(nodo):
    """
    Si todos los misioneros y canibales han podido cruzar el rio sin problemas se habrá terminado el juego.
    :param nodo:
    :return:
    """
    return True if nodo[0] == 3 and nodo[1] == 3 else False


"""
========================================
        OPERADORES PARA EMBARCAR
========================================
"""


def embarcar_misionero(nodo):
    # ¿Hay espacio en la barca?
    if (nodo[4] + nodo[5]) < 2:
        # comprobar que orilla
        if nodo[6] == "derecha":
            # ¿hay misioneros en la orilla?
            if nodo[2] > 0:
                # para poder embarcar a un misionero es necesario que haya
                # más misioneros que canibales.
                if nodo[2]-1 == nodo[3]:
                    return True
            # Se quedarán más canibales que misioneros o no hay misioneros en la orilla. No se puede.
            return False
        elif nodo[6] == "izquierda":
            # ¿hay misioneros en la orilla?
            if nodo[0] > 0:
                # para poder embarcar a un misionero es necesario que haya
                # más misioneros que canibales.
                if nodo[0] - 1 == nodo[1]:
                    return True
            # Se quedarán más canibales que misioneros o no hay misioneros en la orilla. No se puede.
            return False
    else:
        return False


def embarcar_misioneros(nodo):
    # hay espacio en la barca para dos misioneros?
    if nodo[4] + nodo[5] == 0:
        # comprobar que orilla
        if nodo[6] == "derecha":
            # ¿hay suficientes misioneros en la orilla?
            if nodo[2] > 0:
                # para poder embarcar a dos misioneros es necesario que haya
                # más misioneros que canibales.
                if nodo[2] - 2 == nodo[3]:
                    return True
            # Se quedarán más canibales que misioneros o no hay misioneros en la orilla. No se puede.
            return False
        elif nodo[6] == "izquierda":
            # ¿hay misioneros en la orilla?
            if nodo[0] > 0:
                # para poder embarcar a un misionero es necesario que haya
                # más misioneros que canibales.
                if nodo[0] - 2 == nodo[1]:
                    return True
            # Se quedarán más canibales que misioneros o no hay misioneros en la orilla. No se puede.
            return False
    else:
        return False


def embarcar_canibal(nodo):
    # ¿Hay espacio en la barca?
    if nodo[4] + nodo[5] < 2:
        # comprobar que orilla
        if nodo[6] == "derecha":
            # ¿hay canibales en la orilla?
            if nodo[3] > 0:
                # Si hay alguno se puede embarcar.
                return True
            # No hay canibales en la orilla. No se puede.
            return False
        elif nodo[6] == "izquierda":
            # ¿hay canibales en la orilla?
            if nodo[1] > 0:
                # Si hay alguno se puede embarcar.
                return True
            # No hay canibales en la orilla. No se puede.
            return False
    else:
        return False


def embarcar_canibales(nodo):
    # hay espacio en la barca para dos canibales?
    if nodo[4] + nodo[5] == 0:
        # comprobar que orilla
        if nodo[6] == "derecha":
            # ¿hay suficientes canibales en la orilla?
            if nodo[3] >= 2:
                # para poder embarcar a dos canibales es necesario que haya al menos 2
                return True
            # No hay suficientes canibales
            return False
        elif nodo[6] == "izquierda":
            # ¿hay suficientes canibales en la orilla?
            if nodo[1] >= 2:
                # para poder embarcar a dos canibales es necesario que haya al menos 2
                return True
            # No hay suficientes canibales
            return False
    else:
        return False


"""
========================================
      OPERADORES PARA DESEMBARCAR
========================================
    
"""


def desembarcar_misionero(nodo):
    # comprobar que haya algun misionero en la barca
    if nodo[4] > 0:
        # dependiendo de la orilla
        if nodo[6] == "derecha":
            # Comprobar que es seguro para el misionero desembarcar
            if nodo[3] <= nodo[2]+1:
                # habria mas misioneros
                return True
            return False
        elif nodo[6] == "izquierda":
            # Comprobar que es seguro para el misionero desembarcar
            if nodo[1] <= nodo[0]+1:
                # habria mas misioneros
                return True
            return False
    else:
        return False


def desembarcar_misioneros(nodo):
    # comprobar que haya dos misionero en la barca
    if nodo[4] == 2:
        # dependiendo de la orilla
        if nodo[6] == "derecha":
            # Comprobar que es seguro para los misioneros desembarcar
            if nodo[3] <= nodo[2]+2:
                # habria mas misioneros
                return True
            return False
        elif nodo[6] == "izquierda":
            # Comprobar que es seguro para los misioneros desembarcar
            if nodo[1] <= nodo[0]+2:
                # habria mas misioneros
                return True
            return False
    else:
        return False


def desembarcar_canibal(nodo):
    # comprobar que haya algun canibal en la barca
    if nodo[5] > 0:
        # dependiendo de la orilla
        if nodo[6] == "derecha":
            # Comprobar que es no se pueden desembarcar más canibales que misioneros
            if nodo[2] >= nodo[3] + 1:
                # habria mas o el mismo numero de misioneros
                return True
            return False
        elif nodo[6] == "izquierda":
            # Comprobar que es no se pueden desembarcar más canibales que misioneros
            if nodo[0] >= nodo[1] + 1:
                # habria mas o el mismo numero de misioneros
                return True
            return False
    else:
        return False


def desembarcar_canibales(nodo):
    # comprobar que haya dos canibales en la barca
    if nodo[5] == 2:
        # dependiendo de la orilla
        if nodo[6] == "derecha":
            # Comprobar que es no se pueden desembarcar más canibales que misioneros
            if nodo[2] >= nodo[3] + 2:
                # habria mas o el mismo numero de misioneros
                return True
            return False
        elif nodo[6] == "izquierda":
            # Comprobar que es no se pueden desembarcar más canibales que misioneros
            if nodo[0] >= nodo[1] + 2:
                # habria mas o el mismo numero de misioneros
                return True
            return False
    else:
        return False


"""
========================================
      OPERADOR PARA NAVEGAR
========================================
"""


def navegar(nodo):
    # se podrá transitar a la orilla contraria si hay al menos algun tripulante
    if nodo[4] + nodo[5] > 0:
        return True
    return False


resultados = algoritmo_a_estrella()
imprimir_camino(resultados)
