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
