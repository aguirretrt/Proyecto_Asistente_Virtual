import os
import sys
import pickle
import tempfile
import speech_recognition as sr

from time import sleep, time

from config import *
from rc_utils.colores import *
from rc_utils.utils import *
from rc_utils.webdriver import *
from rc_utils.vozdriver import *

class ChatGPT:    

    def __init__(self, user, password):

        self.OPENAI_USER = user
        self.OPENAI_PASSWORD = password
        self.COOKIES_FILE = f'{tempfile.gettempdir()}/openai.cookies'

        print(f'{azul}Iniciando WebDriver{gris}')
        
        self.vtr_display = DisplayManager()
        self.vtr_display.iniciar_display(1) # Manipula la VirtDisplay

        self.driver = init_webdriver(headless=False , pos='maximizada') # Inicia el WebDriver
        self.wait = WebDriverWait(self.driver, 30)  # Espera 30 segundos que inicie
        
        login = self.login_openai() # Login
        
        print()
        if not login:
            sys.exit(1)

    def login_openai(self):
        # Revisa si existe el archivo cookies
        # Realiza Login por cookies
        #
        if os.path.isfile(self.COOKIES_FILE):
            print(f'\33[K{azul}LOGIN POR COOKIES{gris}')
            cookies = pickle.load(open(self.COOKIES_FILE, 'rb'))
            self.driver.get("https://chat.openai.com/robots.txt")
            for cookie in cookies:
                cursor_arriba()
                print(f'\33[K{gris}cargando cookie: {cookie["name"]}{gris}')
                try:
                    self.driver.add_cookie(cookie)
                except:
                    pass
            cursor_arriba()
            print(f'\33[K{gris}Cargando ChatGPT...{gris}')
            self.driver.get("https://chat.openai.com")
            sleep(2)

            # Verifica si se pudo logear correctamente
            login = self.comprobar_login()

            if login:
                print(f'\33[K{azul}LOGIN POR COOKIE: {verde}OK{gris}')
                return login
            else:
                print(f'\33[K{azul}LOGIN POR COOKIE: {rojo}FALLIDO{gris}')

        # Si fallo el logeo por cookie continua con un login desde Cero
        print(f'\33[K{azul}LOGIN DESDE CERO{gris}')
        print(f'\33[K{gris}Cargando ChatGPT{gris}')
        self.driver.get("https://chat.openai.com/")
        
        cursor_arriba()
        print(f'\33[K{gris}click en "login"{gris}')
        # Busca el elemento div que contenga el texto Log in
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(log_in)).click()

        cursor_arriba()
        print(f'\33[K{gris}Accediendo con cuenta Google{gris}')
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(google_oauth_btn)).click()
    
        # try:
        #     # WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'//div[@data-identifier="{self.OPENAI_USER}"]'))
        #     # ).click()
        
        #     WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'//input[@type="email"]{self.OPENAI_USER}"]'))
        #     ).click()

        # except WebDriverException.TimeoutException:
        #     print(f'\33[K{gris}Google no recordo su cuenta{gris}')
            
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(google_email_input)).send_keys(self.OPENAI_USER)

        self.driver.find_element(*google_next_btn).click()

        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(google_pwd_input)).send_keys(self.OPENAI_PASSWORD)

        self.driver.find_element(*google_pwd_next_btn).click()

        cursor_arriba()
        sleep(2)

        
        login = self.comprobar_login()      # Verifica si se pudo loguear correctamente

        if login:
            # Guardamos las cookies
            pickle.dump(self.driver.get_cookies(), open(self.COOKIES_FILE, 'wb'))
            print(f'\33[K{azul}LOGIN DESDE CERO: {verde}OK{gris}')
        else:
            print(f'\33[K{azul}LOGIN DESDE CERO: {rojo}FALLIDO{gris}')
        return login

    def comprobar_login(self, tmpo=30):
        login = False
        while tmpo > 0:
            try:
                self.driver.find_element(By.XPATH, "//div[text()='Next']").click()
            except:
                pass

            try:
                self.driver.find_element(By.XPATH, '//div[text()="Done"]').click()
            except:
                pass
            
            try:
                self.driver.find_element(By.XPATH, '//div[text()="Okay, let’s go"]').click()
            except:
                pass
            

            try:
                self.driver.find_element(By.CSS_SELECTOR, 'textarea[tabindex="0"]').click()
                login = True
                break
            except:
                pass

            try:
                self.driver.find_element(By.ID, 'username')
                # e = self.driver.find_element(By.ID, 'username')
                break
            except:
                pass

            try:
                if 'session has expired' in self.driver.find_element(By.CSS_SELECTOR, 'h3.text-lg').text:
                    cursor_arriba()
                    print(f'\33[K{amarillo}LA SESSION HA EXPIRADO{gris}')
                    print()
                    break
            except:
                pass

            cursor_arriba()
            print(f'\33[K{gris}Comprobando Login... {tmpo}{gris}')
            sleep(1)
            tmpo -= 1

        cursor_arriba()
        print('\33[K')
        cursor_arriba(2)
        return login

    def ultima_conversacion(self, tmpo=10):
        #print('Buscar')
        while tmpo > 0:
            try:
  
                self.driver.find_element(By.XPATH, '//div[text()="Historial"]').click()
                break
            
            except:
                sleep(1)
                tmpo -= 1
                
    def chatear(self, prompt):
        #Intruduce texto en el promp o textbox
        self.driver.find_element(By.CSS_SELECTOR, 'textarea[tabindex="0"]').send_keys(prompt)
        sleep(0.5)

        self.driver.find_element(By.CSS_SELECTOR, 'button[data-testid="send-button"].absolute.md\\:bottom-3').click()

        # Generando las respuestas
        respuesta = ''
        inicio = time()
        segundos = 0
        while True:
            
            respuesta = self.driver.find_elements(By.CSS_SELECTOR, "div.markdown")[-1].text # Extraemos el texto generado

            try:
                self.driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Stop generating"]') # Animacion del stop mientras genera la respuesta
            except:
                # Cuando ya no estan los puntitos y la respuesta termino
                if respuesta: # Si se ha generado alguna respuestas
                    
                    break # Sale del bucle

            segundos = int(time() - inicio)
            if segundos:
                print(f'\33[K{azul2}Generando respuesta... {gris}{segundos} segundos ({len(respuesta)}{gris})')
                sleep(1)
                cursor_arriba()

        if segundos >= 0:
            print(f'\33[K{magenta}Respuesta generada en... {blanco}{segundos} {magenta}segundos{gris}')
        
        sleep(2)
        return self.driver.find_elements(By.CSS_SELECTOR, "div.markdown")[-1].text # Extraemos el texto otra vez por si falto algo para terminar
        
    def cerrar(self):
        print(f'\33[K{azul}Saliendo.........{gris}')
        print(f'\33[K{azul}Saliendo......{gris}')
        print(f'\33[K{azul}Saliendo...{gris}')
        print(f'\33[K{azul}Saliendo{gris}')
        
        self.vtr_display.detener_display()
        self.driver.quit()
        
        print("Conversacion FINALIZADA")
      

