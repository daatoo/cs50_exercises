# TODO
while True:
    try:
        height = int(input("Height: "))
        if (height >= 1) and (height <=8):
            break
    except:
        print("", end="")

for i in range(height):

    for spaces in range(height-i-1):
        print(" ", end="")

    for j in range(i+1):
        print("#", end="")

    print("  ", end="")

    for j in range(i+1):
        print("#", end="")


    print()