import socket
import tqdm
import os
from tkinter import *
from tkinter import filedialog

separator = '<SEPARATOR>'
buffer_size = 4096

ui = Tk()
ui.title("FileShare")

# Inputs for IP, port, buffersize
ipLabel = Label(ui, text="Connecting IP:").grid(row=1, column=0)
ip = Entry(ui, width=40, borderwidth=3)
ip.grid(row=1, column=1)

portLabel = Label(ui, text="TCP Port:").grid(row=2, column=0)
portInput = Entry(ui, width=40, borderwidth=3)
portInput.grid(row=2, column=1)

bufferLabel = Label(ui, text="Buffer Size:").grid(row=3, column=0)
bufferInput = Entry(ui, width=40, borderwidth=3)
bufferInput.insert(0, "4096")
bufferInput.grid(row=3, column=1)

# Button that brings up the file selector
filepath = None
filesize = None


def selectFile():
    ui.filename = filedialog.askopenfilename(initialdir='C:\\', title="Select File")
    global filepath
    global filesize
    filepath = ui.filename
    filesize = os.path.getsize(filepath)
    fileLabel = Label(ui, text=ui.filename).grid(row=4, column=1)


fileButton = Button(ui, text="Select File", padx=10, pady=10, command=selectFile).grid(row=4, column=0)


# Button that actually parses the text boxes and sends stuff
def sendFile():
    host = ip.get()
    port = int(portInput.get())
    buffer_size = int(bufferInput.get())

    s = socket.socket()
    s.connect((host, port))

    s.send(f"{filepath}{separator}{filesize}".encode())
    progress = tqdm.tqdm(range(filesize), f"Sending {filepath}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filepath, "rb") as f:
        for _ in progress:
            bytes_read = f.read(buffer_size)
            if not bytes_read:
                break
            s.sendall(bytes_read)
            progress.update(len(bytes_read))
    s.close()


sendButton = Button(ui, text="Send File", padx=20, pady=20, command=sendFile).grid(row=5, column=0)


# Button that parses text boxes and sets up for receiving
def receiveFiles():
    host = '0.0.0.0'
    port = int(portInput.get())
    buffer_size = int(bufferInput.get())
    print("done parse")
    s = socket.socket()
    s.bind((host, port))
    s.listen(2)
    print(f"Listening as {host} on TCP port {port}")
    client_socket, address = s.accept()
    print(f"{address} connected on TCP port {port}")

    received = client_socket.recv(buffer_size).decode()
    filepath, filesize = received.split(separator)
    filename = os.path.basename(filepath)
    filesize = int(filesize)

    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        for _ in progress:
            bytes_read = client_socket.recv(buffer_size)
            if not bytes_read:
                break
            f.write(bytes_read)
            progress.update(len(bytes_read))

    client_socket.close()


receiveButton = Button(ui, text="Receive Files", padx=20, pady=20, command=receiveFiles).grid(row=5, column=1)
# UI looper, don't remove
ui.mainloop()
