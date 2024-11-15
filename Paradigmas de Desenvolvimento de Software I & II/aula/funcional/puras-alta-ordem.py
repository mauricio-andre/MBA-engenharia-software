def soma(a,b):
  return a + b

print(soma(3,4))
print(soma(3,4))

def aplicar_duas_vezes(func, valor):
  return func(func(valor))

def incrementar(x):
  return x + 1

def elevar_ao_quadrado(x):
  return x ** 2

def dividir_por_dois(x):
  return x / 2

print(incrementar(6))

print(aplicar_duas_vezes(incrementar, 6))

numeros = [1, 2, 3, 4, 5, 6]

def aplicar_transformacao(func, lista):
  return [func(x) for x in lista]

numeros_quadrado = aplicar_transformacao(elevar_ao_quadrado, numeros)
numeros_quadrado_dividido_por_dois = aplicar_transformacao(dividir_por_dois, numeros_quadrado)

print(numeros_quadrado)
print(numeros_quadrado_dividido_por_dois)