from pymata4 import pymata4
import time
import sys
import random

## Tous les pins arduino
board = pymata4.Pymata4(arduino_instance_id=1)
trigger_pin = 11
echo_pin = 12
Distance_en_cm = 2
pinservo = 10
pinavancerA = 9 #pin pour faire avancer le moteur 1
pinavancerB = 5 #pin pour faire avancer le moteur 2
pinreculerA = 3 #pin pour changer le sens de rotation du moteur 1 (ie le fait tourner à reculons)
pinreculerB = 6 #pin pour changer le sens de rotation du moteur 2

##Contrôle de l'artillerie
def the_callback(data):
    print("La distance est" [Distance_en_cm])

def hc_sr04(my_board, trigger_pin, echo_pin, callback):
    my_board.set_pin_mode_sonar(trigger_pin, echo_pin, callback)
    data_sonar = []
    while True:
        try:
            time.sleep(1)
            data_sonar.append(my_board.sonar_read(trigger_pin))
            print(data_sonar)
        except KeyboardInterrupt:
            sys.exit(0)
            pymata4.Pymata4.shutdown(my_board)

def avancer(board, pin1, pin2): #pin1 correspond au sens 1 du moteur 1, pin2 au sens 1 du moteur 2 (donc avance)
    board.set_pin_mode_pwm_output(pin1)
    board.set_pin_mode_pwm_output(pin2)

    board.pwm_write(pin1, 255)
    board.pwm_write(pin2, 255) #255 c'est l'intensité maximale, ça peut aller de 0 à 255

def servo(board, pin):
    board.set_pin_mode_servo(pin)
    time.sleep(1)
    board.servo_write(pin, 0) #met le servo à 0°
    time.sleep(1)
    board.servo_write(pin, 90)
    time.sleep(1)
    board.servo_write(pin, 180)

def servo_droite(board,pin):
    board.set_pin_mode_servo(pin)
    board.servo_write(pin,0)
    time.sleep(1)
    board.servo_write(pin,90)

def arret(board, pin1, pin2):
    board.set_pin_mode_pwm_output(pin1)
    board.set_pin_mode_pwm_output(pin2)

    board.pwm_write(pin1, 0)
    board.pwm_write(pin2, 0)

def reculer(board, pin1, pin2): #pin1 ici correspond au sens 2 du moteur 1, pin2 au sens 2 du moteur 2
    board.set_pin_mode_pwm_output(pin1)
    board.set_pin_mode_pwm_output(pin2)

    board.pwm_write(pin1, 255)
    board.pwm_write(pin2, 255)

def tournerdroite(board, pin1, pin2): #pin1 moteur gauche, pin2 moteur droit (sens1 tous les deux)
    board.set_pin_mode_pwm_output(pin1)
    board.set_pin_mode_pwm_output(pin2)

    board.pwm_write(pin1, 255)
    board.pwm_write(pin2, 0)

def tournergauche(board, pin1, pin2):
    board.set_pin_mode_pwm_output(pin1)
    board.set_pin_mode_pwm_output(pin2)

    board.pwm_write(pin1, 0)
    board.pwm_write(pin2, 255)

##Création d'une map


def chercher(board, pinservo, pintrigger, pinecho):
    board.set_pin_mode_servo(pinservo)
    servo(board, pinservo)
    distancegauche = 0
    distancedroite = 0
    time.sleep(1)
    board.servo_write(pinservo, 90)
    time.sleep(1)
    distancegauche = board.sonar_read(pintrigger)
    print(f'data read: {board.sonar_read(pintrigger)}')

    board.servo_write(pinservo, -180)
    time.sleep(1)
    distancedroite = board.sonar_read(pintrigger)
    print(f'data read : {board.sonar_read(pintrigger)}')

#chercher(board, 10, trigger_pin, echo_pin)

#servo(board, pinservo)


##Création d'un radar mobile
def vitesse_relative(my_board, trigger_pin, echo_pin, callback): #détermine la vitesse relative de l'objet devant la voiture par rapport au radar
    data_sonar = [[0,0]]
    my_board.set_pin_mode_sonar(trigger_pin, echo_pin, callback)
    v = 0
    while True:
        try:
            data_sonar.append(my_board.sonar_read(trigger_pin))
            time.sleep(1)
            if data_sonar[-1][1]-data_sonar[-2][1] != 0:
                d2 = data_sonar[-1][0]
                d1 = data_sonar[-2][0]
                T = data_sonar[-1][1]-data_sonar[-2][1]
                v = (d2-d1)/T #dernière vitesse relative enregistrée
                print('La vitesse relative est',  (d2-d1)/T)
            else:
                print('La vitesse relative est toujours', v)
        except KeyboardInterrupt:
            sys.exit(0)
            pymata4.Pymata4.shutdown(my_board)


