import requests
import sys
#reload(sys)
#sys.setdefaultencoding('utf8')

import os
from bs4 import BeautifulSoup
import time
import base64
from LotusNotes import LotusNotes , CodigosNotes , LeisNotes

URL_BUSCA = "http://www3.alerj.rj.gov.br/lotus_notes/consultaNotes.asp?hdfid=11&txtquery="
URL_BUSCA_GERAL = "http://www3.alerj.rj.gov.br/lotus_notes/consultaNotes.asp?"
URL_WWW3 = "http://www3.alerj.rj.gov.br/lotus_notes/default.asp?id=<ID>&URL="
URL_RAIZ_NOTES = "http://alerjln1.alerj.rj.gov.br"

class TramitacaoNotes:
	def __init__(self, texto = " ", data_publicacao = " " , link_notes = " " , link_www3 = " "):
		self.texto = texto
		self.data_publicacao = data_publicacao
		self.link_notes = link_notes
		self.link_www3 = link_www3

class ProjetoNotes:
	""" Point class for representing and manipulating x,y coordinates. """
	def __init__(self,id = " " , autor = " ",ementa=" ", link_notes=" ", link_www3=" ",data_abertura=" ",comissoes=" "):
		""" Create a new point at the origin """
		self.id = id
		self.autor = autor
		self.ementa =  ementa
		self.link_notes = link_notes
		self.link_www3 = link_www3
		self.data_abertura = data_abertura
		self.comissoes = comissoes
		self.tramitacoes = []

class LeiNotes:
	""" Point class for representing and manipulating x,y coordinates. """
	def __init__(self,id = " " , autoria = " ",ementa=" ", link_notes=" ", link_www3=" ",data_publicacao=" ",ano=" ", status="---"):
		""" Create a new point at the origin """
		self.id = id
		self.autoria = autoria
		self.ementa =  ementa
		self.link_notes = link_notes
		self.link_www3 = link_www3
		self.data_publicacao = data_publicacao
		self.ano = ano
		self.status = status

def listarTramitacoes(soupTR):
	tramit = []
	for tr in soupTR:
		tramit.append(str(tr))
	print(tr)

def pesquisarProcesso(projeto, soup, idW3):
	retorno = ""
	projeto = ProjetoNotes(projeto)
	tramitacoes = []
	tramits = []
	try:
		print("processando")
		i = 0
		fim = len(list(soup.find_all('tr')))
		#link = ""
		#listarTramitacoes(soup.find_all('tr'))
		for elem in soup.find_all('tr'):
			linha = ""
			colunas = len(list(elem.select('td')))
			#print(colunas)
			td = elem.select('td')
			alt1 = ""
			alt2 = ""
			alt3 = ""
			seta_vermelha = ""
			seta_azul = ""
			link = ""
			dataLei = ""
			autorLei = ""
			comissoes = ""
			tipo = "T"
			status = ""
			ementa = ""
			#print(type(td))
			if len(td) > 0:
				if ( td[3].img != None):
					#alt1 = td[3].img.alt
					#if (alt1 == "Two documents Icon"):
					#print("lei")
					tipo = "L"
					status = "lei"
				if ( td[4].img != None):
					#alt2 = td[4].img.alt
					#if ( alt2 == "Red right arrow Icon"):
					#print("raiz")
					tipo = "R"
					status = "raiz"
					#comissoes = td[9].font.string.extract().encode("utf-8")
				if ( td[5].img != None):
					#print(td[5].img.alt)
					#if (alt3 == "Blue right arrow Icon"):
					#print("tramitacao")
					tipo = "T"
					status = "tramitacao"
				if (td[6].a != None):
					if (td[6].a.string !=  None ):
						#id = td[6].a.href
						link = td[6].a['href']
				#if (td[6].font != None):
						ementa = td[6].a.string.extract() #.encode("utf-8")
					else:
						link = td[6].a['href'] #.string.extract()
						del td[6].a['href']
						del td[6].a['target']
						ementa = str(td[6].a) #.encode('utf-8')  #str(td[6].a).replace('<a>'," ").replace("</a>", " " )
				else:
					ementa = "x"
				if (td[7].font != None):
					dataLei = td[7].font.string.extract() #.encode("utf-8")
				if(td[8].font != None):
					autorLei = td[8].font.string.extract() #.encode("utf-8")
				if (td[9].font != None):
					comissoes = td[9].font.string.extract() #.encode("utf-8")
				#print(link)
				#	del td[4].font['face']
				#	autorLei = td[4].font.string.extract()
				#print("antes da linha")
				#linha = tipo + ";" + status + ";" +  link + ";" + ";" + str(dataLei)+ ";" + autorLei + ";" + comissoes.encode('utf-8',errors="ignore")
				#print(linha.encode("utf-8",errors="ignore"))
			i += 1
			if (status == "raiz"):
				#print(buscaLei(link))
				print("raiz")
				linkwww3 = link #link[31:]
				#print(linkwww3)
				www3 = convertBase64(linkwww3,idW3)
				print(www3)
				#retorno = link + ";" + www3 + ";" + ementa +  ";" + dataLei + ";"  + autorLei + ";" + comissoes
				urlP = URL_RAIZ_NOTES+link
				projeto = ProjetoNotes(projeto,autorLei,ementa,urlP,www3,dataLei,comissoes)
				#print("attrib")
				tram = TramitacaoNotes(ementa, dataLei,urlP ,www3)
				tramits.append(tram)
				tramitacoes.append([URL_RAIZ_NOTES+link,www3,ementa,dataLei])
			else:
				print("tram " + str(dataLei))
				linkTram = link #link[31:]
				www3T = convertBase64(linkTram,idW3)
				#print("attrib")
				urlP = URL_RAIZ_NOTES+link
				tram = TramitacaoNotes(ementa, dataLei,urlP,www3T)
				tramits.append(tram)
				tramitacoes.append([urlP,www3T,ementa,dataLei])
		#print("Total de elementos encontrados: " + str(i))
	except:
		print(sys.exc_info())
	projeto.tramitacoes = tramits #tramitacoes
	#texto = tramits[0].texto
	#print(texto)
	#print(projeto.tramitacoes)
	#return  retorno
	#print(projeto.ementa)
	#print(tramits[0].texto)
	return projeto

