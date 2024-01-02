import pdfplumber
import os

def ler_nome_do_arquivo(caminho_arquivo):
    with pdfplumber.open(caminho_arquivo) as pdf:
        primeira_pagina = pdf.pages[0]
        texto = primeira_pagina.extract_text()
        nome = extrair_nome_do_texto(texto)
        return nome

def extrair_nome_do_texto(texto):
    indice_inicio_nome = texto.find("Nome:")
    indice_fim_nome = texto.find("Data de admissão:")
    
    if indice_inicio_nome != -1 and indice_fim_nome != -1:
        nome_completo = texto[indice_inicio_nome + len("Nome:"):indice_fim_nome].strip()
        nome_a_atualizar = nome_completo.split(':', 1)[-1].strip()  # Pega a parte do nome que precisa ser atualizado
        return nome_a_atualizar
    else:
        return "Nome não encontrado no arquivo."

def salvar_arquivo_com_nome_original(caminho_arquivo, pasta_destino, nome_atualizado):
    nome_do_arquivo, extensao = os.path.splitext(os.path.basename(caminho_arquivo))
    nome_do_arquivo = nome_do_arquivo.replace(":", "_")  # Substitui ":" por "_"
    novo_caminho_arquivo = os.path.join(pasta_destino, f"{nome_atualizado}{extensao}")
    
    with open(novo_caminho_arquivo, 'wb') as novo_arquivo:
        with open(caminho_arquivo, 'rb') as arquivo_original:
            novo_arquivo.write(arquivo_original.read())

def processar_pasta(origem, destino):
    for arquivo in os.listdir(origem):
        caminho_arquivo = os.path.join(origem, arquivo)
        if os.path.isfile(caminho_arquivo) and caminho_arquivo.lower().endswith('.pdf'):
            nome_atualizado = ler_nome_do_arquivo(caminho_arquivo)
            salvar_arquivo_com_nome_original(caminho_arquivo, destino, nome_atualizado)

pasta_origem = input("Diretório dos arquivos de origem: ")
pasta_destino = input("Diretório dos arquivos de destino: ")

processar_pasta(pasta_origem, pasta_destino)