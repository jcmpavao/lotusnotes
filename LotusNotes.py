import os
from os import path
import sys

class CodigosLotusNotes():
        def __init__(self,arquivo_codigos="CodigosNotes.data"):
                self.carregado = False
                self.lista_codigos = os.path.abspath(os.getcwd()) + "/" + arquivo_codigos
                self.codigos = {}
                self.carregado = self.carregarCodigos()
        def carregarCodigos(self):
                retorno = False
                #print(self.lista_links)
                if ( os.path.isfile(self.lista_codigos)):
                        try:
                                with open(self.lista_codigos, 'r') as f:
                                        for linha in f.readlines():
                                                campo = linha.replace('\n','').replace('\ufeff','').split(';')
                                                self.codigos[campo[0]] = campo[1]
                                retorno = ( len(self.codigos)> 0 )
                        except:
                                print(str(sys.exc_info()))
                else:
                    print("sem banco")

                return retorno
                #print("fim da carga de classificacao e regressao")
        def imprimirCodigos(self):
            for c in self.codigos:
                print(self.codigos[c])

        def imprimirIDs(self):
            for c in self.codigos:
                print(c)

class LeisLotusNotes():
    def __init__(self, arquivo_leis="contlei.data"):
        self.carregad0 = False
        self.lista_leis = os.path.abspath(os.getcwd()) + "/" + arquivo_leis
        self.leis = {}
        self.carregado = self.carregarLeis()
    def carregarLeis(self):
        retorno = False
        #print(self.lista_links)
        if ( os.path.isfile(self.lista_leis)):
            try:
                print("inicio carregamento")
                with open(self.lista_leis, 'r') as f:
                    for linha in f.readlines():
                        campo = linha.replace('\n','').replace('\ufeff','').split(';')
                        chave = str(campo[1]) + str(campo[0]).zfill(6)
                        try:
                            self.leis[chave] = { "lei" : int(campo[0]) , "ano" : int(campo[1]), "url": campo[2] ,"status" : campo[3], "ementa" : campo[4], "autoria" : campo[5] }
                        except:
                            print("erro chave : " + chave + " " + str(sys.exc_info()))
                retorno = ( len(self.leis) > 0 )
            except:
                print(str(sys.exc_info()))
        else:
            print("sem banco")
        return retorno
    def localizarLeiPorAnoCodigo(self,ano, codigo):
        retorno = {"lei" : 0, "ano" : 0}
        chave = str(ano) + str(codigo).zfill(6)
        if ( chave in self.leis.keys()):
            retorno = self.leis[chave]
        return retorno

    def imprimirLeis(self):
        for b in self.leis:
            print(b)
    def totalLeis(self):
        return len(self.leis.keys())
