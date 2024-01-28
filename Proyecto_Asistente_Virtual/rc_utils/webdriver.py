
# pip install webdriver-manager==3.8.6
# pip install selenium==4.9.1
# pip install undetected_chromedriver==3.4.6    funciona OK
# pip install pyvirtualdisplay

# pip install selenium_stealth==1.0.6

# sudo apt install espeak

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
#ruta = ChromeDriverManager(path="./chromedriver").install

import undetected_chromedriver as uc

from selenium.webdriver.common.by import By                         # para buscar por tipos de elementos
from selenium.webdriver.support.ui import WebDriverWait             # para esperar por elementos en selenium
from selenium.webdriver.support import expected_conditions as EC    # para indicar condiciones en selenium
from selenium.common import exceptions as WebDriverException

from pyvirtualdisplay import Display
from time import sleep

log_in = (By.XPATH, '//div[text()="Log in"]')
google_oauth_btn = (By.XPATH, '//button[@data-provider="google"]')
google_email_input = (By.XPATH, '//input[@type="email"]')
google_next_btn = (By.XPATH, '//*[@id="identifierNext"]')
google_pwd_input = (By.XPATH, '//input[@type="password"]')
google_pwd_next_btn = (By.XPATH, '//*[@id="passwordNext"]')
google_code_samp = (By.TAG_NAME, 'samp')

def init_webdriver(headless=True, pos='maximizada'):   #Por defecto se muestra la ventana maximizada 

    options = uc.ChromeOptions()
    # desactivar el guardado de credenciales
    options.add_argument('--password-store=basic')
    options.add_argument("--no-sandbox")
    options.add_experimental_option(
        'prefs', {
            'credentials_enable_service': False,
            'profile.password_manager_enable': False,
        },
    )

    driver = uc.Chrome(
        options=options,
        headless=headless,
        log_level=3,
    )

    if not headless:
        driver.maximize_window()  # Maximizar la venta

        if pos != 'maximizada':
            
            ancho, alto = driver.get_window_size().values() # Obtener resolucion de la ventana
            if pos == 'izquierda':
                driver.set_window_rect(x=0, y=0, width=ancho//2, height=alto)
            elif pos == 'derecha':
                driver.set_window_rect(x=(ancho//2 - ancho//3), y=0, width=(ancho//2 + ancho//3), height=alto)
    else:
        driver.maximize_window()

    return driver

class DisplayManager:
    def __init__(self):
        self.display = None

    def iniciar_display(self, visible=0):
        if not self.display:
            self.display = Display(visible=visible, size=(800, 600))
            self.display.start()

    def detener_display(self):
        if self.display:
            self.display.stop()
            self.display = None