# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

import re
import pandas as pd
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from typing import Any, Text, Dict, List
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class ActionWorkshopInfo(Action):
    def name(self) -> str:
        return "action_workshop_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:
        try:
            workshops_df = pd.read_csv('./dataset/workshops.csv', sep=';')
            workshop_name = tracker.get_slot('workshop_name')

            if not workshop_name:
                dispatcher.utter_message(text="Non hai specificato il nome del workshop.")
                return []

            if 'Workshop Name' not in workshops_df.columns:
                dispatcher.utter_message(text="Il dataset non contiene informazioni sui workshop.")
                return []

            workshop_info = workshops_df[workshops_df['Workshop Name'] == workshop_name]

            if workshop_info.empty:
                dispatcher.utter_message(text=f"Non ho trovato informazioni sul workshop chiamato {workshop_name}.")
            else:
                workshop_info = workshop_info.iloc[0]
                dispatcher.utter_message(
                    text=f"Il workshop {workshop_info['Workshop Name']} si terrà il {workshop_info['Data']} alle {workshop_info['Orario']} in {workshop_info['Location']}."
                )
        except FileNotFoundError:
            dispatcher.utter_message(text="Il file del dataset dei workshop non è stato trovato.")
        except Exception as e:
            dispatcher.utter_message(text=f"Si è verificato un errore: {str(e)}")
        return []


class ActionLabTourInfo(Action):
    def name(self) -> str:
        return "action_lab_tour_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:
        try:
            lab_tours_df = pd.read_csv('./dataset/lab_tours.csv', sep=';')
            lab_tour_name = tracker.get_slot('lab_tour_name')

            if not lab_tour_name:
                dispatcher.utter_message(text="Non hai specificato il nome del tour.")
                return []

            if 'Lab Tour Name' not in lab_tours_df.columns:
                dispatcher.utter_message(text="Il dataset non contiene informazioni sui tour dei laboratori.")
                return []

            lab_tour_info = lab_tours_df[lab_tours_df['Lab Tour Name'] == lab_tour_name]

            if lab_tour_info.empty:
                dispatcher.utter_message(text=f"Non ho trovato informazioni sul tour chiamato {lab_tour_name}.")
            else:
                lab_tour_info = lab_tour_info.iloc[0]
                dispatcher.utter_message(
                    text=f"Il tour {lab_tour_info['Lab Tour Name']} si terrà il {lab_tour_info['Date']} alle {lab_tour_info['Time']} e il punto di incontro è {lab_tour_info['Meeting Point']}."
                )
        except FileNotFoundError:
            dispatcher.utter_message(text="Il file del dataset dei tour dei laboratori non è stato trovato.")
        except Exception as e:
            dispatcher.utter_message(text=f"Si è verificato un errore: {str(e)}")
        return []


class ActionRoomInfo(Action):
    def name(self) -> str:
        return "action_room_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:
        try:
            aule_df = pd.read_csv('./dataset/aule.csv', sep=';')
            aula_name = tracker.get_slot('aula')

            if not aula_name:
                dispatcher.utter_message(text="Non hai specificato il nome dell'aula.")
                return []

            if 'Aula' not in aule_df.columns:
                dispatcher.utter_message(text="Il dataset non contiene informazioni sulle aule.")
                return []

            aula_info = aule_df[aule_df['Aula'] == aula_name]

            if aula_info.empty:
                dispatcher.utter_message(text=f"Non ho trovato informazioni sull'aula chiamata {aula_name}.")
            else:
                aula_info = aula_info.iloc[0]
                planimetria_link = aula_info['Planimetria']

                dispatcher.utter_message(
                    text=f"L'aula {aula_info['Aula']} si trova in {aula_info['Edificio']} al {aula_info['Quota']}. Precisamente {aula_info['Indicazioni']}. Ecco la planimetria:{planimetria_link}"
                )
                    
        except FileNotFoundError:
            dispatcher.utter_message(text="Il file del dataset delle aule non è stato trovato.")
        except Exception as e:
            dispatcher.utter_message(text=f"Si è verificato un errore: {str(e)}")
        return []
    
class ActionPlanimetriaInfo(Action):
    def name(self) -> Text:
        return "action_planimetria_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Carica il dataset delle aule
        aule_df = pd.read_csv('./dataset/aule.csv', sep=';')
        
        # Ottieni la quota dall'entità rilevata
        quota = tracker.get_slot('quota')
        
        if quota:
            # Trova il link della planimetria corrispondente alla quota
            floor_plan_row = aule_df[aule_df['Quota'] == quota]
            
            if not floor_plan_row.empty:
                planimetria_link = floor_plan_row.iloc[0]['Planimetria']

                dispatcher.utter_message(
                    text=f"Ecco la planimetria per la quota {quota}: {planimetria_link}"
                )
            else:
                dispatcher.utter_message(text=f"Non ho trovato la planimetria per la quota {quota}.")
        else:
            dispatcher.utter_message(text="Non ho capito quale quota ti interessa. Puoi riprovare?")
        return []
    
