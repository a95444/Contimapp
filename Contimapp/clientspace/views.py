from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import ProfileForm, FileForm
from .models import Profile, File
from .utils import webDriverAT, renameFile  # Importando as funções
import os
from pathlib import Path
from django.http import JsonResponse
from .tasks import task_AT, task_SS
from celery.result import AsyncResult


@login_required
def clientspace(request):
    template_path = os.path.join(settings.BASE_DIR, 'Contimapp', 'clientspace', 'templates', 'clientspace', 'home.html')
    profile = Profile.objects.get(user=request.user)
    files = File.objects.filter(created_by=request.user)

    try:
        # Recuperar o estado da tarefa da sessão
        task_state = request.session.pop('task_state', None)
    finally:
        if os.path.exists(template_path):
            print("Template found:", template_path)
        else:
            print("Template not found:", template_path)
        return render(request, 'clientspace/home.html', {
            'profile': profile,
            'files': files,
            'task_state': task_state,
        })

@login_required
def update_profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            passwordAT = form.cleaned_data.get('passAT')
            passwordSS = form.cleaned_data.get('passSS')
            print(f"Senha fornecida: {passwordAT}")
            print(f"Senha fornecida: {passwordSS}")
            # Supondo que você tem um modelo com um método `set_passAT` para guardar a senha
            profile.set_passAT(passwordAT)
            profile.set_passSS(passwordSS)
            profile.save()
            form.save()
            return redirect(reverse('clientspace:clientspace'))
    else:
        initial_data = {
            'company_name': profile.company_name,
            'personal_name': profile.personal_name,
            'phone_number': profile.phone_number,
            'nif': profile.nif,
            'passAT': profile.get_passAT() if profile.encrypted_passAT else '',
            'niss': profile.niss,
            'passSS': profile.get_passSS() if profile.encrypted_passSS else '',
        }
        form = ProfileForm(initial=initial_data, instance=profile)
    return render(request, 'clientspace/update_profile.html', {'form': form})


@login_required
def upload_file(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.created_by = request.user
            file.save()
            return redirect(reverse('clientspace:clientspace'))
    else:
        form = FileForm()
    return render(request, 'clientspace/upload_file.html', {'form': form})

@login_required
def view_AT(request, certidao):
    # Chama a tarefa e obtém o resultado
    print(" A CERTIDÃO É: ", certidao)
    task_result = task_AT(request.user.id, certidao)
    
    # Armazena o resultado da tarefa na sessão
    request.session['task_result'] = task_result
    
    # Redireciona para a página inicial ou para onde for necessário
    return redirect(reverse('clientspace:clientspace'))

@login_required
def view_SS(request, certidao):
    # Chama a tarefa e obtém o resultado
    print(" A CERTIDÃOSS É: ", certidao)
    task_result = task_SS(request.user.id, certidao)
    
    # Armazena o resultado da tarefa na sessão
    request.session['task_result'] = task_result
    
    # Redireciona para a página inicial ou para onde for necessário
    return redirect(reverse('clientspace:clientspace'))

@login_required
def clear_task_result(request):
    if request.method == 'POST':
        if 'task_result' in request.session:
            del request.session['task_result']
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def delete_file(request, file_id):
    # Obtém o arquivo do banco de dados
    file = get_object_or_404(File, id=file_id)
    
    # Exclui o arquivo do sistema de arquivos, se necessário
    if file.file:
        file.file.delete(save=False)  # Exclui o arquivo físico

    # Exclui o arquivo do banco de dados
    file.delete()

    # Redireciona para a página que lista os arquivos
    return redirect(reverse('clientspace:clientspace'))

@login_required
def modaltest(request):
    return render(request, 'clientspace/modaltest.html')