from django import forms
from .models import Profile, File


class ProfileForm(forms.ModelForm):
    passAT = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Palavra Passe AT',
            'class': 'w-full py-4 px-6 rounded-xl',
            'type': 'password'  # Define o tipo do campo como senha
        }),
        required=False
    )

    passSS = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Palavra Passe SS',
            'class': 'w-full py-4 px-6 rounded-xl',
            'type': 'password'  # Define o tipo do campo como senha
        }),
        required=False
    )

    class Meta:
        model = Profile
        fields = ('company_name', 'personal_name', 'phone_number', 'nif', 'passAT', 'niss', 'passSS')
        widgets = {
            'company_name': forms.TextInput(attrs={
                'placeholder': 'Nome Empresa',
                'class': 'w-full py-4 px-6 rounded-xl'
            }),
            'personal_name': forms.TextInput(attrs={
                'placeholder': 'Nome Pessoal',
                'class': 'w-full py-4 px-6 rounded-xl'
            }),
            'phone_number': forms.TextInput(attrs={
                'placeholder': 'Telefone',
                'class': 'w-full py-4 px-6 rounded-xl'
            }),
            'nif': forms.TextInput(attrs={
                'placeholder': 'NIF',
                'class': 'w-full py-4 px-6 rounded-xl'
            }),
            'niss': forms.TextInput(attrs={
                'placeholder': 'NISS',
                'class': 'w-full py-4 px-6 rounded-xl'
            }),
        }

    def save(self, commit=True):
        profile = super().save(commit=False)
        passAT = self.cleaned_data.get('passAT')
        passSS = self.cleaned_data.get('passSS')
        if passAT:
            profile.set_passAT(passAT)
        if passSS:
            profile.set_passSS(passSS)
        if commit:
            profile.save()
        return profile

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('name', 'description', 'file')
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Nome do Ficheiro',
                'class': 'w-full py-4 px-6 rounded-xl'
            }),
            'description': forms.TextInput(attrs={
                'placeholder': 'Nome Pessoal',
                'class': 'w-full py-4 px-6 rounded-xl'
            }),
            'file': forms.FileInput(attrs={
                'placeholder': 'Ficheiro',
                'class': 'w-full py-4 px-6 rounded-xl'
            })
        }