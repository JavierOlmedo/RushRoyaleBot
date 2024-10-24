import time
import webbrowser

def get_time():
    now = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
    return "[{now}] ".format(now=now)

def logprint(queue, event, bidroundOver=False):
    event = str(event)
    combined = [event, bidroundOver]
    queue.put(combined)

def open_url(url):
    webbrowser.open_new_tab(url)