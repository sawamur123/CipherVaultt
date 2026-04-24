# CipherVault - Gerenciador de Senhas Criptografado

O **CipherVault** é uma aplicação de linha de comando (CLI) desenvolvida em Python, focada no gerenciamento seguro de credenciais. O projeto utiliza criptografia para garantir que o usuário seja o único com acesso aos seus dados.

## Detalhes do Projeto
* **Segurança Total:** Nem o desenvolvedor nem administradores podem acessar suas senhas.
* **Criptografia Simétrica:** Utiliza a biblioteca `cryptography` (Fernet) com chaves de 128 bits.
* **Hashing:** A senha-mestra nunca é salva. Apenas o seu rastro (SHA-256) é armazenado para validação.
* **Interface Estilizada:** Ótima experiência de usuário com tabelas e cores via biblioteca `Rich`.
* **Gerador de Senhas:** Algoritmo baseado na biblioteca `secrets`, garantindo senhas de alta variabilidade.

## Bibliotecas Utilizadas
* **Python 3.11**
* **Cryptography (Fernet):** Para cifragem dos dados.
* **Hashlib:** Para proteção da senha-mestra.
* **Rich:** Para a interface visual no terminal.
* **Secrets:** Para geração de números aleatórios seguros.

## Arquivos
O CipherVault utiliza uma estrutura modular para ter facilidade de manutenção:
* `main.py`: Ponto de entrada da aplicação e onde a interação acontece.
* `core.py`: Focado na lógica contendo todas as funções de criptografia e interface.
* `config.json`: Armazena o hash da senha-mestra.
* `chave.key`: Chave física necessária para descriptografar o cofre.
* `vault.crypt`: O cofre criptografado (ilegível sem a chave).

## Como Instalar
Este guia assume que você já tem o Python 3.10 ou superior instalado.
* **1. Preparos:** Abra o Terminal de acordo com seu sistema operacional e cole: pip install cryptography rich
* **2. Baixar:** Existem duas formas de obter os arquivos: Via Git: git clone https://github.com/sawamur123/CipherVaultt.git e via ZIP: Clique no botão verde "Code" no GitHub e selecione "Download ZIP". Extraia os arquivos em uma pasta.
* **3. Roda:** Clique no arquivo "main" da sua pasta já extraida e com o botão direito selecione "Abrir com o Terminal", então digite o código "python main.py" para iniciar.
