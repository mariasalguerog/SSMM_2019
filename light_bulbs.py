from lifxlan import Light, LifxLAN

import ConfigParser
import paho.mqtt.client as mqtt
import time
# import os
# from subprocess import call

config = ConfigParser.RawConfigParser()
lifx = LifxLAN()

#Detect devices available and store them on a list (devices)
devices = lifx.get_devices()
num_lights = len(devices)

print (" ======================== LIGHTS =========================")
print
print
print ("Number of lights found: " + num_lights.__str__())
print
print

#Conocemos la MAC, asignamos segun la MAC
                    ####### LIGHT DATA ######
# bulbTV ---> 'd0:73:d5:10:7f:33', '192.168.0.102' #FUNCIONA
# bulbWin ---> 'D0:73:D5:2D:52:AF', '192.168.0.116' #FUNCIONA
# bulbWinVieja ---> 'd0:73:d5:10:7b:0e'
index = 0
bulbWin = None
bulbTV = None
stateBulbWin = False
stateBulbTV = False

while index < num_lights:
    bulbAux = devices[index]
    nameSplit = bulbAux.mac_addr.split(":")
    if nameSplit[5] == "33":
        print ("MAC termina en 33. Bombilla TV")
        bulbTV = bulbAux

        print ("                    TIPO DE BULBTV: ")
        print ("                    " + str(type.__str__(bulbTV)))
        print
        print

    elif nameSplit[5] == "af":
        print ("MAC temina en AF. Bombilla WIN")
        bulbWin = bulbAux

        print ("                    TIPO DE BULBWIN: ")
        print ("                    " + str(type.__str__(bulbWin)))
        print
        print

    elif nameSplit[5] == "0e":
        print ("MAC termina en 0e. Bombilla Win")
        bulbWin = bulbAux

        print ("                    TIPO DE BULBWIN: ")
        print ("                    " + str(type.__str__(bulbWin)))
        print
        print

    index += 1


# Como no tiene memoria, apagamos y guardamos el estado apagado
if bulbTV is not None:
    bulbTV.set_power(False)
    stateBulbTV = False
    print (" ======= BULB TV =======")
    if stateBulbTV:
        print ("STATE: ON")
    else:
        print ("STATE: OFF")
    print ("MAC: " + bulbTV.mac_addr)
    print ("IP:  " + bulbTV.ip_addr)
    print

if bulbWin is not None:
    bulbWin.set_power(False)
    stateBulbWin = False
    print (" ======= BULB WIN =======")
    if stateBulbWin:
        print ("STATE: ON")
    else:
        print ("STATE: OFF")
    print ("MAC: " + bulbWin.mac_addr)
    print ("IP:  " + bulbWin.ip_addr)
    print

time.sleep(2)

##################################################
#                GET PARAMETERS                  #
##################################################


def get_color (light):
    index = 0
    while index < num_lights:
        if light.mac_addr == devices[index].mac_addr:
            return light.get_color()[0]
        index += 1


def get_intensity(light):
    index = 0
    while index < num_lights:
        if light.mac_addr == devices[index].mac_addr:
            return light.get_color()[1]
        index += 1


def get_brightness(light):
    index = 0
    while index < num_lights:
        if light.mac_addr == devices[index].mac_addr:
            return light.get_color()[2]
        index += 1


def get_warm(light):
    index = 0
    while index < num_lights:
        if light.mac_addr == devices[index].mac_addr:
            return light.get_color()[3]
        index += 1


def get_state_bulbTV():
    if bulbTV is not None:
        return stateBulbTV


def get_state_bulbWin():
    if bulbWin is not None:
        return stateBulbWin


##################################################
#                SET PARAMETERS                  #
##################################################


def set_color(light, new_color):
    index = 0
    while index < num_lights:
        if light.mac_addr == devices[index].mac_addr:
            light.set_color()[0] = new_color
        index += 1


def set_intensity(light, new_intensity):
    index = 0
    while index < num_lights:
        if light.mac_addr == devices[index].mac_addr:
            light.get_color()[1] = new_intensity
        index += 1


