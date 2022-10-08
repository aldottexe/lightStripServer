# lightStripServer
rpi addressable led strip controller 

clone this piece of crap garbage code in your /home/pi directory

next run 'sudo crontab -e' and throw this snippet in der: 
    
    @reboot sleep 120; sudo python3 /home/pi/lightStripServer/LightServer4/ls.py
    
you can probably decrease the sleep ammount, but my pi zero is super slow
