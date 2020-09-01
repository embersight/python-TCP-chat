import sys
import time
import readline

def main():
    for i in range(0, 101, 5):
      print("\r>> You have finished {}%".format(i), end='')
      sys.stdout.flush()
      time.sleep(.2)
      
if __name__ == '__main__':
    main()