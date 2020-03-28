#-*-coding: utf-8-*-
from random import choice
##############################################################################
# Variables globales
##############################################################################

# Crea las letras minúsculas a-z
letrasProposicionales = [chr(x) for x in range(97, 123)]
# inicializa la lista de interpretaciones
listaInterpsVerdaderas = []
# inicializa la lista de hojas
listahojas = []

neg = "-"
Y = "Y"
O = "O"
ent = ">"
conectivosBinarios = [O, Y, ent]


##############################################################################
# Definición de objeto tree y funciones de árboles
##############################################################################

class Tree(object):
	def __init__(self, label, left, right):
		self.left = left
		self.right = right
		self.label = label

def Inorder(f):
    # Imprime una formula como cadena dada una formula como arbol
    # Input: tree, que es una formula de logica proposicional
    # Output: string de la formula
	if f.right == None:
		return f.label
	elif f.label == '-':
		return f.label + Inorder(f.right)
	else:
		return "(" + Inorder(f.left) + f.label + Inorder(f.right) + ")"
def Atomos(f):
        if f.right == None:
                return [f.label]
        elif f.label == neg:
                return Atomos(f.right)
        elif f.label in conectivosBinarios:
                return Atomos(f.left) + Atomos(f.right)
        
def string2Tree(A):
    # Crea una formula como tree dada una formula como cadena escrita en notacion polaca inversa
    # Input: A, lista de caracteres con una formula escrita en notacion polaca inversa
             # letrasProposicionales, lista de letras proposicionales
    # Output: formula como tree

	# OJO: DEBE INCLUIR SU CÓDIGO DE STRING2TREE EN ESTA PARTE!!!!!
#Crea una formula como tree dada una formula
        #como cadena escritra en notacion POLACA INVERSA
        #Input: A, Lista de caracteres con una formula escrita en notacon polaca iinversa
        #LetrasProposicionales, lista de letras proposicionales
#output: formula como tree
    
    
    pila = []
    for c in A:
            
        if c in letrasProposicionales:
            pila.append(Tree(c, None, None))
            #print(inorder(Tree(c,None,None)))
        elif c == neg:
            FormulaAux = Tree(c, None, pila[-1])
            del pila[-1]
            pila.append(FormulaAux)
        elif c in conectivosBinarios:
            FormulaAux = Tree(c, pila[-1], pila[-2])
            del pila[-1]
            del pila[-1]
            pila.append(FormulaAux)
    
    return pila[-1]


##############################################################################
# Definición de funciones de tableaux
##############################################################################

def imprime_hoja(H):
	cadena = "{"
	primero = True
	for f in H:
		if primero == True:
			primero = False
		else:
			cadena += ", "
		cadena += Inorder(f)
	return cadena + "}"


def par_complementario(l):
        # Esta función determina si una lista de solo literales
	# contiene un par complementario
	# Input: l, una lista de literales
	# Output: True/False
        for elemento in l:
                for segundoElem in l:
                        if elemento.label == neg:
                                #en el caso donde el primero fuese una negacion
                                if elemento.right.label == segundoElem.label:
                                        return True
                        
                        if segundoElem.label == neg:
                                if elemento.label == segundoElem.right.label:
                                        return True
        return False


def es_literal(f):
	# Esta función determina si el árbol f es un literal
	# Input: f, una fórmula como árbol
	# Output: True/False
        #ahora debo detectar como tal si bien sea es la letra o contiene una negacio
        if(f.label == neg):
                if f.right.label in letrasProposicionales:
                        return True
        if f.label in letrasProposicionales:
                return True

        return False
def no_literales(l):
	# Esta función determina si una lista de fórmulas contiene
	# solo literales
	# Input: l, una lista de fórmulas como árboles
	# Output: None/f, tal que f no es literal
        for elemento in l:
                #revisar en casa una de las forumas contenidas en l
                if (not(es_literal(elemento))):
                        return False
        return True

def clasifica_y_extiende(f):
    global listahojas
    if f.label == neg:
        if f.right.label == neg:
            for l in listahojas:
                for Arb in l:
                    if Arb.right.label == f.right.label and Arb.right.left.label == f.right.left.label and Arb.right.right.label == f.right.right.label:
                        l.remove(Arb)
                        l.apend([f.right.right])
        elif f.right.label == O:
            for l in listahojas:
                for Arb in l:
                    if Arb.right != None:
                        if Arb.right.label == f.right.label and Arb.right.left.label == f.right.left.label and Arb.right.right.label == f.right.right.label :
                            l.remove(Arb)
                            l.append(Tree('-',None,f.right.left))
                            l.append(Tree('-',None,f.right.right))
        elif f.right.label == ent:
            for l in listahojas:
                for Arb in l:
                    if Arb.right != None:
                        if Arb.right.label == f.right.label and Arb.right.left.label == f.right.left.label and Arb.right.right.label == f.right.right.label :
                            l.remove(Arb)
                            l.append(f.right.left)
                            l.append(Tree('-',None,f.right.right))
        elif f.right.label == Y:
            valores = []
            for l in listahojas:
                for Arb in l:
                    valores.append(Arb)
                    if Arb.right.label == f.right.label and Arb.right.left.label == f.right.left.label and Arb.right.right.label == f.right.right.label :
                        l.remove(Arb)
                        valores = l[:]
                        l.append(Tree('-',None,f.right.left))
                        valores.append(Tree('-',None,f.right.right))
            listahojas.append(valores)

    elif f.label == Y:
        for l in listahojas:
            for Arb in l:
                if Arb.label == f.label and Arb.left.label == f.left.label and Arb.right.label==f.right.label:
                    l.remove(Arb)
                    l.append(f.left)
                    l.append(f.right)
    
    elif f.label == O:
        valores = []
        for l in listahojas:
            for Arb in l:
                if Arb.label == f.label and Arb.left.label == f.left.label and Arb.right.label==f.right.label:
                    l.remove(Arb)
                    valores = l[:]
                    l.append(f.left)
                    valores.append(f.right)
        listahojas.append(valores)
    elif f.label == ent:
        valores = []
        for l in listahojas:
            for Arb in l:
                if Arb.label == f.label and Arb.left.label == f.left.label and Arb.right.label==f.right.label:
                    l.remove(Arb)
                    valores = l[:]
                    l.append(Tree('-',None,f.right.left))
                    valores.append(f.right.right)
                valores.append(Arb)
        listahojas.append(valores)

def Tableaux(f):

	# Algoritmo de creacion de tableau a partir de lista_hojas
	# Imput: - f, una fórmula como string en notación polaca inversa
	# Output: interpretaciones: lista de listas de literales que hacen
	#		 verdadera a f
    global listahojas
    global listaInterpsVerdaderas
    A = string2Tree(f)
    listahojas = [[A]]
    while len(listahojas) > 0 :
        hojas = choice(listahojas)
        if not no_literales(hojas) :
            for tree in hojas:
                clasifica_y_extiende(tree)
                print('hola')
        else:
            if par_complementario(hojas):
                listahojas.remove(hojas)
            else:
                listaInterpsVerdaderas.append(hojas)
                listahojas.remove(hojas)
    return listaInterpsVerdaderas