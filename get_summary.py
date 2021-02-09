import sys

if __name__ == '__main__':
    with open(sys.argv[1], "r") as file:
        first_line = file.readline()
        for last_line in file:
            pass
        print(last_line.replace('=', '').strip())
