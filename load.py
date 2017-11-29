#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  load.py
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

def listar(dir):
    p = os.popen("ls "+dir+"/", "r")
    diretorio = []
    while 1:
        line = p.readline()
        if not line:
            break
        diretorio.append(line.rstrip())
    return diretorio

def load(dir, nome):
    f = open(dir + nome)
    dados = []
    while 1:
        line = f.readline()
        if not line:
            break
        dados.append(line.rstrip())
    f.close()
    return dados

def carregar_cliente(cpf):
    return load("usr/",cpf)

def carregar_categorias():
    f = open("categorias", 'r')
    categorias = {}
    while 1:
        line = f.readline()
        if not line:
            break
        entrada = line.rstrip()
        entrada = entrada.split(" ")
        print(">>",entrada)
        categorias[entrada[0]] = float(entrada[1])
    f.close()
    return categorias

def carregar_carro(placa):
    return load("car/", placa)

def locs():
    return load("loc","")

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

def fresh():
    #global usr_db,car_db,loc,carros_stor
    usr_db,car_db,loc = carregar_dados()
    carros_stor = []

    for carro in car_db.keys():
        carros_stor.append(carro)

    #carros_stor = []
    for carro in carros_stor:
        for locacao in loc:
            placa = locacao.split()[1]
            if placa == carro:
                carros_stor.remove(carro)
    return usr_db,car_db,loc,carros_stor,carregar_categorias()
