import os
from os import path
import sys
import requests
from bs4 import BeautifulSoup
import time

class OrdemDiaLotusNotes():
    def __init__(self, arquivo_ordens="ordemdia.data"):
        self.urlRaiz = "http://alerjln1.alerj.rj.gov.br"
        self.carregad0 = False
        self.lista_ordens = os.path.abspath(os.getcwd()) + "/" + arquivo_ordens
        self.ordens = {}
        self.carregado = self.carregarOrdens()
    def carregarOrdens(self):
        retorno = False
        #print(self.lista_links)
        if ( os.path.isfile(self.lista_ordens)):
            try:
                print("inicio carregamento")
                with open(self.lista_ordens, 'r') as f:
                    for linha in f.readlines():
                        campo = linha.replace('\n','').replace('\ufeff','').split(';')
                        mes, dia ,ano  = str(campo[0]).split("/")[0] , str(campo[0]).split("/")[1] , str(campo[0]).split("/")[2]
                        data = dia +"/" +  mes + "/" + ano
                        chave = ano + mes + dia
                        hora = campo[1]
                        tipo = campo[2]
                        link  = campo[3]
                        try:
                            if ( chave in self.ordens.keys()):
                                self.ordens[chave]["sessao"].append({"tipo":tipo,"hora": hora,"link" : self.urlRaiz + link})
                                self.ordens[chave]["total"] = int(self.ordens[chave]["total"]) + 1
                            else:
                                self.ordens[chave] = {"data" : data ,"ano" : ano , "mes" : mes, "total" : 1,"sessao" :[{ "tipo" : tipo ,  "hora" : hora,"link": self.urlRaiz + link} ]}
                        except:
                            print("erro chave : " + chave + " " + str(sys.exc_info()))
                retorno = ( len(self.ordens) > 0 )
            except:
                print(str(sys.exc_info()))
        else:
            print("sem banco")
        return retorno
    def obterConteudoSessao(self, url):
        retorno = ""
        try:
            result =  requests.get(url.lstrip().rstrip())
            soup = BeautifulSoup(result.content,'lxml')
            ancoras = soup.find_all("a")
            for an in ancoras:
                del an["href"]
                #an["href"] = self.urlRaiz + an["href"].string
            retorno = str(soup.body) #.get_text()
        except:
            retorno = str(sys.exc_info())
        return retorno
    def localizarOrdemPorData(self,data):
        retorno = []
        chave = data.split(";")[0] + data.split(";")[1] + data.split(";")[2]
        if ( chave in self.ordens.keys()):
            retorno = self.ordens[chave]
        return retorno

    def listarOrdemPorAnoMes(self,ano,mes):
        retorno = []
        #chave = data.split("/")[2] + data.split("/")[1] + data.split("/")[0]
        #mes = data.split("/")[1]
        #ano = data.split("/")[2]
        #print(mes)
        for chave in self.ordens:
            ordem = self.ordens[chave]
            if ( ordem["mes"] == mes and ordem["ano"] == ano):
                retorno.append(self.ordens[chave])
        return retorno
    
    def imprimirOrdens(self):
        for b in self.ordens:
            print(b)
    def totalOrdens(self):
        return len(self.ordens.keys())

OrdemDia = OrdemDiaLotusNotes()
if __name__ == "__main__":
    o = OrdemDia()
    o.listarOrdemPorAnoMes("01/07/2020")
