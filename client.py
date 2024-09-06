import socket
import ipaddress
import logging

# Configura o logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def scan_subnet(subnet, port=5555, timeout=1, retries=1):
    logging.info(f"Escaneando a subnet: {subnet}")
    addresses = []
    network = ipaddress.ip_network(subnet)
    
    for ip in network.hosts():
        logging.debug(f"Verificando IP: {ip}")
        for attempt in range(retries):
            try:
                logging.debug(f"Tentativa {attempt + 1} de conectar ao IP {ip} na porta {port}")
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.settimeout(timeout)
                result = client_socket.connect_ex((str(ip), port))
                
                if result == 0:
                    logging.info(f"Dispositivo encontrado: {ip}")
                    addresses.append(str(ip))
                    break
                else:
                    logging.debug(f"Conexão falhou com o IP {ip} na tentativa {attempt + 1}")
                client_socket.close()
            except Exception as e:
                logging.error(f"Erro ao escanear o IP {ip} na tentativa {attempt + 1}: {e}")
    
    logging.info(f"Total de dispositivos encontrados: {len(addresses)}")
    return addresses

def save_addresses_to_file(addresses, filename='addresses.txt'):
    with open(filename, 'w') as file:
        for address in addresses:
            file.write(f"{address}\n")
    logging.info(f"Endereços salvos no arquivo {filename}")

def load_addresses_from_file(filename='addresses.txt'):
    try:
        with open(filename, 'r') as file:
            addresses = [line.strip() for line in file.readlines()]
        logging.info(f"Endereços carregados do arquivo {filename}")
        return addresses
    except FileNotFoundError:
        logging.error(f"Arquivo {filename} não encontrado")
        return []

def send_command(command, server_addresses):
    for server_address in server_addresses:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            logging.info(f"Conectando ao servidor: {server_address}")
            client_socket.connect(server_address)
            
            logging.info(f"Enviando comando: {command} para {server_address}")
            client_socket.sendall(command.encode('utf-8'))
            
            response = client_socket.recv(1024)
            logging.info(f"Resposta do servidor {server_address}: {response.decode('utf-8')}")
        except Exception as e:
            logging.error(f"Erro ao conectar ao servidor {server_address}: {e}")
        finally:
            client_socket.close()
            logging.info(f"Conexão fechada com o servidor: {server_address}")

if __name__ == "__main__":
    subnet = '192.168.0.0/24'
    
    choice = input("Deseja escanear a rede novamente? (s/n): ").strip().lower()
    
    if choice == 's':
        ip_addresses = scan_subnet(subnet)
        save_addresses_to_file(ip_addresses)
    else:
        ip_addresses = load_addresses_from_file()
    
    server_addresses = [(ip, 5555) for ip in ip_addresses]
    
    send_command("desligar", server_addresses)
