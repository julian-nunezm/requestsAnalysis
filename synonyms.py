import thesaurus, urllib.request
from bs4 import BeautifulSoup
from pprint import pprint
import json

url = 'http://www.thesaurus.com/browse/'
search_term = 'well'

def lookForSynonyms(word):
    try:
        synonyms = []
        content = urllib.request.urlopen(url + word)
        #print(fp.geturl())
        #print(fp.info())
        #print(content.getcode())
        data = content.read().decode('utf-8')
        content.close()
        soup = BeautifulSoup(data, 'html.parser')
        #print(soup.get_text())
        results = soup.find_all("script")
        #print(len(results))
        result = results[22].string
        json_txt = result.replace("window.INITIAL_STATE = ","").replace("};","}")
        structure = json.loads(json_txt)
        for synonym in structure['searchData']['tunaApiData']['posTabs']:
            for term in synonym['synonyms']:
                if int(term['similarity']) == 100:
                    synonyms.append(term['term'])
        return synonyms
    except urllib.error.HTTPError:
        raise(urllib.error.HTTPError)
    except Exception as e1:
        print(f"There is an error in lookForSynonyms: {str(e1)}")
        
try:
    pprint(lookForSynonyms(search_term))
except Exception as e_thesaurus:
    print(f"There is an error: {str(e_thesaurus)}")