def set_brightness(light, new_bright):
    index = 0
    while index < num_lights:
        if light.mac_addr == devices[index].mac_addr:
            light.get_color()[2] = new_bright
        index += 1


def set_warm(light, new_warm):
    index = 0
    while index < num_lights:
        if light.mac_addr == devices[index].mac_addr:
            light.get_color()[3] = new_warm
        index += 1


def set_state_bulbTV(new_state):
    stateBulbTV = new_state


def set_state_bulbWin(new_state):
    stateBulbWin = new_state


##################################################
#                 MODIFY LIGHTS                  #
##################################################

#             SUM AND REST QUANTITY

'''
    Modify the color of the light with the given quantity
    Gets this value into bulb.get_color()[0]
RED   ---> 0 or 360  ---> 0 or 65280   
GREEN --->      120  --->      21760
BLUE  --->      240  --->      43520  
'''


def modify_color(light, quantity):
    index = 0
    while index < num_lights:
        if light.mac_addr == devices[index].mac_addr:
            light.get_color()[0] = light.get_color()[0] + quantity
        index += 1


'''
    Modify the intensity of the color
    Gets this value into bulb.get_color()[1] 
MIN --->     0
MAX ---> 60292  
'''


def modify_intensity(light, quantity):
    index = 0
    while index < num_lights:
        if light.mac_addr == devices[index].mac_addr:
            light.get_color()[1] = light.get_color()[1] + quantity
        index += 1


'''
    Modify the brightness of the bulb with the given quantity
    Gets this parameter into bulb.get_color()[2]
MIN --->  1966 --->   1%
MAX ---> 65535 ---> 100%
'''


def modify_brightness(light, quantity, less):
    index = 0
    while index < num_lights:
        if light.mac_addr == devices[index].mac_addr:
            colorArray = list(light.get_color())
            if less is True:
                bright = colorArray[2]
                total = bright - quantity
                colorArray[2] = total
                light.set_color(colorArray)

            if less is False:
                bright = colorArray[2]
                total = bright + quantity
                colorArray[2] = total
                light.set_color(colorArray)
        index += 1
        
        
'''
    Modify from cold light to warm light with the given quantity
    Gets this value into bulb.get_color()[3]
MIN --->    2700 K ---> Warmest Light
MAX --->    6500 K ---> Coolest light
'''


def modify_warm(light, quantity):
    index = 0
    while index < num_lights:
        if light.mac_addr == devices[index].mac_addr:
            light.get_color()[3] = light.get_color()[3] + quantity
        index += 1


##################################################
##################################################
#              METHODS DEFINITION                #
##################################################
##################################################

##################################################
#                    TURN ON                     #
##################################################

# Enciende la bombilla de la TV


def bulb_tv_on():
    if bulbTV is not None:
        print ("Encendiendo luz cerca TV")
        bulbTV.set_power(True)
        stateBulbTV = True

        if stateBulbTV:
            print ("Encendida")
            print


# Enciende la bombilla de la ventana


def bulb_win_on():
    if bulbWin is not None:
        print ("Encendiendo luz cerca ventana")
        bulbWin.set_power(True)
        stateBulbWin = True

        if stateBulbWin:
            print ("Encendida")
            print


# Enciende todas las bombillas


def bulb_all_on():
    print ("Encendiendo todas las luces")
    if bulbTV is not None:
        bulb_tv_on()
    if bulbWin is not None:
        bulb_win_on()


##################################################
#                   TURN OFF                     #
##################################################

# Apaga la bombilla de la TV


def bulb_tv_off():
    print ("Apagando luz cerca TV")
    bulbTV.set_power("off")
    stateBulbTV = False


# Apaga la bombilla de la ventana


def bulb_win_off():
    print ("Apagando luz cerca ventana")
    bulbWin.set_power("off")
    stateBulbWin = False


# Apaga todas las luces


def bulb_all_off():
    print ("Apagando todas las luces")
    bulb_tv_off()
    bulb_win_off()


