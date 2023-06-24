#!/usr/bin/env python3
import os, sys, threading, queue, time, subprocess

button_1_selected = False
button_2_selected = False
DEBUG_BUTTON_STATES = False
POLL_BUTTON_INTERVAL_SECONDS = 0.10
button_1_pin = 4
button_2_pin = 17
q = queue.Queue()

def poll_button(BUTTON):
  subprocess.check_output(['raspi-gpio','set',str(BUTTON),'ip','pu'])
  previous_state = '1'
  while True:
    if DEBUG_BUTTON_STATES:
      print(f'Polling Button #{BUTTON}')
    button_state = subprocess.check_output(["raspi-gpio","get",str(BUTTON)]).decode().split(' ')[2].split('=')[1]
    if DEBUG_BUTTON_STATES:
      print(f'\tGot button state {button_state} for button {BUTTON}, previous state was {previous_state}')
    if button_state != previous_state:
      if DEBUG_BUTTON_STATES:
        print(f'\t\tButton #{BUTTON} Transitioned from state {previous_state} to {button_state}')
      if button_state == '0':
        if DEBUG_BUTTON_STATES:
          print(f'dispatching button #{BUTTON} event to queue...')
        q.put(BUTTON)
      previous_state = button_state
    time.sleep(POLL_BUTTON_INTERVAL_SECONDS)


def poll_threads():
  while True:
    if DEBUG_BUTTON_STATES:
      print(f'Waiting for button events...')
    pressed_button_number = q.get()
    print(f'Received event of pressed button #{pressed_button_number}')
    if pressed_button_number == 4:
      button_1_selected = True
      button_2_selected = False
    elif pressed_button_number == 17:
      button_1_selected = False
      button_2_selected = True

def setup_threads():
  threading.Thread(target=poll_button, args=[button_1_pin], daemon=True).start()
  threading.Thread(target=poll_button, args=[button_2_pin], daemon=True).start()
  if DEBUG_BUTTON_STATES:
    print('Started Button Threads')

if __name__ == "__main__":
  setup_threads()
  poll_threads()
