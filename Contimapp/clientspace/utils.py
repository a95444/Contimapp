from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import os
import random
from pathlib import Path
from tkinter import Tk, messagebox
import unicodedata
from datetime import datetime
import pdfkit
import uuid

def previousYear():
    year = datetime.now().year
    year -=1
    return year

def remove_spaces_and_accents(input_str):
    # Remover acentos
    if input_str=="":
        return ""
    else:
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        without_accents = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
        
        # Remover espaços
        without_spaces = without_accents.replace(" ", "")
        
        return without_spaces

def show_popup(message):
    root = Tk()
    root.withdraw()  # Esconde a janela principal do Tkinter
    messagebox.showerror("Erro", message)
    root.destroy()

def init_chrome(download_dir):
    # Ensure download_dir is a string
    download_dir = str(Path(download_dir).resolve())
    
    # Configurações do Selenium
    chrome_options = Options()

    # Adiciona a opção headless
    # print("Dentro do WebDriver")
    '''
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")  # Necessário para alguns sistemas
    chrome_options.add_argument("--window-size=1920,1080")  # Define o tamanho da janela
    '''
    chrome_prefs = {
        "download.default_directory": download_dir,  # Ensure this is a string
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True  # Força o download de PDFs
    }
    chrome_options.add_experimental_option("prefs", chrome_prefs)
    
    # Ensure the path is correct and converted to string
    service = Service(str(Path(__file__).resolve().parent.parent / 'drivers' / 'chromedriver-win64' / 'chromedriver.exe'))

    # Inicia o navegador
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver
    
