#Definiçôes iniciais 
import os
import json
import hashlib
import secrets
import string
import getpass
from cryptography.fernet import Fernet
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

#--Funções de segurança e configuração--

#Cria uma impressão digital SHA-256 única para a senha mestra
def gerar_hash(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

#Verifica a existência da chave Fernet. Se não existir, gera uma nova para criptografia simétrica
def garantir_chave():
    if not os.path.exists("chave.key"):
        chave = Fernet.generate_key()
        with open("chave.key", "wb") as arquivo_chave:
            arquivo_chave.write(chave)
        console.print("[green]>> Nova chave de criptografia gerada![/green]")

#Lê a chave física do arquivo para ser usada nas operações de cifra
def carregar_chave():
    return open("chave.key", "rb").read()

#Mantém o hash da senha mestra em um arquivo JSON para validação futura
def salvar_configuracao(hash_mestre):
    config = {"master_hash": hash_mestre}
    with open("config.json", "w") as arquivo:
        json.dump(config, arquivo)

#Recupera o hash da senha mestra do disco. Retorna None se o arquivo não existir
def carregar_configuracao():
    if os.path.exists("config.json"):
        # Verifica se o arquivo não está vazio (tamanho > 0)
        if os.path.getsize("config.json") > 0:
            try:
                with open("config.json", "r") as arquivo:
                    config = json.load(arquivo)
                    return config.get("master_hash")
            except json.JSONDecodeError:
                # Se o JSON estiver malformado, retorna None para recadastrar
                return None
        with open("config.json", "r") as arquivo:
            config = json.load(arquivo)
            return config.get("master_hash")
    return None

#Gera e salva uma chave (faz isso UMA vez)
def gerar_chave():
    chave = Fernet.generate_key()
    with open("chave.key", "wb") as arquivo_chave:
        arquivo_chave.write(chave)

#--Funções de dados--

#Criptografa o dicionário de senhas e o salva como um arquivo binário ilegível
def salvar_dados_criptografados(dicionario_cofre):
    #Transforma o dicionário em uma string JSON
    dados_json = json.dumps(dicionario_cofre)
    #Transformar a string em bytes para o Fernet funcionar
    dados_bytes = dados_json.encode()
    #Criptografa
    f = Fernet(carregar_chave())
    dados_trancados = f.encrypt(dados_bytes)
    #Salva os bytes criptografados no arquivo
    #Usa "wb" (Write Binary) porque não é mais texto comum
    with open("vault.crypt", "wb") as arquivo:
        arquivo.write(dados_trancados)
    console.print("[green]>> Arquivo criptografado com sucesso![/green]")

#Lê o arquivo binário, descriptografa os bytes e reconstrói o dicionário de senhas
def carregar_dados_criptografados():
    if not os.path.exists("vault.crypt"):
        return {}
    try:
        #Lê os bytes trancados do arquivo
        with open("vault.crypt", "rb") as arquivo:
            dados_trancados = arquivo.read()
        #Descriptografa
        f = Fernet(carregar_chave())
        dados_bytes = f.decrypt(dados_trancados)
        #Transforma bytes de volta em dicionário
        return json.loads(dados_bytes.decode())
    except Exception as e:
        console.print(f'[red]Erro crítico: Não foi possível descriptografar o cofre. Chave inválida ou arquivo corrompido.[/red]')
        return {}

#--Funções de interface e lógica--

#Gera uma senha aleatória com bastante aleatoriedade usando a biblioteca secrets
def gerar_senha_forte(tamanho=16):
    #Define os "ingredientes": letras, números e símbolos
    caracteres = string.ascii_letters + string.digits + string.punctuation
    #Escolhe caracteres aleatórios e junta numa string
    senha = ''.join(secrets.choice(caracteres) for i in range(tamanho))
    return senha

#Interface para adicionar um novo serviço ao dicionário. Tem geração automática de senha
def salvar_senha(dicionario_cofre):
    console.print(Panel('[cyan] --- Adicionar nova senha ---[/cyan]', border_style="cyan"))
    servico = str(input('Serviço: ')).strip()
    usuario = str(input('Usuário: ')).strip()
    escolha = input('Deseja (1) Digitar a senha ou (2) Gerar uma senha forte? ')
    if escolha == "2":
        senha = gerar_senha_forte()
        print(f'Sua senha gerada é: {senha}')
    else:
        senha = input('Digite a senha: ').strip()
    #Adiciona o serviço, usuário e senha ao cofre. ex: cofre["Netflix"] = {"usuario": "...", "senha": "..."}
    dicionario_cofre[servico] = {"usuario": usuario, "senha": senha}
    return servico

#Apresenta uma tabela formatada com todos os serviços, usuários e senhas descriptografados
def listar_senhas(dicionario_cofre):
   if not dicionario_cofre:
       console.print("[yellow]O cofre está vazio.[/yellow]")
       return
   
   tabela = Table(title="Senhas Armazenadas", title_style="bold cyan", border_style="blue")
   tabela.add_column("Serviço", style="magenta")
   tabela.add_column("Usuário", style="green")
   tabela.add_column("Senha", style="red")

   for servico, info in dicionario_cofre.items():
        tabela.add_row(servico, info['usuario'], info['senha'])

   console.print(tabela)

#Remove uma entrada específica do dicionário de senhas baseado no nome do serviço
def deletar_senha(dicionario_cofre):
    console.print(Panel('[bold red] --- Deletar uma senha ---[/bold red]', border_style="bold red"))
    servico = console.input('Qual [blue]serviço[/blue] deseja [red]remover?[/red] ').strip()
    #O .pop tenta remover. Se não achar, ele retorna o segundo valor (None)
    removido = dicionario_cofre.pop(servico, None)
    if removido:
        console.print(f'[green][!][/green] [blue]{servico}[/blue] foi [red]removido[/red] com sucesso.')
        return True #Indica que houve alteração para salvar o arquivo
    else:
        console.print(f'[red][Erro][/red] Serviço [blue]"{servico}"[/blue] não encontrado no cofre.')
        return False

#Permite ao usuário alterar a senha mestra, validando a senha antiga antes de gerar o novo hash
def redefinir_senha_mestra(hash_atual):
    console.print(Panel("[bold yellow]Redefinição de Senha-Mestra[/bold yellow]", border_style="yellow"))
    #Verifica a senha atual
    console.print("Digite sua senha [bold red]ATUAL[/bold red]:", end=" ")
    senha_atual = getpass.getpass("")
    if gerar_hash(senha_atual) != hash_atual:
        console.print("[red]Erro: Senha atual incorreta. Operação cancelada.[/red]")
        return hash_atual #Retorna o hash antigo sem mudar nada
    #Pede a nova senha
    console.print("Digite sua [bold green]NOVA[/bold green] senha:", end=" ")
    nova_senha = getpass.getpass("")
    console.print("Confirme a [bold green]NOVA[/bold green] senha:", end=" ")
    confirma_senha = getpass.getpass("")
    # Valida e salva
    if nova_senha == confirma_senha:
        if len(nova_senha) < 4: #Uma validação extra
            console.print("[red]Erro: A senha deve ter pelo menos 4 caracteres.[/red]")
            return hash_atual
        novo_hash = gerar_hash(nova_senha)
        salvar_configuracao(novo_hash)
        console.print("[bold green]✓ Senha-Mestra alterada com sucesso![/bold green]")
        return novo_hash
    else:
        console.print("[red]Erro: As senhas novas não coincidem.[/red]")
        return hash_atual
    
#Exibe o painel visual de opções do sistema
def mostrar_menu():
    menu_texto = (
        "[bold cyan]1.[/bold cyan] Adicionar novas senhas\n"
        "[bold cyan]2.[/bold cyan] Listar todos os serviços\n"
        "[bold cyan]3.[/bold cyan] Deletar uma senha\n"
        "[bold cyan]4.[/bold cyan] Redefinir Senha-Mestra\n"
        "[bold cyan]5.[/bold cyan] Sair"
    )
    console.print(Panel(menu_texto, title="[bold white]Menu CipherVault[/bold white]", border_style="blue"))

#Limpa o histórico do terminal de acordo com o sistema operacional (Windows ou Unix)
def limpar_tela():
    # 'cls' para Windows, 'clear' para Linux/Mac
    os.system('cls' if os.name == 'nt' else 'clear')
