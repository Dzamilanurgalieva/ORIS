import socket
import threading
import protocol as proto

HOST = "127.0.0.1"
PORT = 5556


def listen_loop(sock, stop_event):
    while not stop_event.is_set():
        try:
            msg = proto.recv_message(sock)
        except (ConnectionResetError, OSError):
            msg = None

        if msg is None:
            print("\n[!] соединение с сервером потеряно")
            stop_event.set()
            break

        command, payload = msg
        text = payload.decode("utf-8", errors="replace")

        if command == "ERROR":
            print(f"\n[ошибка] {text}\n> ", end="")
        else:
            print(f"\n{text}\n> ", end="")


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))
    except (ConnectionRefusedError, OSError) as e:
        print(f"Не удалось подключиться: {e}")
        return

    stop_event = threading.Event()
    threading.Thread(
        target=listen_loop,
        args=(sock, stop_event),
        daemon=True
    ).start()

    print("Команды: /add <текст>, /list, /done <номер>, /delete <номер>, /quit")
    try:
        while not stop_event.is_set():
            line = input("> ").strip()

            if line == "/quit":
                proto.send_message(sock, "QUIT")
                break

            elif line == "/list":
                proto.send_message(sock, "LIST")

            elif line.startswith("/add "):
                text = line[5:].strip()
                if text:
                    proto.send_message(sock, "ADD", text.encode("utf-8"))
                else:
                    print("Использование: /add <текст>")

            elif line.startswith("/done "):
                num = line[6:].strip()
                proto.send_message(sock, "DONE", num.encode("utf-8"))

            elif line.startswith("/delete "):
                num = line[8:].strip()
                proto.send_message(sock, "DELETE", num.encode("utf-8"))

            elif line:
                print("Неизвестная команда. Доступны: /add, /list, /done, /delete, /quit")

    except (EOFError, KeyboardInterrupt, BrokenPipeError, OSError):
        pass
    finally:
        stop_event.set()
        sock.close()


if __name__ == "__main__":
    main()