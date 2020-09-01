import sys
import time
import readline

def main():
    print()
    print("Hello: ",end='')
    time.sleep(2)
    line = readline.get_line_buffer()
    print(line)
    pass

if __name__ == '__main__':
    main()