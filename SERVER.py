import socket
import multiprocessing

def handle_client(client_socket, client_address, clientes, cliente_nome):
    try:
        client_socket.sendall(f"Bem-vindo, {cliente_nome}! Envie suas mensagens para todos os clientes conectados.\n".encode('utf-8'))
        
        while True:
            mensagem = client_socket.recv(1024).decode('utf-8').strip()
            
            if not mensagem:  
                break 
            print(f"Mensagem de {cliente_nome} ({client_address}): {mensagem}")

            
            for cliente in clientes:
                if cliente != client_socket:  
                    try:
                        cliente.sendall(f"{cliente_nome}: {mensagem}\n".encode('utf-8'))
                    except Exception as e:
                        print(f"Erro ao enviar para um cliente: {e}")

    except Exception as e:
        print(f"Erro ao lidar com cliente {cliente_nome}: {e}")
    finally:
        print(f"{cliente_nome} desconectado.")
        clientes.remove(client_socket)
        client_socket.close()

def start_server():
    SERVER_IP = '0.0.0.0'  
    SERVER_PORT = 0000
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(5)
    print(f"Servidor ouvindo em {SERVER_IP}:{SERVER_PORT}...")

    clientes = []
    
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Novo cliente conectado: {client_address}")
            
            
            client_socket.sendall("Digite seu nome: ".encode('utf-8'))
            cliente_nome = client_socket.recv(1024).decode('utf-8').strip()
            
            
            clientes.append(client_socket)
            
            
            process = multiprocessing.Process(target=handle_client, args=(client_socket, client_address, clientes, cliente_nome))
            process.start()

    except KeyboardInterrupt:
        print("\nServidor sendo desligado...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
