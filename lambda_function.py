import json
import logging
import urllib.request
import time
# import pytz
# from pytz import country_timezones

logger = logging.getLogger()

logger.setLevel(logging.DEBUG)

def lambda_handler(event, context):
    logger.debug(event)
    
    
    if event["currentIntent"]["name"]=='GetLocation':
        global city
        city=event["currentIntent"]["slots"]["Location"]
        message="Please select any one of the choices :temperature,pressure,humidity,general or stop."
        
        return {
          "sessionAttributes": event["sessionAttributes"],
          "dialogAction": {
                "type": "ElicitSlot",
                "intentName":"GetWeather",
                "slotToElicit":"choice",
                "message":{
                    "contentType":"PlainText",
                    "content":message
                    
                }
                }
                }
    elif event["currentIntent"]["name"]=="GetWeather":
        
        choice=event["currentIntent"]["slots"]["choice"]
        
        BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
        API_KEY = "APIKEY"
        URL = BASE_URL + "q=" + city + "&appid=" + API_KEY
        
        response = json.load(urllib.request.urlopen(URL))
        
        if response['cod'] == 200:
    	    main = response['main']
    	    temperature = '{:.2f}'.format(main['temp']-273.15)
    	    min_temp='{:.2f}'.format(main['temp_min']-273.15)
    	    max_temp='{:.2f}'.format(main['temp_max']-273.15)
    	    humidity = main['humidity']
    	    pressure = main['pressure']
    	    report = response['weather']
    	    sunrise = int(response['sys']['sunrise'])
    	    sunset = int(response['sys']['sunset'])
    	    zone=response['sys']['country']
    	    
        if choice=="temperature":
            
            message=f"The Temperature of {city} is {temperature}°C. \n The maximum temperature will be {max_temp}°C and minimum will be {min_temp}°C."
            return {
                "sessionAttributes": event["sessionAttributes"],
                "dialogAction": {
                    "type": "ElicitSlot",
                    "intentName":"GetWeather",
                    "slotToElicit":"choice",
                    "message":{
                        "contentType":"PlainText",
                        "content":message
                    
                }
                }
                }
                
        if choice=="humidity":
            message=f"The Humidity of {city} is {humidity}%."
            return {
                "sessionAttributes": event["sessionAttributes"],
                "dialogAction": {
                    "type": "ElicitSlot",
                    "intentName":"GetWeather",
                    "slotToElicit":"choice",
                    "message":{
                        "contentType":"PlainText",
                        "content":message
                    
                }
                }
                }
                
        if choice=="pressure":
            message=f"The Pressure of {city} is {pressure}."
            return {
                "sessionAttributes": event["sessionAttributes"],
                "dialogAction": {
                    "type": "ElicitSlot",
                    "intentName":"GetWeather",
                    "slotToElicit":"choice",
                    "message":{
                        "contentType":"PlainText",
                        "content":message
                        }}}
                        
        if choice=="general":
            # code=country_timezones(zone)
            # old_timezone = pytz.timezone("US/Eastern")
            # new_timezone = pytz.timezone(code[0])
            # sunrise_new= old_timezone.localize(sunrise).astimezone(new_timezone)
            # sunset_new= old_timezone.localize(sunset).astimezone(new_timezone) 

            # ts=time.strftime("%-I:%M %p", time.localtime(sunrise_new))
            # ts2=time.strftime("%-I:%M %p", time.localtime(sunset_new))
            message = f"The weather report of {city} is {report[0]['description']}."
            return {
                "sessionAttributes": event["sessionAttributes"],
                "dialogAction": {
                    "type": "ElicitSlot",
                    "intentName":"GetWeather",
                    "slotToElicit":"choice",
                    "message":{
                        "contentType":"PlainText",
                        "content":message
                    
                }
                }
                }
                
        if choice=='stop':
            message ="Bye."
            return {
                "sessionAttributes": event["sessionAttributes"],
                "dialogAction": {
                    "type": "Close",
                    "fulfillmentState":"Fulfilled",
                    "message":{
                        "contentType":"PlainText",
                        "content":message
                    
                }
                }
                }

