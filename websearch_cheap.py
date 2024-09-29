from duckduckgo_search import DDGS
from bs4 import BeautifulSoup
import requests
def search(search_string): # search Duck duck go for the first 5 results 
    results = DDGS().text(search_string, max_results=3)
    search_result = ""
    for result in results:
        soup = BeautifulSoup(requests.get(result['href']).content, 'html.parser')
        article_content = soup.find('article')
        if(article_content):
            paragraphs = article_content.find_all("p")
       
        else:
            paragraphs = soup.find_all("p", limit=5)
        for p in paragraphs:
            search_result += f"Content: {p.get_text()}\n"
        


        
      
        
    return search_result

