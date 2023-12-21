from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
import re
from utils.validate_cpf import valida_cpf

# Create your models here.
#TODO: Create separeted model for multiple adresses
#TODO: Add verbose name to all models
#TODO: ADD PHONE NUMBER
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuário')
    birth_date = models.DateField(verbose_name='Data de nascimento')
    cpf = models.CharField(max_length=11, verbose_name='CPF')
    address = models.CharField(max_length=50, verbose_name='Endereço')
    number = models.CharField(max_length=5, verbose_name='Número')
    address_line2 = models.CharField(max_length=30, verbose_name='Complemento')
    neighborhood = models.CharField(max_length=30, verbose_name='Bairro')
    zipcode = models.CharField(max_length=8, verbose_name='CEP')
    city = models.CharField(max_length=30, verbose_name='Cidade')
    state = models.CharField(
        max_length=2,
        default='SP',
        verbose_name='Estado',
        choices = (
            ('AC', 'Acre'),
            ('AL', 'Alagoas'),
            ('AP', 'Amapá'),
            ('AM', 'Amazonas'),
            ('BA', 'Bahia'),
            ('CE', 'Ceará'),
            ('DF', 'Distrito Federal'),
            ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'),
            ('MA', 'Maranhão'),
            ('MT', 'Mato Grosso'),
            ('MS', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'),
            ('PA', 'Pará'),
            ('PB', 'Paraíba'),
            ('PR', 'Paraná'),
            ('PE', 'Pernambuco'),
            ('PI', 'Piauí'),
            ('RJ', 'Rio de Janeiro'),
            ('RN', 'Rio Grande do Norte'),
            ('RS', 'Rio Grande do Sul'),
            ('RO', 'Rondônia'),
            ('RR', 'Roraima'),
            ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'),
            ('SE', 'Sergipe'),
            ('TO', 'Tocantins'),
        )
    )

    def __str__(self):
        return f'{self.user}'
    
    def clean(self):
        error_messages = {}

        user_cpf = self.cpf or None
        saved_cpf = None
        profile = Profile.objects.filter(cpf=user_cpf).first()

        if profile:
            saved_cpf = profile.cpf

            if saved_cpf is not None and self.pk != profile.pk:
                error_messages['cpf'] = 'Este CPF já está cadastrado.'

        if not valida_cpf(self.cpf):
            error_messages['cpf'] = 'Digite um CPF válido.'

        if re.search(r'[^0-9]', self.zipcode) or len(self.zipcode) != 8:
            error_messages['zipcode'] = 'CEP inválido. Digite os 8 digitos do CEP.'

        if error_messages:
            raise ValidationError(error_messages)