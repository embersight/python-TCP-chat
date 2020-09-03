import sys
import threading
import time

input_lock = False

def user_input():
    input_lock = True
    print()
    sys.stdout.write("\033[F"+"\033[K") #previous line and delete
    response = input("Input: ")
    input_lock = False
    sys.stdout.write("\033[F"+"\033[K") #previous line and delete
    return response

def continuously_send():
    while True:
        message = user_input()
        print("User: "+message)

def continuously_receive():
    while True:
        time.sleep(1)
        if input_lock==False:
            print("",end='\n',flush=True)
        sys.stdout.write("\033[F"+"\033[K") #previous line and delete
        print("Some Output has been displayed.")
        print("Input: ", end='', flush=True)

def main():
    print(f'Starting Application')
    # Chat Input
    user_input_thread = threading.Thread(target=continuously_send, args=[])
    user_input_thread.daemon = True
    user_input_thread.start()

    # Chat Output
    output_thread = threading.Thread(target=continuously_receive, args=[])
    output_thread.daemon = True
    output_thread.start()



    while True:
        if not user_input_thread.is_alive():
            print(f'\nExiting Application')
            break

if __name__ == '__main__':
    main()