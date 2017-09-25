#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  malloc_cars.py
#
#  Copyright 2017 Thiago da Silva Teixeira <teixeira.zeus@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
import os
import copy
import time

def clear():
    os.system("clear")

def listar(dir):
    p = os.popen("ls "+dir+"/", "r")
    diretorio = []
    while 1:
        line = p.readline()
        if not line:
            break
        diretorio.append(line.rstrip())
    #for item in diretorio:
    #    print(item)
    return diretorio

def carregar_cliente(cpf):
    f = open("usr/" + cpf)
    dados = []
    while 1:
        line = f.readline()
        if not line:
            break
        dados.append(line.rstrip())
    f.close()
    return dados

def carregar_carro(placa):
    f = open("car/" + placa)
    dados = []
    while 1:
        line = f.readline()
        if not line:
            break
        dados.append(line.rstrip())
    f.close()
    return dados

def carregar_dados():
    usuarios = listar("usr")
    usr_db = {}
    for cliente in usuarios:
        dados = carregar_cliente(cliente)
        usr_db[cliente] = dados

    usuarios = listar("car")
    car_db = {}
    for placa in usuarios:
        dados = carregar_carro(placa)
        car_db[placa] = dados

    return usr_db,car_db,locs()

def locs():
    f = open("loc")
    dados = []
    while 1:
        line = f.readline()
        if not line:
            break
        dados.append((line.rstrip()).split())
    f.close()
    return dados

def cadastro_cliente():
    cpf = input("CPF:")
    if cpf in listar("usr"):
        print("Usuario já cadastrado!")
        return
    dados = []
    info = ['Nome:', 'Data de nascimento (dd/mm/aaaa):', 'RG:', 'CNH:', 'Validade:']
    for imp in info:
        dados.append(input(imp))

    f = open("usr/" + cpf, 'w')
    i = 0
    for dado in dados:
        f.write(info[i]+dado + "\n")
        i += 1
    f.close()

    print("Cliente cadastrado com sucesso.")


def cadastro_carro():
    cpf = input("Placa:")
    if cpf in listar("car"):
        print("Carro já cadastrado!")
        return
    dados = []
    info = ['Categoria:', 'Renavan:', 'Marca:', 'Modelo:', 'Combustivel:','Cor:']
    for imp in info:
        dados.append(input(imp))

    f = open("car/" + cpf, 'w')
    i = 0
    for dado in dados:
        f.write(info[i]+dado + "\n")
        i += 1
    f.close()

    print("Carro cadastrado com sucesso.")

def fresh():
    usr_db,car_db,loc = carregar_dados()
    carros_stor = []
    for carro in car_db.keys():
        carros_stor.append(carro) #carros na garagem

    for carro in carros_stor:   #tira carros alugados da garagem
        for locacao in loc:
            if locacao[1] == carro:
                carros_stor.remove(carro)


def alugar():
    clear()
    id = input("Entre com o cpf do cliente:")
    if id not in listar("usr"):
        print("Usuario não cadastrado!")
        resp = input("Deseja realizar seu cadastro?[s/n]:")
        if resp == "n":
            return
        cadastro_cliente()
    print("Escolha uma categoria de carro.")
    print("1.economica")
    print("2.")


def banner():
    os.system("cat banner")

def main(args):
    #configurações globais
    #Preço das categorias
    global p1, p2, p3
    p1 = 5  #economica
    p2 = 10 #
    p3 = 20

    #inicialização
    global usr_db,car_db,loc,carros_stor
    #usr_db,car_db,loc = carregar_dados()
    fresh()
    #/inicialização

    while(True):
        clear()
        banner()
        print("|-----------|")
        print("|1.Cliente  |")
        print("|2.Carros   |")
        print("|3.Locação  |")
        print("|-----------|")
        resp = input(":")
        if resp == "1":
            print("|<Cliente>--|")
            print("|1.Atualizar|")
            print("|2.Cadastro |")
            print("|3.Remover  |")
            print("|-----------|")
            resp = input(":")
            if resp == "1":
                id = input("Insira o cpf do usuario:")
                os.system("nano usr/"+id)
            elif resp == "2":
                cadastro_cliente()
            elif resp == "3":
                id = input("Insira o cpf do usuario:")
                os.system("cat usr/"+id)
                rest = input("Você deseja remover o usuario acima?[s/n]")
                    if resp == "s":
                        os.system("rm usr/"+id)
                        print("Usuario deletado!")
                        time.sleep(2)
        elif resp == "2":
            print("|<Carros>--|")
            print("|1.Atualizar|")
            print("|2.Cadastro |")
            print("|3.Remover  |")
            print("|-----------|")
            resp = input(":")
            if resp == "1":
                id = input("Insira a placa do carro:")
                os.system("nano car/"+id)
            elif resp == "2":
                cadastro_carro()
            elif resp == "3":
                id = input("Insira a placa do carro:)
                os.system("cat carro/"+id)
                rest = input("Você deseja remover o carro acima?[s/n]")
                    if resp == "s":
                        os.system("rm car/"+id)
                        print("Carro deletado!")
                        time.sleep(2)
        elif resp == "3":
            locacao()












    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
