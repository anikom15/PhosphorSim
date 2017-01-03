# PhosphorSim
# Copyright 2017 Westley M. Martinez
# MIT License
"""A phosphor simulation in the 8-bit sRGB color space."""

import sys
from array import array
from math import exp

DELTA_TIME = 1 / 60

def main():
    while True:
        s = input('1 - Exponential, 2 - Inverse Power, '
                  '3 - Generate Threshold LUT, 0 - Quit\n> ')
        if s == '0':
            break
        elif s == '1':
            tau = float(input('tau = '))
            run_exp(tau)
        elif s == '2':
            beta = float(input('beta = '))
            gamma = float(input('gamma = '))
            run_inv_pow(beta, gamma)
        elif s == '3':
            run_lut()
    return 0

def RGB(c):
    c /= 255
    if c < 0.04045:
        return c / 12.92
    else:
        return ((c + 0.055) / (1 + 0.055)) ** 2.4

def sRGB(c):
    if c < 0.0031308:
        c *= 12.92
    else:
        c = (1 + 0.055) * c ** (1 / 2.4) - 0.055
    return int(round(255 * c))

def run_exp(tau):
    if tau <= 0:
        return
    color = 255;
    print(color)
    while color > 0:
        Y = RGB(color)
        Y *= exp(-DELTA_TIME / tau);
        threshold = RGB(color) - RGB(color - 0.5)
        Y = max(0, Y - threshold)
        color = sRGB(Y)
        print(color)

def run_inv_pow(beta, gamma):
    if beta < 0.5 or beta > 2.0 or gamma <= 0:
        return
    color = 255;
    print(color)
    while color > 0:
        Y = RGB(color)
        Y = (gamma * DELTA_TIME + (1 / Y) ** (1 / beta)) ** -beta
        threshold = RGB(color) - RGB(color - 0.5)
        Y = max(0, Y - threshold)
        color = sRGB(Y)
        print(color)

def run_lut():
    a = array('f')
    for i in range(256):
        a.append(i/255 - RGB(sRGB(i/255) - 0.5))
    for f in a:
        print('%g, ' % f, end='')
    print()

if __name__ == '__main__':
    sys.exit(main())
