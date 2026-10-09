import struct

HEADER_FORMAT = "!II"
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
MAX_MESSAGE_SIZE = 10 * 1024 * 1024
MAX_COMMAND_SIZE = 64


def recv_exact(sock, size):
    chunks = bytearray()
    while len(chunks) < size:
        chunk = sock.recv(size - len(chunks))
        if not chunk:
            raise ConnectionError("соединение закрыто до получения всех данных")
        chunks.extend(chunk)
    return bytes(chunks)


def send_message(sock, command, payload=b""):
    command_bytes = command.encode("utf-8")
    if len(command_bytes) > MAX_COMMAND_SIZE:
        raise ValueError(f"команда слишком длинная: {len(command_bytes)}")
    if len(payload) > MAX_MESSAGE_SIZE:
        raise ValueError(f"payload слишком большой: {len(payload)}")
    header = struct.pack(HEADER_FORMAT, len(command_bytes), len(payload))
    sock.sendall(header + command_bytes + payload)


def recv_message(sock):
    try:
        header = recv_exact(sock, HEADER_SIZE)
    except (ConnectionError, OSError):
        return None
    cmd_len, payload_len = struct.unpack(HEADER_FORMAT, header)
    if cmd_len > MAX_COMMAND_SIZE:
        raise ValueError(f"заявленная длина команды {cmd_len} превышает лимит")
    if payload_len > MAX_MESSAGE_SIZE:
        raise ValueError(f"заявленная длина {payload_len} превышает лимит")
    command_bytes = recv_exact(sock, cmd_len) if cmd_len else b""
    payload = recv_exact(sock, payload_len) if payload_len else b""
    return command_bytes.decode("utf-8"), payload