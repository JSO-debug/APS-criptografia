#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTAÇÕES
from cryptography.fernet import Fernet
from random import randint
from time import time

'''
#CRIPTOGRAFIA
key = Fernet.generate_key()
cipher_suite = Fernet(key)

mensagem = input("Insira a mensagem que deseja criptografar: ")
cipher_text = cipher_suite.encrypt(bytes(mensagem.encode()))
plain_text = cipher_suite.decrypt(cipher_text)                                      #bytes
print("\nMinha mensagem criptografada é: " + str(cipher_text)[1:], '\n')
print("A chave é: " + str(key)[1:], '\n')
print("Minha mensagem descriptografada é: " + bytearray(plain_text).decode())       #str
print(type(cipher_text))
'''
# CHAVES PÚBLICA E PRIVADA
def CalcPrimo(n1):
    primo = True
    num = 2
    # Verifica excessão do número 1
    if n1 == 1:
        primo = False
        return n1, primo
    # Verifica se o número é primo
    for i in range(3, n1, 2):
        if n1 % num == 0:
            primo = False
            break
        num = i
    return n1, primo


def mdc(n1, n2):
    resto = 1
    while True:
        resto = n1 % n2
        n1 = n2
        n2 = resto
        if resto == 0:
            break
    return n1


# PARTE 1/2 - Chave Pública e Fernet
p = 0
while True:
    aleat = randint(10 ** 2, (10 ** 3 - 1))
    q = 0
    if CalcPrimo(aleat)[1] and p == 0:
        p = aleat
    if CalcPrimo(aleat)[1] and p != 0 and p != aleat:
        q = aleat
    if p != 0 != q:
        break

n = p * q
phiN = (p - 1) * (q - 1)

e = 2
while mdc(phiN, e) != 1:
    e += 1

#Criptografia Fernet
key = Fernet.generate_key()
msg = input("Insira a mensagem que deseja criptografar: ")
criptoF = Fernet(key).encrypt(bytes(msg.encode()))
print(f"Fernet: {criptoF}")

#Chave Pública
cifraPublica = []  # Lista que recebe msg criptografada
cont = 1  # Disfarça caracteres repetidos
for i in criptoF:
    cifraPublica.append(((ord(chr(i)) ** e) % n) * cont)
    cont += 1
print(f"Sua mensagem criptografada é: {cifraPublica}\n")


# PARTE 2/2 - Chave Privada e Fernet
iniTotal = time()
pergunta = input("Digite qualquer tecla para descriptografar a sua mensagem: ")
print()
d = 1

#Cálculo do D
while d * e % phiN != 1:
    d += 1

cifraTraduzida = []
cont = 1
ini = time()
aviso = True
for i in cifraPublica:
    cifraTraduzida.append((i // cont) ** d % n)
    fim = time()
    if (fim - ini > 15) and aviso:
        print("Aguarde enquanto descriptografamos sua mensagem.")
        aviso = False
    cont += 1
cifraPrivada = ''

for i in cifraTraduzida:
    cifraPrivada += chr(i)

conversao = bytes(cifraPrivada, encoding='utf-8')
msgTraduzida = Fernet(key).decrypt(conversao2).decode()

fimTotal = time()
dif = fimTotal - iniTotal
print(f"Mensagem traduzida: {msgTraduzida}\n{type(msgTraduzida)}")
print()
print(f"O processo de descriptografia levou {dif} segundos para ser executado.")



'''
def main():
    try:
        f = open("keys.ppk", "x")
        f.write(cifraPublica)
    except:
        open("keys.ppk", "r+")
    finally:
        f.close()
'''