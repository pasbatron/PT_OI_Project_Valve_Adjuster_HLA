import os
import time
def shutdown_computer():
    time.sleep(7)
    os.system("sudo shutdown -h now")

if __name__ == "__main__":
    shutdown_computer()