if __name__ == '__main__':
        
        chatgpt = ChatGPT(OPENAI_USER, OPENAI_PASS)
    
        chatgpt.ultima_conversacion() # Busca la ultimaconversacion
        
        print(f'{azul}Detectando Drivers de Sonido...{gris}')      
        rec = sr.Recognizer()
        with sr.Microphone() as source:
            rec.adjust_for_ambient_noise(source)
        rec.listen_in_background(source, recognizer_voice)
        
        sleep(1)
        text = 'Buenas, ya puedes comunicarte libremente conmigo...'
        print(f'{verde}{text}{gris}')
        
        thread_text_to_speech(text)
        
        print(f'{rojo}{gris}')
        sleep(1)
        while True:

            aux = return_string()

            if 'salir' in aux:
                print(f'\33[K{magenta}Usted dijo.: Quiero salir{gris}')
                text_to_speech("Usted dijo quiero salir, asi que hasta luego.")
                break
            elif 'terminar' in aux:
                print(f'\33[K{magenta}Usted dijo.: Terminar{gris}')
                thread_text_to_speech("Quiere hacerme otra pregunta?")
                aux = ''
            elif 'asistente' in aux:
                # Envia el texto en la variable aux al terminal y al prompt
                aux = aux.replace('asistente', '') 
                print(f'\33[K{amarillo}{aux}{gris}')
                respuesta = chatgpt.chatear(aux)
                print(f'{verde}{respuesta}{gris}')
                print()
                # Envia la respuesta de texto a reproducir en audio
                thread_text_to_speech(respuesta)
                aux = ''
        
            print(f'{rojo}Escuchando...{gris}')
            cursor_arriba()
            sleep(1)
        
        chatgpt.cerrar()
        sys.exit()

