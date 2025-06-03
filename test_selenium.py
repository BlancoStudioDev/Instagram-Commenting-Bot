from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

def test_selenium_setup():
    print("Inizializzazione del test di Selenium...")
    
    # Configurazione delle opzioni di Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Esecuzione in modalità headless (senza interfaccia grafica)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Inizializzazione del driver
    try:
        print("Configurazione del webdriver...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Test di navigazione
        print("Navigazione su una pagina web di test...")
        driver.get("https://www.google.com")
        print(f"Titolo della pagina: {driver.title}")
        
        # Chiusura del driver
        driver.quit()
        print("Test completato con successo!")
        return True
    except Exception as e:
        print(f"Si è verificato un errore: {e}")
        return False

if __name__ == "__main__":
    test_selenium_setup()
