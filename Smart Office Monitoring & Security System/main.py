from machine import Pin,ADC,PWM,time_pulse_us,I2C
from dht import DHT22 
import time
import math
import ssd1306
import network
import BlynkLib

BLYNK_TEMPLATE_ID = "TMPL2PvSilT32"
BLYNK_TEMPLATE_NAME = "Smart Office Monitoring And Security System"
BLYNK_AUTH_TOKEN = "-aQ3BrucFh4D41pKzIr-lTsO5u3WKQk5"

# ---------------- WiFi ----------------

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect("Wokwi-GUEST", "")

print("Connecting WiFi...")

while not wifi.isconnected():
    time.sleep(0.1)

print("WiFi Connected!")

# ---------------- Blynk ----------------

blynk = BlynkLib.Blynk(
    BLYNK_AUTH_TOKEN,
    tmpl_id=BLYNK_TEMPLATE_ID,
    insecure=True
)
# ------------------- Inputs Pins -------------------------------- #

DHT22_PIN         = 13
PIR_PIN           = 12
ULT_ECHO_PIN      = 14
PAGE_PIN          = 26
DOORBELL_PIN      = 27
LDR_PIN           = 33
WATER_LVL_PIN     = 32
GAS_SENS_PIN      = 35

# ------------------- Output Pins -------------------------------- #

RGB_RED_PIN       = 15
RGB_GREEN_PIN     = 2
RGB_BLUE_PIN      = 0
LAMP_PIN          = 4
FAN_PIN           = 23
ALERT_RED_LED_PIN = 16
ALERT_BUZZER_PIN  = 17
SERVO_PIN         = 5
ULT_TRIG_PIN      = 18
NORMAL_GREEN_LED  = 19
OLED_SDA_PIN      = 21
OLED_SCL_PIN      = 22

# --------------------------- Limits/Thresholds ------------------- #

TEMPERATURE_THRESHOLD =  37
HUMIDITY_THRESHOLD    =  80 
MIN_DISTANCE          =  40
CRITICAL_GAS_CONC     =  400
LOW_LIGHT_LEVEL       =  500
MIN_WATER_LEVEL       =  20
AUTO                  =  0
WARNING_FREQ          =  900
ALARM_FREQ            =  1500
DOORBELL_FREQ         =  2000

SERIAL_SAMPLE_TIME     =  500
DISTANCE_SAMPLE_TIME   =  1000
DHT22_SAMPLE_TIME      =  2000
GAS_SAMPLE_TIME        =  500
LIGHT_SAMPLE_TIME      =  500
WATER_SAMPLE_TIME      =  500
CONNECTION_SAMPLE_TIME =  500

# ------------------ Pin Configuration ---------------------------- #

# Input Sensors
water_lvl_adc    = ADC(Pin(WATER_LVL_PIN))
light_intens_adc = ADC(Pin(LDR_PIN))
gas_sensor_adc   = ADC(Pin(GAS_SENS_PIN))
temp_humid_sens  = DHT22(Pin(DHT22_PIN))
PIR_sensor       = Pin(PIR_PIN,Pin.IN)
ULTRASONIC_TRIG  = Pin(ULT_TRIG_PIN,Pin.OUT)
ULTRASONIC_ECHO  = Pin(ULT_ECHO_PIN,Pin.IN)
page_but         = Pin(PAGE_PIN,Pin.IN,Pin.PULL_UP)
doorbell_but     = Pin(DOORBELL_PIN,Pin.IN,Pin.PULL_UP)

# Output Actuators
lamp             = Pin(LAMP_PIN,Pin.OUT)
fan              = Pin(FAN_PIN,Pin.OUT)
RGB_red_led      = PWM(Pin(RGB_RED_PIN),freq=1000)
RGB_green_led    = PWM(Pin(RGB_GREEN_PIN),freq=1000)
RGB_blue_led     = PWM(Pin(RGB_BLUE_PIN),freq=1000)

def RGB_LEDs_off():
    RGB_red_led.duty(0)
    RGB_green_led.duty(0)
    RGB_blue_led.duty(0)
RGB_LEDs_off()

servo            = PWM(Pin(SERVO_PIN),freq=50)

