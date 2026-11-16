#!/usr/bin/env python3

import signal
import time

import RPi.GPIO as GPIO

PINO_LED = 18        # numeração BCM
MEIO_PERIODO = 0.5   # s aceso / s apagado

executando = True


def encerrar(signum, frame):
    # Só baixa a flag; o laço termina no próximo ciclo e o finally faz a limpeza
    global executando
    executando = False


signal.signal(signal.SIGTERM, encerrar)   # systemctl stop
signal.signal(signal.SIGINT, encerrar)    # CTRL+C, quando rodado no terminal

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(PINO_LED, GPIO.OUT, initial=GPIO.LOW)

print("blink_led.py iniciado: LED piscando na GPIO18")

try:
    while executando:
        GPIO.output(PINO_LED, GPIO.HIGH)
        time.sleep(MEIO_PERIODO)
        GPIO.output(PINO_LED, GPIO.LOW)
        time.sleep(MEIO_PERIODO)
finally:
    GPIO.output(PINO_LED, GPIO.LOW)
    GPIO.cleanup()
    print("blink_led.py encerrado: LED apagado e GPIO liberada")
