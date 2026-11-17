#!/usr/bin/env python3
## Eduardo M. Cardoso (14567242) e Caua S. Fernandes (14754734)
# Programa do ExecStop, executado em "sudo systemctl stop blink_python".
# Encerra o blink_led.py (PID recebido via $MAINPID), pisca o LED 3 vezes,
# deixa-o apagado e registra a data/hora da parada em paradas_servico.log.

import os
import signal
import sys
import time
from datetime import datetime

import RPi.GPIO as GPIO

PINO_LED = 18
ARQUIVO_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "paradas_servico.log")


def parar_processo(pid, tempo_max=5.0):
    try:
        os.kill(pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    limite = time.time() + tempo_max
    while time.time() < limite:
        try:
            os.kill(pid, 0)          # sinal 0 apenas testa se o processo ainda existe
        except ProcessLookupError:
            return
        time.sleep(0.1)


if len(sys.argv) > 1 and sys.argv[1].isdigit():
    parar_processo(int(sys.argv[1]))

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(PINO_LED, GPIO.OUT, initial=GPIO.LOW)

for _ in range(3):
    GPIO.output(PINO_LED, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(PINO_LED, GPIO.LOW)
    time.sleep(0.1)

GPIO.cleanup()

with open(ARQUIVO_LOG, "a") as log:
    log.write(f"{datetime.now():%d/%m/%Y %H:%M:%S} - servico blink_python parado\n")

print("blink_off.py: LED apagado e parada registrada em", ARQUIVO_LOG)
