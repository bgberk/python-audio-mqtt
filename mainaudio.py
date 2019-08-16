# python mainaudio.py -v 1 -s 192.168.254.17

import os
import argparse,time
import pygame
import paho.mqtt.client as paho

parser = argparse.ArgumentParser()
parser.add_argument("-s","--server", default="127.0.0.1", help="The IP address of the MQTT server")
parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1],  default=0,
                    help="increase output verbosity")
args = parser.parse_args()

def task_music():
    pygame.mixer.music.load("./combinedthemes.wav")
    pygame.mixer.music.play()
   
def task_success1():
    success1 = pygame.mixer.Sound("./success1.wav")
    success1.play()

def task_failure3():
    failure3 = pygame.mixer.Sound("./failure3.wav")
    failure3.play()

def task_incVolume():
    currVolume = pygame.mixer.music.get_volume();
    newVolume = currVolume + 0.1;
    pygame.mixer.music.set_volume(newVolume)

def task_decVolume():
    currVolume = pygame.mixer.music.get_volume();
    newVolume = currVolume - 0.1;
    pygame.mixer.music.set_volume(newVolume)

def task_stop():
    pygame.mixer.music.fadeout(2000)
    pygame.mixer.fadeout(2000)

def task_start():
    darkTheme = pygame.mixer.Sound("./darktheme.wav")
    combinedThemes = pygame.mixer.Sound("./combinedthemes.wav")
    channel1.play(darkTheme)
    channel2.play(combinedThemes)
    channel2.set_volume(0)
    # darkTheme.play()
    # combinedThemes.play(fade_ms=5000)
    # combinedThemes.set_volume(0)

def task_fade():
    for i in range(1, 100, 1):
        vol = i/100.0
        channel2.set_volume(vol)
        channel1.set_volume(1-vol)
        time.sleep(0.05)

def task_analyze():
    print("channel 1 volume: ")
    print(channel1.get_volume())

    print("channel 2 volume: ")
    print(channel2.get_volume())    

def task_doh():
    print("SOUNDPLAYER DOH!")
    pygame.mixer.music.load("../sounds/doh.wav") 
    pygame.mixer.music.play()

def on_message(mosq, obj, msg):

        print("SOUNDPLAYER: Message received on topic "+msg.topic+" with payload "+msg.payload)
        print(len(msg.payload));
        if(msg.payload=="SUCCESS1"):
            task_success1()

        if(msg.payload=="MUSIC"):
            task_music()

        if(msg.payload=="VOLUP"):
            task_incVolume()

        if(msg.payload=="VOLDN"):
            task_decVolume()

        if(msg.payload=="FAILURE3"):
            task_failure3()

        if(msg.payload=="STOP"):
            task_stop()

        if(msg.payload=="START"):
            task_start()

        if(msg.payload=="FADE"):
            task_fade()

        if(msg.payload=="ANALYZE"):
            task_analyze()

print("SOUNDPLAYER: Connecting")
mypid = os.getpid()
client = paho.Client("sound_broker_"+str(mypid))
client.connect(args.server)
connect_time=time.time()
client.on_message = on_message
client.subscribe('/raspberry/1/incoming',0)

pygame.mixer.init()

channel1 = pygame.mixer.Channel(0)
channel2 = pygame.mixer.Channel(1)

try:
    while client.loop()==0:
        pass

except KeyboardInterrupt:
    print('SOUNDPLAYER: Interrupt')
    client.unsubscribe("/raspberry/1/incoming")
    client.disconnect()