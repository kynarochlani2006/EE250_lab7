import time
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# Constants
LED_PIN = 11
SPI_PORT = 0
SPI_DEVICE = 0
SPI_PORT2 = 1
LIGHT_THRESHOLD = 350
SOUND_THRESHOLD = 350

# Initialize GPIO and MCP3008
def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LED_PIN, GPIO.OUT)
    return Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

# Blink LED
def blink_led(times, speed):
    for _ in range(times):
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(speed)
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(speed)

# Read light and print status
def read_light(mcp, duration):
    start_time = time.time()
    while(time.time() - start_time) < duration:
        light = mcp.read_adc(SPI_PORT)
        if light > LIGHT_THRESHOLD:
            print(f"{light} - showing bright")
        else:
            print(f"{light} - showing dark")
        time.sleep(0.1)

# Read sound and control LED based on sound presence
def read_sound(mcp, duration):
    start_time = time.time()
    while(time.time() - start_time) < duration:
        sound = mcp.read_adc(SPI_PORT2)
        if sound > SOUND_THRESHOLD:
            print(f"{sound} - sound playing")
            GPIO.output(LED_PIN, GPIO.HIGH)
        else:
            print(f"{sound} - sound done")
            GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(0.1)

def main():
    mcp = setup()
    
    print("Begining of 4 LED: ")
    blink_led(4, 0.5)
    print("4 LED blinks done!")

    print("Begining of 5 lights:")
    read_light(mcp, 5)
    print("End of 5 lights.")

    print("Begining of 10 LED: ")
    blink_led(10, 0.2)
    print("10 LED blinks done!")

    print("Begining of sound taking: ")
    read_sound(mcp, 10)
    print("sound taking done")
    
    GPIO.cleanup()

if __name__ == '__main__':
    main()
