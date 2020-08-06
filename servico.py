import os
import shutil
from random import randint
from flask import Flask, render_template,request,send_from_directory, jsonify
from flask_cors import CORS
import sys, time
import threading
from threading import Thread
#import comtypes.client
from buscaDadosProjetoNotes import buscaProcesso, buscaGeralPorCodigo,buscaGeralPorLei, ProjetoNotes
from OrdemDia import OrdemDia
#possiveis status do processamento
listaStatus = [{ "id" : 0 , "mensagem" : "Erro" } , { "id" : 1 , "mensagem" : "Aguardando" } ,
{ "id" : 2 , "mensagem" : "Em Processamento" }, { "id" : 3 , "mensagem" : "Finalizado" } ]


class StatusProcessamento():
#Classe que controla o andamento do processamento
#
#
	def __init__(self, listastatus):
		self.listastatus = listastatus
		self.alterarStatus(1)

	def limparArquivos(self):
		self.arquivo_recebido = ""
		self.arquivos_processados = []

	def alterarStatus(self,id,mensagem=""):
		self.status = self.listastatus[id]["id"]
		if(mensagem !=""):
			self.mensagem = mensagem
		else:
			self.mensagem = self.listastatus[id]["mensagem"]
		if(self.status == 1):
			self.limparArquivos()

	def copiarRenomear(self,copia=False):
		self.arquivos_processados.append(self.arquivo_recebido[0:11]+"R"+self.arquivo_recebido[12:])
		self.arquivos_processados.append(self.arquivo_recebido[0:11]+"R1"+self.arquivo_recebido[12:])
		try:
			if( copia):
				#print(self.asDictionary())
				for arq in self.arquivos_processados:
					shutil.copy(r"upload/"+self.arquivo_recebido,r"upload/"+arq)
		except:
			erro = str(sys.exc_info())
			#print(erro)
			self.alterarStatus(0,erro)
			#print(self.asDictionary())
		#return novo

	def asDictionary(self):
		return { "status" : self.status , "mensagem" : self.mensagem , "arquivo_recebido" : self.arquivo_recebido , "arquivo_processado" : self.arquivos_processados}

	def gerarPDF(self):
		retorno = False
		try:
			in_file = "upload/" + self.arquivos_processados[0]
			out_file = "upload/" + self.arquivos_processados[0][:12]+".pdf"
			#convert(in_file, out_file)
			retorno = True
		except:
			print(str(sys.exc_info()))
		return retorno

class ProcessaReq(Thread):
	global STATUS
	def __init__ (self):
		Thread.__init__(self)
		self.status = ""
	def run(self):
		print("inicio")
		#STATUS.copiarRenomear()
		STATUS.alterarStatus(2)
		time.sleep(20)
		STATUS.alterarStatus(3)
		threading.Thread(target=alterarStatus, args=(STATUS,1)).start()
		print("fim")
#Thrd = ProcessaReq(STATUS)

class ProcessamentoDoc(Thread):
	def __init__ (self):
		Thread.__init__(self)
	def run(self):
		global STATUS
		print("inicio")
		STATUS.alterarStatus(2)
		time.sleep(20)
		STATUS.copiarRenomear(True)
		STATUS.gerarPDF()
		STATUS.alterarStatus(3)
		print("fim")

STATUS = StatusProcessamento(listaStatus)

def alterarStatus(STATUS,id):
	time.sleep(5)
	STATUS.alterarStatus(id)

def liberar():
	global Thrd
	Thrd = None

def copiaRenomeia(arquivo):
	ext = arquivo.split(".")[1]
	novo = str(randint(1000,9999))+"."+ext
	shutil.copy(r"upload/"+arquivo,r"upload/"+novo)
	print(novo)
	return novo

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
CORS(app)

@app.route("/")
def status():
	global STATUS
	return jsonify(STATUS.asDictionary())

@app.route("/status")
def index():
	global STATUS
	return jsonify(STATUS.asDictionary())

@app.route("/uploadTeste")
def on_upload():
	global STATUS
	retorno = ""
	if (STATUS.status == 1):
		STATUS.alterarStatus(2)
		Thrd = ProcessaReq()
		Thrd.start()
		retorno = STATUS.asDictionary()
	else:
		retorno = { "status" : 0 , "mensagem" : "Ja existe um JOB em andamento"}
	return jsonify(retorno)

@app.route('/up')
def post_file():
	return render_template('upload.html')

@app.route("/download/<arquivo>")
def on_Download(arquivo):
	global STATUS
	if(STATUS.status == 3):
		#if ( arquivo != ""):
		#	ARQUIVO = arquivo
		#else:
		if arquivo in STATUS.arquivos_processados:
			ARQUIVO = arquivo
			#STATUS.alterarStatus(1)
			#threading.Thread(target=alterarStatus, args=(STATUS,1)).start()
			return send_from_directory("upload/",ARQUIVO, as_attachment=True)
		else:
			return jsonify({"status":0, "mensagem" : "Arquivo "+ arquivo + " nao encontrado no servidor"})
	else:
		return jsonify(STATUS.asDictionary())
	#return "{\"status\":\"" + STATUS + "\"}"