def pesquisarLei(leiano, soup, idW3):
	print("entrou na pesquisa " + str(leiano))
	retorno = ""
	lei = LeiNotes(leiano)
	try:
		i = 0
		fim = len(list(soup.find_all('tr')))
		#if ( fim > 1):
		#	print("achou " + str(fim) + " linhas")
		for elem in soup.find_all('tr'):
			linha = ""
			colunas = len(list(elem.select('td')))
			td = elem.select('td')
			idLei = ""
			link = ""
			dataLei = ""
			autoriaLei = ""
			ano = ""
			ementa = ""
			#print(type(td))
			if len(td) > 0:
				if (td[2].a != None):
					if (td[2].a.string !=  None ):
						idLei = td[2].a.string.extract()
						link = td[2].a['href']
				if (td[3].font != None):
					ano = td[3].font.string.extract() #.encode("utf-8")
				#print("ano " + str(ano) + " lei " + str(idLei))
				anoL, leiL = leiano.split("&")[1] , leiano.split("&")[0]
				try:
					anoI = int(ano)
					leiI = int(idLei)
				except:
					ano, idLei = -1,-1
				if (( int(anoL) == int(ano)) and ( int(leiL) == int(idLei) ) ):
					if (td[4].font != None):
						dataLei = td[4].font.string.extract() #.encode("utf-8")
					if (td[5].font != None):
						if (td[5].font.string != None): 
							ementa = td[5].font.string.extract() #.encode("utf-8")
						else: 
							ementa = td[5].font.get_text() #.encode("utf-8")
					if (td[6].font != None):
						autoriaLei = td[6].font.string.extract() #.encode("utf-8")
					#	del td[4].font['face']
					#	autorLei = td[4].font.string.extract()
					linha = idLei + ";" + link + ";" + ";" + str(dataLei)+ ";" + str(autoriaLei) + ";" + str(ementa)  #ementa.encode('utf-8',errors="ignore")
					#print(linha.encode("utf-8",errors="ignore"))
					i += 1
					linkwww3 = link #link[31:]
					#print("fim da arttrri")
					#print(linkwww3)
					www3 = convertBase64(linkwww3,idW3)
					#print(linkwww3)
					#retorno = idLei + ";" + link + ";" + www3 + ";" + str(ementa) +  ";" + dataLei + ";"  + str(autoriaLei) + ";" + ano
					lei = LeiNotes(idLei,autoriaLei,ementa,URL_RAIZ_NOTES+link,www3,dataLei,ano)
					break
            #print("Total de elementos encontrados: " + str(i))
	except:
		print(sys.exc_info())
	return lei

def buscaLei(lei,url=" ",idW3 = 0 ):
	global URL_BUSCA
	if (url == " "):
		url = URL_BUSCA+lei
	else:
		url = url + lei
	print("vai buscar em " + url)
	result = requests.get(url)
	src = result.content
	soup = BeautifulSoup(src, 'lxml')
	if ( soup.body.select('table') != None):
		#print(soup.table)
		lei = pesquisarLei(lei,soup,idW3)
		#return processo + ";" + pesquisar(soup)
		return lei
	else:
		return "nenhum registro encontrado"

	#return soup.body