# 20% LESS -- QUANTITY = -12400


def less_bright_bulbTV():
    if bulbTV is not None:
        brillo = int(bulbTV.get_color()[2])
        total = brillo - 12400
        if total > 0:
            less = True
            modify_brightness(bulbTV, 12400, less)
        else:
            print ("Ha llegado al brillo minimo")

# 20% MORE -- QUANTITY = +12400


def more_bright_bulbTV():
    if bulbTV is not None:
        brillo = int(bulbTV.get_color()[2])
        total = brillo + 12400
        if total < 65535:
            less = False
            modify_brightness(bulbTV, 12400, less)
        else:
            print("Ha llegado al brillo maximo")


# 20% LESS -- QUANTITY = -12400


def less_bright_bulbWin():
    if bulbWin is not None:
        brillo = int(bulbWin.get_color()[2])
        total = brillo - 12400
        if total > 0:
            less = True
            modify_brightness(bulbWin, 12400, less)
        else:
            print ("Ha llegado al brillo minimo")

# 20% MORE -- QUANTITY = +12400


def more_bright_bulbWin():
    if bulbWin is not None:
        brillo = int(bulbWin.get_color()[2])
        total = brillo + 12400
        if total < 65535:
            less = False
            modify_brightness(bulbWin, 12400, less)
        else:
            print ("Ha llegado al brillo maximo")


def less_bright_all():
    less_bright_bulbTV()
    less_bright_bulbWin()


def more_bright_all():
    more_bright_bulbTV()
    more_bright_bulbWin()


#############################
#        MAIN METHOD        #
#############################

# --------------------------- PROBANDO CODIGO -------------------------


bulb_all_on()
# bulb_tv_on()

while True:

    if bulbTV is not None:
        print ("        --- TV ---")
        less_bright_bulbTV()

    if bulbWin is not None:
        print ("        --- WIN ---")
        less_bright_bulbWin()

    time.sleep(2)

# ---------------------------------------------------------------------

#############################
#          TOPICS           #
#############################


topics = {"acho/lights/on/all":  {"command": bulb_all_on, "text": "encendiendo luces"},
          "acho/lights/off/all": {"command": bulb_all_off, "text": "apagando luces"},
          "acho/lights/on/tv": 	 {"command": bulb_tv_on, "text": "encendiendo luz TV"},
          "acho/lights/on/win":      {"command": bulb_win_on, "text": "encendiendo luz ventana"},
          "acho/lights/off/tv": 	 {"command": bulb_tv_off, "text": "apagando luz TV"},
          "acho/lights/off/win": 	 {"command": bulb_win_off, "text": "apagando luz ventana"},
          "acho/lights/brightnessdown/tv": 	 {"command": less_bright_bulbTV(), "text": "bajando brillo en luz TV"},
          "acho/lights/brightnessup/tv": 	 {"command": more_bright_bulbTV(), "text": "subiendo brillo TV"},
          "acho/lights/brightnessdown/win":  {"command": less_bright_bulbWin(), "text": "bajando brillo ventana"},
          "acho/lights/brightnessup/win":  {"command": more_bright_bulbWin(), "text": "subiendo brillo ventana"},
          "acho/lights/brightnessdown/all":  {"command": less_bright_all(), "text": "bajando brillo luces"},
          "acho/lights/brightnessup/all":  {"command": more_bright_all(), "text": "subiendo brillo luces"}
}


##########################################
##########################################


def on__connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("acho/lights/#")


