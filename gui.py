import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os
import sys
from instagram_bot import InstagramReelBot

class InstagramBotGUI:
    """
    Interfaccia grafica per il bot Instagram per commentare i Reels.
    """
    
    def __init__(self, root):
        """
        Inizializza l'interfaccia grafica.
        
        Args:
            root: Finestra principale di Tkinter
        """
        self.root = root
        self.root.title("Instagram Reels Comment Bot")
        self.root.geometry("500x450")
        self.root.resizable(False, False)
        
        # Variabili per memorizzare i valori inseriti dall'utente
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.comment_var = tk.StringVar()
        self.num_reels_var = tk.StringVar(value="5")  # Valore predefinito: 5 Reels
        self.headless_var = tk.BooleanVar(value=False)
        
        # Bot Instagram (verrà inizializzato quando necessario)
        self.bot = None
        
        # Flag per indicare se il bot è in esecuzione
        self.is_running = False
        
        # Creazione dell'interfaccia
        self._create_widgets()
        
        # Configurazione dello stile
        self._configure_style()
    
    def _create_widgets(self):
        """
        Crea i widget dell'interfaccia grafica.
        """
        # Frame principale
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titolo
        title_label = ttk.Label(main_frame, text="Instagram Reels Comment Bot", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Frame per le credenziali
        cred_frame = ttk.LabelFrame(main_frame, text="Credenziali Instagram", padding=10)
        cred_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Username
        username_label = ttk.Label(cred_frame, text="Username:")
        username_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        username_entry = ttk.Entry(cred_frame, textvariable=self.username_var, width=30)
        username_entry.grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)
        
        # Password
        password_label = ttk.Label(cred_frame, text="Password:")
        password_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        password_entry = ttk.Entry(cred_frame, textvariable=self.password_var, show="*", width=30)
        password_entry.grid(row=1, column=1, sticky=tk.W, pady=5, padx=5)
        
        # Frame per le impostazioni del bot
        settings_frame = ttk.LabelFrame(main_frame, text="Impostazioni del Bot", padding=10)
        settings_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Commento
        comment_label = ttk.Label(settings_frame, text="Commento:")
        comment_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        comment_entry = ttk.Entry(settings_frame, textvariable=self.comment_var, width=30)
        comment_entry.grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)
        
        # Numero di Reels
        num_reels_label = ttk.Label(settings_frame, text="Numero di Reels:")
        num_reels_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        num_reels_spinbox = ttk.Spinbox(settings_frame, from_=1, to=100, textvariable=self.num_reels_var, width=5)
        num_reels_spinbox.grid(row=1, column=1, sticky=tk.W, pady=5, padx=5)
        
        # Modalità headless
        headless_check = ttk.Checkbutton(settings_frame, text="Modalità headless (senza interfaccia browser)", variable=self.headless_var)
        headless_check.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Frame per i pulsanti
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Pulsante per avviare il bot
        self.start_button = ttk.Button(button_frame, text="Avvia Bot", command=self._start_bot)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        # Pulsante per fermare il bot
        self.stop_button = ttk.Button(button_frame, text="Ferma Bot", command=self._stop_bot, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # Frame per lo stato
        status_frame = ttk.LabelFrame(main_frame, text="Stato", padding=10)
        status_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Area di testo per i log
        self.log_text = tk.Text(status_frame, height=8, width=50, wrap=tk.WORD, state=tk.DISABLED)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar per l'area di testo
        scrollbar = ttk.Scrollbar(status_frame, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)
    
    def _configure_style(self):
        """
        Configura lo stile dell'interfaccia grafica.
        """
        style = ttk.Style()
        
        # Configurazione dei pulsanti
        style.configure("TButton", font=("Helvetica", 10))
        
        # Configurazione delle etichette
        style.configure("TLabel", font=("Helvetica", 10))
        
        # Configurazione dei frame con etichetta
        style.configure("TLabelframe.Label", font=("Helvetica", 10, "bold"))
    
    def _log(self, message):
        """
        Aggiunge un messaggio all'area di log.
        
        Args:
            message (str): Messaggio da aggiungere
        """
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def _validate_inputs(self):
        """
        Valida gli input dell'utente.
        
        Returns:
            bool: True se gli input sono validi, False altrimenti
        """
        # Verifica che username e password siano stati inseriti
        if not self.username_var.get().strip():
            messagebox.showerror("Errore", "Inserisci il tuo username Instagram.")
            return False
        
        if not self.password_var.get().strip():
            messagebox.showerror("Errore", "Inserisci la tua password Instagram.")
            return False
        
        # Verifica che il commento sia stato inserito
        if not self.comment_var.get().strip():
            messagebox.showerror("Errore", "Inserisci il commento da pubblicare.")
            return False
        
        # Verifica che il numero di Reels sia valido
        try:
            num_reels = int(self.num_reels_var.get())
            if num_reels <= 0:
                raise ValueError("Il numero di Reels deve essere maggiore di zero.")
        except ValueError:
            messagebox.showerror("Errore", "Inserisci un numero valido di Reels.")
            return False
        
        return True
    
    def _start_bot(self):
        """
        Avvia il bot Instagram in un thread separato.
        """
        # Verifica che gli input siano validi
        if not self._validate_inputs():
            return
        
        # Verifica che il bot non sia già in esecuzione
        if self.is_running:
            messagebox.showinfo("Informazione", "Il bot è già in esecuzione.")
            return
        
        # Disabilita il pulsante di avvio e abilita il pulsante di arresto
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        # Imposta il flag di esecuzione
        self.is_running = True
        
        # Avvia il bot in un thread separato
        self._log("Avvio del bot in corso...")
        threading.Thread(target=self._run_bot).start()
    
    def _run_bot(self):
        """
        Esegue il bot Instagram.
        """
        try:
            # Ottieni i valori inseriti dall'utente
            username = self.username_var.get().strip()
            password = self.password_var.get().strip()
            comment = self.comment_var.get().strip()
            num_reels = int(self.num_reels_var.get())
            headless = self.headless_var.get()
            
            # Inizializza il bot
            self._log(f"Inizializzazione del bot in modalità {'headless' if headless else 'normale'}...")
            self.bot = InstagramReelBot(headless=headless)
            
            # Effettua il login
            self._log(f"Tentativo di login come {username}...")
            if not self.bot.login(username, password):
                self._log("Login fallito. Verifica le credenziali.")
                self.root.after(0, self._reset_ui)
                return
            
            # Commenta i Reels
            self._log(f"Inizio commento su {num_reels} Reels...")
            reels_commented = self.bot.comment_multiple_reels(comment, num_reels)
            
            # Verifica se il bot è stato fermato manualmente
            if not self.is_running:
                self._log("Operazione interrotta dall'utente.")
                return
            
            # Mostra il risultato
            self._log(f"Operazione completata. Commentati {reels_commented} Reels su {num_reels}.")
            
        except Exception as e:
            self._log(f"Si è verificato un errore: {e}")
        finally:
            # Chiudi il bot se è stato inizializzato
            if self.bot:
                self._log("Chiusura del browser...")
                self.bot.close()
                self.bot = None
            
            # Reimposta l'interfaccia utente
            self.root.after(0, self._reset_ui)
    
    def _stop_bot(self):
        """
        Ferma il bot Instagram.
        """
        if not self.is_running:
            return
        
        self._log("Arresto del bot in corso...")
        self.is_running = False
        
        # Disabilita il pulsante di arresto
        self.stop_button.config(state=tk.DISABLED)
    
    def _reset_ui(self):
        """
        Reimposta l'interfaccia utente dopo l'esecuzione del bot.
        """
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

def main():
    """
    Funzione principale per avviare l'applicazione.
    """
    root = tk.Tk()
    app = InstagramBotGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
