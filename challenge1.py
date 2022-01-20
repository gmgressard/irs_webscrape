import requests 
from bs4 import BeautifulSoup
import json



requested_forms_input = input('What form(s) would you like to see?  > ')
requested_forms = requested_forms_input.split(',')
print('\n')
print("See Results Below:")
print('\n')

requested_forms_list = []
for form in requested_forms:
    requested_forms_list.append(form.strip())


def get_urls():
    """return urls of search pages containing the form names from requested forms list"""

    url_list = []
    
    for form_number in requested_forms_list:
        form_number_url = form_number.replace(' ','+')
        url = f'https://apps.irs.gov/app/picklist/list/priorFormPublication.html?resultsPerPage=200&sortColumn=sortOrder&indexOfFirstRow=0&criteria=formNumber&value={form_number_url}&isDescending=false'
        url_list.append(url)
    return url_list 


def get_data():
    """return json object of data on requested forms"""

    urls = get_urls() 
    dic_list = []

    for url in urls:
        dic = {}
        form_years_list = []

        res = requests.get(url) 
        src = res.content
        res_soup = BeautifulSoup(src, 'html.parser')
        table = res_soup.find_all(True, {'class':['even','odd']})
        
        for row in table:
            form_title_html = row.find('td', class_='MiddleCellSpacer')
            form_number_html = row.find('td', class_='LeftCellSpacer')
            form_year_html = row.find('td', class_='EndCellSpacer')

            form_number_steralized = form_number_html.get_text().strip()
            form_title_steralized = form_title_html.get_text().strip()
        
            for form_year in form_year_html:
                form_year_steralized = form_year.text.strip()
                form_years_list.append(form_year_steralized)
    
            for form in requested_forms_list:
                if form == form_number_steralized:
                    dic['form_number'] = form_number_steralized
                    dic['form_title'] = form_title_steralized
                    dic['min_year'] = min(form_years_list)
                    dic['max_year'] = max(form_years_list)
        dic_list.append(dic)
    return json.dumps(dic_list, indent=4)

print(get_data())