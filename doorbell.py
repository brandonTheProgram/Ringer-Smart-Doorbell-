from   twilio.rest import Client    # Import Client so that the Pi can
                                    # send SMS Messages
import pyimgur                      # Import pyimgur to upload photos
from   picamera    import PiCamera  # Import the function PiCamera
from   time        import sleep     # Import the function sleep
import RPi.GPIO    as     GPIO      # Import Raspberry Pi GPIO library
from   espeak      import espeak    # Make the Rasberry Pi speak
import pygame                       # Make the Rasberry Pi play sounds
  
#Store the basic information for Twilio, Imgur, and the Camera
account_sid     = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"  # The SID needed
                                                        # for the Twilio
                                                        # account
                                                        
auth_token      = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"  # The Token needed
                                                        # for the Twilio
                                                        # account
                                                        
CLIENT_IMGUR_ID = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"  # The id to connect
                                                        # to the Client
                                                        
IMAGE_DIR       = "/home/pi/"                           # The path of the 
                                                        # picture taken
                                                        
IMG             = "picture.jpg"                         # The file name the 
                                                        # picture will be 
                                                        # saved as
                                                        
RINGTONE_DIR    = "/home/pi/Ringtones/"                 # The ringtone dir

RINGTONE        = "ringtone.wav"                        # The ringtone name      

ALARM           = "alarm.wav"                           # The alarm name

client          = Client(account_sid, auth_token)       # Crate the client 
                                                        # for Twilio
                                                        
camera          = PiCamera()                            # The camera

# Initialize the Pygame to play sounds
pygame.init()
pygame.mixer.init()

# Initialize the sounds
my_ringtone     = pygame.mixer.Sound(RINGTONE_DIR + RINGTONE)
my_alarm        = pygame.mixer.Sound(RINGTONE_DIR + ALARM)

# Ignore warning for now
GPIO.setwarnings(False)

#Set the mode of the GPIO
GPIO.setmode(GPIO.BCM)

#Set the button GPIO18 for input
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    #Get the state of the push button
    button_state = GPIO.input(4)
    
    #If the Button is pressed, take a picture and send it to the user
    if button_state == False:
        #Play the ringtone
        my_ringtone.play()

        sleep(5)
        
        #Take the picture and store it
        camera.capture(IMAGE_DIR + IMG)
        
        sleep(3)

        my_ringtone.stop()
        
        #Verbally speak the message back to the person whom rang
        espeak.synth("Please wait one moment while I respond")
         
        #Store the picture for imgur
        image = pyimgur.Imgur(CLIENT_IMGUR_ID)
        
        #Upload the given picture to Imgur
        uploaded_image = image.upload_image(IMAGE_DIR + IMG)
        
        #Create a message to send to the user including the capture photo
        message = client.messages \
                  .create(
                      body='Someone is at your door! Press 1 to trigger' + 
                            'alarm or type a message to respond',
                      from_='+1xxxxxxxxxx',
                      media_url=uploaded_image.link,
                      to='+1xxxxxxxxxx',
                    )
                 
        #Give a cooldown timer in between pressing the button
        #It takes 15 sec to send the message
        sleep(20)

        #Get the list of messages
        message = client.messages.list(limit=5)[1].body
        
        if(message == "1"):
            my_alarm.play()
            message = "Please leave the premises"
            sleep(6)
            my_alarm.stop()
            
        #Verbally speak the message back to the person whom rang
        espeak.synth(message)
            
        sleep(5)
