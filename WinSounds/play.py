import winsound
from random import randint

FREQ_MAX = 32767
FREQ_MIN = 37
FREQ_HUMAN_MAX = 15000
s = 60

# 15k-20k or higher - humans can't hear
# frequency duration in milliseconds

for i in range(37, 1000):
    for j in range(37, 1000, 10):
        freq = randint(1000, 8000)
        winsound.Beep(freq, s * 2)
        print(freq)