buzzer           = PWM(Pin(ALERT_BUZZER_PIN),freq=1000)
buzzer.duty(0)

alert_green_led  = Pin(19,Pin.OUT)
alert_red_led    = Pin(16,Pin.OUT) 

i2c = I2C(sda=Pin(OLED_SDA_PIN), scl=Pin(OLED_SCL_PIN))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
oled.fill(0)
oled.text("Driver Connected!", 0, 0)
oled.show()

# -------------------- Variables ----------------------------------- #
last_read_time     = time.ticks_ms()  
is_motion          = False
past_page_val      = 0
past_doorbell_val  = 0
past_doorbell_time = time.ticks_ms()
doorbell_pressed   = False

page_number        = -1
past_oled_time     = time.ticks_ms()

connection_led     = 1
connection_status  = False

serial_past_time   = 0

# System Data
temperature        = 0.0
humidity           = 0.0
light_intensity    = 0.1
gas_concentration  = 0.1 
water_level        = 0
motion_state       = False
distance           = 0

mode               = AUTO
is_auto            = mode == AUTO
system_status      = "Healthy"


past_dht22_read_time        = 0
past_light_read_time        = 0
past_gas_read_time          = 0
past_water_read_time        = 0
past_distance_read_time     = 0
past_time_connection_status = 0
# -------------------- Input Functions ---------------------------------- #

# Water Level Potentiometer
def read_water():
    water_adc_value = water_lvl_adc.read()
    if water_adc_value > 4095:
        water_adc_value = 4095
    elif water_adc_value < 0 :
        water_adc_value = 0
    return ((water_adc_value * 100)/ 4095)

# Light Sensor Intensity Function
def read_light():
    light_adc_value = light_intens_adc.read()
    if light_adc_value > 4095:
        light_adc_value = 4095
    elif light_adc_value < 0 :
        light_adc_value = 0
    
    # Predefined formula for LDR Sensor
    GAMMA = 0.7;
    RL10 = 50;
    voltage = light_adc_value / 4095. * 5;
    resistance = 2000 * voltage / (1 - voltage / 5);
    lux = math.pow(RL10 * 1e3 * pow(10, GAMMA) / resistance, (1 / GAMMA));

    return lux

def warming_up_gas_sens():
    time.sleep_ms(200)
warming_up_gas_sens()

# Gas Sensor Concentration 
def read_gas():
    # Your calibration data profile
    ADC_TABLE = [843, 962, 1267, 1637, 1769, 2603, 2924, 3146, 3436, 3643, 3679, 3732, 3774, 3889, 3899, 3916, 3932, 3940, 3959, 3993, 4007, 4025, 4029, 4033, 4038, 4041]
    PPM_TABLE = [0.1, 0.2, 0.3, 0.4, 1.0, 10.0, 25.0, 50.0, 151.0, 437.0, 550.0, 794.0, 1096.0, 3467.0, 3981.0, 5012.0, 6310.0, 7244.0, 10000.0, 20893.0, 30200.0, 52481.0, 60256.0, 72444.0, 87096.0, 100000.0]

    # Pre-calculate Log10 values of PPM for high accuracy mapping across exponential spans
    LOG_PPM_TABLE = [math.log10(x) for x in PPM_TABLE]
    
    gas_adc_value = gas_sensor_adc.read()
    
    # Bound input to the table's absolute lower and upper limits
    if gas_adc_value <= ADC_TABLE[0]:
        return PPM_TABLE[0], gas_adc_value
    if gas_adc_value >= ADC_TABLE[-1]:
        return PPM_TABLE[-1], gas_adc_value
        
    # Binary search to find the correct lookup table data index segment
    low = 0
    high = len(ADC_TABLE) - 1
    while high - low > 1:
        mid = (low + high) // 2
        if gas_adc_value >= ADC_TABLE[mid]:
            low = mid
        else:
            high = mid
            
    # Extract lower and upper boundary bounds
    adc0, adc1 = ADC_TABLE[low], ADC_TABLE[high]
    log_ppm0, log_ppm1 = LOG_PPM_TABLE[low], LOG_PPM_TABLE[high]
    
    # Calculate interpolation percentage weight between the two points
    weight = (gas_adc_value - adc0) / (adc1 - adc0)
    
    # Interpolate smoothly within logarithmic scale
    log_predicted_ppm = log_ppm0 + weight * (log_ppm1 - log_ppm0)
    
    # Revert base-10 exponent back to real PPM values
    PPM = math.pow(10, log_predicted_ppm)
    return PPM, gas_adc_value