def buscaProcesso(processo,url=" ", idW3 = 0):
	#print("capturando conteudo")
	#result = requests.get("http://alerjln1.alerj.rj.gov.br/scpro1923.nsf/Internet/LeiInt?OpenForm")
	global URL_BUSCA
	if (url == " "):
		url = URL_BUSCA+processo
	else:
		url = url + processo
	print("vai executar requests em " + url)
	result = requests.get(url)
	#result = requests.get("http://alerjln1.alerj.rj.gov.br/ordemdia.nsf/OrdemInt?OpenForm")
	src = result.content
	soup = BeautifulSoup(src,"lxml") # "'html.parser')
	#print(soup.body)
	if ( soup.body.select('table') != None):
		#print(soup.table)
		projeto = pesquisarProcesso(processo,soup,idW3)
		#return processo + ";" + pesquisar(soup)
		return projeto
	else:
		return "nenhum registro encontrado"

def convertBase64(url, idW3):
	global URL_WWW3
	#print("base 64")
	param = base64.b64encode(url.encode('utf-8')).decode('utf8')
	encoded = URL_WWW3.replace("<ID>",str(idW3)) +  param
	return encoded

def buscaGeralPorCodigo(projeto):
	retorno = ProjetoNotes()
	print (projeto + " len" + str(len(projeto)))
	if ( len(projeto) >= 8 ):
		if ( len(projeto) == 11):
			ano, tema,proj_lei = int(projeto[:4]),projeto[4:6],projeto[6:]
		elif ( len(projeto) == 9):
			ano, tema, proj_lei = int(projeto[:2]) ,projeto[2:4],projeto[4:]
			if ( ano in [1,2,3]):
				ano = 2000 + ano
			else:
				ano = 1900 + ano
			ano = int(ano)
		#ano, tema,proj_lei = int(projeto[:4]),projeto[4:6],projeto[6:]
		url = ""
		leg = 0
		idWww3 = 0
		urlBusca = ""
		if ( tema in CodigosNotes.codigos):
			print("Assunto da busca: " + CodigosNotes.codigos[tema])
			print("Numero: " + proj_lei + " do ano " + str(ano))
			#print(CodigosNotes.codigos[tema])
			#LotusNotes.imprimirLinks()
			#LotusNotes.imprimirBancos()
			#projetos de Lei, definir qual o banco$
			lt = LotusNotes.obterLinkIdPorAno(ano)
			print(lt["link"])            
			url = URL_BUSCA_GERAL  + "hdfid=" + lt["id"]
			leg = lt["leg"]
			idWww3 = lt["idWWW"]
			urlBusca = lt["link"]
		else:
			print("tema " + tema + "invalido")
		if(url != ""):
			print("Busca inicial: " + urlBusca)
			print("legis " + str(leg))
			#print(projeto)
			#Projeto = buscaProcesso(projeto,url+"&txtquery=",idWww3)
			Projeto = buscaProcesso(projeto,urlBusca,idWww3)
			#print(Projeto)
			if(Projeto.autor != " "):
				#print("prim")
				#print(len(Projeto.autor))
				#print(Projeto.ementa)
				retorno = Projeto
			else:
				#tentar na legislatura anterior e na proxima
				prim, ult = LotusNotes.primeiraUltimaLeg()["primeira"], LotusNotes.primeiraUltimaLeg()["ultima"]
				if ((int(leg) < ult) and (int(leg) > prim)):
					nlt = LotusNotes.obterLinkIdPorLeg(leg - 1) #anterior
					print("busca leg anterior")
					print(nlt["link"])            
					url = URL_BUSCA_GERAL  + "hdfid=" + str(nlt["id"])
					#leg = nlt["leg"]
					idWww3 = nlt["idWWW"]
					urlBusca = nlt["link"]
					Projeto = buscaProcesso(projeto,urlBusca,idWww3)
					if(Projeto.autor != " "):
						retorno = Projeto
					else:
						nlt = LotusNotes.obterLinkIdPorLeg(leg + 1) #posterior
						print("busca leg posterior")
						print(nlt["link"])            
						url = URL_BUSCA_GERAL  + "hdfid=" + str(nlt["id"])
						#leg = nlt["leg"]
						idWww3 = nlt["idWWW"]
						urlBusca = nlt["link"]
						Projeto = buscaProcesso(projeto,urlBusca,idWww3)
						if(Projeto.autor != " "):
							retorno = Projeto
				elif (int(leg) == ult):
					nlt = LotusNotes.obterLinkIdPorLeg(leg - 1) #anterior
					print("busca leg anterior")
					print(nlt["link"])            
					url = URL_BUSCA_GERAL  + "hdfid=" + str(nlt["id"])
					#leg = nlt["leg"]
					idWww3 = nlt["idWWW"]
					urlBusca = nlt["link"]
					Projeto = buscaProcesso(projeto,urlBusca,idWww3)
					if(Projeto.autor != " "):
						retorno = Projeto
				elif (int(leg) == prim ):
					nlt = LotusNotes.obterLinkIdPorLeg(leg + 1) #posterior
					print("busca leg posterior")
					print(nlt["link"])            
					url = URL_BUSCA_GERAL  + "hdfid=" + str(nlt["id"])
					#leg = nlt["leg"]
					idWww3 = nlt["idWWW"]
					urlBusca = nlt["link"]
					Projeto = buscaProcesso(projeto,urlBusca,idWww3)
					if(Projeto.autor != " "):
						retorno = Projeto
		else:
			print("banco nao encontrado")

	print(retorno.ementa)
	print(retorno.link_notes)
	print(retorno.link_www3)
	print(str(len(retorno.tramitacoes)))
	return retorno

