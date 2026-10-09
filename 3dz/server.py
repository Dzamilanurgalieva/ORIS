import socket
import threading
import protocol as proto

HOST = "0.0.0.0"
PORT = 5556

tasks = []
tasks_lock = threading.Lock()


def format_tasks():
    with tasks_lock:
        if not tasks:
            return "(список задач пуст)"
        lines = []
        for i, task in enumerate(tasks, start=1):
            mark = "x" if task["done"] else " "
            lines.append(f"{i}. [{mark}] {task['text']}")
        return "\n".join(lines)


def handle_client(sock, addr):
    print(f"[+] клиент подключился: {addr}")
    try:
        while True:
            msg = proto.recv_message(sock)
            if msg is None:
                break

            command, payload = msg
            text = payload.decode("utf-8", errors="replace").strip()

            if command == "ADD":
                if not text:
                    proto.send_message(sock, "ERROR", b"usage: /add <text>")
                else:
                    with tasks_lock:
                        tasks.append({"text": text, "done": False})
                    proto.send_message(sock, "TEXT", b"* task added")

            elif command == "LIST":
                body = format_tasks().encode("utf-8")
                proto.send_message(sock, "TEXT", body)

            elif command == "DONE":
                if not text.isdigit():
                    proto.send_message(sock, "ERROR", b"usage: /done <number>")
                else:
                    n = int(text)
                    with tasks_lock:
                        if 1 <= n <= len(tasks):
                            tasks[n - 1]["done"] = True
                            ok = True
                        else:
                            ok = False
                    if ok:
                        proto.send_message(sock, "TEXT",
                                           f"* task {n} marked as done".encode("utf-8"))
                    else:
                        proto.send_message(sock, "ERROR",
                                           f"no task with number {n}".encode("utf-8"))

            elif command == "DELETE":
                if not text.isdigit():
                    proto.send_message(sock, "ERROR", b"usage: /delete <number>")
                else:
                    n = int(text)
                    with tasks_lock:
                        if 1 <= n <= len(tasks):
                            tasks.pop(n - 1)
                            ok = True
                        else:
                            ok = False
                    if ok:
                        proto.send_message(sock, "TEXT",
                                           f"* task {n} deleted".encode("utf-8"))
                    else:
                        proto.send_message(sock, "ERROR",
                                           f"no task with number {n}".encode("utf-8"))

            elif command == "QUIT":
                proto.send_message(sock, "TEXT", b"* bye")
                break

            else:
                proto.send_message(sock, "ERROR",
                                   f"unknown command {command}".encode("utf-8"))

    except ConnectionResetError:
        print(f"[!] {addr} - соединение сброшено")
    except BrokenPipeError:
        print(f"[!] {addr} - не удалось отправить")
    finally:
        sock.close()
        print(f"[-] клиент отключился: {addr}")


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()
        print(f"[*] сервер слушает {HOST}:{PORT}")
        while True:
            client_sock, addr = server.accept()
            threading.Thread(
                target=handle_client,
                args=(client_sock, addr),
                daemon=True
            ).start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[*] сервер остановлен")