import os, sys
import time

print("> Starting capture")
os.system("gnome-terminal -- sudo motion")

while True:
  file_list = os.listdir("/var/lib/motion")

  if not file_list:
    print("> No image")
    time.sleep(5)
    continue

  else:
    file_name = file_list[len(file_list) // 2]
    os.system("sshpass -p abcdefg scp /var/lib/motion/" + file_name + " pi@192.168.112.10:~/Desktop")
    time.sleep(5)
    print("> Transfered " + file_name)

    os.system("sudo rm /var/lib/motion/*")
    print("> Cleared existing images")

