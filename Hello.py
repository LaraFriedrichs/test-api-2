import streamlit as st
from pathlib import Path
import json
import requests
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
  st.header('API-Request Mindat',divider='violet')
  st.markdown('Diese App soll dazu dienen, Daten über Minerale aus der Mindat.org Datenbank abzurufen. Es können verschiedenen eingetragene Eigenschaften der Minerale abgerufen werden. Hier betrachtet werden nur Minerale die durch die IMA (International Mineralogical Association) bestätigt wurden. Hier ist das Abrufen der folgenden Felder vorgesehen:')   
  st.markdown("""
            - name  
            - ima_formula  
            - ima_status   
            - ima_notes    
            - description_short   
            - mindat_formula  
            - mindat_formula_note.
  """
  )
  st.subheader('1. API-Key:',divider='violet')
  st.write('Für den API-Request von Mindat.org wird ein individueller API-Key benötigt. Um den API-Key zu erhalten, muss ein Account bei Mindat.org erstellt werden. Dort kann man den API-Key nach Bestätigung durch Mindat.org auf der Seite "my page" unter "Edit my page" finden.')
  st.link_button(label='Account bei Mindat.org erstellen',url= 'https://www.mindat.org/register.php')
  key=st.text_input(label='Bitte geben Sie Ihren API-Key ein:')
  st.subheader('2. Speicherort:',divider='violet')
  speicherort=st.text_input(label=' Legen Sie einen Speicherort für die abgerufenen Daten fest z.B. :blue[C:/Users/Desktop/mindat_data/] :')
  st.subheader('3. Überprüfen der angegebenen Daten:',divider='violet')
  st.text('Ihr API Key ist:')
  st.write(key)
  st.text('Ihr Speicherort ist:')
  st.write(speicherort)
  if st.checkbox('API-Key und ausgewählter Speicherort wurden überprüft.'):
    st.subheader('4. Starten des API-Requests:',divider='violet')
    st.write(''':black[!!! Achtung, das Abrufen der Daten kann 15 - 20 Minuten dauern !!!]''')

    if st.button(label=':violet[API-Request starten]',use_container_width=True):
        fields_str ='name,ima_formula,ima_status,ima_notes,description_short,mindat_formula,mindat_formula_note'
        Path(speicherort).mkdir(parents=True, exist_ok=True)
        MINDAT_API_URL = "https://api.mindat.org"
        headers = {'Authorization': 'Token '+ key}

        select_file_name = "mindat_data_IMA_download_2.json" 
        select_file_path = Path(speicherort,select_file_name) 
        select_file_path


        with open(select_file_path, 'w') as f:
            params = {
                'fields': fields_str,
                'format': 'json'
            }
            response = requests.get(MINDAT_API_URL+"/minerals_ima/",
                    params=params,
                    headers=headers)

            result_data = response.json()["results"]
            json_data = {"results": result_data}

            while True:
                try:
                    next_url = response.json()["next"]
                    response = requests.get(next_url, headers=headers)
                    json_data["results"] += response.json()['results']

                except requests.exceptions.MissingSchema as e:
                    break

            json.dump(json_data, f, indent=4)
        st.write("Der API-Request ist abgeschlossen. Sie können die abgerufenen Daten jetzt in Ihrem ausgewählten Speicherort öffnen und ansehen.")
if __name__ == "__main__":
    run()
