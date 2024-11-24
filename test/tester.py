import requests
import csv
import os
import time
from bs4 import BeautifulSoup

def write_to_csv(data, file_path):
    file_exists = os.path.isfile(file_path)

    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        if not file_exists:
            writer.writerow(['question', 'answer'])

        for d in data:
            question = d['question']
            answer = d['answer']
            writer.writerow([question, answer])

            
def extract_text_from_elements(elements):
    ref = []
    for element in elements:
        ref.append(element.get_text(separator=' ', strip=True))
    return ref


def main():
    data = []
    
    url = 'https://www.hukumonline.com'
    
    for i in range(23, 173+1):
        print(f'Halaman ke {i}')
        
        response = requests.get(url+f'/klinik/pidana/page/{i}/')
        soup = BeautifulSoup(response.content, 'html.parser')
        section = soup.find(id='result-list')
        
        try:
            lists = section.find_all('div', class_='klinik-list d-flex flex-column divider-bottom my-3')
            
            links = []
            for l in lists:
                a_tag = l.find('a')
                title = l.find('h2')

                links.append(a_tag['href'])
            
            for j, link in enumerate(links):
                time.sleep(2)
                try:
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
                    answer = answer_content.get_text() if answer_content else "None"
                    
                    print(title)
                    print(question)
                    print(answer)
                    
                    data.append({
                        "question": question,
                        "answer" : answer,
                    })
                    
                except:
                    pass
            
            write_to_csv(data, file_path = 'hukum_online_pidana.csv')
            data.clear()
            
        except:
            pass
    
if __name__ == '__main__':
    main()