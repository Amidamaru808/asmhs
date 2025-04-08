import socket
import cv2
import numpy as np
import keyboard

def read_exact(client_socket, size):
    data = b""
    while len(data) < size:
        packet = client_socket.recv(size - len(data))
        if not packet:
            break
        data += packet
    return data

def send_command(client_socket, command):
    try:
        marker = b'C'

        data_to_send = marker + command.encode('utf-8')

        print(f"Sending data: {data_to_send}")

        client_socket.sendall(data_to_send)
        print(f"Sent command: {command}")
    except Exception as e:
        print(f"Failed to send command: {e}")

def main():
    server_ip = "192.168.1.66" #ВСТАВИТЬ IP
    server_port = 12242 #ВСТАВИТЬ ПОРТ

    width, height = 848, 480

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        print(f"Connecting to server {server_ip}:{server_port}...")
        client_socket.connect((server_ip, server_port))
        print("Connection established!")

        while True:
            if keyboard.is_pressed('1'):
                send_command(client_socket, "10500")

            if keyboard.is_pressed('2'):
                send_command(client_socket, "2")

            marker = read_exact(client_socket, 1)
            if not marker:
                break

            if marker == b'A':
                session_data = read_exact(client_socket, 2)
                session_number = int.from_bytes(session_data, byteorder='big')
                print(f"Received SessionNumber: {session_number}")

                status_data = read_exact(client_socket, 1)
                niagara_status = int.from_bytes(status_data, byteorder='big')
                print(f"Niagara Component Status: {'Active' if niagara_status == 1 else 'Inactive'}")

                size_data = read_exact(client_socket, 4)
                image_size = int.from_bytes(size_data, byteorder='big')
                print(f"Image size: {image_size} bytes")

                image_data = read_exact(client_socket, image_size)
                if not image_data:
                    print("Failed to receive image data")
                    break

                try:
                    rgb_array = np.frombuffer(image_data, dtype=np.uint8).reshape((height, width, 3))
                    bgr_array = cv2.cvtColor(rgb_array, cv2.COLOR_RGB2BGR)
                    cv2.imshow("client window", bgr_array)
                except Exception as e:
                    print(f"Failed to process image: {e}")

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            else:
                print(f"Unknown marker: {marker}")

    except ConnectionRefusedError:
        print(f"Cannot connect to server {server_ip}:{server_port}. Is the server running?")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Closing connection...")
        client_socket.close()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
