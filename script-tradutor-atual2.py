import re
import os
from pathlib import Path
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

a = input("Insira a pasta inteira com os arquivos que deverão ser traduzidos")
path = Path(a);
sub_path = os.listdir(path)
options = Options() #segundo plano
options.headless = True #oculto
options.add_argument('--headless')
options.add_argument('--disable-gpu')
browser = webdriver.Chrome(options=options, executable_path=r'C:\Users\Scarlxrd2112\AppData\Local\Programs\Python\Python38-32\chromedriver.exe')


def escrevaLegendas(arquivo_legendas,caminho_arquivo_escrever):
        legendas = open(caminho_arquivo_escrever,"w", -1, "utf-8")
        for x in range(len(arquivo_legendas)):
            arquivo_legendas[x] = arquivo_legendas[x].strip()
            if re.search('^(?!.*\d+:\d+\.\d+\s+-->\s\d+:\d+\.\d+).*$',arquivo_legendas[x]):
                if arquivo_legendas[x]:
                    legendas.write(original[x]+"\n")
        legendas.close()

def enviarTextoNavegador(browser,caminho_arquivo_enviar):
    browser.get("https://translate.google.com.br/#view=home&op=docs&sl=en&tl=pt")
    browser.find_element_by_id("tlid-file-input").send_keys(caminho_arquivo_enviar)

def getTraducaoNavegador(browser,options):
    element = browser.find_element_by_css_selector(".tlid-translate-doc-button.button")
    browser.execute_script("arguments[0].click();", element)
    resposta = browser.find_element_by_css_selector("body").text
    resposta = resposta.split("\n")
    return resposta

def removeArquivo(caminho):
    os.remove(caminho)

def gerarArquivoLegendaTraduzido(arquivo_legendas,caminho_arquivo_final):
    cont = 0
    arquivo_final = open(caminho_arquivo_final,"w", -1, "utf-8")
    for x in range(len(arquivo_legendas)):
        if re.search('^(?!.*\d+:\d+\.\d+\s+-->\s\d+:\d+\.\d+).*$',arquivo_legendas[x]):
            if arquivo_legendas[x]:
                arquivo_final.write(resposta[cont]+"\n" + "\n")
                cont+=1
        else:
            arquivo_final.write(arquivo_legendas[x] + "\n")


for name_sub_path in sub_path:
    diretorio = str(path)+"\\"+str(name_sub_path)
    if os.path.isdir(diretorio):
        for file in Path(diretorio).glob('*.vtt'):
            try:
                original = open(str(file),'r',encoding="utf-8")
                original = original.readlines()
            except:
                print("Este arquivo há algum erro na sua codificação da legenda")
                continue
            caminho_txt = diretorio + "\\" + file.name + "_temp.txt"  
                
            escrevaLegendas(original, caminho_txt)
                
            enviarTextoNavegador(browser,caminho_txt)
                
            resposta = getTraducaoNavegador(browser,options)
                
            removeArquivo(caminho_txt)
                
            caminho_arquivo_final = diretorio + "\\" + file.name + "_legendado"

            gerarArquivoLegendaTraduzido(original, caminho_arquivo_final)  
    elif diretorio.endswith(".vtt"):
        try:
            original = open(str(diretorio),'r',encoding="utf-8")
            original = original.readlines()
        except:
            print("Este arquivo há algum erro na sua codificação da legenda")
            continue
        caminho_txt = str(path) + "\\" + str(name_sub_path) + "_temp.txt"
        escrevaLegendas(original, caminho_txt)
            
        enviarTextoNavegador(browser,caminho_txt)
            
        resposta = getTraducaoNavegador(browser,options)
            
        removeArquivo(caminho_txt)
            
        caminho_arquivo_final = str(path) + "\\" + str(name_sub_path) + "_legendado"
            
        
        try:
            gerarArquivoLegendaTraduzido(original, caminho_arquivo_final)
        except:
            print("Este arquivo há algum erro na sua codificação da legenda")
            continue
        
 