@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
	global STATUS
	retorno = " "
	try:
		if request.method == 'POST':
			if ( STATUS.status == 1):
				f = request.files['file']
				if( f.filename.split('.')[1] not in [ "doc","DOC","docx","DOCX"]):
					raise ValueError("Extensao de arquivo invalida")
				if( len(f.filename[:12]) != 12):
					raise ValueError("Padrao de nome de arquivo invalido")			
				else:
					palavra = f.filename.upper()
					if(palavra[0:5]!= "PAUTA"):
						raise ValueError("Erro no nome do arquivo: Pauta")
					elif(palavra[11:12] != "E"):
						raise ValueError("Caracter invalido")
					else:
						try:
							num = int(palavra[5:11])
						except:
							raise ValueError("Numero " + palavra[5:11] + " invalido")
					f.save("upload/"+f.filename)
					STATUS.arquivo_recebido = f.filename
					STATUS.alterarStatus(2)
					Thrd = ProcessamentoDoc()
					Thrd.start()
					retorno = STATUS.asDictionary()
			else:
				retorno = { "status" : 0 , "mensagem" : "Ja existe um JOB em andamento"}
		else:
			retorno = STATUS.asDictionary()
	except:
		mensagem = str(sys.exc_info())
		STATUS.status = 0
		STATUS.mensagem = mensagem
		print(mensagem)
		retorno = STATUS.asDictionary()
	return jsonify(retorno)

@app.route('/limpar')
def clear():
	global STATUS
	STATUS.alterarStatus(1)
	return jsonify(STATUS.asDictionary())
@app.route('/finalizar')
def finalizar():
	global STATUS
	STATUS.alterarStatus(1)
	return jsonify(STATUS.asDictionary())

@app.route('/projeto/<id>')
def getProjeto(id):
	#projeto = buscaProcesso(id)
	projeto = buscaGeralPorCodigo(id)
	#imprimir o autor
	#print(projeto.autor)
	#imprimir a ementa
	saida = "<h3>Projeto de Lei</h3></br>"
	#ementa = projeto.ementa.decode("utf-8")
	#print(ementa)
	#print(ementa.encode('iso8859-1'))
	#print(type(projeto.ementa))
	saida = saida + "ementa:     " + projeto.ementa + "<br>" #.decode('utf-8') + "<br>"
	saida = saida + "autor:      " + projeto.autor + "<br>" #.decode('utf-8') + "<br>"
	saida = saida + "comissoes:  " + projeto.comissoes + "<br>" # ".decode('utf-8') + "<br>"
	saida = saida + "link notes: " + projeto.link_notes + "<br>"
	saida = saida + "link www3:  " + projeto.link_www3 + "<br>"
	saida = saida + "<br><br><h3>Tramitacoes</h3><hr>"
	#for t in projeto.tramitacoes:
	#	#texto = t[2]
	#	#data = t[3]
	#	#print(texto.decode('utf-8'))
	#	#print(type(texto))
	for tram in projeto.tramitacoes:
		saida = saida + "data:       " + tram.data_publicacao + "<br>"  #+ str(t[3]) + "<br>"
		saida = saida + "texto:      " + tram.texto + "<br>" #+ str(t[2]) + "<br>"
		saida = saida + "link notes: " + tram.link_notes + "<br>" #+ t[0] + "<br>"
		saida = saida + "link www3:  " + tram.link_www3 + "<br>" #+ t[1] + "<br>"
		saida = saida + "<hr>"
	return saida

@app.route('/lei/<id>')
def getLei(id):
	lei = buscaGeralPorLei(id)
	saida = "<h3>Lei</h3></br>"
	saida = saida + "Lei:          " + str(lei.id) + "<br>" + " ano " + str(lei.ano) + "<br>"
	saida = saida + "ementa:       " + lei.ementa + "<br>"
	saida = saida + "autoria:      " + lei.autoria + "<br>"
	saida = saida + "status:      " + lei.status + "<br>"
	saida = saida + "link notes: " + lei.link_notes + "<br>"
	saida = saida + "link www3:  " + lei.link_www3 + "<br>"
	return saida

@app.route('/ordemdia/<anomesdia>')
def listarOrdem(anomesdia):
	retorno = ""
	try:
		if (len(anomesdia.split(";")) > 2):
			ord = OrdemDia.localizarOrdemPorData(anomesdia)
		else:
			ano = anomesdia.split(";")[0]
			mes = anomesdia.split(";")[1]
			ord = OrdemDia.listarOrdemPorAnoMes(ano,mes)
		retorno = str(ord)
	except:
		retorno = str(sys.exc_info())
	return retorno
	
@app.route('/ordemdiasessoes/<anomesdiasessao>')
def listarSessao(anomesdiasessao):
	retorno = ""
	try:
		print(anomesdiasessao)
		if (len(anomesdiasessao.split(";")) > 3):
			sessao = int(anomesdiasessao.split(";")[3])
			data = anomesdiasessao.split(";")[0] + ";" + anomesdiasessao.split(";")[1] + ";" + anomesdiasessao.split(";")[2]
			#print(data)
			ord = OrdemDia.localizarOrdemPorData(data)
			#print(ord)
			if (ord != None):
				total = ord["total"]
				url = ord["sessao"][total - sessao]["link"]
				print(url)
				retorno = OrdemDia.obterConteudoSessao(url)               
		else:
			retorno = ""
	except:
		retorno = str(sys.exc_info())
	return retorno
	
if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)
