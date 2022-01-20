import requests 
from bs4 import BeautifulSoup
import os
import urllib.request



requested_form_input = input('What form would you like to see?  > ')
print('What year(s) would you like to see?')
requested_years_input = input("Please enter in format xxxx-xxxx or xxxx > ")
requested_years_list = requested_years_input.split('-')
print('\n')


def get_years_list():
    """returns list of years as integers requested by user"""

    years_list = []
    years_range_int = []
    for year in requested_years_list:
        years_range_int.append(int(year))
    for year in years_range_int:
        while year < years_range_int[1]:
            years_list.append(year)
            year+=1
    years_list.append(years_range_int[1])
    return years_list


def get_data():
    """returns list of dictionaries containing pdf url,form date and form name for form name requested by user"""

    form_dic_list = []

    form_number_url = requested_form_input.replace(' ','+')
    url = f'https://apps.irs.gov/app/picklist/list/priorFormPublication.html;jsessionid=_3vovvYIRtL-9x8T6VqBsnCO.20?value={form_number_url}&criteria=formNumber'
    res = requests.get(url) 
    src = res.content
    res_soup = BeautifulSoup(src, 'html.parser')
    table = res_soup.find_all(True, {'class':['even','odd']})
    
    for row in table:  
        form_number_html = row.find('td', class_='LeftCellSpacer')
        form_year_html = row.find('td', class_='EndCellSpacer')
        form_link_html = row.find('a', href=True)

        form_number = form_number_html.text.strip()
        form_year = form_year_html.text.strip()
        form_link = form_link_html['href']
        
        form_dic = {}
        if requested_form_input == form_number:   
            form_dic['form_number'] = form_number
            form_dic['form_year'] = int(form_year)
            form_dic['link'] = form_link
            form_dic_list.append(form_dic)
    return form_dic_list


def check_for_years_requested():
    """returns list of dictionaries containing pdf url,form date and form name of forms within year range provided by user"""

    form_data_dic_list = get_data()
    requested_years_list = get_years_list()

    requested_data_dic_list = []
    for data_dic in form_data_dic_list:
        if data_dic['form_year'] in requested_years_list:
            requested_data_dic_list.append(data_dic)
    return requested_data_dic_list


def download_pdf():
    """download pdfs of requested form and its years"""

    requested_forms_data = check_for_years_requested()
    # cwd = '/home/hackbright/src/pw_takehome'
    cwd = os.getcwd()
    
    for data_dic in requested_forms_data:    
        directory_name = data_dic['form_number']
        pdf_file_name = data_dic['form_number']+' - '+ str(data_dic['form_year']) +'.pdf'
        pdf_url = data_dic['link']
        path = os.path.join(cwd,directory_name)
       
        if os.path.isfile(os.path.join(path, pdf_file_name)):
            print(f'File {pdf_file_name} Already Exists')
        elif os.path.isdir(path):
            os.path.join(path, pdf_file_name)
            os.chdir(path)
            data = urllib.request.urlopen(pdf_url)
            file = open(pdf_file_name, 'wb')
            file.write(data.read())
            file.close()
            print(f'Downloading {pdf_file_name}')
        elif os.path.isdir(path):
            os.path.join(path, pdf_file_name)
            data = urllib.request.urlopen(pdf_url)
            file = open(pdf_file_name, 'wb')
            file.write(data.read())
            file.close()
            print(f'Downloading {pdf_file_name}')
        else:
            os.mkdir(path)
            os.chdir(path)
            data = urllib.request.urlopen(pdf_url)
            file = open(pdf_file_name, 'wb')
            file.write(data.read())
            file.close()
            print(f'Downloading {pdf_file_name}')    
     
download_pdf()