# Temperature and Humidity Sensor
def temp_and_humid_read():
    temp_humid_sens.measure()
    temperature = temp_humid_sens.temperature()
    humidity    = temp_humid_sens.humidity()
    return (temperature,humidity) 

def motion_capture():
    global last_read_time
    global is_motion
    current_time = time.ticks_ms()
    if(time.ticks_diff(current_time,last_read_time) >= 1200 ):
        motion_value = PIR_sensor.value()
        is_motion = motion_value == 1
        if is_motion:
            last_read_time = time.ticks_ms()
    return is_motion

def distance_measure():
    ULTRASONIC_TRIG.on()
    time.sleep_us(10)
    ULTRASONIC_TRIG.off()
    duration = time_pulse_us(ULT_ECHO_PIN, 1)
    speed = 340/1000000
    distance = (speed * duration) / 2
    return distance*100

def change_page():
    global past_page_val,page_number
    current_page_val = page_but.value()
    if(current_page_val == 0 and past_page_val == 1):
        page_number =(page_number + 1)%4
        try:
            blynk.virtual_write(15,page_number+1)
        except e as Exception:
            print("Blynk Not Connected")
    past_page_val = current_page_val
    return page_number

def doorbell_activate():
    global past_doorbell_val,doorbell_pressed,past_doorbell_time
    current_doorbell_val = doorbell_but.value()
    current_doorbell_time = time.ticks_ms()
    if (doorbell_pressed and time.ticks_diff(current_doorbell_time,past_doorbell_time) < 1500) :
       buzzer_control(1,freq=DOORBELL_FREQ)
    else :
        doorbell_pressed = False
        if(current_doorbell_val == 0 and past_doorbell_val == 1):
            doorbell_pressed = True
            past_doorbell_time = time.ticks_ms()
        else:
            buzzer_control(0,freq=DOORBELL_FREQ)
    past_doorbell_val = current_doorbell_val

# -------------------- Output Functions ---------------------------------- #

def lamp_control(control_signal):
    control = {
        "on":1,
        "off":0
    }
    lamp.value(control[control_signal])

def fan_control(control_signal):
    control = {
        "on":1,
        "off":0
    }
    fan.value(control[control_signal])

