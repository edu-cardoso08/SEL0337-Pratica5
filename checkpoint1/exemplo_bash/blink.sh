#!/bin/bash
# Exemplo do roteiro: blink na GPIO18 acessando a GPIO direto pelo sistema de arquivos (sysfs).
# Exige o kernel 6.1.54 (rpi-update da Prática 2): a partir do 6.6 o número no sysfs muda.

# Exporta o pino só se ainda não estiver exportado (evita erro ao reiniciar o serviço)
[ -d /sys/class/gpio/gpio18 ] || echo 18 > /sys/class/gpio/export
sleep 0.1
echo out > /sys/class/gpio/gpio18/direction

while [ 1 ]
do
    echo 1 > /sys/class/gpio/gpio18/value
    sleep 0.2s
    echo 0 > /sys/class/gpio/gpio18/value
    sleep 0.2s
done
