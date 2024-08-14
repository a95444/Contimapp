from cryptography.fernet import Fernet

# Gere a chave
key = Fernet.generate_key()

# Armazene a chave em um arquivo chamado 'secret.key'
with open("secret.key", "wb") as key_file:
    key_file.write(key)
