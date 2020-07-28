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
                                                self.links[campo[1]] = [ campo[0] ,  campo[2] ,campo[3] ]
                                retorno = ( len(self.links)> 0 )
                        except:
                                print(str(sys.exc_info()))
                else:
                    print("sem banco")

                return retorno
                #print("fim da carga de classificacao e regressao")
        def imprimirBancos(self):
                for b in self.links:
                    print(b)

        def imprimirLinks(self):
                for l in self.links:
                    print(self.links[l][1])

        def imprimirIDs(self):
                for l in self.links:
                    print(self.links[l][0])

LotusNotes = LotusNotesHREFs()
CodigosNotes = CodigosLotusNotes()
if __name__ == "__main__":
	Lt = LotusNotesHREFs()
	if ( Lt.carregado):
		Lt.imprimirBancos()
		Lt.imprimirLinks()
		Lt.imprimirIDs()
		print(Lt.links)
	CodigosNotes.imprimirCodigos()
	CodigosNotes.imprimirIDs()
