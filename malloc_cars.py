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
import datetime
from datetime import date

import load
import cadastro

def clear():
    os.system("clear")

def vencido(data):
    data = data.split("/")
    data = date(int(data[2]),int(data[1]),int(data[0]))
    if data < date.today():
        return True
    else:
        return False

def mod(target, nome):

    if target == "cliente":
        dados = load.carregar_cliente(nome)
        dir = "usr"
    else:
        dados = load.carregar_carro(nome)
        dir = "car"

    while(True):
        clear()
        print("================")
        i = 0
        for x in dados:
            print(i,'.',x)
            i += 1
        print("================")
        resp = input("Digite o numero da linha deseja modificar ou digite s para salvar:")
        if resp != "s":
            item = (dados[int(resp)].split(":"))[0]
            novo = input(item+':')
            dados[int(resp)] = item+":"+novo
        else:
            os.system("rm "+dir+"/"+nome)
            f = open(dir+"/" + nome, 'w')
            for dado in dados:
                f.write(dado+"\n")
            f.close()
            return




def lista_categoria(resp):
    for carro in car_db:
        if carro in carros_stor and car_db[carro][1] == "Categoria:"+resp:
            print("===========================")
            for dados in car_db[carro]:
                print(dados)
            print("===========================")

def calc_preco(categoria, dia_locacao, dia_devolucao):
    dias = date_dif(dia_devolucao,dia_locacao)
    custo = dias*preco[categoria-1]

    data = dia_devolucao.split("/")
    data = date(int(data[2]),int(data[1]),int(data[0]))

    if data < date.today():
        multa = date_dif(dia_devolucao)*preco[categoria-1]*2 #multa com o dobro
    else:
        multa = 0
    return custo, multa


def locacao():
    cpf = input("Entre com o cpf do cliente:")

    if cpf not in load.listar("usr"):
        print("Usuario não cadastrado!")
        resp = input("Deseja realizar seu cadastro?[s/n]:")
        if resp == "n":
            return
        cadastro.cliente()
        return

    if vencido(usr_db[cpf][5].split(":")[1]):
        print("Erro: cliente com carteira vencida!")
        return

    print("Escolha uma categoria de carro.")
    print("1.economica")
    print("2.intermediaria")
    print("3.luxo")
    resp = input(":")

    lista_categoria(resp)


    placa = input("Insira o numero da placa do carro:")
    dia = input("Insira o dia da entrega dd/mm/yyyy:")

    clear()
    print("CPF:",cpf)
    print("Carro:",placa)
    print("Dia de devolucao:", dia)
    print("Dias:",date_dif(dia))
    print("Preço: R$ ",preco[int(resp)-1]*int(date_dif(dia)))
    resp = input("Deseja alugar o carro? [s/n]:")
    if resp == "s":
        temp = cpf+' '+placa+' '+str(date.today())+ ' ' +dia
        os.system("echo "+temp+" >> loc")
        print("Carro locado!")
    else:
        print("Operação cancelada!")


def date_dif(data, data2 = date.today()):
    data = data.split("/")
    data = date(int(data[2]),int(data[1]),int(data[0]))

    if type(data2) == type(''):
        data2 = data2.split("-")
        data2 = date(int(data2[0]),int(data2[1]),int(data2[2]))

    dif = data - data2

    return abs(dif.days)

def str2date(data):
    data = data.split("/")
    data = date(int(data[2]),int(data[1]),int(data[0]))
    return date

def banner():
    os.system("cat banner")

