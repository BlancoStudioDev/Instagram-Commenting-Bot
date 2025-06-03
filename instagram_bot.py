from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
import os
import sys

class InstagramReelBot:
    """
    Bot per commentare automaticamente i Reels di Instagram.
    Utilizza Selenium per automatizzare le interazioni con il browser.
    """
    
    def __init__(self, headless=False):
        """
        Inizializza il bot con le configurazioni necessarie.
        
        Args:
            headless (bool): Se True, esegue il browser in modalità headless (senza interfaccia grafica)
        """
        self.BASE_URL = "https://www.instagram.com/"
        self.chrome_options = Options()
        
        if headless:
            self.chrome_options.add_argument("--headless")
        
        # Configurazioni aggiuntive per evitare problemi di rilevamento bot
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.chrome_options.add_experimental_option("useAutomationExtension", False)
        
        # Inizializzazione del driver
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service, options=self.chrome_options)
        
        # Modifica dello user agent per evitare il rilevamento come bot
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
        })
        
        # Impostazione di un timeout predefinito per le attese
        self.wait = WebDriverWait(self.driver, 10)
        
        # Aggiunta di un ritardo casuale tra le azioni per simulare comportamento umano
        self.min_delay = 1
        self.max_delay = 3
        
        # Contatore per i Reels commentati
        self.reels_commented = 0
        
        print("Bot Instagram inizializzato con successo!")
    
    def random_delay(self, min_seconds=None, max_seconds=None):
        """
        Aggiunge un ritardo casuale tra le azioni per simulare comportamento umano.
        
        Args:
            min_seconds (float, optional): Ritardo minimo in secondi
            max_seconds (float, optional): Ritardo massimo in secondi
        """
        min_s = min_seconds if min_seconds is not None else self.min_delay
        max_s = max_seconds if max_seconds is not None else self.max_delay
        delay = random.uniform(min_s, max_s)
        time.sleep(delay)
    
    def login(self, username, password):
        """
        Effettua il login su Instagram.
        
        Args:
            username (str): Nome utente Instagram
            password (str): Password Instagram
            
        Returns:
            bool: True se il login ha avuto successo, False altrimenti
        """
        try:
            print(f"Tentativo di login come {username}...")
            self.driver.get(self.BASE_URL)
            self.random_delay(2, 4)
            
            # Gestione dei cookie se appare il popup
            try:
                cookie_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Consenti tutti i cookie') or contains(text(), 'Allow all cookies')]"))
                )
                cookie_button.click()
                self.random_delay()
            except:
                print("Nessun popup cookie trovato o già gestito.")
            
            # Inserimento username
            username_field = self.wait.until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_field.clear()
            self.type_like_human(username_field, username)
            self.random_delay()
            
            # Inserimento password
            password_field = self.wait.until(
                EC.presence_of_element_located((By.NAME, "password"))
            )
            password_field.clear()
            self.type_like_human(password_field, password)
            self.random_delay()
            
            # Click sul pulsante di login
            login_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
            )
            login_button.click()
            
            # Attesa per il completamento del login
            self.random_delay(4, 6)
            
            # Verifica se il login è avvenuto con successo
            try:
                self.wait.until(
                    EC.presence_of_element_located((By.XPATH, "//div[@class='x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1n2onr6 x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1']"))
                )
                print("Login effettuato con successo!")
                
                # Gestione del popup "Salva le tue credenziali di accesso"
                try:
                    not_now_button = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Non ora') or contains(text(), 'Not Now')]"))
                    )
                    not_now_button.click()
                    self.random_delay()
                except:
                    print("Nessun popup 'Salva credenziali' trovato o già gestito.")
                
                # Gestione del popup "Attiva le notifiche"
                try:
                    not_now_button = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Non ora') or contains(text(), 'Not Now')]"))
                    )
                    not_now_button.click()
                    self.random_delay()
                except:
                    print("Nessun popup 'Attiva notifiche' trovato o già gestito.")
                
                return True
            except TimeoutException:
                print("Errore durante il login. Verifica le credenziali.")
                return False
                
        except Exception as e:
            print(f"Si è verificato un errore durante il login: {e}")
            return False
    
    def type_like_human(self, element, text):
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.2))
    
    def navigate_to_reels(self):
        """
        Naviga alla sezione Reels di Instagram.
        
        Returns:
            bool: True se la navigazione ha avuto successo, False altrimenti
        """
        try:
            print("Navigazione verso la sezione Reels...")
            
            # METODO 1: Usa l'URL diretto (più affidabile)
            self.driver.get("https://www.instagram.com/reels/")
            self.random_delay(3, 5)
            
            # Controlla se c'è contenuto caricato
            try:
                # Cerca un elemento video o contenitore di Reels
                self.wait.until(
                    EC.presence_of_element_located((By.TAG_NAME, "video"))
                )
                print("Navigazione alla sezione Reels completata con successo! (URL diretto)")
                return True
            except TimeoutException:
                print("Non rilevato contenuto video con l'URL diretto, provo un metodo alternativo...")
            
            # METODO 2: Trova e clicca il pulsante Reels nella barra di navigazione
            try:
                # Vai alla home
                self.driver.get(self.BASE_URL)
                self.random_delay(2, 4)
                
                # Cerca il pulsante Reels (prova diversi selettori)
                selectors = [
                    "//a[contains(@href, '/reels/')]",
                    "//a[contains(@aria-label, 'Reels')]",
                    "//span[contains(text(), 'Reels')]/ancestor::a",
                    "//div[contains(@role, 'tablist')]//a[2]"  # Spesso il secondo tab è Reels
                ]
                
                reels_button = None
                for selector in selectors:
                    try:
                        reels_button = WebDriverWait(self.driver, 3).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        break
                    except:
                        continue
                
                if reels_button:
                    reels_button.click()
                    self.random_delay(3, 5)
                    
                    # Verifica se ci sono video
                    self.wait.until(
                        EC.presence_of_element_located((By.TAG_NAME, "video"))
                    )
                    print("Navigazione alla sezione Reels completata con successo! (Pulsante Reels)")
                    return True
                else:
                    print("Nessun pulsante Reels trovato")
            except Exception as e:
                print(f"Errore durante la navigazione tramite pulsante: {e}")
            
            # METODO 3: Assumiamo che siamo comunque nei Reels se ci sono video
            try:
                videos = self.driver.find_elements(By.TAG_NAME, "video")
                if len(videos) > 0:
                    print("Video trovati nella pagina, assumiamo di essere nella sezione Reels")
                    return True
            except:
                pass
            
            print("Tutti i metodi di navigazione hanno fallito.")
            return False
            
        except Exception as e:
            print(f"Si è verificato un errore durante la navigazione alla sezione Reels: {e}")
            return False
    
    def scroll_to_next_reel(self):
        """
        Scorre al Reel successivo.
        
        Returns:
            bool: True se lo scorrimento ha avuto successo, False altrimenti
        """
        try:
            print("Scorrimento al Reel successivo...")
            
            # Utilizzo di ActionChains per simulare la pressione del tasto freccia giù
            actions = ActionChains(self.driver)
            actions.send_keys(Keys.ARROW_DOWN)
            actions.perform()
            
            # Attesa per il caricamento del nuovo Reel
            self.random_delay(2, 4)
            
            print("Scorrimento al Reel successivo completato.")
            return True
            
        except Exception as e:
            print(f"Si è verificato un errore durante lo scorrimento al Reel successivo: {e}")
            return False
    
    def comment_on_current_reel(self, comment_text):
        """
        Commenta il Reel attualmente visualizzato usando metodi multipli.
        
        Args:
            comment_text (str): Testo del commento da inserire
            
        Returns:
            bool: True se il commento è stato inviato con successo, False altrimenti
        """
        try:
            print(f"Tentativo di commentare il Reel con: '{comment_text}'")
            
            # METODO 1: Cerca il campo di input direttamente, che potrebbe essere già visibile
            try:
                comment_input = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//textarea[contains(@placeholder, 'commento') or contains(@placeholder, 'comment')]"))
                )
                # Se il campo è già visibile, usiamolo direttamente
                self.type_like_human(comment_input, comment_text)
                self.random_delay()
                comment_input.send_keys(Keys.ENTER)
                self.random_delay(2, 4)
                print("Commento inviato con successo! (Metodo 1)")
                self.reels_commented += 1
                return True
            except TimeoutException:
                print("Campo commento non immediatamente visibile, provando a trovare il pulsante commento...")
            
            # METODO 2: Trova e clicca prima il pulsante commento
            try:
                # Prova diversi selettori per il pulsante commento
                selectors = [
                    "//span[@class='_aamw']//div[contains(@aria-label, 'Commenta') or contains(@aria-label, 'Comment')]",
                    "//div[contains(@class, '_aamu')]//div[contains(@class, '_abm0')]",
                    "//span[contains(@class, '_15y0l')]//button",
                    "//div[contains(@aria-label, 'Commenta') or contains(@aria-label, 'Comment')]",
                    "//svg[@aria-label='Commenta' or @aria-label='Comment']",
                    "//span[@role='button' and contains(@class, 'comment')]"
                ]
                
                comment_button = None
                for selector in selectors:
                    try:
                        comment_button = WebDriverWait(self.driver, 3).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        break
                    except:
                        continue
                
                if comment_button:
                    # Clicca sul pulsante commento
                    comment_button.click()
                    self.random_delay(1, 2)
                    
                    # Ora cerca il campo di input
                    comment_input = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, "//textarea[contains(@placeholder, 'commento') or contains(@placeholder, 'comment')]"))
                    )
                    
                    # Inserisci il commento
                    self.type_like_human(comment_input, comment_text)
                    self.random_delay()
                    
                    # Invia il commento
                    comment_input.send_keys(Keys.ENTER)
                    
                    # Attesa per l'invio del commento
                    self.random_delay(2, 4)
                    
                    print("Commento inviato con successo! (Metodo 2)")
                    self.reels_commented += 1
                    return True
                else:
                    print("Nessun pulsante commento trovato con i selettori standard")
            except Exception as e:
                print(f"Errore con il metodo 2: {e}")
            
            # METODO 3: Utilizzo di JavaScript per trovare e interagire con gli elementi
            try:
                print("Tentativo con JavaScript...")
                
                # Trova tutte le aree interattive nella parte inferiore del Reel
                interactive_areas = self.driver.find_elements(By.XPATH, "//section[contains(@class, 'x')]//div[contains(@role, 'button')]")
                
                # Clicca sulla seconda o terza area (spesso corrisponde al pulsante commento)
                if len(interactive_areas) >= 3:
                    self.driver.execute_script("arguments[0].click();", interactive_areas[2])
                elif len(interactive_areas) >= 2:
                    self.driver.execute_script("arguments[0].click();", interactive_areas[1])
                else:
                    raise Exception("Non abbastanza aree interattive trovate")
                
                self.random_delay(1, 2)
                
                # Cerca tutte le textarea sulla pagina
                textareas = self.driver.find_elements(By.TAG_NAME, "textarea")
                if textareas:
                    # Usa la prima textarea trovata
                    self.type_like_human(textareas[0], comment_text)
                    self.random_delay()
                    textareas[0].send_keys(Keys.ENTER)
                    self.random_delay(2, 4)
                    print("Commento inviato con successo! (Metodo 3)")
                    self.reels_commented += 1
                    return True
                else:
                    raise Exception("Nessuna textarea trovata")
            except Exception as e:
                print(f"Errore con il metodo 3: {e}")
            
            # METODO 4: Utilizzo di posizioni fisse per il click (ultima risorsa)
            try:
                print("Tentativo con posizioni fisse...")
                
                # Dimensioni del viewport
                viewport_width = self.driver.execute_script("return window.innerWidth")
                viewport_height = self.driver.execute_script("return window.innerHeight")
                
                # Calcola posizione approssimativa per il commento (parte inferiore centrale)
                comment_x = viewport_width // 2
                comment_y = int(viewport_height * 0.9)  # 90% dall'alto
                
                # Crea azione per cliccare nella posizione
                actions = ActionChains(self.driver)
                actions.move_by_offset(comment_x, comment_y).click().perform()
                
                self.random_delay(1, 2)
                
                # Cerca di nuovo le textarea dopo il click
                textareas = self.driver.find_elements(By.TAG_NAME, "textarea")
                if textareas:
                    self.type_like_human(textareas[0], comment_text)
                    self.random_delay()
                    textareas[0].send_keys(Keys.ENTER)
                    self.random_delay(2, 4)
                    print("Commento inviato con successo! (Metodo 4)")
                    self.reels_commented += 1
                    return True
                else:
                    raise Exception("Nessuna textarea trovata dopo il click")
            except Exception as e:
                print(f"Errore con il metodo 4: {e}")
                
            # Se tutti i metodi falliscono
            print("Tutti i metodi hanno fallito. Impossibile commentare questo Reel.")
            return False
                
        except Exception as e:
            print(f"Si è verificato un errore durante il commento del Reel: {e}")
            return False
    
    def comment_multiple_reels(self, comment_text, num_reels):
        """
        Commenta un numero specificato di Reels con lo stesso testo.
        
        Args:
            comment_text (str): Testo del commento da inserire
            num_reels (int): Numero di Reels da commentare
            
        Returns:
            int: Numero di Reels commentati con successo
        """
        print(f"Iniziando a commentare {num_reels} Reels con il testo: '{comment_text}'")
        
        # Naviga alla sezione Reels
        if not self.navigate_to_reels():
            print("Impossibile navigare alla sezione Reels. Operazione annullata.")
            return 0
        
        self.reels_commented = 0
        
        # Commenta il primo Reel
        self.comment_on_current_reel(comment_text)
        
        # Commenta i Reels successivi
        for i in range(1, num_reels):
            print(f"Procedendo con il Reel {i+1}/{num_reels}...")
            
            # Scorrimento al Reel successivo
            if not self.scroll_to_next_reel():
                print(f"Impossibile scorrere al Reel successivo. Commentati {self.reels_commented} Reels su {num_reels}.")
                break
            
            # Commenta il Reel corrente
            self.comment_on_current_reel(comment_text)
            
            # Aggiunta di un ritardo più lungo tra i commenti per evitare il rilevamento come bot
            self.random_delay(3, 6)
        
        print(f"Operazione completata. Commentati {self.reels_commented} Reels su {num_reels}.")
        return self.reels_commented
    
    def close(self):
        """
        Chiude il browser e termina la sessione.
        """
        if self.driver:
            self.driver.quit()
            print("Browser chiuso e sessione terminata.")

# Funzione principale per test
def main():
    bot = InstagramReelBot(headless=False)
    try:
        # Nota: le credenziali dovrebbero essere fornite dall'utente
        # o caricate da un file di configurazione
        print("Questo è uno script di test. Per utilizzare il bot, fornisci le tue credenziali.")
        print("Esempio di utilizzo:")
        print("bot = InstagramReelBot()")
        print("bot.login('username', 'password')")
        print("bot.comment_multiple_reels('Grande video!', 5)")
    finally:
        bot.close()

if __name__ == "__main__":
    main()