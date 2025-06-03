#!/usr/bin/env python3
"""
Instagram Reels Comment Bot - Interfaccia a riga di comando (CLI)
Questo script permette di utilizzare il bot Instagram per commentare i Reels tramite riga di comando.
"""

import argparse
import getpass
import sys
import time
from instagram_bot import InstagramReelBot

def main():
    """
    Funzione principale per l'interfaccia a riga di comando.
    """
    # Configurazione del parser degli argomenti
    parser = argparse.ArgumentParser(description="Instagram Reels Comment Bot - CLI")
    
    # Argomenti opzionali
    parser.add_argument("-u", "--username", help="Username Instagram")
    parser.add_argument("-c", "--comment", help="Commento da inserire nei Reels")
    parser.add_argument("-n", "--num-reels", type=int, default=5, help="Numero di Reels da commentare (default: 5)")
    parser.add_argument("--headless", action="store_true", help="Esegui in modalità headless (senza interfaccia browser)")
    
    # Parsing degli argomenti
    args = parser.parse_args()
    
    # Richiedi username se non fornito
    username = args.username
    if not username:
        username = input("Inserisci il tuo username Instagram: ")
    
    # Richiedi password (non mostrata durante la digitazione)
    password = getpass.getpass("Inserisci la tua password Instagram: ")
    
    # Richiedi commento se non fornito
    comment = args.comment
    if not comment:
        comment = input("Inserisci il commento da pubblicare: ")
    
    # Conferma numero di Reels
    num_reels = args.num_reels
    print(f"Verranno commentati {num_reels} Reels.")
    
    # Conferma modalità headless
    headless = args.headless
    if headless:
        print("Il bot verrà eseguito in modalità headless (senza interfaccia browser).")
    
    # Chiedi conferma all'utente
    confirm = input("Vuoi procedere? (s/n): ")
    if confirm.lower() not in ["s", "si", "sì", "y", "yes"]:
        print("Operazione annullata.")
        sys.exit(0)
    
    # Inizializza e avvia il bot
    try:
        print("\nInizializzazione del bot...")
        bot = InstagramReelBot(headless=headless)
        
        print(f"Tentativo di login come {username}...")
        if not bot.login(username, password):
            print("Login fallito. Verifica le credenziali.")
            return
        
        print(f"Inizio commento su {num_reels} Reels...")
        reels_commented = bot.comment_multiple_reels(comment, num_reels)
        
        print(f"Operazione completata. Commentati {reels_commented} Reels su {num_reels}.")
        
    except KeyboardInterrupt:
        print("\nOperazione interrotta dall'utente.")
    except Exception as e:
        print(f"Si è verificato un errore: {e}")
    finally:
        if 'bot' in locals():
            print("Chiusura del browser...")
            bot.close()

if __name__ == "__main__":
    main()
