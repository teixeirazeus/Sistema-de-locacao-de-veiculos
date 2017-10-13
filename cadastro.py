#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  cadastro.py
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

from load import listar

def cadastro(dadoi, dir, info):
    nome = input(dadoi)
    if nome in listar(dir):
        print("Já Cadastrado!")
        return
    dados = []
    for imp in info:
        dados.append(input(imp))

    f = open(dir+"/" + nome, 'w')
    i = 0
    f.write(dadoi+nome+ "\n")
    for dado in dados:
        f.write(info[i]+dado + "\n")
        i += 1
    f.close()
    

def cliente():
    dadoi = "CPF:"
    dir = "usr"
    info = ['Nome:', 'Data de nascimento (dd/mm/aaaa):', 'RG:', 'CNH:', 'Validade:']
    cadastro(dadoi, dir, info)

def carro():
    dadoi = "Placa:"
    dir = "car"
    info = ['Categoria:', 'Renavan:', 'Marca:', 'Modelo:', 'Combustivel:','Cor:']
    cadastro(dadoi, dir, info)
