import urllib2,json
import time
import RPi.GPIO as gpio

gpio.setwarnings(False)

#for mailing
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


fromaddr="from address"
toaddr="to address"



gpio.setmode(gpio.BOARD)
gpio.setup(40,gpio.OUT)#for led glowing
gpio.setup(3,gpio.OUT)#for rotating fan
gpio.setup(5,gpio.OUT)#for rotating fan
gpio.output(3,0)
gpio.output(5,0)


data='xy'.encode('utf8')
bata='89'.encode('utf8')
while(1) :
    
    conn=urllib2.urlopen("https://api.thingspeak.com/channels/562273/feeds/last.json?api_key=SFPISK14ISF5F0SN")
    response=conn.read()
    data=json.loads(response)
    
   
   
    
    
    

    if((data['field4']=="009".encode('utf8') or data['field4']=="007".encode('utf8')) and data!=bata):

        # Physical pins 11,12,13,15
        # GPIO11,GPIO12,GPIO13,GPIO15
        StepPins = [11,12,13,15]
 
        # Set all pins as output
        for pin in StepPins:
            print "Setup pins"
            gpio.setup(pin,gpio.OUT)
            gpio.output(pin, False)
 
    # Define advanced sequence
    # as shown in manufacturers datasheet
        Seq = [[1,0,0,1],
                [1,0,0,0],
               [1,1,0,0],
           [0,1,0,0],
           [0,1,1,0],
           [0,0,1,0],
           [0,0,1,1],
           [0,0,0,1]]
        
        StepCount = len(Seq)
        StepDir = 1 # Set to 1 or 2 for clockwise
        # Set to -1 or -2 for anti-clockwise
        # Initialise variables
        StepCounter = 0
 
        # Start main loop
        for i in range(400):
 
            print StepCounter
            print Seq[StepCounter]
 
            for pin in range(0, 4):
                xpin = StepPins[pin]
                if Seq[StepCounter][pin]!=0:
                    print " Enable GPIO %i" %(xpin)
                    gpio.output(xpin, True)
                else:
                    gpio.output(xpin, False)
 
            StepCounter += StepDir
 
            # If we reach the end of the sequence
            # start again
            if (StepCounter>=StepCount):
                StepCounter = 0
            if (StepCounter<0):
                StepCounter = StepCount+StepDir
 
            # Wait before moving on
            time.sleep(.01)
	gpio.output(40,1)
        time.sleep(4)

    

        #for rotating fan
        if(data["field2"]>'40'.encode('utf8')):
            gpio.output(3,1)
            gpio.output(5,0)
	    
            time.sleep(5)


        #mailing part if
        
        
	
       
        if data['field4']=='009'.encode('utf8'):
		msg=MIMEMultipart()
	        msg['from']=fromaddr
        	msg['to']=toaddr
        	msg['subject']="Someone Entered !"


		body="sourabh checked in !"
		
		msg.attach(MIMEText(body,'plain'))
		server=smtplib.SMTP('smtp.gmail.com',587)
	        server.starttls()
        	server.login(fromaddr,"Exploreiot18*")

		text=msg.as_string()
		server.sendmail(fromaddr,toaddr,text)
		server.quit()
	else:
		msg=MIMEMultipart()
        	msg['from']=fromaddr
		msg['to']=toaddr
        	msg['subject']="Someone Entered !"
	

		body="himanshu checked in !"
		msg.attach(MIMEText(body,'plain'))
                server=smtplib.SMTP('smtp.gmail.com',587)
        	server.starttls()
        	server.login(fromaddr,"from address mail password")
	
		text=msg.as_string()
		server.sendmail(fromaddr,toaddr,text)
		server.quit()

        print 'email sent from if'
        

    elif((data['field4']=='001'.encode('utf8')) and (data!=bata) ):
        msg=MIMEMultipart()
        msg['from']=fromaddr
        msg['to']=toaddr
        msg['subject']="Invalid card Scanned !"
        
	body="Unknown tries to enter"
	msg.attach(MIMEText(body,'plain'))
	server=smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(fromaddr,"from address mail password")
        text=msg.as_string()
        server.sendmail(fromaddr,toaddr,text)
        print 'email sent from else'
        server.quit()

        
    
    bata=data
    conn.close()
	

