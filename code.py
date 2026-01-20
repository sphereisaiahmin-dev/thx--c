import time
time.sleep(5)
from keybow2040 import Keybow2040
#from keybow_hardware.pim56x import PIM56X as Hardware # for Keybow 2040
from keybow_hardware.pim551 import PIM551 as Hardware # for Pico RGB Keypad Base

import usb_midi
import adafruit_midi
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn

keybow = Keybow2040(Hardware())
keys = keybow.keys

BRIGHTNESS_SCALE = 0.9

def set_led_scaled(index, red, green, blue):
    keybow.set_led(
        index,
        int(red * BRIGHTNESS_SCALE),
        int(green * BRIGHTNESS_SCALE),
        int(blue * BRIGHTNESS_SCALE),
    )

ARPEGGIO_MODIFIER_COLORS = {
    12: (200, 100, 100),
    13: (100, 200, 100),
    14: (100, 100, 200),
    15: (100, 50, 100),
}

SUSTAIN_MODIFIER_COLORS = {
    12: (50, 180, 200),
    13: (200, 180, 50),
    14: (200, 80, 180),
    15: (180, 200, 60),
}

def update_modifier_leds(arpeggio_mode):
    colors = ARPEGGIO_MODIFIER_COLORS if arpeggio_mode else SUSTAIN_MODIFIER_COLORS
    for index in (12, 13, 14, 15):
        red, green, blue = colors[index]
        set_led_scaled(index, red, green, blue)

set_led_scaled(0, 100, 100, 100)
set_led_scaled(1, 50, 100, 10)
set_led_scaled(2, 100, 100, 100)
set_led_scaled(3, 50, 100, 10)
set_led_scaled(4, 100, 100, 100)
set_led_scaled(5, 100, 100, 100)
set_led_scaled(6, 50, 100, 10)
set_led_scaled(7, 100, 100, 100)
set_led_scaled(8, 50, 100, 10)
set_led_scaled(9, 100, 100, 100)
set_led_scaled(10, 50, 100, 10)
set_led_scaled(11, 100, 100, 100)

midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)
ROLL_DELAY = 0.012

def roll_chord(messages, delay=ROLL_DELAY):
    for message in messages:
        midi.send(message)
        time.sleep(delay)

def play_chord(messages, arpeggio_mode):
    if arpeggio_mode:
        roll_chord(messages)
    else:
        midi.send(messages)

arpeggio_mode = True
toggle_latched = False
update_modifier_leds(arpeggio_mode)

while True:
    keybow.update()

    if keys[5].pressed and keys[3].pressed:
        if not toggle_latched:
            arpeggio_mode = not arpeggio_mode
            update_modifier_leds(arpeggio_mode)
            toggle_latched = True
    else:
        toggle_latched = False