def on__message(client, userdata, msg):
    print ("topic", msg.topic)
    if msg.topic in topics:
        t = topics[msg.topic]
        client.publish("acho/tts", t["text"])
        t["command"]()

    #elif (msg.topic == "acho/bombillas/unpocobrillo1"):
        #client.publish("acho/tts", "encendiendo bombilla 1")
        #control_percentual_vble_B(bombilla1)
    #elif (msg.topic == "acho/bombillas/unpocobrillo2"):
        #client.publish("acho/tts", "encendiendo bombilla 2")
        #control_percentual_vble_B(bombilla2)
    #elif (msg.topic == "acho/bombillas/unpocobrillo"):
        #client.publish("acho/tts", "encendiendo bombillas")
        #control_percentual_vble_B(bombilla1)
        #control_percentual_vble_B(bombilla2)
    #elif (msg.topic == "acho/bombillas/brillo1"):
        #client.publish("acho/tts", "encendiendo bombilla 1")
        #control_percentual_total_B(bombilla1)
    #elif (msg.topic == "acho/bombillas/brillo2"):
        #client.publish("acho/tts", "encendiendo bombilla 2")
        #control_percentual_total_B(bombilla2)
    #elif (msg.topic == "acho/bombillas/brillo"):
        #client.publish("acho/tts", "encendiendo bombillas")
        #control_percentual_total_B(bombilla1)
        #control_percentual_total_B(bombilla2)
    #elif (msg.topic == "acho/bombillas/unpococolor1"):
        #client.publish("acho/tts", "encendiendo bombilla 1")
        #control_percentual_vble_K(bombilla1)
    #elif (msg.topic == "acho/bombillas/unpococolor2"):
        #discover()
        #client.publish("acho/tts", "encendiendo bombilla 2")
        #control_percentual_vble_K(bombilla2)
    #elif (msg.topic == "acho/bombillas/unpococolor"):
        #client.publish("acho/bombillas", "encendiendo bombillas")
        #control_percentual_vble_K(bombilla1)
        #control_percentual_vble_K(bombilla2)
    #elif (msg.topic == "acho/bombillas/color1"):
        #client.publish("acho/tts", "encendiendo bombilla 1")
        #control_percentual_total_K(bombilla1)
    #elif (msg.topic == "acho/bombillas/color2"):
        #client.publish("acho/tts", "encendiendo bombilla 2")
        #control_percentual_total_K(bombilla2)
    #elif (msg.topic == "acho/bombillas/color"):
        #client.publish("acho/tts", "encendiendo bombillas")
        #control_percentual_total_K(bombilla1)
        #control_percentual_total_K(bombilla2)
