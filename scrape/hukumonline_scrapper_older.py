import requests
import csv
import os
from bs4 import BeautifulSoup

def write_to_csv(data, file_path):
    file_exists = os.path.isfile(file_path)

    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        if not file_exists:
            writer.writerow(['question', 'dasar_hukum'])

        for d in data:
            question = d['question']
            dasar_hukum = d['dasar_hukum']
            writer.writerow([question, dasar_hukum])

def main():
    data = []
    
    url = 'https://www.hukumonline.com'
    
    for i in range(95, 174+1):
        print(f'Halaman ke {i}')
        
        response = requests.get(url+f'/klinik/teknologi/page/{i}/')
        soup = BeautifulSoup(response.content, 'html.parser')
        section = soup.find(id='result-list')
        lists = section.find_all('div', class_='klinik-list d-flex flex-column divider-bottom my-3')
        
        links = []
        for l in lists:
            a_tag = l.find('a')

            links.append(a_tag['href'])
        
        for j, link in enumerate(links):
            print(f'Iterasi ke {j}')
            new_url = url+link
            
            new_response = requests.get(new_url)
            new_soup = BeautifulSoup(new_response.content, 'html.parser')
            
            content = new_soup.find('div', class_='css-lycprl')

            question_content = content.find('div', class_='css-c816ma e1vjmfpm0')
            
            if question_content:
                question = question_content.get_text()
                
            content2 = new_soup.find('div', class_='css-103zlhi elbhtsw0')
            
            answer_content = content2.find('div', class_='css-c816ma e1vjmfpm0')

            answers = answer_content.find_all(['div', 'p', 'b'])
            
            ref = [] 
            for answer in answers:
                u_tag = answer.find('u', string=lambda text: text and ('Dasar Hukum' in text or 'Legal Basis' in text))
                
                if u_tag:
                    parent_p = u_tag.find_parent(['div', 'p', 'b'])
                    print(parent_p)
                    
                    if parent_p:
                        next_element = parent_p.find_next_sibling()
                                
                        if next_element and next_element.name == 'div':
                            ol_inside_div = next_element.find('ol')
                            if ol_inside_div:
                                    ref = [li.get_text() for li in ol_inside_div.find_all('li')]

                        elif next_element and next_element.name == 'ol':
                            ref = [li.get_text() for li in next_element.find_all('li')]

                        elif next_element and next_element.name == 'p':
                            for item in next_element.find_all(['a', 'span', 'u']):
                                ref.append(item.text)  
                        
                        else:
                            print('Tidak ditemukan element')
                        
                        if next_element.name == 'ol':
                            for li in next_element.find_all('li'):
                                div_inside_li = li.find('div')
                                if div_inside_li:
                                    spans = div_inside_li.find_all('span')
                                    ref.extend([span.get_text(separator=' ', strip=True) for span in spans])
                                    
                        if next_element.name == 'ol':
                            for li in next_element.find_all('li'):
                                div_inside_li = li.find('div')
                                if div_inside_li:
                                    spans = div_inside_li.find_all('a')
                                    ref.extend([span.get_text(separator=' ', strip=True) for span in spans])
                                    
                    else:
                        print('Tidak ditemukan parent P')
            print(question)      
            print(ref) 
            print('---------------------------------------------------------------')   
                            
            data.append({
                "question": question,
                "dasar_hukum" : ref,
            })
        
        # write_to_csv(data, file_path = 'hukum_online_pidana.csv')
    
if __name__ == '__main__':
    main()