from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import subprocess
import time

class MyHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.has_reacted = False

    def on_modified(self, event):
        print(f'File {event.src_path} has been modified')
        self.react_to_event(event)

    def react_to_event(self, event):
        # If a file in the sensitive directory is modified, block Computer A
        if not self.has_reacted:
            subprocess.call(f'netsh advfirewall firewall add rule name="BlokirajSSHPovezavo" dir=in action=block remoteip=192.168.1.10', shell=True)
            print(f'Blokiran omrežni promet od računalnika A zaradi sumljivih sprememb imen datotek')
            self.has_reacted = True

if __name__ == "__main__":
    path = r"C:\Users\jasag\OneDrive\Desktop\Privat"
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
