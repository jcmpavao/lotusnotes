import requests
import sys
reload(sys)
sys.setdefaultencoding('utf8')
#import sys, codecs
#sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
import os
from bs4 import BeautifulSoup
import time

def carregarViews():
 	v = []
	v.append("http://alerjln1.alerj.rj.gov.br/ordemdia.nsf/OrdemInt?OpenForm&Start=1&Count=1000")
	v.append("http://alerjln1.alerj.rj.gov.br/ordemdia.nsf/OrdemInt?OpenForm&Start=6.4.12&Count=1000")
	v.append("http://alerjln1.alerj.rj.gov.br/ordemdia.nsf/OrdemInt?OpenForm&Start=12.10.12&Count=1000")
	v.append("http://alerjln1.alerj.rj.gov.br/ordemdia.nsf/OrdemInt?OpenForm&Start=19.7.6&Count=1000")
	v.append("http://alerjln1.alerj.rj.gov.br/ordemdia.nsf/OrdemInt?OpenForm&Start=24.1.2&Count=1000")
	return v
def salvarArquivo(soup, tag,arquivoP,post):
	try:
		print("salvando em arquivo")
		arquivo = open(arquivoP,"a")
		i = 0
		fim = len(list(soup.find_all(tag)))
		for elem in soup.find_all(tag):
			linha = ""
			colunas = len(list(elem.select('td')))
			td = elem.select('td')
			#print(type(td))
			if len(td) == 7:
				dataOrd = ""
				horaOrd = ""
				link = ""
				tipo = ""
				try:
					if (td[2].a != None):
						if (td[2].a.string !=  None ):
							dataOrd = td[2].a.string.extract()
						link = td[2].a['href']
					if (td[3].font != None):
						horaOrd = td[3].font.string.extract()
					if (td[5].font != None):
						tipo = td[5].font.string.extract().decode("utf-8")
					linha = dataOrd + ";" + horaOrd + ";" + tipo + ";" + link
					if ( i < fim):
						linha = linha + "\r\n"
					arquivo.write(linha)
				except:
					print("erro na linha " + str(i) + " do post " + str(post) + " lei " + str(dataOrd) + " ano " + str(horaOrd))
					print(sys.exc_info())
			i += 1
		print("Total de elementos encontrados: " + str(i))
		arquivo.close()
	except:
		print(sys.exc_info())

def percorrerElementosTable(soup,arquivo,contador):
	linhas = list()
	for table in soup.find_all("table"):
		if (( len(list(table.children)))  > 3 ): #somente as tabelas com mais de 3 elementos
			salvarArquivo(table,"tr",arquivo,contador)

def salvarPost(post):
		arquivo = open("listaPosts.txt","a")
		arquivo.writelines(post)
		arquivo.close

def postsRecursivos(url,arquivo):
	contador = 1
	view = carregarViews()
	for url in view:
		print("post numero " + str(contador) + " url: " + url)
		result =  requests.get(url)
		soup = BeautifulSoup(result.content,'lxml')
		percorrerElementosTable(soup,arquivo,contador)
		table = printResumo(soup)
		#inicio = (qtdRegistros * contador) - dec
		contador += 1
		#dec += 1
		#urlPost = url + "&Start=" + str(inicio) + "&Count=" + str(qtdRegistros)
		time.sleep(9)
		#if ( len(list(table.find_all('tr'))) < qtdRegistros):
		#	final = True
	print("FIM")
def postUnico(url,arquivo):
	qtdRegistros = 1000
	inicio = 1
	final = False
	contador = 1
	dec = 0
	urlPost = url + "&Start=" + str(inicio) + "&Count=" + str(qtdRegistros)
	#while ( not (final)):
	print("post numero " + str(contador) + " url: " + urlPost)
	result =  requests.get(urlPost)
	soup = BeautifulSoup(result.content.decode('utf-8','ignore'),'lxml')
	percorrerElementosTable(soup,arquivo,1)
	table = printResumo(soup)
	#	inicio = (qtdRegistros * contador) - dec
	#	contador += 1
	#	dec += 1
	#	urlPost = url + "&Start=" + str(inicio) + "&Count=" + str(qtdRegistros)
	#	time.sleep(8)
	#	if ( len(list(table.find_all('tr'))) < qtdRegistros):
	#		final = True

def encontrarTabPrincipal(soup):
        for table in soup.find_all("table"):
                if (( len(list(table.children)))  > 3 ): #somente as tabelas com mais de 3 elementos
                        return table


def printResumo(soup):
	print("Total de elementos do Body: " + str(len(list(soup.body.descendants))))
	if ( len(list(soup.table)) > 0 ):
		if ( soup.table.children != None):
			print("Table filhos: " + str(len(list(soup.table.children))))
		table = encontrarTabPrincipal(soup)
		print("Linhas da table: " + str(len(list(table.find_all('tr')))))
		if (soup.table.descendants != None):
			print("Table descendentes " + str(len(list(soup.table.descendants))))
	else:
		table = None
	return table


def main2():
	print("capturando conteudo ")
	#postUnico("http://alerjln1.alerj.rj.gov.br/CONTLEI.NSF/LeiOrdInt?OpenForm","contlei.data")    
	postsRecursivos("http://alerjln1.alerj.rj.gov.br/ordemdia.nsf/OrdemInt?OpenForm","ordemdia.data")
def main1():
	print("capturando conteudo ")
	postUnico("http://alerjln1.alerj.rj.gov.br/ordemdia.nsf/OrdemInt?OpenForm","ordemdia.data")   

if __name__ == '__main__':
	tipo = sys.argv[1]
	print(tipo)
	#main(processo,URL_BUSCA)
	#main(processo)
	if ( int(tipo) == 1):
		main1()
	else:
		main2()
#main()
#testeRetirar()
#teste()