class ActionResetSlots(Action):
    def name(self):
        return "action_reset_slots"

    async def run(self, dispatcher, tracker, domain):
        # Resetta gli slot specificati
        return [SlotSet("workshop_name", None), SlotSet("lab_tour_name", None), SlotSet("aula", None), SlotSet("quota", None), SlotSet("study_course", None), SlotSet("name", None), SlotSet("email", None), SlotSet("workshop_name_text", None)]
    

class ActionShowWorkshops(Action):
    def name(self) -> Text:
        return "action_show_workshops"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Carica il dataset dei workshop
        workshops_df = pd.read_csv('./dataset/workshops.csv', sep=';')
        
        # Ottieni il corso di studi dall'entità rilevata
        course_name = tracker.get_slot('study_course')
        
        if course_name:
            # Filtra i workshop per il corso di studi selezionato
            filtered_workshops = workshops_df[workshops_df['Corso di Studi'].str.contains(course_name, case=False, na=False)]
            if not filtered_workshops.empty:
                workshops_list = filtered_workshops['Workshop Name'].tolist()
                workshops_str = "\n".join(workshops_list)
                
                # Invio della risposta all'utente
                dispatcher.utter_message(text=f"Ecco i workshop disponibili per {course_name}: \n{workshops_str}")
            else:
                dispatcher.utter_message(text=f"Non ci sono workshop disponibili per il corso di studi {course_name}.")
        else:
            dispatcher.utter_message(text="Non ho capito quale corso di studi ti interessa. Puoi riprovare?")
        
        return []


class ActionSubmitWorkshopBooking(Action):
    def name(self) -> Text:
        return "action_submit_workshop_booking"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Ottieni i valori degli slot
        workshop = tracker.get_slot('workshop_name_text')
        name = tracker.get_slot('name')
        email = tracker.get_slot('email')

        # Verifica se uno degli slot è vuoto
        if not workshop or not name or not email:
            dispatcher.utter_message(text="Richiedimi di prenotare un workshop inserendo tutti i dati correttamente.")
            return []

        try:
            # Invio dell'email di conferma
            self.send_confirmation_email(workshop, name, email)
            dispatcher.utter_message(response="utter_booking_confirmed")
        except Exception as e:
            dispatcher.utter_message(text=f"Si è verificato un errore: {str(e)}")
            dispatcher.utter_message(response="utter_booking_failed")

        return []

    def send_confirmation_email(self, workshop: Text, name: Text, email: Text):
        # Configurazione dell'email
        from_email = "laura.pistagnesi@gmail.com"
        to_email = email
        subject = f"Conferma Prenotazione Workshop: {workshop}"
        body = f"Ciao {name},\n\nLa tua prenotazione per il workshop '{workshop}' è stata confermata.\n\nCordiali saluti,\nUnivpm"

        # Creazione dell'email
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Invio dell'email
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login(from_email, 'ljog lnsq hzpv gnqv')
            server.send_message(msg)
            server.quit()
        except Exception as e:
            raise Exception(f"Errore durante l'invio dell'email: {str(e)}")
        

class ActionValidateForm(Action):
    def name(self) -> Text:
        return "action_validate_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Ottieni i valori dei slot
        workshop_name = tracker.get_slot('workshop_name_text')
        name = tracker.get_slot('name')
        email = tracker.get_slot('email')

        errors = []

        # Validazione del workshop
        try:
            workshops_df = pd.read_csv('./dataset/workshops.csv', sep=';')
            workshop_info = workshops_df[workshops_df['Workshop Name'].str.lower() == workshop_name.lower()]
            if workshop_info.empty:
                errors.append(f"Il workshop '{workshop_name}' non è disponibile. Per favore scegli un workshop valido.")
        except FileNotFoundError:
            errors.append("Il file dei workshop non è stato trovato.")

        # Validazione del nome
        if not name or len(name.strip()) == 0:
            errors.append("Per favore fornisci un nome valido.")

        # Validazione dell'email
        email_regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not email or not re.match(email_regex, email):
            errors.append("Per favore fornisci un indirizzo email valido.")

        if errors:
            for error in errors:
                dispatcher.utter_message(text=error)
            return [SlotSet("name", None), SlotSet("email", None), SlotSet("workshop_name_text", None)]
        return []