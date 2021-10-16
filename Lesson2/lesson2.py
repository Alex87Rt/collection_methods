from bs4 import BeautifulSoup as bs
import requests
import re


headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                         ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'}

def HeadHunter(link, search_str, str):
    html = requests.get(link+'/search/vacancy?clusters=true&enable_snippets=true&text='+search_str+
                        '&showClusters=true',headers=headers).text
    parsed_html = bs(html,'lxml')
    vacancy = []
    for i in range(str):
        vacancy_block = parsed_html.find('div',{'class':'vacancy-serp'})
        vacancy_list = vacancy_block.findChildren(recursive=False)
        for vac in vacancy_list:
            vac_data={}
            req=vac.find('span',{'class':'g-user-content'})
            if req!=None:
                main_info = req.findChild()
                vac_name = main_info.getText()
                vac_link = main_info['href']
                salary = vac.find('div',{'class':'vacancy-serp-item__compensation'})
                if not salary:
                    salary_min = None
                    salary_max = None
                else:
                    salary=salary.getText().replace(u'\xa0', u'')
                    salaries=salary.split('-')
                    salaries[0] = re.sub(r'[^0-9]', '', salaries[0])
                    salary_min=int(salaries[0])
                    if len(salaries)>1:
                        salaries[1] = re.sub(r'[^0-9]', '', salaries[1])
                        salary_max=int(salaries[1])
                    else:
                        salary_max=None
                vac_data['name'] = vac_name
                vac_data['salary_min'] = salary_min
                vac_data['salary_max'] = salary_max
                vac_data['link'] = vac_link
                vac_data['site'] = link
                vacancy.append(vac_data)
        next_btn_block=parsed_html.find('a',{'class':'bloko-button HH-Pager-Controls-Next HH-Pager-Control'})
        next_btn_link=next_btn_block['href']
        html = requests.get(link+next_btn_link,headers=headers).text
        parsed_html = bs(html,'lxml')

    print(vacancy)
    return vacancy


search_str='инженер'
str=2

HeadHunter('https://voronezh.hh.ru/',search_str, str)

