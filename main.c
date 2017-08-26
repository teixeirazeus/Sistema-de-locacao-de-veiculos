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

        if( (result1==0) || (result1==1) ) {
                digito1=0;
        }else{
                digito1 = 11-result1;
        }

        somador=0;

        for(i=0; i<10; i++) somador+=icpf[i]*(11-i);
        valor=(somador/11)*11;
        result2=somador-valor;

        if( (result2==0) || (result2==1) ) {
                digito2=0;
        }else{
                digito2=11-result2;
        }

        if((digito1==icpf[9]) && (digito2==icpf[10])) {
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


int padrao_tempo(char nascimento[]){
        char temp[8];
        //05/04/1999
        for (size_t i = 0; i < 4; i++) temp[i] = nascimento[i+6];
        for (size_t i = 0; i < 2; i++) temp[i+4] = nascimento[i+3];
        for (size_t i = 0; i < 2; i++) temp[i+6] = nascimento[i];
        temp[8] = '\0';

        return atoi(temp);

}

bool check_nascimento(char nascimento[]){
        int hoje = dia_atual();

        if (strlen(nascimento) != 10) {  //Tamanho errado
                printf("Erro: tamanho da data de nascimento está errada.\n");
                printf("Siga o padrão 05/04/1999\n");
                return false;
        }

        int barra = 0;
        for (size_t index = 0; index < 10; index++)
                if (nascimento[index] == '/') barra++;

        if(barra != 2) {
                printf("Erro: sintaxe errada na data de nascimento.\n");
                printf("Siga o padrão 05/04/1999\n");
                return false;
        }

        if (hoje-padrao_tempo(nascimento) < 180000) {
                printf("Menor de idade detectado!\n");
                return false;
        }

        return true;

}

int dia_atual(){
        //Retorna data atual
        char saida[8] = {}, meses[] = "JanFebMarAprMayJunJulAugSepOctNovDec",
             mes_atual[3] = {}, buff[30] = {};

        int index=0, i=0;

        struct tm tm = *localtime(&(time_t){time(NULL)});
        //printf("%s", asctime(&tm));

      #ifdef __STDC_LIB_EXT1__
        char str[26];
        asctime_s(str, sizeof str, &tm);
        //printf("%s", str);
      #endif

        //Sat Aug 26 03:58:08 2017
        strcat(buff, asctime(&tm));

        for (index = 0; index < 4; index++) saida[index] = buff[index+20];  //ano no saida
        for (index = 0; index < 3; index++) mes_atual[index] = buff[index+4];


        for (index = 0; index < 36; index += 3) {
                for (i = 0; i < 2; i++)
                        if (mes_atual[i] != meses[index+i]) break;

                if (i == 2) break;
        }

        //mes na saida
        if (i < 10) {
                saida[4] = '0';
                saida[5] = ((index/3)+1)+'0';
        }else{
                saida[4] = '1';
                saida[5] = ((index/3)-9)+'0';
        }

        //dia na saida
        saida[6] = buff[8]; saida[7] = buff[9]; saida[8] = '\0';

        return atoi(saida);
}

void gravar_cliente(char nome[],char cpf[],char nascimento[]) {
        char dir[] = "usr/";
        strcat(dir, cpf);
        FILE *fp;
        fp = fopen (dir, "w");
        if (fp == NULL) { printf("Erro ao acessar arquivo %s\n", cpf); return false; }

        fprintf(fp,"%s;%s;%s;", nome,cpf,nascimento);
        fclose(fp);

        printf("Usuario cadastrado.\n");

        return 0;
}

void cadastro_cliente() {
        printf("Cadastro\n");

        char cpf[20], nome[50], nascimento[10];
        printf("Nome: ");
        scanf("%s", &nome);

        //Ativar validacao de cpf na implementação
        //Para realizar testes deixar comentado :D
        //while (true) {
        printf("CPF: ");
        scanf("%s", &cpf);
        //if(cpf_validacao(cpf)) break;

        //printf("CPF invalido\n");
        //}

        if(existe(cpf)) {
                printf("O usuario já possui cadastro\n");
                return;
        }

        printf("Nascimento dia/mes/ano: ");
        scanf("%s", &nascimento);
        check_nascimento(nascimento);

        gravar_cliente(nome,cpf,nascimento);

}

void consultar_cliente(arquivo){
        char dir[] = "usr/", ch,
             cpf[20], nome[50], nascimento[10],
             buff[100]={};

        int corte=0,index=0, i=0;

        strcat(dir, arquivo);
        FILE *fp;
        fp = fopen (dir, "r");
        if (fp == NULL) { printf("Erro ao acessar arquivo %s\n", arquivo); return false; }

        while( ( ch = fgetc(fp) ) != EOF ) buff[corte++] = ch;
        buff[corte] = '\0';
        corte = 0;

        for (index=0; index < 100; index++) {if (buff[index] == ';'){nome[i] = '\0'; break; }  nome[i++] = buff[index]; }
        for (i=0,index++; index < 100; index++) {if (buff[index] == ';'){cpf[i] = '\0'; break;} cpf[i++] = buff[index]; }
        for (i=0,index++; index < 100; index++) {if (buff[index] == ';'){nascimento[i] = '\0'; break;} nascimento[i++] = buff[index]; }

        //printf("Conteudo buff %s\n", buff);

        printf("Nome: %s\n", nome);
        printf("CPF: %s\n", cpf);
        printf("Nascimento: %s\n", nascimento);

        return 0;
}

int main(int argc, char const *argv[]) {
        //Lembretes
        //Descomentar validacao cpf no castro
        //cadastro_cliente();
        consultar_cliente("666");



        return 0;
}
