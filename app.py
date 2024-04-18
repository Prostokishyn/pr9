import time
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"{timestamp} - {event.event_type}: {event.src_path}\n"
        with open('event_log.txt', 'a', encoding='cp1251') as log_file:
            log_file.write(log_message)

class FileMonitor:
    def __init__(self, path):
        self.path = path
        self.event_handler = MyHandler()
        self.observer = Observer()
        self.observer.schedule(self.event_handler, path, recursive=True)

    def start(self):
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

def analyze_file_changes():
    log_df = pd.read_csv('event_log.txt', names=['Timestamp', 'Event Type', 'File Path'], delimiter=' - ', encoding='cp1251')
    
    print("Останні події:")
    print(log_df.tail())
    
    print("\nАналіз останньої події:")
    last_event = log_df.iloc[-1]
    print(f"Час події: {last_event['Timestamp']}")
    print(f"Тип події: {last_event['Event Type']}")
    print(f"Шлях до файлу: {last_event['File Path']}")

if __name__ == "__main__":
    path_to_monitor = r'D:\TEST'
    file_monitor = FileMonitor(path_to_monitor)
    file_monitor.start()
    analyze_file_changes()
