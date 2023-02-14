from bs4 import BeautifulSoup

import pytube # library for downloading YouTube videos
import pandas as pd
import numpy as np
import csv
import os
import random

def is_download(link, FILE_NAME):
    index = int(link.split("&index=")[1])
    df = pd.read_csv(FILE_NAME)
    
    return df["Status"][index-1] == True
        
def ordenar_links(lista):
    
    dicc = {}
    list_index = []
    sort_list = []

    
    for item in lista:
        index = item.split("&index=")[1]    #I'm left with only the index
        list_index.append(int(index))
        
    dicc = {key:value for key,value in zip(list_index,lista)}
    
    list_index=sorted(list_index)
    
    for index in list_index:
        sort_list.append(dicc[index])

    return sort_list

def asignar_nombre_archivo(nombre_con_csv):
    nombre = nombre_con_csv
    cant=0
    CURR_DIR = os.getcwd()
    aux = nombre.split(".")[0]
    fileName = CURR_DIR + "\\"+ nombre + ".csv"
    while(os.path.isfile(fileName)):
            cant+=1
            aux = nombre + "(" +str(cant)+ ")"
            fileName = CURR_DIR + "\\"+ aux +".csv"
    return aux+".csv"

def marcar_descargado(link, FILE_NAME):
    df = pd.read_csv(FILE_NAME)
    print(df)
    index = int(link.split("&index=")[1])
    df["Status"][index-1] = True
    df.to_csv(FILE_NAME, index = False)
             
#Guardo todos los links en un archivo csv

def para_descargar(lista, dir_arch_links, FILE_NAME):

    #FILE_NAME = asignar_nombre_archivo("archivo")          #Asigna el nombre nuevo al .csv

    with open(FILE_NAME, 'w', newline='') as csvfile:
        fieldnames = ['Links', 'Status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for link in lista:
            writer.writerow({'Links': link, 'Status': False})

def agregar_https(conjunto):
    links_download = []
    for item in conjunto:
         links_download.append("https://www.youtube.com"+item)
    return links_download

def get_links(soup):
    for link in soup.find_all('a'):
        dir = str(link.get('href')).strip()

        if ("/watch?v=" in dir and "=WL&index=" in dir and not(dir.endswith("s"))):
            lista.append(dir)
            
    conjunto = list(set(lista))
       
    print("##########################\n\n\n")

    return agregar_https(conjunto)

def existe(file):
    return os.path.isfile(file)

def get_links_of_csv(file):

    df = pd.read_csv(file)

    lista = df["Links"]
    
    return lista

#Read file with the list

dir_arch_links = "html2.txt"

FILE_NAME = dir_arch_links+"FILE_CSV.csv"

if not(existe(FILE_NAME)):

    arch = open(dir_arch_links, 'r', encoding='utf-8')

    soup = BeautifulSoup(arch.read(), 'html.parser')

    lista = []

    links_download = get_links(soup)

    arch.close()

    links_download = ordenar_links(links_download)

    para_descargar(links_download, dir_arch_links, FILE_NAME)  #Llena un archivo .csv con los links y si esta descargado o no

else:
    print("else")
    
    links_download = get_links_of_csv(FILE_NAME)
    
var = str(input("Deseas descargar todos los archivos? Y/N:\n"))

if (var == "y"):
    print("Comenzando descargas")

    for link in links_download:
        print("Link Nuevo, cargando\n")
        if not(is_download(link, FILE_NAME)):

            yt = pytube.YouTube(link)


          # The uploaded video will be of the best quality
            
            stream = yt.streams.get_by_resolution("360p")
        
            #stream = yt.streams.filter(progressive = True ,file_extension = 'mp4' , res = "360").order_by('resolution').desc().first()

            #stream = yt.streams.filter(progressive = True ,file_extension = 'mp4' ).order_by('resolution').desc().first() 
        
            try :
                
                print("Comenzando a descargar:" , yt.title,"\nTamaño: ",stream.filesize_mb)
                stream.download()


        # print uploaded links

                print ( "Downloaded:" , yt.title)

                marcar_descargado(link, FILE_NAME) #Marca el link como descargado en el .csv

            except Exception as e:

                print ( 'Some error in downloading:\n', link, " \n ",e)
        else:
            print(link+ " Ya esta descargado\n")
else:
    pass
