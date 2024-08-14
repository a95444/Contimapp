from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
import os

def get_key():
    key = os.getenv('SECRET_KEY')
    if key is None:
        raise ValueError("A chave de criptografia não está definida!")
    return key.encode()

class Profile(models.Model):
    user = models.OneToOneField(User,  on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    personal_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    nif = models.CharField(max_length=20, blank=True, null=True)
    encrypted_passAT = models.BinaryField(blank=True, null=True)
    niss = models.CharField(max_length=20, blank=True, null=True)
    encrypted_passSS = models.BinaryField(blank=True, null=True)

    def set_passAT(self, raw_passAT):
        f = Fernet(get_key())
        self.encrypted_passAT = f.encrypt(raw_passAT.encode())

    def get_passAT(self):
        try:
            f = Fernet(get_key())
            return f.decrypt(self.encrypted_passAT).decode()
        except:
            return("")
        
    def set_passSS(self, raw_passSS):
        f = Fernet(get_key())
        self.encrypted_passSS = f.encrypt(raw_passSS.encode())

    def get_passSS(self):
        try:
            f = Fernet(get_key())
            return f.decrypt(self.encrypted_passSS).decode()
        except:
            return("")


    def __str__(self):
        return self.user.username


def user_files_path(instance, filename):
    user_folder = f'files_user{instance.created_by.id}'
    return os.path.join(user_folder, filename)


class File(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)  # permite que a variável esteja vazia
    file = models.FileField(upload_to=user_files_path, blank=True, null=True)  # pasta onde se vão guardar os arquivos
    created_by = models.ForeignKey(User, related_name='files', on_delete=models.CASCADE)  # associa o arquivo ao usuário que o criou
    created_at = models.DateTimeField(auto_now_add=True)  # data e hora de criação do arquivo

    class Meta:
        ordering = ('-created_at',)  # ordena os arquivos por data de criação, do mais recente ao mais antigo

    def __str__(self):
        return self.name
    