def main(args):
    #configurações globais
    #Preço das categorias
    global preco
    #p1 = 89.9  #economica
    #p2 = 174.9 #intermediaria
    #p3 = 289.9 #luxo
    preco = [89.9,174.9,289.9]

    #inicialização
    global usr_db,car_db,loc,carros_stor
    #usr_db,car_db,loc = carregar_dados()
    #usr_db,car_db,loc,carros_stor = load.fresh()
    #/inicialização

    while(True):
        usr_db,car_db,loc,carros_stor = load.fresh()
        clear()
        banner()
        print("|-----------|")
        print("|1.Cliente  |")
        print("|2.Carros   |")
        print("|3.Locação  |")
        print("|4.Devolução|")
        print("|5.Busca    |")
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
                #os.system("nano usr/"+id)
                mod("cliente", id)
            elif resp == "2":
                cadastro.cliente()
                print("Cadastrado com sucesso.")
                time.sleep(2)
            elif resp == "3":
                id = input("Insira o cpf do usuario:")
                os.system("cat usr/"+id)
                rest = input("Você deseja remover o usuario acima?[s/n]")
                if resp == "s":
                    os.system("rm usr/"+id)
                    print("Usuario deletado!")
                    time.sleep(2)
        elif resp == "2":
            print("|<Carros>---|")
            print("|1.Atualizar|")
            print("|2.Cadastro |")
            print("|3.Remover  |")
            print("|-----------|")
            resp = input(":")
            if resp == "1":
                id = input("Insira a placa do carro:")
                mod("carro", id)
                #os.system("nano car/"+id)
            elif resp == "2":
                cadastro.carro()
                print("Cadastrado com sucesso.")
                time.sleep(2)
            elif resp == "3":
                id = input("Insira a placa do carro:")
                os.system("cat car/"+id)
                rest = input("Você deseja remover o carro acima?[s/n]")
                if resp == "s":
                    os.system("rm car/"+id)
                    print("Carro deletado!")
                    time.sleep(2)
        elif resp == "3":
            clear()
            locacao()
            time.sleep(2)
            #Remove
            #grep -vwE "(cat|666)" loc
        elif resp == "4":
            clear()
            cpf = input("Insira o cpf do cliente:")
            output = subprocess.check_output("cat loc | grep "+cpf, shell=True) #pega os dados da linha em loc
            output = output.decode('ascii')
            output = output.rstrip()
            output = output.split(" ")
            print("CPF:",output[0])
            print("Placa:", output[1])
            print("Data de locação:", output[2])
            print("Data de devolução:", output[3])
            categoria = int((car_db[output[1]][1]).split(":")[1])

            #pegar categoria_preco
            custo,multa = calc_preco(categoria, output[2], output[3])

            #Incluir multa
            print("--------------------------")
            print("Preço: %.2f" % (custo))
            print("Multa: %.2f" % (multa))
            print("Total: %.2f" % (custo+multa))
            #soma de multa

            print("--------------------------")
            x = input("Pagar? [s/n]")
            if x == "s":
                os.system('cat loc | grep '+cpf+' >> log') #Salva o log
                os.system('grep -vwE "(cat|'+cpf+')" loc > temp')   #Tira a linha com cpf em loc
                os.system('cp temp loc')
                print("O carro retornou a garagem!")
                time.sleep(2)
        elif resp == "5":
            print("|<Busca>----|")
            print("|1.Cliente  |")
            print("|2.Carro    |")
            print("|-----------|")
            resp = input(":")
            if resp == '1':
                cpf = input("CPF:")
                if cpf in usr_db.keys():
                    clear()
                    print("===========================")
                    os.system('cat usr/'+cpf)
                    print("===========================")
                    x = input("pressione enter para voltar")
                else:
                    print("Erro: usuario não encontrado")
                    time.sleep(2)
            elif resp == '2':
                    print("|<Busca/Carro>--|")
                    print("|1.Placa        |")
                    print("|2.Categoria    |")
                    print("|---------------|")
                    resp = input(":")
                    if resp == '1':
                        placa = input("Placa:")
                        if placa in car_db.keys():
                            clear()
                            print("===========================")
                            os.system('cat car/'+placa)
                            print("===========================")
                            x = input("pressione enter para voltar")
                        else:
                            print("Erro: carro não encontrado")
                            time.sleep(2)
                    if resp == '2':
                        resp = input("Categoria:")
                        clear()
                        lista_categoria(resp)
                        x = input("pressione enter para voltar")


    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
