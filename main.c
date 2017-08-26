/*
 * main.c
 *
 * Copyright 2017 Thiago da Silva Teixeira <teixeira.zeus@gmail.com>
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 * MA 02110-1301, USA.
 *
 *
 */

#include <stdio.h>
#include <stdbool.h>
#include <time.h>

int cpf_validacao(char cpf[]){
        int icpf[12];
        int i,somador=0,digito1,result1,result2,digito2,valor;

        for(i=0; i<11; i++) icpf[i]=cpf[i]-48;
        for(i=0; i<9; i++) somador+=icpf[i]*(10-i);
        result1=somador%11;

        if( (result1==0) || (result1==1) ){
                digito1=0;
        }else{
                digito1 = 11-result1;
        }

        somador=0;

        for(i=0; i<10; i++) somador+=icpf[i]*(11-i);
        valor=(somador/11)*11;
        result2=somador-valor;

        if( (result2==0) || (result2==1) ){
                digito2=0;
        }else{
                digito2=11-result2;
        }

        if((digito1==icpf[9]) && (digito2==icpf[10])){
                //printf("\nCPF VALIDADO.\n");
                return true;
        }else{
                //printf("Problema com os digitos.\n");
                return false;
        }
}

bool existe(char nome_arquivo[]){
        char dir[] = "usr/";
        strcat(dir, nome_arquivo);
        FILE *fp;
        fp = fopen (dir, "r");
        if (fp == NULL) return false;  //não existe

        return true; //existe
}

void cadastro_cliente() {
        printf("Cadastro\n");
}

bool check_nascimento(char nascimento[]){

        printf("Tamanho da data = %d \n",strlen(nascimento));

        if (strlen(nascimento) != 10){  //Tamanho errado
                printf("Erro: tamanho da data de nascimento está errada.\n");
                printf("Siga o padrão 05/04/1999\n");
                return false;
        }

        int barra = 0;
        for (size_t index = 0; index < 10 ; index++)
                if (nascimento[index] == "/") barra++;
        if(barra != 2){
                printf("Erro: sintaxe errada na data de nascimento\n");
                printf("Siga o padrão 05/04/1999\n");
        }

        return true;

}

void tempo(){
        char buffer[32];
        struct tm *ts;
        char* c_time_string;
        size_t last;
        time_t timestamp = time(NULL);

        c_time_string = ctime(&timestamp);

        //ts   = localtime(&timestamp);
        //last = strftime(buffer, 32, "%A", ts);
        //buffer[last] = '\0';

        printf("%s\n", c_time_string);
        return 0;
}

int main(int argc, char const *argv[]) {
        //cadastro_cliente();

        tempo();

        char cpf[10], nome[50], nascimento[10];
        printf("Nome: ");
        scanf("%s", &nome);
        printf("\n Seu nome é %s \n", &nome );

        printf("CPF: ");
        scanf("%s", &cpf);
        printf("\n Seu cpf é <%s> \n", &cpf );

        printf("Length of string a = %d \n",strlen(cpf));

        printf("Nascimento dia/mes/ano: ");
        scanf("%s", &nascimento);
        check_nascimento(nascimento);

        if(cpf_validacao(cpf))
                printf("CPF valido\n");


        printf("teixeirazeus\n");
        return 0;
}
