import socket
import pickle
import threading
from psycopg2 import connect
from dotenv import load_dotenv
from os import environ

# Client -> Server: Fixed + Custom Size (SQL arguments are unknown)
HEADER_FIX_SIZE = 2
# Server -> Client: Fixed Size, no SQL arguments
HEADER_FEEDBACK_SIZE = 5


BUFFER = 1024
APP_IP = ""
APP_PORT = 1248

FORMAT = "utf-8"

whitelist = []
desc_list = []
db_connector = None
db_cursor = None


# setting up the database
def connect_to_database():
    global db_cursor, db_connector
    try:
        print("Trying to get .env data...")
        load_dotenv()
        database_url = environ.get("HEROKU_POSTGRESQL_BLUE_URL")
        password_db = environ.get("password_db")
        user_db = environ.get("user_db")
        name_db = environ.get("name_db")
        port_db = environ.get("port_db")
        db_connector = connect(str(database_url), user=str(user_db), port=port_db, dbname=str(name_db),
                               password=str(password_db))
        db_cursor = db_connector.cursor()
    except KeyError as e:
        print(f"ERROR: {e}. Program to be terminated.")
        exit()
    else:
        print("Loaded .env from the system path.")
    

#  Functions
def update_whitelist():
    global whitelist, desc_list
    db_cursor.execute("SELECT ip, description FROM ew_ips")
    whitelist, desc_list = zip(*db_cursor.fetchall())


def update_ip():
    global APP_IP
    hostname = socket.gethostname()
    APP_IP = socket.gethostbyname(hostname)
    print(f"debug ip: {APP_IP}")


def handle_data(client_socket, address):
    try:
        idx = whitelist.index(address)
    except ValueError:
        client_socket.sendall(bytes("Access was denied. Contact with the creator of the tool for help.", FORMAT))
        client_socket.close()
        return
    else:
        print(f"Connection from {address} aka {desc_list[idx]} has been established")
    
    full_data = b""
    new_msg = True
    msg_len = -1
    header_custom_size = 0  # placeholder value
    headers_sizes = []  # list of integers, data + SQL args if relevant

    # getting the data
    while True:
        p_data = client_socket.recv(BUFFER)  # bytes type
        # handling the header
        if new_msg:
            header_custom_size = int(p_data[:HEADER_FIX_SIZE].decode(FORMAT))  # int, constant
            headers_sizes = pickle.loads(p_data[HEADER_FIX_SIZE:HEADER_FIX_SIZE + header_custom_size])  # a list
            if len(headers_sizes) == 2:
                msg_len = sum(headers_sizes)
            else:
                msg_len = headers_sizes[0]
        # checking for the end
        if len(p_data) <= 0:
            if len(full_data) - (HEADER_FIX_SIZE + header_custom_size) == msg_len:
                print("Transfer succeeded")
            elif len(full_data) - (HEADER_FIX_SIZE + header_custom_size) > msg_len:
                print(f"ERROR: Incorrect header setting, received data too long.\n"
                      f"Custom size: {header_custom_size} for value: {headers_sizes}\n"
                      f"String of the data: {pickle.loads(full_data)}")
                client_socket.close()
                return
            else:
                print(f"ERROR: Received data too short, possible connection issue or incorrect header setting.\n"
                      f"Custom size: {header_custom_size} for value: {headers_sizes}\n"
                      f"String of the data: {pickle.loads(full_data)}")
                client_socket.close()
                return
            break
        # removing the header, accumulating the data
        if new_msg:
            full_data = p_data[HEADER_FIX_SIZE + header_custom_size:]
            new_msg = False
        else:
            full_data += p_data
    
    # Preparing and using the data
    if len(headers_sizes) == 2:
        sql_request = pickle.loads(full_data[:headers_sizes[0]])
        sql_arguments = pickle.loads(full_data[headers_sizes[0]:])
    else:
        sql_request = pickle.loads(full_data)
        sql_arguments = set()
    
    # taking requested data from the database
    db_cursor.execute(sql_request, sql_arguments)
    db_data = db_cursor.fetchall()
    
    # serialising and sending back
    ser_data = pickle.dumps(db_data)
    client_socket.sendall(bytes(f"{len(db_data):<{HEADER_FEEDBACK_SIZE}}", FORMAT)+ser_data)
    client_socket.close()


def main_loop():
    # setting up connection
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)  # reconnecting?
    s.bind((APP_IP, APP_PORT))
    s.listen(5)
    while True:
        conn, address = s.accept()
        thread = threading.Thread(target=handle_data, args=(conn, address))
        thread.start()


#  getting things started
connect_to_database()
update_whitelist()
update_ip()
main_loop()
