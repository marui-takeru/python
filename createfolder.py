import os

for i in range(1, 166):
    number=str(i).zfill(3)
    os.mkdir(str(number))