def webDriverAT(certidao, NIF, PASS, driver, download_dir):
    
    try:
        # Acesse a página de login da AT
        driver.get('https://www.acesso.gov.pt/v2/loginForm?partID=PFAP&path=/geral/dashboard')

        # Aguarde até que o formulário de login esteja visível (ajuste o tempo se necessário)
        #time.sleep(5)  # Alternativamente, use WebDriverWait para esperar por um elemento específico

        # Preencha o formulário de login
        nif_label = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "//label[@for='tab2']")))
        nif_label.click()
        print("Dentro do NIF LABEL")
        # Aguarde até que os campos de login estejam visíveis
        WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, 'password-nif')))

        username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
        password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'password-nif')))
        submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'sbmtLogin')))

        # Preencha o formulário de login
        username_field.send_keys(NIF)  # Substitua com seu número de contribuinte
        password_field.send_keys(PASS)  # Substitua com sua senha
        submit_button.click()

        try:
            WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, 'cumprimento'))) #é o elemento onde aparece "Bom,dia ou boa tarde ..."
        except:
            return "error"
        
        if(certidao == 'divida'):
                # Aguarde até que a página de dashboard carregue (ajuste o tempo se necessário)
            driver.get('https://www.portaldasfinancas.gov.pt/pt/emissaoCertidaoForm.action')

            # Aguarde até que o elemento <select> esteja presente
            tipo_certidao_select = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'tipoCertidao')))

            # Use a classe Select do Selenium para interagir com o <select>
            select = Select(tipo_certidao_select)
            # Selecione a opção com o value "N" (Dívida e Não Dívida)
            select.select_by_value('N')

            confirm_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'confirmarBtn'))) 
            confirm_button.click()

            certid_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'certidaoBtn'))) 
            certid_button.click()
            
            time.sleep(1)
            return "success"
        
        if(certidao == 'liq_IRS'):
                # Aguarde até que a página de dashboard carregue (ajuste o tempo se necessário)
            driver.get('https://www.portaldasfinancas.gov.pt/pt/emissaoCertidaoForm.action')

            # Aguarde até que o elemento <select> esteja presente
            tipo_certidao_select = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'tipoCertidao')))

            # Use a classe Select do Selenium para interagir com o <select>
            select = Select(tipo_certidao_select)
            # Selecione a opção com o value "N" (Dívida e Não Dívida)
            year=previousYear()
            select.select_by_value('L')
            ano_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ano')))
            ano_input.clear()
            ano_input.send_keys(str(year))

            confirm_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'confirmarBtn'))) 
            confirm_button.click()

            try:
                elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'feedbackDisposition')))
                # Verifique se algum dos elementos contém o texto desejado
                text_to_find = "Não existe liquidação de IRS para a consulta efectuada."
                text_to_find2 = "Já existe uma certidão activa. Para obter segunda via utilize a consulta."
                found = any(text_to_find in element.text for element in elements)
                found2 = any(text_to_find2 in element.text for element in elements)
                if found:
                    print("O elemento com o texto desejado está presente na página.")
                    return("error_liq")
                    
                elif found2:
                    print("FOUND2")
                    driver.get("https://www.portaldasfinancas.gov.pt/pt/consultaCertidoes.action?tipoCertidao=&estado=&dataInicial=&dataFinal=&continuarButton=Continuar")
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'interaccoesTab')))
                    # Encontrar todas as linhas da tabela
                    rows = driver.find_elements(By.XPATH, '//*[@id="interaccoesTab"]/tbody/tr')                    
                    for row in rows:
                        tipo_certidao = row.find_elements(By.XPATH, './td[1]')[0].text
                        if "Liquidação de IRS" in tipo_certidao:
                            link = row.find_elements(By.XPATH, './td[5]/a')[0]
                            link.click()
                            time.sleep(2)
                            return "success"            
                else:
                    print("NÃO FUNCIONOU")
                    pass
            except:
                print("O elemento com a classe 'feedbackForbiddenFoto' não foi encontrado na página.")
                certid_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'obterBtn'))) 
                certid_button.click()
                
                time.sleep(1)
                return "success"
        
        if(certidao == 'comp_IRS'):
            # Selecione a opção com o value "N" (Dívida e Não Dívida)
            driver.get('https://irs.portaldasfinancas.gov.pt/comprovativo/obterComprovativoForm')
            try:
                elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'alert')))
                # Verifique se algum dos elementos contém o texto desejado
                text_to_find = "Não existem comprovativos."
                found = any(text_to_find in element.text for element in elements)
                if found:
                    print("O elemento com o texto desejado está presente na página.")
                    return("error_compIRS")
                else:
                    print("O elemento com o texto desejado não está presente na página.")
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'documentos')))
                    rows = driver.find_elements(By.XPATH, '//*[@id="documentos"]/tbody/tr')
                    for row in rows:
                        link = row.find_elements(By.XPATH, './td[4]/a')[0]
                        link.click()
                        time.sleep(2)
                        return "success"        
            except:
                return("error_uk")
            
        if(certidao == 'veiculos'):
            # Selecione a opção com o value "N" (Dívida e Não Dívida)
            driver.get('https://veiculos.portaldasfinancas.gov.pt/consulta/automoveis/consultar')
            try:
                elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.ID, 'tabela')))
                # Verifique se algum dos elementos contém o texto desejado
                text_to_find = "Não foram encontrados resultados"
                found = any(text_to_find in element.text for element in elements)
                if found:
                    print("O elemento com o texto desejado está presente na página.")
                    return("error_veiculos")
                else:
                    print("O elemento com o texto desejado não está presente na página.")
                    driver.implicitly_wait(4)
                    # Extrair a tabela
                    table_html = driver.find_element(By.CSS_SELECTOR, '#tabela').get_attribute('outerHTML')

                    # Salvar o HTML da tabela em um arquivo temporário
                    with open('tabela.html', 'w', encoding='utf-8') as file:
                        file.write('<html><head><meta charset="UTF-8"></head><body>')
                        file.write(table_html)
                        file.write('</body></html>')

                    # Configurar o caminho do executável do wkhtmltopdf
                    path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"

                    # Configurar o pdfkit para usar o wkhtmltopdf
                    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

                    # Caminho onde o PDF será salvo
                    pdf_path = os.path.join(download_dir, 'tabela.pdf')

                    # Converter o HTML para PDF e salvar no caminho especificado
                    pdfkit.from_file('tabela.html', pdf_path, configuration=config)
                    return('success')


            except:
                return("error_uk")
            
        if(certidao == 'comp_IES'):
            # Selecione a opção com o value "N" (Dívida e Não Dívida)
            driver.get('https://oa.portaldasfinancas.gov.pt/ies/consultarIES.action?anoDeclaracoes=2023')
            try:
                elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'panel-body')))
                # Verifique se algum dos elementos contém o texto desejado
                text_to_find = "Não existem declarações"
                found = any(text_to_find in element.text for element in elements)
                if found:
                    print("O elemento com o texto desejado está presente na página.")
                    return("error_compIES")
                else:
                    print("O elemento com o texto desejado não está presente na página.")
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'listaSituacaoVigente')))
                    #rows = driver.find_elements(By.XPATH, '//*[@id="listaSituacaoVigente"]/tbody/tr')
                    first_row = driver.find_element(By.CSS_SELECTOR, "#listaSituacaoVigente tbody tr:first-child")
                    button = first_row.find_element(By.CSS_SELECTOR, "button.btn.btn-default.btn-sm")
                    button.click()
                    time.sleep(2)
                    return "success"
            except:
                return("error_uk") 

    except Exception as e:
        show_popup(f"Ocorreu um erro: {e}")
        return "error"
    finally:
        driver.quit()
        
