from win10toast import ToastNotifier
import time


if __name__ == '__main__':
	while True:
		try:
			time.sleep(1200)
			notification = ToastNotifier()
			notification.show_toast("Reminder to look away for 20 seconds!",
			                        duration=3, msg=" ")
		except:
			pass