#
#
# # def discover():
# #     global num_lights
# #     global lifx
# #     global config
# #     global devices
# #
# #     print("\n {} luces encontradas \n".format(len(devices)))
# #     for d in devices:
# #         print(d)
# #         # i += 1
# #         # aux_mac = config.get('bombilla_{}'.format(i), 'mac')
# #         # if aux_mac != d.get_mac_addr():
# #         #     d.set_label("bombilla_{}".format(i))
# #         #     config.add_section('bombilla_{}'.format(i))
# #         #     config.set('bombilla_{}'.format(i), 'mac', d.get_mac_addr())
# #         #     with open('bulbs.cfg', 'wb') as configfile:
# #         #         config.write(configfile)
#
#
#
#
#
# # FROM 0 to 65535
# def modify_B(light, quantity):
#     global num_lights
#     global lifx
#     global config
#     global devices
#     lifx = LifxLAN(num_lights)
#     devices = lifx.get_lights()
#     for d in devices:
#         if d.get_mac_addr() == light:
#             bombilla = d
#             break
#     ogcolor = bombilla.get_color()
#     if ogcolor[2] <= quantity:
#         for i in range(ogcolor[2], quantity, 100):
#             color = [ogcolor[0], ogcolor[1], i, ogcolor[3]]
#             bombilla.set_color(color)
#             print (bombilla.get_color())
#     elif ogcolor[2] > quantity:
#         for i in range(ogcolor[2], quantity, -100):
#             color = [ogcolor[0], ogcolor[1], i, ogcolor[3]]
#             bombilla.set_color(color)
#             print (bombilla.get_color())
#
#
# # FROM 2500 to 9000
# def modify_K(light, quantity):
#     global num_lights
#     global lifx
#     global config
#     global devices
#     lifx = LifxLAN(num_lights)
#     devices = lifx.get_lights()
#     for d in devices:
#         if d.get_mac_addr() == light:
#             bombilla = d
#             break
#     ogcolor = bombilla.get_color()
#     if ogcolor[3] <= quantity:
#         for i in range(ogcolor[3], quantity, 100):
#             color = [ogcolor[0], ogcolor[1], ogcolor[2], i]
#             bombilla.set_color(color)
#             print (bombilla.get_color())
#     elif ogcolor[3] > quantity:
#         for i in range(ogcolor[3], quantity, -100):
#             color = [ogcolor[0], ogcolor[1], ogcolor[2], i]
#             bombilla.set_color(color)
#             print (bombilla.get_color())
#
#
# def control_percentual_vble_K(light):
#
#     ogcolor = bombilla.get_color()
#     quantity = ogcolor[3] * 0.1
#     if ogcolor[3] <= quantity:
#         for i in range(ogcolor[3], quantity, 100):
#             color = [ogcolor[0], ogcolor[1], ogcolor[2], i]
#             bombilla.set_color(color)
#             print (bombilla.get_color())
#     elif ogcolor[3] > quantity:
#         for i in range(ogcolor[3], quantity, -100):
#             color = [ogcolor[0], ogcolor[1], ogcolor[2], i]
#             bombilla.set_color(color)
#             print (bombilla.get_color())
#
#
# def control_percentual_total_K(light):
#     global num_lights
#     global lifx
#     global config
#     global devices
#     lifx = LifxLAN(num_lights)
#     devices = lifx.get_lights()
#     for d in devices:
#         if d.get_mac_addr() == light:
#             bombilla = d
#             break
#     ogcolor = bombilla.get_color()
#     if ogcolor[3] <= 900:
#         for i in range(ogcolor[3], 900, 100):
#             color = [ogcolor[0], ogcolor[1], ogcolor[2], i]
#             bombilla.set_color(color)
#             print (bombilla.get_color())
#     elif ogcolor[3] > 900:
#         for i in range(ogcolor[3], 900, -100):
#             color = [ogcolor[0], ogcolor[1], ogcolor[2], i]
#             bombilla.set_color(color)
#             print (bombilla.get_color())
#
#
# def control_percentual_vble_B(light):
#     global num_lights
#     global lifx
#     global config
#     global devices
#     lifx = LifxLAN(num_lights)
#     devices = lifx.get_lights()
#     for d in devices:
#         if d.get_mac_addr() == light:
#             bombilla = d
#             break
#     ogcolor = bombilla.get_color()
#     quantity = ogcolor[2] * 0.1
#     if ogcolor[2] <= quantity:
#         for i in range(ogcolor[3], quantity, 100):
#             color = [ogcolor[0], ogcolor[1], ogcolor[2], i]
#             bombilla.set_color(color)
#             print (bombilla.get_color())
#     elif ogcolor[2] > quantity:
#         for i in range(ogcolor[3], quantity, -100):
#             color = [ogcolor[0], ogcolor[1], ogcolor[2], i]
#             bombilla.set_color(color)
#             print (bombilla.get_color())
#
#
# def control_percentual_total_B(light):
#     global num_lights
#     global lifx
#     global config
#     global devices
#     lifx = LifxLAN(num_lights)
#     devices = lifx.get_lights()
#     for d in devices:
#         if d.get_mac_addr() == light:
#             bombilla = d
#
#     ogcolor = bombilla.get_color()
#     if ogcolor[2] <= 3650:
#         for i in range(ogcolor[3], 3650, 100):
#             color = [ogcolor[0], ogcolor[1], ogcolor[2], i]
#             bombilla.set_color(color)
#             print (bombilla.get_color())
#     elif ogcolor[2] > 3650:
#         for i in range(ogcolor[3], 3650, -100):
#             color = [ogcolor[0], ogcolor[1], ogcolor[2], i]
#             bombilla.set_color(color)
#             print (bombilla.get_color())

#


# client = mqtt.Client()
# client.on_connect = on__connect
# client.on_message = on__message
# client.connect("localhost", 1883, 60)
# # print ("Connected to Mosquitto broker")
# client.loop_forever()
