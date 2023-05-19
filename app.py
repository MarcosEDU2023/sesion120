from flask import Flask, render_template, request
import spacy
from spacy.language import Language
from spacy_langdetect import LanguageDetector

app = Flask(__name__)
nlp = spacy.load("es_core_news_sm")  # Carga el modelo de idioma de Spacy
nlp_en = spacy.load("en_core_web_sm") #Carga el idioma inglés.

def get_lang_detector(nlp, name):
   return LanguageDetector()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    raw_text = request.form['rawtext']
    task_option = request.form['taskoption']

    #Detectar el idioma del texto
    nlp = spacy.load("es_core_news_sm")
    Language.factory("language_detector", func=get_lang_detector)
    nlp.add_pipe('language_detector', last=True)

    doc = nlp(raw_text)
    if doc._.language["language"] == "en":
        print('INGLES')
        nlp = nlp_en
    else:
        print('ESPAÑOL')
      # Procesar el texto con el modelo de idioma correspondiente    
    doc = nlp(raw_text)  # Procesa el texto con Spacy

    for ent in doc.ents:
        print(ent.text, ent.label_)
    
    # Extrae las entidades según la opción seleccionada
    entities=[]
    if doc._.language["language"] == "en":
        idioma='INGLÉS'
        print("Dentro de IF en INGLES")
        if task_option == 'organization':
            entities = [ent.text for ent in doc.ents if ent.label_ == 'ORG']
        elif task_option == 'person':
            entities = [ent.text for ent in doc.ents if ent.label_ == 'PERSON'] 
        elif task_option == 'location':
            entities = [ent.text for ent in doc.ents if ent.label_ == 'GPE']
        elif task_option == 'currency':
            entities = [ent.text for ent in doc.ents if ent.label_ == 'MONEY']
        
    if doc._.language["language"] == "es":
        idioma='ESPAÑOL'
        print("Dentro de IF en ESPAÑOL")
        if task_option == 'organization':
            entities = [ent.text for ent in doc.ents if ent.label_ == 'ORG']
        elif task_option == 'person':
            entities = [ent.text for ent in doc.ents if ent.label_ == 'PER'] 
        elif task_option == 'location':
            entities = [ent.text for ent in doc.ents if ent.label_ == 'LOC']  
        elif task_option == 'currency':
            entities = [ent.text for ent in doc.ents if ent.label_ == 'MONEY']
              
         
    return render_template('index.html', idioma=idioma, results=entities, num_of_results=len(entities))   

if __name__ == '__main__':
    app.run(debug=True)
