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

def extract_strong_from_paragraph(paragraphs):
    """
    Extracts text from <strong> tags within <p> elements.
    """
    strong_texts = []
    for paragraph in paragraphs:
        strong_tags = paragraph.find_all('strong')  # Find all <strong> tags
        for strong_tag in strong_tags:
            strong_texts.append(strong_tag.get_text(strip=True))  # Extract text
    return strong_texts


def main():
    data = []
    
    url = 'https://www.hukumonline.com'
    
    for i in range(1, 22+1):
        print(f'Halaman ke {i}')
        
        response = requests.get(url+f'/klinik/teknologi/page/{i}/')
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
                    if content2:
                        paragraphs = content2.find_all(['p', 'div'])
                        answer = extract_strong_from_paragraph(paragraphs)
                    
                    print(title)
                    print(question)
                    print(answer)
                    
                    data.append({
                        "question": question,
                        "answer" : answer,
                    })
                    
                except:
                    pass
            
            write_to_csv(data, file_path = 'hukum_online_tech_v2.csv')
            data.clear()
            
        except:
            pass
    
if __name__ == '__main__':
    main()