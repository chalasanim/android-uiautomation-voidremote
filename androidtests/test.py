from voidremote import VoidRemote
import time

client = VoidRemote()

client.start()


#grab the first connected device



device = client.devices().first()

print("Connected to ", device)

#---Basic actions --

#1. screen shot to device

device.screenshot("screen.png")

print("screen shot  saved as  screen.png")

#2. List installed packages (to help finding the app under test package)

packages = device.list_packages()

print(" Packages installed: ")
for p in packages:
    print(" ", p)


#3 press the home key
device.key_event(3)

time.sleep(1)

#4. press somewhere into device screen

device.tap(500,1000)
time.sleep(1)

#5. press back key

device.key_event(4)

print([m for m in dir(client) if not m.startswith('_')])

client.close()
print("Done")