def webDriverSS(certidao, NISS, PASS_SS, driver, download_dir):
    
    try:
        driver.get('https://app.seg-social.pt/sso/login?service=https%3A%2F%2Fapp.seg-social.pt%2Fptss%2Fcaslogin#')

        username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
        password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
        submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'submitBtn')))

        username_field.send_keys(NISS)  
        password_field.send_keys(PASS_SS)  
        submit_button.click()
        
        try:
            WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, 'frawWelcome'))) #é o elemento onde aparece "Bom,dia ou boa tarde ..."
        except:
            return "error"
        
        if(certidao == 'TSU'):
                # Aguarde até que a página de dashboard carregue (ajuste o tempo se necessário)
            driver.get('https://app.seg-social.pt/ptss/ci/posicao-atual/posicao-atual?frawmenu=1&dswid=-1')
            time.sleep(2)
            driver.get('https://app.seg-social.pt/ptss/ci/documento-pagamento/pesquisar-doc-pagamento?dswid=-1')
            # Clique no link que expande a seção
            link_valores_pagar = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.ID, "linkValoresPagarcol"))
            )
            link_valores_pagar.click()
            '''
            # Espere até que a nova seção esteja visível
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "divAccordionPagar1"))
            )

            # Clique no link final dentro da seção expandida
            link_consultar_doc_pagp = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "form:accordion5:linkConsultarDocPagP"))
            )
            link_consultar_doc_pagp.click()'''
            time.sleep(10000)
            # Use a classe Select do Selenium para interagir com o <select>
            select = Select(tipo_certidao_select)
            # Selecione a opção com o value "N" (Dívida e Não Dívida)
            select.select_by_value('N')

            confirm_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'confirmarBtn'))) 
            confirm_button.click()

            certid_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'certidaoBtn'))) 
            certid_button.click()
            
            time.sleep(1)
            return "success"
        

    except Exception as e:
        show_popup(f"Ocorreu um erro: {e}")
        return "error"
    finally:
        driver.quit()

def renameFile(download_dir, name, username, fileType):
    dic = {'divida': 'CertificadoDivNDiv', 'liq_IRS': 'LiquidacaoIRS', 'comp_IRS': 'ComprovativoIRS', 'comp_IES': 'ComprovativoIES', 'veiculos':'ListagemVeiculos'}
    print('Começou a renomear')
    
    if name == "None":
        name = username
    name = remove_spaces_and_accents(name)
    
    # Lista todos os arquivos no diretório
    files = [os.path.join(download_dir, f) for f in os.listdir(download_dir)]
    
    # Encontra o arquivo mais recente
    latest_file = max(files, key=os.path.getctime)
    if name != "":
        for key in dic:
            if key == fileType:
                new_filename = dic[key] + name + ".pdf"
                old_path = latest_file
                new_path = os.path.join(download_dir, new_filename)
                
                counter = 1
                while os.path.exists(new_path):
                    new_filename = f"{dic[key]}{name}_{counter}.pdf"
                    new_path = os.path.join(download_dir, new_filename)
                    counter += 1
                
                os.rename(old_path, new_path)
                print(f"Arquivo renomeado para: {new_filename}")
                return new_path
            else:
                print('O tipo de arquivo não corresponde ao esperado')
    else:
        print('Nome não pode ser vazio')
    
    return new_path
