# from datetime import datetime, timedelta
# import time
#
# now = '0800'
# start = '0000'
# end = '1159'
#
# time_now = (datetime.strptime(now, "%H%M") - timedelta(hours=12)).time()
#
# start_time = (datetime.strptime(start, "%H%M") - timedelta(hours=12)).time()
# end_time = (datetime.strptime(end, "%H%M") - timedelta(hours=12)).time()
#
# print(start_time <= time_now < end_time)

update_list = []

update_list.append(1)
update_list.append(2)
update_list.append(3)

while update_list:
	print(update_list.pop())

print(update_list)
