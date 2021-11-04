import socket
import pickle


# Client -> Server: Fixed + Custom Size (SQL arguments are unknown)
HEADER_FIX_SIZE = 2
# Server -> Client: Fixed Size, no SQL arguments
HEADER_FEEDBACK_SIZE = 5

BUFFER = 1024
APP_URL = "https://eventwriter.herokuapp.com/" # isn't valid anymore
APP_PORT = 1248

FORMAT = "utf-8"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def connect():
    global s
    s.connect((APP_URL, APP_PORT))


def disconnect():
    global s
    s.close()


def get_data():
    full_data = b""
    new_msg = True
    header = "ERROR: didn't receive the header"

    while True:
        p_data = s.recv(1024)  # bytes type
        # handling the header
        if new_msg:
            header = int(pickle.loads(p_data[:HEADER_FEEDBACK_SIZE]))
        # checking for the end
        if len(p_data) <= 0:
            if len(full_data) == header:
                print("Transfer succeeded")
            elif len(full_data) > header:
                print(f"ERROR: Incorrect heading setting, received data too long.\n"
                      f"Header: {header}\nString of the data: {pickle.loads(full_data)}")
            else:
                print(f"ERROR: Received data too short, possible connection issue or incorrect heading setting.\n"
                      f"Header: {header}\nString of the data: {pickle.loads(full_data)}")
            break
        # removing the header, accumulating the data
        if new_msg:
            full_data = p_data[HEADER_FEEDBACK_SIZE:]
            new_msg = False
        else:
            full_data += p_data

    return pickle.loads(full_data)


def send_data(data, arguments=None):
    """
    :param data: todo
    :param arguments:
    """
    if arguments:
        actual_data = [pickle.dumps(data), pickle.dumps(arguments)]
        length_data = pickle.dumps([len(actual_data[0]), len(actual_data[1])])
    else:
        actual_data = pickle.dumps(data)
        length_data = pickle.dumps(len(actual_data))

    # length data is kind of custom size header
    fix_header = bytes(f"{len(length_data):<{HEADER_FIX_SIZE}}", FORMAT)  # HEADER_FIX_SIZE - padding
    s.sendall(b"".join([fix_header, length_data, actual_data]))
