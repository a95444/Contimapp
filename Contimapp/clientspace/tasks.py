# clientspace/tasks.pyuser_files
from celery import shared_task
from .models import Profile, File
from .utils import webDriverAT, renameFile, init_chrome, webDriverSS
from django.conf import settings
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import ProfileForm, FileForm
from pathlib import Path
from django.http import JsonResponse
from celery.result import AsyncResult


@shared_task
def task_AT(user_id, certidao):
    from django.contrib.auth.models import User
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"Starting download_certidao_task for user_id: {user_id}")

    try:
        user = User.objects.get(id=user_id)
        profile = Profile.objects.get(user=user)
        NIF = str(profile.nif)
        PASS = profile.get_passAT() # método python
        print('A PASS É: ' + PASS)
        download_dir = os.path.join(settings.MEDIA_ROOT, f'files_user{user_id}')

        try:
            name =  str(profile.personal_name)
            print("NAME: "+ name)
            print(type(name))
        except:
            name=""
        finally:
            username=str(user.username)
            logger.info(f"Downloading certificate for NIF: {NIF}")
            driver= init_chrome(download_dir)
            transferResult = webDriverAT(certidao, NIF, PASS, driver, download_dir)
            print("TRANSFERRESULT: "+ str(transferResult))

            if(transferResult=='success'):
                file_path = renameFile(download_dir, name, username,certidao)

                if file_path:
                    #print("entrei no file_path")
                    file = File(
                        name=os.path.basename(file_path),
                        file=os.path.join(f'files_user{user_id}', os.path.basename(file_path)),
                        created_by=user
                    )
                    file.save()
                    logger.info(f"File saved: {file_path}")
                else:
                    logger.error("No file was downloaded or renamed.")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

    return (transferResult)

@shared_task
def task_SS(user_id, certidao):
    from django.contrib.auth.models import User
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"Starting download_certidao_task for user_id: {user_id}")

    try:
        user = User.objects.get(id=user_id)
        profile = Profile.objects.get(user=user)
        NISS = str(profile.niss)
        PASS = profile.get_passSS() # método python
        print('A PASS É: ' + PASS)
        download_dir = os.path.join(settings.MEDIA_ROOT, f'files_user{user_id}')

        try:
            name =  str(profile.personal_name)
            print("NAME: "+ name)
            print(type(name))
        except:
            name=""
        finally:
            username=str(user.username)
            logger.info(f"Downloading certificate for NIF: {NISS}")
            driver= init_chrome(download_dir)
            transferResult = webDriverSS(certidao, NISS, PASS, driver, download_dir)
            print("TRANSFERRESULT: "+ str(transferResult))

            if(transferResult=='success'):
                file_path = renameFile(download_dir, name, username,certidao)

                if file_path:
                    #print("entrei no file_path")
                    file = File(
                        name=os.path.basename(file_path),
                        file=os.path.join(f'files_user{user_id}', os.path.basename(file_path)),
                        created_by=user
                    )
                    file.save()
                    logger.info(f"File saved: {file_path}")
                else:
                    logger.error("No file was downloaded or renamed.")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

    return (transferResult)

@shared_task
def test_task():
    print("Test task executed")