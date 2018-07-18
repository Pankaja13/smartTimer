import csv
from datetime import datetime, timedelta
import time
import atexit
import threading
import os


UPDATE_TIME = 60*10
# UPDATE_TIME = 20
update_list = []
updating_list = []
run_update_thread = True

try:
	import RPi.GPIO as GPIO
	GPIO.setmode(GPIO.BOARD)
	pass
except RuntimeError:
	print("Run with sudo!")

print('Initialising timetables')
times_list = []
with open('times.csv', newline='') as times_csv:
	raw_list = csv.reader(times_csv)
	for row in raw_list:
		if row:
			try:
				new_row = {
					'timer_no':		int(row[0]),
					'start_time':	(datetime.strptime(row[1], "%H%M") - timedelta(hours=12)) .time(),
					'end_time':		(datetime.strptime(row[2], "%H%M") - timedelta(hours=12)).time()
				}
				times_list.append(new_row)
			except ValueError as e:
				print(e)

print('Initialising pin layout')
pins = {}
with open('pins.csv', newline='') as times_csv:
	raw_list = csv.reader(times_csv)
	for row in raw_list:
		if row:
			timer = int(row[0])
			input_pin = int(row[1])
			output_pin = int(row[2])
			new_obj = {
				timer: {
					'input_pin': input_pin,
					'output_pin': output_pin
				}
			}
			pins.update(new_obj)

list_of_timers = []

for each_timer_row in times_list:
	list_of_timers.append(each_timer_row['timer_no'])
list_of_timers = list(set(list_of_timers))


def update_thread():
	print('Start Thread')
	while run_update_thread:
		while update_list:
			timer_to_power = update_list.pop()
			updating_list.append(timer_to_power)
			print('Updating Timer ', timer_to_power)
			pin_to_power = pins[timer_to_power]['output_pin']

			GPIO.output(pin_to_power, True)
			time.sleep(UPDATE_TIME)
			GPIO.output(pin_to_power, False)

			time.sleep(5)

			GPIO.output(pin_to_power, True)
			time.sleep(UPDATE_TIME)
			GPIO.output(pin_to_power, False)

			time.sleep(5)

			GPIO.output(pin_to_power, True)
			time.sleep(UPDATE_TIME)
			GPIO.output(pin_to_power, False)

			print('Powering Off Timer ', timer_to_power)
			updating_list.pop()
	print('Stop Thread')


def update_timers():

	timer_state = {}

	print('UpdateList ', updating_list, update_list)

	for x in list_of_timers:
		timer_state.update({x: False})

	for row in times_list:
		time_now = (datetime.now() - timedelta(hours=12)).time()
		timer = row['timer_no']

		start_time = row['start_time']
		end_time = row['end_time']

		if start_time <= time_now < end_time:
			timer_state[timer] = True

	for y in timer_state:
		set_pin(y, timer_state[y])

	print()
	print()


def set_pin(this_timer, state):
	this_pin = pins[this_timer]['output_pin']

	if this_timer not in updating_list:
		if state:
			# print(this_timer, ' - ', this_pin, ' ON')
			GPIO.output(this_pin, True)
		else:
			# print(this_timer, ' - ', this_pin, ' OFF')
			GPIO.output(this_pin, False)


def update_filimin(channel):
	for x in pins:
		if channel == pins[x]['input_pin']:
			timer_to_power = x
			if timer not in update_list:
				update_list.append(timer_to_power)
			else:
				print('Already updating')


@atexit.register
def goodbye():
	global run_update_thread
	run_update_thread = False
	print("Resetting GPIO and quitting")
	GPIO.cleanup()
	os._exit(0)


print('Setting Output Pins')
for each_timer in pins:
	GPIO.setup(pins[each_timer]['output_pin'], GPIO.OUT, initial=GPIO.LOW)

print('Setting Input Pins\n\n')
for each_timer in pins:
	GPIO.setup(pins[each_timer]['input_pin'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.add_event_detect(pins[each_timer]['input_pin'], GPIO.FALLING, callback=update_filimin, bouncetime=1000)


# Starting update thread
this_thread = threading.Thread(target=update_thread, daemon=True)
this_thread.start()


print('Starting Loop')
while True:
	try:
		update_timers()
		time.sleep(60)
	except KeyboardInterrupt:
		goodbye()
