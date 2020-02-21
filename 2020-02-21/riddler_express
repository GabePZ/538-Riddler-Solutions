def fahrenheit_to_celsius(temp: int) -> int:
    return int(round(((temp - 32) * 5)/9))

def same_backwards(fahrenheit_temp: int) -> None:
    celsius_temp = fahrenheit_to_celsius(fahrenheit_temp)
    if ''.join(reversed(str(celsius_temp))) == str(fahrenheit_temp):
        print(f'F: {fahrenheit_temp}, C: {celsius_temp}')

for f in range(0, 100_000):
    same_backwards(f)

## OUTPUT ##
F: 61, C: 16
F: 82, C: 28
F: 7514, C: 4157