def vitesse_objet_mobile(my_board, trigger_pin, echo_pin, callback):
    while True:
        try:
            vitesse = 20 + vitesse_relative(my_board,trigger_pin, echo_pin, callback) #20 est la vitesse de la voiture
            print("la vitesse est" + vitesse)
        except KeyboardInterrupt:
            sys.exit(0)
            pymata4.Pymata4.shutdown(my_board)

##Prudence sur la route!!
def prudence(my_board, trigger_pin, echo_pin, callback):
    while True:
        try:
            if vitesse_objet_mobile(my_board, trigger_pin, echo_pin, callback) >= 0:
                print('Pas de problème chauffeur !')
            elif vitesse_objet_mobile(my_board, trigger_pin, echo_pin, callback) = 0:
                print('Obstacle !!')
            elif vitesse_objet_mobile(my_board, trigger_pin, echo_pin, callback) <= 0:
                print("Tu devrais t'arrêter...")
                return 1

def prevision(my_board, trigger_pin, echo_pin, callback):
    if prudence(my_board, trigger_pin, echo_pin, callback) == 1:
        vitesse = vitesse_objet_mobile(my_board, trigger_pin, echo_pin, callback)
        my_board.set_pin_mode_sonar(trigger_pin, echo_pin, callback)
        distance_objet_mobile = my_board.sonar_read(trigger_pin)[-1][0] #La distance de l'objet mobile à la voiture
        temps_avant_arret_urgent = (distance_objet_mobile-20)/vitesse #20 étant la distance maximale entre la voiture et un obstacle avant qu'elle freine d'urgence.
        return temps_avant_arret_urgent

##Fonctionnement voiture naïf
def Boubou_roule(my_board, trigger_pin, echo_pin, servopin, moteur1sens1, moteur1sens2, moteur2sens1, moteur2sens1):
    distance_droite = 0
    distance_gauche = 0
    aleatoire = 0
    while prudence(my_board, trigger_pin, echo_pin, callback) != 1:
        avancer(my_board, pinavancerA, pinavancerB)
    if prudence(my_board, trigger_pin, echo_pin, callback) == 1:
        arret(my_board, moteur1, moteur2) #voiture s'arrête
        servo_droite(my_board, servopin) # le servomoteur tourne à droite
        distance_droite = my_board.sonar_read(trigger_pin) #On regarde la distance à droite
        servo_gauche(my_board, servopin) #le servomoteur tourne à gauche
        distance_gauche = my_board.sonar_read(trigger_pin) #On regarde la distance à gauche
        if distance_droite < 15:#Condition si on peut pas aller à gauche ou à droite, on va dans la seule direction possible
            tournergauche(my_ board, moteur1sens1, moteur2,sens1)
        if distance_gauche < 15:
            tournerdroite(my_board, moteur2sens1, moteur1sens1)
        if distance_gauche < 15 and distance_droite < 15: #condition pour le demi-tour
            reculer(my_board, moteur1sens2, moteur2sens2)
            time.sleep(1)
            tournerdroite(my_board, moteur2sens1, moteur1sens1)
            time.sleep(0.5)
            tournerdroite(my_board, moteur2sens1, moteur1sens1)
        else: #Si on peut aller à droite et à gauche, on a 50% de chance d'aller à droite ou à gauche
            aleatoire = random.random()
            if aleatoire > 0.5:
                tournerdroite(my_board, moteur2sens1, moteur1sens1)
            else:
                tournergauche(my_board, moteur1sens1, moteur2sens1)

t = time.time()
u = 0
while u < 300: # la voiture roule pendant 5 minutes
    Boubou_roule(board, trigger_pin, echo_pin, servopin, pinavancerA, pinreculerA, pinavancerB, pinreculerB)
    t1 = time.time()
    u = t1 - t











"""try:
    hc_sr04(board, trigger_pin, echo_pin, the_callback)
    board.pymata4.Pymata4.shutdown()
except (KeyboardInterrupt, RuntimeError):
    pymata4.Pymata4.shutdown(board)
    sys.exit(0)"""

"""try:
    servo(board, 10)

 KeyboardInterrupt:
    my.board.pymata4.Pymata4.shutdown()
    sys.exit(0)"""
"""print(f'data read: {my_board.sonar_read(trigger_pin)}')""" #print(f print une fonction...