def RGB_control(color):
    colorList={
        "red"    : (255,0,0),
        "green"  : (0,255,0),
        "blue"   : (0,0,255),
        "yellow" : (255,255,0),
        "cyan"   : (0,255,255),
        "purple" : (255,0,255),
        "white"  : (255,255,255),
    }
    RGB_red_led.duty   ((colorList[color][0]*1023//255))
    RGB_green_led.duty ((colorList[color][1]*1023//255))
    RGB_blue_led.duty  ((colorList[color][2]*1023//255))                                          


def servo_control(angle):   
    if angle >= 0 and angle <= 180:
        to_time_ms = 0.5+(angle/180.0)*2 
        to_duty    = int((to_time_ms*1023)/20) 
        servo.duty(to_duty)

def buzzer_control(control_signal,level=100,freq=1000):
    if  0 <= level <= 100:
        volume = (level * 512) // 100
        if   control_signal == 1 :
            buzzer.duty(volume)
            buzzer.freq(freq)
        elif control_signal == 0 :
            buzzer.duty(0)
            buzzer.freq(freq)  

def green_led_control(control_signal):
    control = {
        "on"  : 1,
        "off" : 0
    }
    alert_green_led.value(control[control_signal])

def red_led_control(control_signal):
    control = {
        "on"  : 1,
        "off" : 0
    }
    alert_red_led.value(control[control_signal])

def oled_display():
    global page_number,connection_status,serial_past_time
    global temperature,humidity
    global light_intensity
    global gas_concentration
    global water_level
    global motion_state
    global distance

    global system_status
    global is_auto

    oled.fill(0)
    change_page()
    serial_current_time = time.ticks_ms()
    if page_number == -1 :
        oled.text("System Starting",1,0)
        print("=============================================")
        print("               System Start              ")
        print("=============================================")
    elif page_number == 0:
        oled.text("System Status",1,0)
        oled.text(f"{system_status[0:13]} ",1,10)
        oled.text("Connectivity ",1,20)
        oled.text(f"   {connection_status}  ",1,30)
        if is_auto:
            oled.text(f"Mode : Auto  ",1,40)
        else:
            oled.text(f"Mode : Man  ",1,40)            
        oled.text(" Page No. 1",1,50)
        if(time.ticks_diff(serial_current_time,serial_past_time) >= SERIAL_SAMPLE_TIME):
            print("=============================================")
            print("               System Status Page            ")
            print("=============================================")
            print("               System Status                 ")
            print(f"                  {system_status}           ")
            print(f"                Connectivity                ")
            print(f"                  {connection_status}       ")
            if is_auto:
                print("                    Mode : Automatic         ")
            else:
                print("                    Mode : Manual            ")
            print("                   Page 1                    ")
            print("                                             ")
            serial_past_time = serial_current_time
    elif page_number == 1 :
        oled.text("Temperature : ",1,0)
        oled.text(f"   {temperature} C ",1,10)
        oled.text("Humidity   :",1,20)
        oled.text(f"   {humidity} % ",1,30)
        oled.text(" Page No. 2",1,50)
        if(time.ticks_diff(serial_current_time,serial_past_time) >= SERIAL_SAMPLE_TIME):
            print("=============================================")
            print("               Temperature Humidity Page     ")
            print("=============================================")
            print("               Temperature                   ")
            print(f"                  {temperature} C           ")
            print(f"               Humidity                     ")
            print(f"                  {humidity} %              ")
            print("                                             ")
            print("                   Page 2                    ")
            print("                                             ")
            serial_past_time = serial_current_time
    elif page_number == 2 :
        oled.text(f"Motion : {motion_state}",1,0)
        oled.text("Distance : ",1,10)
        oled.text(f"   {distance} cm ",1,20)
        oled.text("Light : ",1,30)
        oled.text(f"{light_intensity} Lux ",1,40)
        oled.text(" Page No. 3",1,50)
        if(time.ticks_diff(serial_current_time,serial_past_time) >= SERIAL_SAMPLE_TIME):
            print("=============================================")
            print("               Distance-Motion Page          ")
            print("=============================================")
            print("                  Motion                     ")
            print(f"                  {motion_state}            ")
            print(f"                 Distance                   ")
            print(f"                  {distance} cm             ")
            print(f"                 Light Intensity            ")
            print(f"                  {light_intensity} Lux     ")
            print("                                             ")
            print("                   Page 3                    ")
            print("                                             ")
            serial_past_time = serial_current_time
    elif page_number == 3 :
        oled.text("Water lvl - Gas ",1,0)
        oled.text("Water lvl : ",1,10)
        oled.text(f"   {water_level} % ",1,20)
        oled.text("Gas Conc : ",1,30)
        oled.text(f"   {gas_concentration} ppm ",1,40)        
        oled.text(" Page No. 4",1,50)
        if(time.ticks_diff(serial_current_time,serial_past_time) >= SERIAL_SAMPLE_TIME):
            print("=============================================")
            print("               Water Level - Gas Conc Page   ")
            print("=============================================")
            print("               Water Level                   ")
            print(f"               {water_level} %              ")
            print(f"               Gas Concentration            ")
            print(f"                {gas_concentration} ppm     ")
            print("                                             ")
            print("                   Page 4                    ")
            print("                                             ")
            serial_past_time = serial_current_time
    oled.show()
    

# ------------------------------ Blynk Events--- ------------------------- #

@blynk.on("connected")
def connected():
    global connection_status , page_number
    print("Blynk is Connected")
    blynk.sync_virtual(13)
    blynk.sync_virtual(14)
    blynk.sync_virtual(15)
    blynk.sync_virtual(16)
    blynk.sync_virtual(17)
    blynk.sync_virtual(19)
    blynk.virtual_write(11,"Connected")
    blynk.virtual_write(18,connection_led)
    connection_status = True
    page_number += 1
    
    
    

@blynk.on("V13")
def blynk_lamp(value):
    global is_auto
    if not is_auto:
        lamp_control_signal = int(value[0])
        lamp_cont_list={
            0:"off",
            1:"on"
        }
        lamp_control(lamp_cont_list[lamp_control_signal])
    else:
        pass

    

@blynk.on("V14")
def blynk_mode_change(value):
    global mode
    mode_switch_val = int(value[0])
    mode            = mode_switch_val

    

@blynk.on("V15")
def blynk_page_change(value):
    global page_number
    page_number = int(value[0])-1

@blynk.on("V16")
def blynk_servo_angle(value):
    global is_auto
    if not is_auto:
        servo_angle = int(value[0])
        servo_control(servo_angle)
    else:
        pass
    

@blynk.on("V17")
def blynk_doorbell(value):
    global is_auto,doorbell_pressed,past_doorbell_time
    if not is_auto:
        doorbell_val = int(value[0])
        doorbell_pressed = doorbell_val == 1
        if doorbell_pressed:
            past_doorbell_time = time.ticks_ms()
    else:
        pass

@blynk.on("V19")
def blynk_fan(value):
    global is_auto
    if not is_auto:
        fan_control_signal = int(value[0])
        fan_cont_list={
            0:"off",
            1:"on"
        }
        fan_control(fan_cont_list[fan_control_signal])
    else:
        pass

def connection_status_check():
    global connection_led
    blynk.virtual_write(18,connection_led)
    connection_led = (1+connection_led)%2

def temp_humid_update(temperature,humidity):
    blynk.virtual_write(0,temperature)
    blynk.virtual_write(1,humidity)

def light_intens_update(light_intensity):
    blynk.virtual_write(4,light_intensity)

def gas_conc_update(gas_concentration):
    blynk.virtual_write(2,gas_concentration)

def water_level_update(water_level):
    blynk.virtual_write(3,water_level)

def motion_update(motion_state):
    if motion_state:
        blynk.virtual_write(6,"Occupied")
        blynk.virtual_write(7,1)
    else :
        blynk.virtual_write(6,"Empty")
        blynk.virtual_write(7,0)

def distance_update(distance):
    blynk.virtual_write(5,distance)


def mode_status_update():
    global is_auto
    blynk.virtual_write(20,"Auto" if is_auto else "Manual")

def alarm_sound_trigger():
    global system_status
    if system_status is "Emergency : Fire" or system_status is "Emergency : Gas" :
        blynk.virtual_write(12,1)
    else :
        blynk.virtual_write(12,0)

    

# ------------------- Input Test Functions ------------------------------- #

def water_lvl_test():
    water_level = read_water()
    print("--------------- Water Level Reading Test ----------------")
    print("Water Level : ",water_level," %")
    time.sleep_ms(200)

def light_intens_test():
    Light_Lux = read_light()
    print("--------------- Light Intensity Reading Test ----------------")
    print("Light Intensity : ",Light_Lux," Lux")
    time.sleep_ms(200)

def gas_sensor_test():
    gas_value = read_gas()
    print("--------------- Gas Sensor Reading Test ----------------")
    print("Gas Value : ",gas_value," ppm", " ADC Value : ",gas_adc_value)
    time.sleep_ms(200)

def temp_humid_test():
    (temperature,humidity) = temp_and_humid_read()
    print("------------- Temperature and Humidity Reading Test ------")
    print("Temperature : ", temperature , " C")
    print("Humidity    : ", humidity , " %")

def motion_test():
    motion_occured = motion_capture()
    print("---------------------- Motion Detection Test ----------------")
    print("Motion : ",motion_occured, " Time Stamp : ",time.ticks_ms()/1000)
    time.sleep_ms(200)

def distance_test():
    distance = distance_measure()
    print("---------------------- Distance Measure Test ----------------")
    print("Distance : ", distance, " cm")
    time.sleep_ms(200)
def doorbell_pageChange_test():
    page_val = change_page()
    print("---------------------- Page Change Test ----------------")
    if page_val == 0:
        print("Page 1 : Automatic Control")
    else:
        print("Page 2 : Manual Control")
    print("------------------------ Doorbell Test ------------------")
    doorbell_activate()
    time.sleep_ms(200)


# ------------------- Output Test Functions ------------------------------ #

def lamp_control_test():
    lamp_control("on")
    time.sleep_ms(1000)
    lamp_control("off")
    time.sleep_ms(1000)

def fan_control_test():
    fan_control("on")
    time.sleep_ms(1000)
    fan_control("off")
    time.sleep_ms(1000)

def RGB_test():
    RGB_control("red")
    time.sleep_ms(1000)
    RGB_control("blue")
    time.sleep_ms(1000)
    RGB_control("green")
    time.sleep_ms(1000)
    RGB_control("yellow")
    time.sleep_ms(1000)
    RGB_control("cyan")
    time.sleep_ms(1000)
    RGB_control("purple")
    time.sleep_ms(1000)
    RGB_control("white")
    time.sleep_ms(1000)

def servo_control_test():
    print("------------------------ Servo Test ------------------")
    for angle in range(0,180,1):
        print("Servo at angle = ",angle," degree")
        servo_control(angle)
        time.sleep_ms(100)

def buzzer_test():
    print("------------------------ Buzzer Test ------------------")
    print("Normal Mode : No Sound")
    print(" ")
    buzzer_control(0)
    time.sleep_ms(500)
    print("Warning Buzzer Sound")
    print(" ")
    for _ in range(5):
        buzzer_control(1)
        time.sleep_ms(100)
        buzzer_control(0)
        time.sleep_ms(100)
    print("Alarm Buzzer Sound")
    print(" ")
    buzzer_control(1,50,400)
    time.sleep_ms(500)
    print("Emergency Buzzer Sound")
    print(" ")
    buzzer_control(1,freq=2000)
    time.sleep_ms(500)

def alert_leds_test():
    green_led_control("on")
    red_led_control  ("off")
    time.sleep_ms(500)
    green_led_control("off")
    red_led_control  ("off")
    time.sleep_ms(500)
    green_led_control("off")
    red_led_control  ("on")
    time.sleep_ms(500)
    green_led_control("on")
    red_led_control  ("on")
    time.sleep_ms(500)

def display_test():
    oled_display()
# ------------------------------- Logic Functions --------------------- #
past_system_time = 0
led_blink_flag   = 0

def check_system_status():
    global temperature,humidity
    global light_intensity
    global gas_concentration
    global water_level
    global motion_state
    global distance
    global is_auto
    global system_status
    global past_system_time
    global led_blink_flag

    current_system_time = time.ticks_ms()
    system_status = "Healthy"

    is_hot        = temperature > TEMPERATURE_THRESHOLD
    is_gasy       = gas_concentration > CRITICAL_GAS_CONC
    
    is_sultry     =  humidity    > HUMIDITY_THRESHOLD

    is_dry        = water_level < MIN_WATER_LEVEL

    is_dark       = light_intensity < LOW_LIGHT_LEVEL
    is_occupied   = motion_state == True

    is_near       = distance < MIN_DISTANCE

    is_auto       = mode == AUTO
    is_RGB_locked = False

    if is_auto :
        # System Status Check Critical

        if is_hot and is_gasy :
            system_status = "Emergency : Fire"
            # Turn Red LED On and Buzzer Alarm
            # RGB LED => Red , RGB Locked
            red_led_control("on")
            buzzer_control(1,freq=ALARM_FREQ)
            RGB_control("red")
            is_RGB_locked = True
        elif is_gasy :
            system_status = "Emergenecy : Gas"
            # Blink Red LED and Buzzer Warning
            if time.ticks_diff(current_system_time,past_system_time) > 500:
                if led_blink_flag == 0 :
                    red_led_control("off")
                    buzzer_control(0,freq=WARNING_FREQ)
                else:
                    red_led_control("on")
                    buzzer_control(1,freq=WARNING_FREQ)
                led_blink_flag =(1 + led_blink_flag)%2
                past_system_time = current_system_time

            # Servo go 90 degree
            servo_control(90)
            # RGB LED => Yellow , RGB Locked
            fan_control("on")
            RGB_control("yellow")
            is_RGB_locked = True
        elif is_dark and is_occupied:
            system_status = "Dark Room"
            # Turn Green LED On
            green_led_control("on")
            red_led_control("off")
            buzzer_control(0)
            # Lamp Relay Turn On
            lamp_control("on")
            # RGB LED => Purple , RGB Locked
            RGB_control("purple")
            is_RGB_locked = True
        elif is_hot or is_sultry:
            system_status = "Hot Weather"
            # Turn Green LED On
            green_led_control("on")
            red_led_control("off")
            buzzer_control(0)
            # Fan Relay Turn On
            fan_control("on")
            # RGB LED => White , RGB Locked
            RGB_control("white")
            is_RGB_locked = True
        else :
            
            # Turn Green LED On
            red_led_control("off")
            
            # RGB Released
            # Lamp Relay Turn Off
            lamp_control("off")
            fan_control("off")
            servo_control(0)
            is_RGB_locked = False
            
            # Door Monitor System
            if is_near:
                # Play Buzzer Tone as Doorbell
                if time.ticks_diff(current_system_time,past_system_time) > 200:
                    if led_blink_flag == 0 :
                        green_led_control("off")
                        buzzer_control(0,freq=DOORBELL_FREQ)
                    else:
                        green_led_control("on")
                        buzzer_control(1,freq=DOORBELL_FREQ)
                    led_blink_flag =(1 + led_blink_flag)%2
                    past_system_time = current_system_time


            else:
                # Turn Green LED on and Stop Buzzer
                green_led_control("on")
                buzzer_control(0)
                
        
            # Hydration Meter
            if is_dry :
                system_status = "Low Water"
                # RGB LED => Blue , RGB Released
                if not is_RGB_locked:
                    RGB_control("blue")
            else:
                system_status = "Healthy"
                # RGB LED => Cyan , RGB Released
                if not is_RGB_locked:
                    RGB_control("cyan")
        

    else:
        system_status = "Manual"
        # Turn Red LED Off
        red_led_control("off")
        # Green LED Blink
        if time.ticks_diff(current_system_time,past_system_time) > 200:
                    if led_blink_flag == 0 :
                        green_led_control("off")
                    else:
                        green_led_control("on")
                    led_blink_flag =(1 + led_blink_flag)%2
                    past_system_time = current_system_time
        # Check Doorbell Button
        doorbell_activate()
        # RGB LED => Green
        RGB_control("green")
        # RGB Released
        is_RGB_locked = False

def update():
    global temperature,humidity
    global light_intensity
    global gas_concentration
    global water_level
    global motion_state
    global distance
    global system_status

    global past_dht22_read_time 
    global past_light_read_time 
    global past_gas_read_time 
    global past_water_read_time 
    global past_distance_read_time 
    global past_time_connection_status

    now = time.ticks_ms()

    if (time.ticks_diff(now,past_dht22_read_time) > DHT22_SAMPLE_TIME):
        (temperature,humidity) = temp_and_humid_read()
        
        past_dht22_read_time = now

    if (time.ticks_diff(now,past_light_read_time) > LIGHT_SAMPLE_TIME):
        light_intensity        = read_light()
        
        past_light_read_time = now

    if (time.ticks_diff(now,past_gas_read_time) > GAS_SAMPLE_TIME):
        gas_concentration      = read_gas()[0]
        
        past_gas_read_time = now

    if (time.ticks_diff(now,past_water_read_time) > WATER_SAMPLE_TIME):
        water_level            = read_water()
        
        past_water_read_time = now
    if (time.ticks_diff(now,past_distance_read_time) > DISTANCE_SAMPLE_TIME):
        distance               = distance_measure()
        
        past_distance_read_time = now
    
    if(time.ticks_diff(now,past_time_connection_status) > CONNECTION_SAMPLE_TIME):
        connection_status_check()
        temp_humid_update(temperature,humidity)
        light_intens_update(light_intensity)
        gas_conc_update(gas_concentration)
        water_level_update(water_level)
        distance_update(distance)
        motion_update(motion_state)
        mode_status_update()
        alarm_sound_trigger()
        past_time_connection_status = now
    
    motion_state           = motion_capture()
    check_system_status()
    oled_display()



while True:
    blynk.run()
    update()
    