#stops hanging notes 

    if keys[15].pressed:
        M = keys[15]
        @keybow.on_release(M)
        def release_handler(M):

            midi.send([NoteOff(60, 0),
                       NoteOff(61, 0),
                       NoteOff(62, 0),
                       NoteOff(63, 0),
                       NoteOff(64, 0),
                       NoteOff(65, 0),
                       NoteOff(66, 0),
                       NoteOff(67, 0),
                       NoteOff(68, 0),
                       NoteOff(69, 0),
                       NoteOff(70, 0),
                       NoteOff(71, 0),
                       NoteOff(72, 0),
                       NoteOff(73, 0),
                       NoteOff(74, 0),
                       NoteOff(75, 0),
                       NoteOff(76, 0),
                       NoteOff(77, 0),
                       NoteOff(78, 0),
                       NoteOff(79, 0),
                       NoteOff(80, 0),
                       NoteOff(81, 0),
                       NoteOff(82, 0),
                       NoteOff(83, 0),
                       NoteOff(84, 0),
                       NoteOff(85, 0),
                       NoteOff(86, 0)])


    if keys[14].pressed:
        O = keys[14]
        @keybow.on_release(O)
        def release_handler(O):

            midi.send([NoteOff(60, 0),
                       NoteOff(61, 0),
                       NoteOff(62, 0),
                       NoteOff(63, 0),
                       NoteOff(64, 0),
                       NoteOff(65, 0),
                       NoteOff(66, 0),
                       NoteOff(67, 0),
                       NoteOff(68, 0),
                       NoteOff(69, 0),
                       NoteOff(70, 0),
                       NoteOff(71, 0),
                       NoteOff(72, 0),
                       NoteOff(73, 0),
                       NoteOff(74, 0),
                       NoteOff(75, 0),
                       NoteOff(76, 0),
                       NoteOff(77, 0),
                       NoteOff(78, 0),
                       NoteOff(79, 0),
                       NoteOff(80, 0),
                       NoteOff(81, 0),
                       NoteOff(82, 0),
                       NoteOff(83, 0),
                       NoteOff(84, 0),
                       NoteOff(85, 0),
                       NoteOff(86, 0)])


    if keys[13].pressed:
        D = keys[13]
        @keybow.on_release(D)
        def release_handler(D):

            midi.send([NoteOff(60, 0),
                       NoteOff(61, 0),
                       NoteOff(62, 0),
                       NoteOff(63, 0),
                       NoteOff(64, 0),
                       NoteOff(65, 0),
                       NoteOff(66, 0),
                       NoteOff(67, 0),
                       NoteOff(68, 0),
                       NoteOff(69, 0),
                       NoteOff(70, 0),
                       NoteOff(71, 0),
                       NoteOff(72, 0),
                       NoteOff(73, 0),
                       NoteOff(74, 0),
                       NoteOff(75, 0),
                       NoteOff(76, 0),
                       NoteOff(77, 0),
                       NoteOff(78, 0),
                       NoteOff(79, 0),
                       NoteOff(80, 0),
                       NoteOff(81, 0),
                       NoteOff(82, 0),
                       NoteOff(83, 0),
                       NoteOff(84, 0),
                       NoteOff(85, 0),
                       NoteOff(86, 0)])


    if keys[12].pressed:
        S = keys[12]
        @keybow.on_release(S)
        def release_handler(S):

            midi.send([NoteOff(60, 0),
                       NoteOff(61, 0),
                       NoteOff(62, 0),
                       NoteOff(63, 0),
                       NoteOff(64, 0),
                       NoteOff(65, 0),
                       NoteOff(66, 0),
                       NoteOff(67, 0),
                       NoteOff(68, 0),
                       NoteOff(69, 0),
                       NoteOff(70, 0),
                       NoteOff(71, 0),
                       NoteOff(72, 0),
                       NoteOff(73, 0),
                       NoteOff(74, 0),
                       NoteOff(75, 0),
                       NoteOff(76, 0),
                       NoteOff(77, 0),
                       NoteOff(78, 0),
                       NoteOff(79, 0),
                       NoteOff(80, 0),
                       NoteOff(81, 0),
                       NoteOff(82, 0),
                       NoteOff(83, 0),
                       NoteOff(84, 0),
                       NoteOff(85, 0),
                       NoteOff(86, 0)])

                      #Single note
    if not keys[15].pressed and not keys[14].pressed \
    and not keys[13].pressed and not keys[12].pressed:
        C = keys[0]
        @keybow.on_press(C)
        def press_handler(C):

            midi.send(NoteOn(60, 127))

        @keybow.on_release(C)
        def release_handler(C):

            midi.send(NoteOff(60, 0))

        Db = keys[1]
        @keybow.on_press(Db)
        def press_handler(Db):

            midi.send(NoteOn(61, 127))

        @keybow.on_release(Db)
        def release_handler(Db):

            midi.send(NoteOff(61, 0))

        D = keys[2]
        @keybow.on_press(D)
        def press_handler(D):

            midi.send(NoteOn(62, 127))

        @keybow.on_release(D)
        def release_handler(D):

            midi.send(NoteOff(62, 0))
                      
        Eb = keys[3]
        @keybow.on_press(Eb)
        def press_handler(Eb):

            midi.send(NoteOn(63, 127))

        @keybow.on_release(Eb)
        def release_handler(Eb):

            midi.send(NoteOff(63, 0))

        E = keys[4]
        @keybow.on_press(E)
        def press_handler(E):

            midi.send(NoteOn(64, 127))

        @keybow.on_release(E)
        def release_handler(E):

            midi.send(NoteOff(64, 0))

        F = keys[5]
        @keybow.on_press(F)
        def press_handler(F):

            midi.send(NoteOn(65, 127))

        @keybow.on_release(F)
        def release_handler(F):

            midi.send(NoteOff(65, 0))

        Gb = keys[6]
        @keybow.on_press(Gb)
        def press_handler(Gb):

            midi.send(NoteOn(66, 127))

        @keybow.on_release(Gb)
        def release_handler(Gb):

            midi.send(NoteOff(66, 0))

        G = keys[7]
        @keybow.on_press(G)
        def press_handler(G):

            midi.send(NoteOn(67, 127))

        @keybow.on_release(G)
        def release_handler(G):

            midi.send(NoteOff(67, 0))

        Ab = keys[8]
        @keybow.on_press(Ab)
        def press_handler(Ab):

            midi.send(NoteOn(68, 127))

        @keybow.on_release(Ab)
        def release_handler(Ab):

            midi.send(NoteOff(68, 0))

        A = keys[9]
        @keybow.on_press(A)
        def press_handler(A):

            midi.send(NoteOn(69, 127))

        @keybow.on_release(A)
        def release_handler(A):

            midi.send(NoteOff(69, 0))

        Bb = keys[10]
        @keybow.on_press(Bb)
        def press_handler(Bb):

            midi.send(NoteOn(70, 127))

        @keybow.on_release(Bb)
        def release_handler(Bb):

            midi.send(NoteOff(70, 0))

        B = keys[11]
        @keybow.on_press(B)
        def press_handler(B):

            midi.send(NoteOn(71, 127))

        @keybow.on_release(B)
        def release_handler(B):

            midi.send(NoteOff(71, 0))

                      #Single note
    if not keys[15].pressed and not keys[14].pressed \
    and not keys[13].pressed and not keys[12].pressed:
        C = keys[0]
        @keybow.on_press(C)
        def press_handler(C):

            midi.send(NoteOn(60, 127))

        @keybow.on_release(C)
        def release_handler(C):

            midi.send(NoteOff(60, 0))

        Db = keys[1]
        @keybow.on_press(Db)
        def press_handler(Db):

            midi.send(NoteOn(61, 127))

        @keybow.on_release(Db)
        def release_handler(Db):

            midi.send(NoteOff(61, 0))

        D = keys[2]
        @keybow.on_press(D)
        def press_handler(D):

            midi.send(NoteOn(62, 127))

        @keybow.on_release(D)
        def release_handler(D):

            midi.send(NoteOff(62, 0))
                      
        Eb = keys[3]
        @keybow.on_press(Eb)
        def press_handler(Eb):

            midi.send(NoteOn(63, 127))

        @keybow.on_release(Eb)
        def release_handler(Eb):

            midi.send(NoteOff(63, 0))

        E = keys[4]
        @keybow.on_press(E)
        def press_handler(E):

            midi.send(NoteOn(64, 127))

        @keybow.on_release(E)
        def release_handler(E):

            midi.send(NoteOff(64, 0))

        F = keys[5]
        @keybow.on_press(F)
        def press_handler(F):

            midi.send(NoteOn(65, 127))

        @keybow.on_release(F)
        def release_handler(F):

            midi.send(NoteOff(65, 0))

        Gb = keys[6]
        @keybow.on_press(Gb)
        def press_handler(Gb):

            midi.send(NoteOn(66, 127))

        @keybow.on_release(Gb)
        def release_handler(Gb):

            midi.send(NoteOff(66, 0))

        G = keys[7]
        @keybow.on_press(G)
        def press_handler(G):

            midi.send(NoteOn(67, 127))

        @keybow.on_release(G)
        def release_handler(G):

            midi.send(NoteOff(67, 0))

        Ab = keys[8]
        @keybow.on_press(Ab)
        def press_handler(Ab):

            midi.send(NoteOn(68, 127))

        @keybow.on_release(Ab)
        def release_handler(Ab):

            midi.send(NoteOff(68, 0))

        A = keys[9]
        @keybow.on_press(A)
        def press_handler(A):

            midi.send(NoteOn(69, 127))

        @keybow.on_release(A)
        def release_handler(A):

            midi.send(NoteOff(69, 0))

        Bb = keys[10]
        @keybow.on_press(Bb)
        def press_handler(Bb):

            midi.send(NoteOn(70, 127))

        @keybow.on_release(Bb)
        def release_handler(Bb):

            midi.send(NoteOff(70, 0))

        B = keys[11]
        @keybow.on_press(B)
        def press_handler(B):

            midi.send(NoteOn(71, 127))

        @keybow.on_release(B)
        def release_handler(B):

            midi.send(NoteOff(71, 0))

                     #Major chord
    if keys[15].pressed and not keys[14].pressed \
    and not keys[13].pressed and not keys[12].pressed:
        C = keys[0]
        @keybow.on_press(C)
        def press_handler(C):

            play_chord([NoteOn(60, 127),
                       NoteOn(64, 127),
                       NoteOn(67, 127)], arpeggio_mode)

        @keybow.on_release(C)
        def release_handler(C):

            midi.send([NoteOff(60, 0),
                       NoteOff(64, 0),
                       NoteOff(67, 0)])

        Db = keys[1]
        @keybow.on_press(Db)
        def press_handler(Db):

            play_chord([NoteOn(61, 127),
                       NoteOn(65, 127),
                       NoteOn(68, 127)], arpeggio_mode)

        @keybow.on_release(Db)
        def release_handler(Db):

            midi.send([NoteOff(61, 0),
                       NoteOff(65, 0),
                       NoteOff(68, 0)])

        D = keys[2]
        @keybow.on_press(D)
        def press_handler(D):

            play_chord([NoteOn(62, 127),
                       NoteOn(66, 127),
                       NoteOn(69, 127)], arpeggio_mode)

        @keybow.on_release(D)
        def release_handler(D):

            midi.send([NoteOff(62, 0),
                       NoteOff(66, 0),
                       NoteOff(69, 0)])

        Eb = keys[3]
        @keybow.on_press(Eb)
        def press_handler(Eb):

            play_chord([NoteOn(63, 127),
                       NoteOn(67, 127),
                       NoteOn(70, 127)], arpeggio_mode)

        @keybow.on_release(Eb)
        def release_handler(Eb):

            midi.send([NoteOff(63, 0),
                       NoteOff(67, 0),
                       NoteOff(70, 0)])

        E = keys[4]
        @keybow.on_press(E)
        def press_handler(E):

            play_chord([NoteOn(64, 127),
                       NoteOn(68, 127),
                       NoteOn(71, 127)], arpeggio_mode)

        @keybow.on_release(E)
        def release_handler(E):

            midi.send([NoteOff(64, 0),
                       NoteOff(68, 0),
                       NoteOff(71, 0)])

        F = keys[5]
        @keybow.on_press(F)
        def press_handler(F):

            play_chord([NoteOn(65, 127),
                       NoteOn(69, 127),
                       NoteOn(72, 127)], arpeggio_mode)

        @keybow.on_release(F)
        def release_handler(F):

            midi.send([NoteOff(65, 0),
                       NoteOff(69, 0),
                       NoteOff(72, 0)])

        Gb = keys[6]
        @keybow.on_press(Gb)
        def press_handler(Gb):

            play_chord([NoteOn(66, 127),
                       NoteOn(70, 127),
                       NoteOn(73, 127)], arpeggio_mode)

        @keybow.on_release(Gb)
        def release_handler(Gb):

            midi.send([NoteOff(66, 0),
                       NoteOff(70, 0),
                       NoteOff(73, 0)])

        G = keys[7]
        @keybow.on_press(G)
        def press_handler(G):

            play_chord([NoteOn(67, 127),
                       NoteOn(71, 127),
                       NoteOn(74, 127)], arpeggio_mode)

        @keybow.on_release(G)
        def release_handler(G):

            midi.send([NoteOff(67, 0),
                       NoteOff(71, 0),
                       NoteOff(74, 0)])

        Ab = keys[8]
        @keybow.on_press(Ab)
        def press_handler(Ab):

            play_chord([NoteOn(68, 127),
                       NoteOn(72, 127),
                       NoteOn(75, 127)], arpeggio_mode)

        @keybow.on_release(Ab)
        def release_handler(Ab):

            midi.send([NoteOff(68, 0),
                       NoteOff(72, 0),
                       NoteOff(75, 0)])

        A = keys[9]
        @keybow.on_press(A)
        def press_handler(A):

            play_chord([NoteOn(69, 127),
                       NoteOn(73, 127),
                       NoteOn(76, 127)], arpeggio_mode)

        @keybow.on_release(A)
        def release_handler(A):

            midi.send([NoteOff(69, 0),
                       NoteOff(73, 0),
                       NoteOff(76, 0)])

        Bb = keys[10]
        @keybow.on_press(Bb)
        def press_handler(Bb):

            play_chord([NoteOn(70, 127),
                       NoteOn(74, 127),
                       NoteOn(77, 127)], arpeggio_mode)

        @keybow.on_release(Bb)
        def release_handler(Bb):

            midi.send([NoteOff(70, 0),
                       NoteOff(74, 0),
                       NoteOff(77, 0)])

        B = keys[11]
        @keybow.on_press(B)
        def press_handler(B):

            play_chord([NoteOn(71, 127),
                       NoteOn(75, 127),
                       NoteOn(78, 127)], arpeggio_mode)

        @keybow.on_release(B)
        def release_handler(B):

            midi.send([NoteOff(71, 0),
                       NoteOff(75, 0),
                       NoteOff(78, 0)])


                      #Minor chord
    if not keys[15].pressed and keys[14].pressed \
    and not keys[13].pressed and not keys[12].pressed:
        C = keys[0]
        @keybow.on_press(C)
        def press_handler(C):

            play_chord([NoteOn(60, 127),
                       NoteOn(63, 127),
                       NoteOn(67, 127)], arpeggio_mode)

        @keybow.on_release(C)
        def release_handler(C):

            midi.send([NoteOff(60, 0),
                       NoteOff(63, 0),
                       NoteOff(67, 0)])

        Db = keys[1]
        @keybow.on_press(Db)
        def press_handler(Db):

            play_chord([NoteOn(61, 127),
                       NoteOn(64, 127),
                       NoteOn(68, 127)], arpeggio_mode)

        @keybow.on_release(Db)
        def release_handler(Db):

            midi.send([NoteOff(61, 0),
                       NoteOff(64, 0),
                       NoteOff(68, 0)])
        D = keys[2]
        @keybow.on_press(D)
        def press_handler(D):

            play_chord([NoteOn(62, 127),
                       NoteOn(65, 127),
                       NoteOn(69, 127)], arpeggio_mode)

        @keybow.on_release(D)
        def release_handler(D):

            midi.send([NoteOff(62, 0),
                       NoteOff(65, 0),
                       NoteOff(69, 0)])

        Eb = keys[3]
        @keybow.on_press(Eb)
        def press_handler(Eb):

            play_chord([NoteOn(63, 127),
                       NoteOn(66, 127),
                       NoteOn(70, 127)], arpeggio_mode)

        @keybow.on_release(Eb)
        def release_handler(Eb):

            midi.send([NoteOff(63, 0),
                       NoteOff(66, 0),
                       NoteOff(70, 0)])

        E = keys[4]
        @keybow.on_press(E)
        def press_handler(E):

            play_chord([NoteOn(64, 127),
                       NoteOn(67, 127),
                       NoteOn(71, 127)], arpeggio_mode)

        @keybow.on_release(E)
        def release_handler(E):

            midi.send([NoteOff(64, 0),
                       NoteOff(67, 0),
                       NoteOff(71, 0)])

        F = keys[5]
        @keybow.on_press(F)
        def press_handler(F):

            play_chord([NoteOn(65, 127),
                       NoteOn(68, 127),
                       NoteOn(72, 127)], arpeggio_mode)

        @keybow.on_release(F)
        def release_handler(F):

            midi.send([NoteOff(65, 0),
                       NoteOff(68, 0),
                       NoteOff(72, 0)])

        Gb = keys[6]
        @keybow.on_press(Gb)
        def press_handler(Gb):

            play_chord([NoteOn(66, 127),
                       NoteOn(69, 127),
                       NoteOn(73, 127)], arpeggio_mode)

        @keybow.on_release(Gb)
        def release_handler(Gb):

            midi.send([NoteOff(66, 0),
                       NoteOff(69, 0),
                       NoteOff(73, 0)])

        G = keys[7]
        @keybow.on_press(G)
        def press_handler(G):

            play_chord([NoteOn(67, 127),
                       NoteOn(70, 127),
                       NoteOn(74, 127)], arpeggio_mode)

        @keybow.on_release(G)
        def release_handler(G):

            midi.send([NoteOff(67, 0),
                       NoteOff(70, 0),
                       NoteOff(74, 0)])

        Ab = keys[8]
        @keybow.on_press(Ab)
        def press_handler(Ab):

            play_chord([NoteOn(68, 127),
                       NoteOn(71, 127),
                       NoteOn(75, 127)], arpeggio_mode)

        @keybow.on_release(Ab)
        def release_handler(Ab):

            midi.send([NoteOff(68, 0),
                       NoteOff(71, 0),
                       NoteOff(75, 0)])

        A = keys[9]
        @keybow.on_press(A)
        def press_handler(A):

            play_chord([NoteOn(69, 127),
                       NoteOn(72, 127),
                       NoteOn(76, 127)], arpeggio_mode)

        @keybow.on_release(A)
        def release_handler(A):

            midi.send([NoteOff(69, 0),
                       NoteOff(72, 0),
                       NoteOff(76, 0)])

        Bb = keys[10]
        @keybow.on_press(Bb)
        def press_handler(Bb):

            play_chord([NoteOn(70, 127),
                       NoteOn(73, 127),
                       NoteOn(77, 127)], arpeggio_mode)

        @keybow.on_release(Bb)
        def release_handler(Bb):

            midi.send([NoteOff(70, 0),
                       NoteOff(73, 0),
                       NoteOff(77, 0)])

        B = keys[11]
        @keybow.on_press(B)
        def press_handler(B):

            play_chord([NoteOn(71, 127),
                       NoteOn(74, 127),
                       NoteOn(78, 127)], arpeggio_mode)

        @keybow.on_release(B)
        def release_handler(B):

            midi.send([NoteOff(71, 0),
                       NoteOff(74, 0),
                       NoteOff(78, 0)])


                      #Maj7 chord
    if not keys[15].pressed and not keys[14].pressed \
    and keys[13].pressed and not keys[12].pressed:
        C = keys[0]
        @keybow.on_press(C)
        def press_handler(C):

            play_chord([NoteOn(60, 127),
                       NoteOn(64, 127),
                       NoteOn(71, 127)], arpeggio_mode)

        @keybow.on_release(C)
        def release_handler(C):

            midi.send([NoteOff(60, 0),
                       NoteOff(64, 0),
                       NoteOff(71, 0)])

        Db = keys[1]
        @keybow.on_press(Db)
        def press_handler(Db):

            play_chord([NoteOn(61, 127),
                       NoteOn(65, 127),
                       NoteOn(72, 127)], arpeggio_mode)
       
        @keybow.on_release(Db)
        def release_handler(Db):

            midi.send([NoteOff(61, 0),
                       NoteOff(65, 0),
                       NoteOff(72, 0)])

        D = keys[2]
        @keybow.on_press(D)
        def press_handler(D):

            play_chord([NoteOn(62, 127),
                       NoteOn(66, 127),
                       NoteOn(73, 127)], arpeggio_mode)
       
        @keybow.on_release(D)
        def release_handler(D):

            midi.send([NoteOff(62, 0),
                       NoteOff(66, 0),
                       NoteOff(73, 0)])

        Eb = keys[3]
        @keybow.on_press(Eb)
        def press_handler(Eb):

            play_chord([NoteOn(63, 127),
                       NoteOn(67, 127),
                       NoteOn(74, 127)], arpeggio_mode)
       
        @keybow.on_release(Eb)
        def release_handler(Eb):

            midi.send([NoteOff(63, 0),
                       NoteOff(67, 0),
                       NoteOff(74, 0)])

        E = keys[4]
        @keybow.on_press(E)
        def press_handler(E):

            play_chord([NoteOn(64, 127),
                       NoteOn(68, 127),
                       NoteOn(75, 127)], arpeggio_mode)

        @keybow.on_release(E)
        def release_handler(E):

            midi.send([NoteOff(64, 0),
                       NoteOff(68, 0),
                       NoteOff(75, 0)])

        F = keys[5]
        @keybow.on_press(F)
        def press_handler(F):

            play_chord([NoteOn(65, 127),
                       NoteOn(69, 127),
                       NoteOn(76, 127)], arpeggio_mode)
       
        @keybow.on_release(F)
        def release_handler(F):

            midi.send([NoteOff(65, 0),
                       NoteOff(69, 0),
                       NoteOff(76, 0)])

        Gb = keys[6]
        @keybow.on_press(Gb)
        def press_handler(Gb):

            play_chord([NoteOn(66, 127),
                       NoteOn(70, 127),
                       NoteOn(77, 127)], arpeggio_mode)
       
        @keybow.on_release(Gb)
        def release_handler(Gb):

            midi.send([NoteOff(66, 0),
                       NoteOff(70, 0),
                       NoteOff(77, 0)])

        G = keys[7]
        @keybow.on_press(G)
        def press_handler(G):

            play_chord([NoteOn(67, 127),
                       NoteOn(71, 127),
                       NoteOn(78, 127)], arpeggio_mode)
       
        @keybow.on_release(G)
        def release_handler(G):

            midi.send([NoteOff(67, 0),
                       NoteOff(71, 0),
                       NoteOff(78, 0)])

        Ab = keys[8]
        @keybow.on_press(Ab)
        def press_handler(Ab):

            play_chord([NoteOn(68, 127),
                       NoteOn(72, 127),
                       NoteOn(79, 127)], arpeggio_mode)
       
        @keybow.on_release(Ab)
        def release_handler(Ab):

            midi.send([NoteOff(68, 0),
                       NoteOff(72, 0),
                       NoteOff(79, 0)])

        A = keys[9]
        @keybow.on_press(A)
        def press_handler(A):

            play_chord([NoteOn(69, 127),
                       NoteOn(73, 127),
                       NoteOn(80, 127)], arpeggio_mode)

        @keybow.on_release(A)
        def release_handler(A):

            midi.send([NoteOff(69, 0),
                       NoteOff(73, 0),
                       NoteOff(80, 0)])

        Bb = keys[10]
        @keybow.on_press(Bb)
        def press_handler(Bb):

            play_chord([NoteOn(70, 127),
                       NoteOn(74, 127),
                       NoteOn(81, 127)], arpeggio_mode)

        @keybow.on_release(Bb)
        def release_handler(Bb):

            midi.send([NoteOff(70, 0),
                       NoteOff(74, 0),
                       NoteOff(81, 0)])

        B = keys[11]
        @keybow.on_press(B)
        def press_handler(B):

            play_chord([NoteOn(71, 127),
                       NoteOn(75, 127),
                       NoteOn(82, 127)], arpeggio_mode)

        @keybow.on_release(B)
        def release_handler(B):

            midi.send([NoteOff(71, 0),
                       NoteOff(75, 0),
                       NoteOff(82, 0)])

                      #Min7 chord
    if not keys[15].pressed and not keys[14].pressed \
    and not keys[13].pressed and keys[12].pressed:
        C = keys[0]
        @keybow.on_press(C)
        def press_handler(C):

            play_chord([NoteOn(60, 127),
                       NoteOn(63, 127),
                       NoteOn(70, 127)], arpeggio_mode)

        @keybow.on_release(C)
        def release_handler(C):

            midi.send([NoteOff(60, 0),
                       NoteOff(63, 0),
                       NoteOff(70, 0)])

        Db = keys[1]
        @keybow.on_press(Db)
        def press_handler(Db):

            play_chord([NoteOn(61, 127),
                       NoteOn(64, 127),
                       NoteOn(71, 127)], arpeggio_mode)
       
        @keybow.on_release(Db)
        def release_handler(Db):

            midi.send([NoteOff(61, 0),
                       NoteOff(64, 0),
                       NoteOff(71, 0)])

        D = keys[2]
        @keybow.on_press(D)
        def press_handler(D):

            play_chord([NoteOn(62, 127),
                       NoteOn(65, 127),
                       NoteOn(72, 127)], arpeggio_mode)

        @keybow.on_release(D)
        def release_handler(D):

            midi.send([NoteOff(62, 0),
                       NoteOff(65, 0),
                       NoteOff(72, 0)])

        Eb = keys[3]
        @keybow.on_press(Eb)
        def press_handler(Eb):

            play_chord([NoteOn(63, 127),
                       NoteOn(66, 127),
                       NoteOn(73, 127)], arpeggio_mode)

        @keybow.on_release(Eb)
        def release_handler(Eb):

            midi.send([NoteOff(63, 0),
                       NoteOff(66, 0),
                       NoteOff(73, 0)])

        E = keys[4]
        @keybow.on_press(E)
        def press_handler(E):

            play_chord([NoteOn(64, 127),
                       NoteOn(67, 127),
                       NoteOn(74, 127)], arpeggio_mode)

        @keybow.on_release(E)
        def release_handler(E):

            midi.send([NoteOff(64, 0),
                       NoteOff(67, 0),
                       NoteOff(74, 0)])

        F = keys[5]
        @keybow.on_press(F)
        def press_handler(F):

            play_chord([NoteOn(65, 127),
                       NoteOn(68, 127),
                       NoteOn(75, 127)], arpeggio_mode)

        @keybow.on_release(F)
        def release_handler(F):

            midi.send([NoteOff(65, 0),
                       NoteOff(68, 0),
                       NoteOff(75, 0)])

        Gb = keys[6]
        @keybow.on_press(Gb)
        def press_handler(Gb):

            play_chord([NoteOn(66, 127),
                       NoteOn(69, 127),
                       NoteOn(76, 127)], arpeggio_mode)

        @keybow.on_release(Gb)
        def release_handler(Gb):

            midi.send([NoteOff(66, 0),
                       NoteOff(69, 0),
                       NoteOff(76, 0)])

        G = keys[7]
        @keybow.on_press(G)
        def press_handler(G):

            play_chord([NoteOn(67, 127),
                       NoteOn(70, 127),
                       NoteOn(77, 127)], arpeggio_mode)

        @keybow.on_release(G)
        def release_handler(G):

            midi.send([NoteOff(67, 0),
                       NoteOff(70, 0),
                       NoteOff(77, 0)])

        Ab = keys[8]
        @keybow.on_press(Ab)
        def press_handler(Ab):

            play_chord([NoteOn(68, 127),
                       NoteOn(71, 127),
                       NoteOn(78, 127)], arpeggio_mode)

        @keybow.on_release(Ab)
        def release_handler(Ab):

            midi.send([NoteOff(68, 0),
                       NoteOff(71, 0),
                       NoteOff(78, 0)])

        A = keys[9]
        @keybow.on_press(A)
        def press_handler(A):

            play_chord([NoteOn(69, 127),
                       NoteOn(72, 127),
                       NoteOn(79, 127)], arpeggio_mode)

        @keybow.on_release(A)
        def release_handler(A):

            midi.send([NoteOff(69, 0),
                       NoteOff(72, 0),
                       NoteOff(79, 0)])

        Bb = keys[10]
        @keybow.on_press(Bb)
        def press_handler(Bb):

            play_chord([NoteOn(70, 127),
                       NoteOn(73, 127),
                       NoteOn(80, 127)], arpeggio_mode)

        @keybow.on_release(Bb)
        def release_handler(Bb):

            midi.send([NoteOff(70, 0),
                       NoteOff(73, 0),
                       NoteOff(80, 0)])

        B = keys[11]
        @keybow.on_press(B)
        def press_handler(B):

            play_chord([NoteOn(71, 127),
                       NoteOn(74, 127),
                       NoteOn(81, 127)], arpeggio_mode)

        @keybow.on_release(B)
        def release_handler(B):

            midi.send([NoteOff(71, 0),
                       NoteOff(74, 0),
                       NoteOff(81, 0)])