class LotusNotesHREFs():
        def __init__(self, arquivo_links="BancosNotes.data"):
                self.carregado = False
                self.lista_links = os.path.abspath(os.getcwd()) + "/" +arquivo_links
                self.links = {}
                self.carregado = self.carregarLinks()
        def carregarLinks(self):
                retorno = False
                #print(self.lista_links)
                if ( os.path.isfile(self.lista_links)):
                        try:
                                with open(self.lista_links, 'r') as f:
                                        for linha in f.readlines():
                                                campo = linha.replace('\n','').replace('\ufeff','').split(';')
                                                self.links[campo[1]] = [ campo[0] ,  campo[2] ,campo[3], int(campo[4]) ]
                                retorno = ( len(self.links)> 0 )
                        except:
                                print(str(sys.exc_info()))
                else:
                    print("sem banco")

                return retorno
        def primeiraUltimaLeg(self):
            lista = []
            for b in self.links:
                if(self.links[b][3] > 0 ):
                     lista.append(self.links[b][3])
            return {"primeira" : min(lista) , "ultima" : max(lista)}
            
        def imprimirBancos(self):
                for b in self.links:
                    print(b)

        def imprimirLinks(self):
                for l in self.links:
                    print(self.links[l][1])
        
        def obterLinkPorLeg(self,leg):
            retorno = ""
            for b in self.links:
                 if ( self.links[b][3] == leg):
                        retorno = self.links[b][1]
                        break
            return retorno            

        def obterLinkIdPorLeg(self,leg):
            retorno = {"id" : 0 , "link" : "" , "idWWW" : "" , "leg" : 0}
            for b in self.links:
                 if ( self.links[b][3] == leg):
                        retorno["id"] = self.links[b][0]
                        retorno["idWWW"] = self.links[b][2]
                        retorno["link"] = self.links[b][1]
                        retorno["leg"] = self.links[b][3]
                        break
            return retorno   

        def obterLinkIdPorAno(self,ano):
            retorno = {"id" : 0 , "link" : "" , "idWWW" : "" , "leg" : 0}
            if (ano in range(1991,1995)):
                retorno["id"] = self.links["Processo Leg. 1991/1994"][0]
                retorno["link"] = self.links["Processo Leg. 1991/1994"][1]                
                retorno["idWWW"] = self.links["Processo Leg. 1991/1994"][2]
                retorno["leg"] = self.links["Processo Leg. 1991/1994"][3]                
            elif (ano in range(1995,1999)):
                retorno["id"] = self.links["Processo Leg. 1995/1998"][0]
                retorno["link"] = self.links["Processo Leg. 1995/1998"][1]  
                retorno["idWWW"] = self.links["Processo Leg. 1995/1998"][2]
                retorno["leg"] = self.links["Processo Leg. 1995/1998"][3]                
            elif (ano in range(1999,2003)):
                retorno["id"] = self.links["Processo Leg. 1999/2003"][0]
                retorno["link"] = self.links["Processo Leg. 1999/2003"][1]  
                retorno["idWWW"] = self.links["Processo Leg. 1999/2003"][2]
                retorno["leg"] = self.links["Processo Leg. 1999/2003"][3]  
            elif (ano in range(2003,2007)):
                retorno["id"] = self.links["Processo Leg. 2003/2007"][0]
                retorno["link"] = self.links["Processo Leg. 2003/2007"][1]  
                retorno["idWWW"] = self.links["Processo Leg. 2003/2007"][2]
                retorno["leg"] = self.links["Processo Leg. 2003/2007"][3]  
            elif (ano in range(2007,2011)):
                retorno["id"] = self.links["Processo Leg. 2007/2011"][0]
                retorno["link"] = self.links["Processo Leg. 2007/2011"][1]  
                retorno["idWWW"] = self.links["Processo Leg. 2007/2011"][2]
                retorno["leg"] = self.links["Processo Leg. 2007/2011"][3]  
            elif (ano in range(2011,2015)):
                retorno["id"] = self.links["Processo Leg. 2011/2015"][0]
                retorno["link"] = self.links["Processo Leg. 2011/2015"][1]  
                retorno["idWWW"] = self.links["Processo Leg. 2011/2015"][2]
                retorno["leg"] = self.links["Processo Leg. 2011/2015"][3]  
            elif (ano in range(2015,2019)):
                retorno["id"] = self.links["Processo Leg. 2015/2019"][0]
                retorno["link"] = self.links["Processo Leg. 2015/2019"][1]  
                retorno["idWWW"] = self.links["Processo Leg. 2015/2019"][2]
                retorno["leg"] = self.links["Processo Leg. 2015/2019"][3]  
            elif (ano in range(2019,2023)):
                retorno["id"] = self.links["Processo Leg. 2019/2023"][0]
                retorno["link"] = self.links["Processo Leg. 2019/2023"][1]  
                retorno["idWWW"] = self.links["Processo Leg. 2019/2023"][2]
                retorno["leg"] = self.links["Processo Leg. 2019/2023"][3]  
 
            return retorno  
        
        def imprimirIDs(self):
                for l in self.links:
                    print(self.links[l][0])

LotusNotes = LotusNotesHREFs()
CodigosNotes = CodigosLotusNotes()
LeisNotes = LeisLotusNotes()
if __name__ == "__main__":
	Lt = LotusNotesHREFs()
	if ( Lt.carregado):
		Lt.imprimirBancos()
		Lt.imprimirLinks()
		Lt.imprimirIDs()
		print(Lt.links)
	CodigosNotes.imprimirCodigos()
	CodigosNotes.imprimirIDs()
