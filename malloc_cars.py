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
import subprocess
from datetime import date

import load
import cadastro

def clear():
    os.system("clear")

def locacao():
    clear()
    id = input("Entre com o cpf do cliente:")
    if id not in listar("usr"):
        print("Usuario não cadastrado!")
        resp = input("Deseja realizar seu cadastro?[s/n]:")
        if resp == "n":
            return
        cadastro.cadastro_cliente()
    print("Escolha uma categoria de carro.")
    print("1.economica")
    print("2.intermediaria")
    print("3.luxo")
    resp = input(":")

    for cat in carros_stor:
        if cat[0] == resp:
            print("--------------")
            for dados in cat:
                print(dados)
            print("--------------")

    placa = input("Insira o numero da placa do carro:")
    dia = input("Insira o dia da entrega dd/mm/yyyy:")

    clear()
    print("CPF:",id)
    print("Carro:",placa)
    print("Dia de locacao:", dia)
    print("Dias:",date_dif(dia))
    resp = input("Deseja alugar o carro? [s/n]:")
    if resp == "s":
        temp = id+' '+placa+' '+' '+dia
        os.system("echo "+temp+" >> loc")
        print("Carro locado!")
        load.fresh()
    else:
        print("Operação cancelada!")

    time.sleep(1)

def date_dif(data, data2 = date.today()):
    data = str2date(data)
    if type(data2) == type(''):
        data2 = str2date(data2)
    dif = abs(data-data2)
    if mod == 1:
        return dif.years
    return dif.days

def str2date(data):
    data = data.split("/")
    data = date(int(data[2]),int(data[1]),int(data[0]))
    return date

def banner():
    os.system("cat banner")

def main(args):
    #configurações globais
    #Preço das categorias
    global p1, p2, p3
    p1 = 89.9  #economica
    p2 = 174.9 #intermediaria
    p3 = 289.9 #luxo

    #inicialização
    global usr_db,car_db,loc,carros_stor
    #usr_db,car_db,loc = carregar_dados()
    load.fresh()
    #/inicialização

    while(True):
        clear()
        banner()
        print("|-----------|")
        print("|1.Cliente  |")
        print("|2.Carros   |")
        print("|3.Locação  |")
        print("|4.Devolução|")
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
                id = input("Insira a placa do carro:")
                os.system("cat carro/"+id)
                rest = input("Você deseja remover o carro acima?[s/n]")
                if resp == "s":
                    os.system("rm car/"+id)
                    print("Carro deletado!")
                    time.sleep(2)
        elif resp == "3":
            locacao()
            #Remove
            #grep -vwE "(cat|666)" loc
        elif resp == "4":
            cpf = input("Insira o cpf do cliente:")
            output = subprocess.check_output("cat loc | grep "+cpf, shell=True) #pega os dados da linha em loc
            output = output.decode('ascii')
            output = output.rstrip()
            output = output.split(" ")
            print("CPF:",output[0])
            print("Placa:", output[1])
            print("Data de devolução:", output[2])

            #pegar categoria_preco
            #Incluir multa
            print("--------------------------")
            print("Total:",preco*date_dif(output[2]))
            #soma de multa

            print("--------------------------")
            x = input("Pagar? [s/n]")
            if x == "s":
                os.system('cat loc | grep '+cpf+' >> log') #Salva o log
                os.system('grep -vwE "(cat|'+cpf+')" loc >> loc')   #Tira a linha com cpf em loc
                load.fresh()
                print("Computado!")
                time.sleep(2)

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
