def calculate_factorial(n):
    if n == 0:
        return 1
    else:
        result = 1
        for i in range(1, n + 1):
            result *= i
        return result

def convert_degrees_to_radians(degrees):
    return degrees * (3.14159265358979323846 / 180.0)

def calculate_sine_degrees(degrees, terms=10):
    radians = convert_degrees_to_radians(degrees)
    sin_value = 0
    for n in range(terms):
        coefficient = (-1) ** n
        numerator = radians ** (2 * n + 1)
        denominator = calculate_factorial(2 * n + 1)
        sin_value += coefficient * (numerator / denominator)
    return sin_value

try:
    while True:
        try:
            degrees = input("Enter The Value Of X In Degrees: ")
            if not degrees.isdigit():
                raise ValueError("Invalid Input! Please Enter A Valid Number.")
            degrees = float(degrees)
        except ValueError as e:
            print(e)
            continue

        sin_x = calculate_sine_degrees(degrees)
        print(f"\033[1;32;40mThe Sine Of {degrees} Degrees Is: {sin_x}\033[0m")

        while True:
            another_value = input("Do You Want To Calculate Another Value? (yes/no): ").lower()
            if another_value == "no":
                print("Exiting Program...")
                exit()
            elif another_value == "yes":
                break
            else:
                print("Invalid Input! Please Enter 'yes' Or 'no'.")
                continue

except KeyboardInterrupt:
    print("\nProgram Interrupted. Exiting...")
