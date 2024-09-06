import socket
import os
import threading
import time

def show_status():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print(f"Hostname: {hostname}")
    print(f"IP Address: {ip_address}")
    time.sleep(10)
    print("Executando em segundo plano...")

def handle_client(conn, addr):
    print(f"Conexão estabelecida com {addr}")

    while True:
        # Recebe dados do cliente
        data = conn.recv(1024).decode('utf-8')
        if not data:
            break

        print(f"Comando recebido: {data}")

        if data.strip().lower() == 'desligar':
            conn.send("Comando recebido".encode('utf-8'))
            print("Desligando o PC...")
            os.system('shutdown /p')  # Comando para Windows
            # os.system('sudo shutdown -h now')  # Comando para Linux
            break

        # Envia resposta ao cliente
        conn.send("Comando recebido".encode('utf-8'))

    conn.close()
    print(f"Conexão com {addr} encerrada. Aguardando nova conexão...")

def main():
    host = '0.0.0.0'  # Escuta em todas as interfaces
    port = 5555

    # Cria o socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    # Cria e inicia a thread para exibir o status
    status_thread = threading.Thread(target=show_status)
    status_thread.start()

    print(f"Servidor aguardando conexões na porta {port}...")

    while True:
        conn, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

if __name__ == "__main__":
    main()
