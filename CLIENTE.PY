import socket
import threading

def receber_mensagens(client_socket):
    while True:
        try:
            
            resposta = client_socket.recv(1024).decode('utf-8')
            if resposta:
                
                print(f"\n{resposta.strip()}")
        except Exception as e:
            print(f"Erro ao receber a mensagem: {e}")
            break

def run_client():
    
    SERVER_IP = "192.168.216.1"  
    SERVER_PORT = 0000

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    try:
        print(f"Conectando ao servidor em {SERVER_IP}:{SERVER_PORT}...")
        client_socket.connect((SERVER_IP, SERVER_PORT))
        print("Conexão estabelecida!")
   
        nome_cliente = input("Digite seu nome: ")
        client_socket.sendall(nome_cliente.encode('utf-8'))
    
        welcome_msg = client_socket.recv(1024).decode('utf-8')
        print(welcome_msg.strip())  
        threading.Thread(target=receber_mensagens, args=(client_socket,), daemon=True).start()

        while True:      
            mensagem = input(f"{nome_cliente}: ").strip()
            if mensagem.lower() == 'sair':
                break          
            client_socket.sendall(mensagem.encode('utf-8'))

    except ConnectionRefusedError:
        print("Erro: Não foi possível conectar ao servidor. Verifique:")
    except ConnectionResetError:
        print("Erro: Conexão com o servidor foi perdida.")
    except Exception as e:
        print(f"Erro inesperado: {e}")
    finally:
        
        client_socket.close()
        print("Conexão encerrada.")

if __name__ == "__main__":
    print("Cliente de Chat Distribuído")
    print("---------------------------")
    run_client()
