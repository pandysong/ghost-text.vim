import time
import server_thread

t = server_thread.ServerThread()
t.start()

time.sleep(0.3)  # wait for thread to start up before printing
print("started")
print("press any key to sotp")
input()
t.stop()
print("stopped")
