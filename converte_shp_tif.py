from Tkinter import *
import ogr, gdal
import os.path

class Application:
	def __init__(self, master=None):
		self.fontePadrao = ("Arial", "10")
		self.primeiroContainer = Frame(master)
		self.primeiroContainer["pady"] = 10
		self.primeiroContainer.pack()

		self.segundoContainer = Frame(master)
		self.segundoContainer["padx"] = 20
		self.segundoContainer.pack()

		self.terceiroContainer = Frame(master)
		self.terceiroContainer["padx"] = 20
		self.terceiroContainer.pack()

		self.quartoContainer = Frame(master)
		self.quartoContainer["pady"] = 20
		self.quartoContainer.pack()

		self.titulo = Label(self.primeiroContainer, text="Conversor de .shp pra .tif")
		self.titulo["font"] = ("Arial", "10", "bold")
		self.titulo.pack()

		self.nomeLabel = Label(self.segundoContainer,text="Nome do arquivo (sem ext .shp)", font=self.fontePadrao)
		self.nomeLabel.pack(side=LEFT)

		self.nome = Entry(self.segundoContainer)
		self.nome["width"] = 30
		self.nome["font"] = self.fontePadrao
		self.nome.pack(side=LEFT)

		self.tam_pixelLabel = Label(self.terceiroContainer, text="Tamanho do pixel (ex: 1)", font=self.fontePadrao)
		self.tam_pixelLabel.pack(side=LEFT)

		self.tam_pixel = Entry(self.terceiroContainer)
		self.tam_pixel["width"] = 30
		self.tam_pixel["font"] = self.fontePadrao

		self.tam_pixel.pack(side=LEFT)

		self.autenticar = Button(self.quartoContainer)
		self.autenticar["text"] = "Converter"
		self.autenticar["font"] = ("Calibri", "8")
		self.autenticar["width"] = 12
		self.autenticar["command"] = self.verificaDados
		self.autenticar.pack()

		self.mensagem = Label(self.quartoContainer, text="", font=self.fontePadrao)
		self.mensagem.pack()

	#Metodo verificar senha
	def verificaDados(self):
		nome_arq_shp = self.nome.get()
		tam_pixel = self.tam_pixel.get()
		
		#Verifica se o nome do arquivo existe
		dirlist = os.listdir(".")
		for i in dirlist:
			filename = os.path.abspath(i)
			if((filename.find("Entrada")) != -1):
				break;		
				
		nome_arquivo_temp = filename + filename[2] + nome_arq_shp + ".shp"
		
		try:
			with open(nome_arquivo_temp, 'r') as f:
				#Salva os dados em um arquivo temporario
				dirlist = os.listdir(".")
				for i in dirlist:
					filename = os.path.abspath(i)
					if((filename.find("Temp")) != -1):
						break

				nome_arq = filename + filename[2] + "temp.txt"
				arq = open(nome_arq, 'w')
				texto = []
				texto.append(nome_arq_shp)
				texto.append('\n')
				texto.append(tam_pixel)
				arq.writelines(texto)
				arq.close()

				#Fecha a tela
				root.destroy()
		except IOError:
			self.mensagem["text"] = "Arquivo nao existe"	

#Roda aplicacao
root = Tk()
Application(root)
root.mainloop()
			
# -------------------------------- RASTERIZE --------------------------------
def Funcao_Rasterize(outputFile, inputFile, tam_pixel, nome_arq):
	sql = "select field_4, * from " + nome_arq
	rasterizeOptions = gdal.RasterizeOptions(options=[],
		format = 'Gtiff',
		creationOptions = None,
		noData = 0,
		initValues = None, 
		outputBounds = None, 
		outputSRS = None,
		width = None, 
		height = None, 
		xRes= tam_pixel, 
		yRes= tam_pixel, 
		targetAlignedPixels = False,
		bands = None,
		inverse = False,
		allTouched = True,
		burnValues = None, 
		attribute = 'field_4', 
		useZ = False, 
		layers = None,
		SQLStatement=sql, 
		SQLDialect = None, 
		where = None, 
		callback = None, 
		callback_data = None)

	gdal.Rasterize(outputFile, inputFile, options=rasterizeOptions)
	
def Percorre_dir_entrada():
	achou = 0
	dirlist = os.listdir(".")
	for i in dirlist:
		filename = os.path.abspath(i)
		if((filename.find("Entrada")) != -1):
			achou = 1
			return filename
	if(achou == 0):
		return 0
		
def Percorre_dir_saida():
	achou = 0
	dirlist = os.listdir(".")
	for i in dirlist:
		filename = os.path.abspath(i)
		if((filename.find("Saida")) != -1):
			achou = 1
			return filename
	if(achou == 0):
		return 0
		
def le_nome_arq():
	dirlist = os.listdir(".")
	for i in dirlist:
		filename = os.path.abspath(i)
		if((filename.find("Temp")) != -1):
			break
	nome_arq = filename + filename[2] + "temp.txt"
	
	arq = open(nome_arq, 'r')
	texto = arq.readlines()
	inicial = 0
	for linha in texto :
		if (inicial == 0): 
			return linha
		else :
			inicial += 1
	arq.close()
			
def le_tam_pixel():
	dirlist = os.listdir(".")
	for i in dirlist:
		filename = os.path.abspath(i)
		if((filename.find("Temp")) != -1):
			break
	nome_arq = filename + filename[2] + "temp.txt"
	
	arq = open(nome_arq, 'r')
	texto = arq.readlines()
	inicial = 0
	for linha in texto :
		if (inicial == 1): 
			return linha
		else :
			inicial += 1
	arq.close()
		
# ----------- Le o arquivo temp
nome_arq = le_nome_arq()
tam_pixel = le_tam_pixel()

temp = "\n"

# Retira o \n quando le os dados do temp
for i in range(0,len(temp)):
	nome_arq = nome_arq.replace(temp[i],"")

for i in range(0,len(temp)):
	tam_pixel = tam_pixel.replace(temp[i],"")

# ----------- Trata diretorio IO
diretorioEntrada = Percorre_dir_entrada()
if(diretorioEntrada == 0): 
	print("erro")
	
diretorioSaida = Percorre_dir_saida()
if(diretorioSaida == 0): 
	print("erro")

inputFile = diretorioEntrada + diretorioEntrada[2] + nome_arq + ".shp"
outputFile = diretorioSaida + diretorioSaida[2] + nome_arq + ".tif"
	
# ----------- Chama rasterize
Funcao_Rasterize(outputFile, inputFile, tam_pixel, nome_arq)

# -------------------------------- Se rodou, abre tela --------------------------------
class Application2:
	def __init__(self, master=None):
		self.widget1 = Frame(master)
		self.widget1.pack()
		self.msg = Label(self.widget1, text="Conversao realizada")
		self.msg["font"] = ("Verdana", "10", "italic", "bold")
		self.msg.pack ()
		self.sair = Button(self.widget1)
		self.sair["text"] = "Sair"
		self.sair["font"] = ("Calibri", "10")
		self.sair["width"] = 5
		self.sair["command"] = self.widget1.quit
		self.sair.pack ()

#Se feita a conversao
#Verifica se o nome do arquivo existe
dirlist = os.listdir(".")
for i in dirlist:
	filename = os.path.abspath(i)
	if((filename.find("Temp")) != -1):
		break;		
		
nome_arquivo_temp = filename + filename[2] + "temp.txt"

try:
	with open(nome_arquivo_temp, 'r') as f:
		root2 = Tk()
		Application2(root2)
		root2.mainloop()

except IOError:	
	print("Conversao nao realizada")

os.remove(nome_arquivo_temp)