import time
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

#using physical pin 11 to blink an LED
GPIO.setmode(GPIO.BOARD)
chan_list = [11]
LED_PIN = 11
GPIO.setup(chan_list, GPIO.OUT)

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

LIGHT_CH = 0  
SOUND_CH = 1  

# by taking readings and printing them out, find
# appropriate threshold levels and set them 
# accordingly. Then, use them to determine
# when it is light or dark, quiet or loud.
lux_threshold = 350
sound_threshold = 350



# helper functions
def blink_led(times, interval):
    """Blink LED n times with delay interval in seconds."""
    for _ in range(times):
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(interval)
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(interval)

def read_light_sensor(mcp, duration=5.0, interval=0.1):
    """Read light sensor for duration seconds."""
    print("\n--- Reading Light Sensor ---")
    start = time.time()
    while time.time() - start < duration:
        value = mcp.read_adc(LIGHT_CH)
        if value < lux_threshold:
            status = "bright"
        else:
            status = "dark"
        print("Light: {0:4d} -> {1}".format(value, status))
        time.sleep(interval)

def read_sound_sensor(mcp, duration=5.0, interval=0.1):
    """Read sound sensor for duration seconds."""
    print("\n--- Reading Sound Sensor ---")
    start = time.time()
    while time.time() - start < duration:
        value = mcp.read_adc(SOUND_CH)
        print("Sound: {0:4d}".format(value))
        if value > sound_threshold:
            GPIO.output(LED_PIN, GPIO.HIGH)
            time.sleep(0.1)
            GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(interval)


while True: 
    time.sleep(0.5)
    blink_led(5, 0.5)
    read_light_sensor(mcp)
    blink_led(4, 0.2)
    read_sound_sensor(mcp)

    # Following commands control the state of the output (for manual testing)
    # GPIO.output(pin, GPIO.HIGH)
    # GPIO.output(pin, GPIO.LOW)

    # Example for reading raw ADC manually:
    # val = mcp.read_adc(0)
    # print(val)

    