def buscaGeralPorLei(lei):
	retorno = LeiNotes()
	if (len(lei) > 0):
		ano, id_lei = lei.split(";")[0],lei.split(";")[1]
		url = ""
		hdfid = 0
		if (LeisNotes.carregado):
			print("buscar no banco local")
			leiBanco = LeisNotes.localizarLeiPorAnoCodigo(ano,id_lei)
			print(leiBanco)
			if(leiBanco["ano"] > 0):
				print("achou local")
				ano = leiBanco["ano"]
				lei = leiBanco["lei"]
				urlNotes = URL_RAIZ_NOTES + leiBanco["url"]
				ementa = leiBanco["ementa"]
				autoria = leiBanco["autoria"]
				hdfid = LotusNotes.links["Legislacao"][0]
				w3Id = LotusNotes.links["Legislacao"][2]
				w3 = leiBanco["url"]
				st = leiBanco["status"]
				urlW3 = convertBase64(w3,w3Id)
				retorno = LeiNotes(lei,autoria,ementa, urlNotes, urlW3 ," ",ano,st)
			else:
				print("nao achou local")
				print("Assunto da busca: Legislacao")
				print("Numero: " + id_lei + " do ano " + str(ano))
				hdfid = LotusNotes.links["Legislacao"][0]
				url = LotusNotes.links["Legislacao"][1]
				w3Id = LotusNotes.links["Legislacao"][2]
				if(url != ""):
					#print(hdfid)
					print(url)
					#url = URL_BUSCA_GERAL + "hdfid=" + hdfid + "&txtquery="
					#url = url +  ano + "&" + id_lei
					Lei = buscaLei(id_lei+"&"+ano,url,w3Id)
					#print(Projeto)
					if(Lei.autoria != " "):
						#print("prim")
						#print(len(Lei.autoria))
						#print(Lei.ementa)
						retorno = Lei
		else:
			print("Assunto da busca: Legislacao")
			print("Numero: " + id_lei + " do ano " + str(ano))
			hdfid = LotusNotes.links["Legislacao"][0]
			url = LotusNotes.links["Legislacao"][1]
			w3Id = LotusNotes.links["Legislacao"][2]
			if(url != ""):
				#print(hdfid)
				print(url)
				#url = URL_BUSCA_GERAL + "hdfid=" + hdfid + "&txtquery="
				#url = url +  ano + "&" + id_lei
				Lei = buscaLei(id_lei+"&"+ano,url,w3Id)
				#print(Projeto)
				if(Lei.autoria != " "):
					#print("prim")
					#print(len(Lei.autoria))
					#print(Lei.ementa)
					retorno = Lei
			else:
				print("banco nao encontrado")

	print("ementa: " + retorno.ementa)
	print("autoria: " + retorno.autoria)
	print("link notes: " + retorno.link_notes)
	print("link www: " + retorno.link_www3)
	return retorno
	
def main(processo,url= " " ):
	processo = buscaProcesso(processo,url)
	#print(processo.autor)

#main(URL_BUSCA, "20190300835")

if __name__ == '__main__':
	processo = sys.argv[1]
	tipo = sys.argv[2]
	print(tipo)
	#main(processo,URL_BUSCA)
	#main(processo)
	if ( int(tipo) == 1):
		buscaGeralPorCodigo(processo)
	else:
		buscaGeralPorLei(processo)
#testeRetirar()
#teste()
