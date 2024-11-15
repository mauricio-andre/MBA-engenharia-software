limite = 100
soma = 0
numero = 1

# ENQUANTO A SOMA FOR MENOR QUE O LIMITE, CONTINUE SOMANDO
while soma < limite:
    soma += 1

print (soma)

# ENCONTRAR O PRIMEIRO NÚMERO DIVISÍVEL POR 7 EM UM INTERVALO
for numero in range(1, 100):
    if numero % 7 == 0:
      print(numero)
      break

# VERIFICA SE TODOS OS ITENS DE UMA LISTA SÃO POSITIVOS
numeros = [1, 2, 3, 8, 9, -1]
todos_positivos = True

for numero in numeros:
   if numero <= 0:
      todos_positivos = False
      break

if todos_positivos:
   print("Todos são positivos")
else:
   print("Há números negativos")