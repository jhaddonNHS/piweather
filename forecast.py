import dynaconf
from config import settings
import json 
import time
import urllib.request
import urllib.parse
from inky import InkyPHAT
from inky.auto import auto
inky_display = auto(ask_user=True, verbose=True)
from PIL import Image,ImageDraw,ImageFont # Needed for the e-ink display.
import textwrap # This is so your text can wrap if it gets too long.
import datetime # To get time of last update.

meteocons = ImageFont.truetype('meteocons.ttf', 32) # Get here: https://www.alessioatzeni.com/meteocons/ and put .ttf file in the same directory
meteoconssmall = ImageFont.truetype('meteocons.ttf', 20) # This is the same for a smaller text size, in case you want smaller symbols.
glyphter = ImageFont.truetype('glyphter.ttf', 20) # This is for humidity icon. Font is here: https://freebiesbug.com/psd-freebies/80-stroke-icons-psd-ai-webfont/
#font22 = ImageFont.truetype('Font.ttc', 22) # Various font sizes to choose from.
font22 = ImageFont.truetype('arialn.ttf', 22)
font21 = ImageFont.truetype('arialn.ttf', 21)
font20 = ImageFont.truetype('arialn.ttf', 20)
font18 = ImageFont.truetype('arialn.ttf', 18)
font16 = ImageFont.truetype('arialn.ttf', 16)
font14 = ImageFont.truetype('arialn.ttf', 14)
font12 = ImageFont.truetype('arialn.ttf', 12)
width = 296 # width and height of the inkyPHAT
height = 128

APIKEY = settings.API_KEY # Get a free api key from the Open Weather Map: https://openweathermap.org/api
LAT= "52.4143"
LON= "-1.7809"
WETTER_API_URL = "https://api.openweathermap.org/data/2.5/onecall" # This is the weather API. They have other APIs like the "One Call" one that has other info like forecast or moonrise. Pick your poison.

def ausgabe(y):
	image = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
	today = datetime.datetime.today()
	drawblack = ImageDraw.Draw(image)
	tempInt = y["current"]["temp"]
	message = ""
	drawblack.text((0,2), message, inky_display.RED,font = meteoconssmall) # It's red. Adjust this for black/white displays.
	message = " C:" + str(tempInt) + "ºC" # Getting the data from the API.
	hightemp = str(y["daily"][0]["temp"]["max"]) + "ºC"
	lowtemp = str(y["daily"][0]["temp"]["min"]) + "ºC"
	#message = message + "| Feels " + str(y["current"]["feels_like"]) + "ºC" # Feel like temp.
	message = message + " H:" + hightemp + " L:" + lowtemp
	drawblack.text((3,0), message, inky_display.BLACK,font = font21)
    
	#Tomorrow
	message = "" #Meteocon symbol for the thermometer
	drawblack.text((0,22), message, inky_display.RED,font = meteoconssmall) # It's red. Adjust this for black/white displays.
	message = " H:"
	hightemp = str(y["daily"][1]["temp"]["max"]) + "ºC"
	lowtemp = str(y["daily"][1]["temp"]["min"]) + "ºC"
	rain = str(y["daily"][1]["pop"] * 100) 
	#message = message + "| Feels " + str(y["current"]["feels_like"]) + "ºC" # Feel like temp.
	message = message  + hightemp + " L:" + lowtemp + " R:" + rain + "%"
	drawblack.text((3,22), message, inky_display.BLACK,font = font21)
	
	#Next Day
	message = "" #Meteocon symbol for the thermometer
	drawblack.text((0,42), message, inky_display.RED,font = meteoconssmall) # It's red. Adjust this for black/white displays.
	message = " H:"
	hightemp = str(y["daily"][2]["temp"]["max"]) + "ºC"
	lowtemp = str(y["daily"][2]["temp"]["min"]) + "ºC"
	#message = message + "| Feels " + str(y["current"]["feels_like"]) + "ºC" # Feel like temp.
	message = message  + hightemp + " L:" + lowtemp
	drawblack.text((3,42), message, inky_display.BLACK,font = font21)
		
	message = "B " # Sunrise icon
	drawblack.text((0,85), message, inky_display.BLACK, font = meteocons)
	message = "   " + time.strftime('%H:%M', time.localtime(y["current"]["sunrise"]))
	drawblack.text((20,85), message, inky_display.BLACK, font = font18)
	message = "Sunrise"
	drawblack.text((32,100), message,inky_display.BLACK, font = font14)

	message = "A " # Sunset icon
	drawblack.text((80,85), message, inky_display.RED, font = meteocons)
	message = "   " + time.strftime('%H:%M', time.localtime(y["current"]["sunset"]))
	drawblack.text((95,85), message, inky_display.BLACK, font = font18)
	message = "Sunset"
	drawblack.text((110,100), message,  inky_display.BLACK, font = font14)

#	DATE AND TIME
	drawblack.text((165, 85), 'Last update:', inky_display.BLACK, font = font14) #
	drawblack.text((165, 100), '{:%a, %d.%m. (%H:%M)}'.format(today), inky_display.BLACK, font = font12)
	drawblack.line((155, 85, 155, 128), inky_display.BLACK, width = 1)
	image = image.rotate(180)
	inky_display.set_image(image)
	inky_display.show()

# Set up where we'll be fetching data from
params = {"lat": LAT, "lon": LON, "appid": APIKEY, "units":"metric" } # options are standard, metric, imperial
data_source = WETTER_API_URL + "?" + urllib.parse.urlencode(params) +"&lang=en" # change "&lang=en" to "&lang=de" for German, etc.
weather_refresh = None

wait = 0

if wait == 0:
	response = urllib.request.urlopen(data_source) 
	if response.getcode() == 200: 
		value = response.read() 
		y = json.loads(value)
		ausgabe(y)
	else: 
		print("Unable to retrieve data at {}".format(url))

