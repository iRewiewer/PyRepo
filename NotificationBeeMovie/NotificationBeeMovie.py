from notifypy import Notify

notification = Notify()
notification.title = "BeeMovie Reader"
notification.icon = "AnnoyMe.jpg"

import time, requests
page = requests.get('https://gist.githubusercontent.com/MattIPv4/045239bc27b16b2bcf7a3a9a4648c08a/raw/2411e31293a35f3e565f61e7490a806d4720ea7e/bee%2520movie%2520script')
script = page.text.split("\n")
i = 1
for sentence in script:
    print(f"({i}/{len(script)}) {sentence}")
    notification.message = f"({i}/{len(script)}) {sentence}"
    notification.send()
    time.sleep(3)
    i += 1