import paho.mqtt.client as mqtt
import requests
import time

mqttc = mqtt.Client()
mqttc.connect("test.mosquitto.org", 1883)

mqttc.loop_start()


def send_message():
    weather_link = 'https://api.openweathermap.org/data/2.5/weather?id=3452925&u' \
                   'nits=metric&appid=a9a877fdd3fc5035b226a2f9eed79e48'
    weather_map = requests.get(weather_link)
    weather_map = weather_map.json()

    name_city = weather_map['name']
    temp = weather_map['main']['temp']
    humidity = weather_map['main']['humidity']
    feels_like = weather_map['main']['feels_like']
    wind_speed = weather_map['wind']['speed'] * 3.6

    mqttc.publish("dblab/nome", name_city)
    mqttc.publish("dblab/velocidadevento", wind_speed)
    mqttc.publish("dblab/sensacaotermica", feels_like)
    mqttc.publish("dblab/humidade", humidity)
    mqttc.publish("dblab/temperatura", temp)


def on_message(client, userdata, message):
    print(message.payload)
    send_message()


# def on_message2(client, userdata, message):
#     print(message.payload, "payload2")
#     send_message()


mqttc.on_message = on_message
# mqttc.message_callback_add("dblab/atualiza", on_message2)
mqttc.subscribe("dblab/atualizar")
# mqttc.subscribe("dblab/atualiza")
# mqttc.subscribe("dblab/atualiza2")

send_message()

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("exiting")
    mqttc.disconnect()
    mqttc.loop_stop()
