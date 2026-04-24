#Definições iniciais
import json
import hashlib
from cryptography.fernet import Fernet
import os
import secrets
import string
import getpass
import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from core import *
console = Console()
logado = False
n_tentativas = 4
chave_mestra = '0'
tentativa = '0'
nome_gerenciador = "CipherVault"
opcao = "0"

BANNER = """
  ____ _       _               __     __            _ _   
 / ___(_)_ __ | |__   ___ _ __ \ \   / /_ _ _   _ _| |_ |_ 
| |   | | '_ \| '_ \ / _ \ '__| \ \ / / _` | | | | | __| __|
| |___| | |_) | | | |  __/ |     \ V / (_| | |_| | | |_| |_ 
 \____|_| .__/|_| |_|\___|_|      \_/ \__,_|\__,_|_|\__|\__|
        |_|                                                 
"""
console.print(f"[bold blue]{BANNER}[/bold blue]")

#Início do programa
garantir_chave()
cofre = carregar_dados_criptografados()

#Tenta carregar uma senha já cadastrada
chave_mestra_hash = carregar_configuracao()

#Abertura
console.print(f'Bem vindo ao [bold blue]{nome_gerenciador}![/bold blue]')

#Se não encontrou nenhuma senha salva, faz o cadastro
if chave_mestra_hash is None:
    print('Parece que é sua primeira vez por aqui.')
    senha_cadastro = console.input('Cadastre sua [bold blue]Chave-Mestra[/bold blue]: ').strip()
    chave_mestra_hash = gerar_hash(senha_cadastro)
    salvar_configuracao(chave_mestra_hash) #Salva para a próxima vez
    console.print('[green]Senha mestra cadastrada com sucesso![/green]')

try:
    #Sistema de login (requer logado == false)
    while not logado:
        console.print("[bold blue]Insira sua Chave-Mestra para logar[/bold blue] [yellow](invisível):[/yellow]", end=" ")
        tentativa = getpass.getpass("").strip()
        #Gera o rastro do que o usuário acabou de digitar
        tentativa_hash = gerar_hash(tentativa)
        #Compara o rastro da tentativa com o rastro guardado no cadastro
        if gerar_hash(tentativa) == chave_mestra_hash:
            logado = True
            console.print('[green]Cofre aberto![/green]')
        else:
            n_tentativas -= 1
            console.print(f'[red]Erro! Tentativas restantes: {n_tentativas}[/red]')
            if n_tentativas <= 0: break
            time.sleep(2) #Pausa de 2 segundos para previnir robôs

    #Menu principal (entra se estiver logado)
    while logado:
        mostrar_menu()
        opcao = input('Escolha uma opção: ')

        if opcao == "1": #Adiciona senhas
            limpar_tela()
            nome_do_item = salvar_senha(cofre)
            console.print(f'[green][OK][/green][blue] {nome_do_item}[/blue] adicionado ao cofre!')
            salvar_dados_criptografados(cofre) #Salva logo em seguida para não perder nada
   
        elif opcao == "2": #Mostra as senhas salvas
            limpar_tela()
            console.print(Panel('[green]--- Suas senhas salvas ---[/green]', border_style="green"))
            listar_senhas(cofre)

        elif opcao == "3": #Deleta senhas
            limpar_tela()
        if deletar_senha(cofre):
            salvar_dados_criptografados(cofre) #Só salva se deletou algo

        elif opcao == "4": #Redefinir senha-mestra
            limpar_tela()
            #Atualiza a variável do hash com o retorno da função
            chave_mestra_hash = redefinir_senha_mestra(chave_mestra_hash)

        elif opcao == "5": #Fecha o meu programa honesto
            limpar_tela()
            salvar_dados_criptografados(cofre)
            del cofre #Apaga os dados da memória RAM
            console.print("[bold blue]Cofre trancado... Até logo![/bold blue]")
            break
except KeyboardInterrupt:
    console.print("\n[bold yellow]Interrupção detectada. Fechando o cofre com segurança...[/bold yellow]")
    salvar_dados_criptografados(cofre)
