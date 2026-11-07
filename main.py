import requests
import datetime as dt
import smtplib
import os

my_email = os.getenv("EMAIL_ADDR")
password = os.getenv("EMAIL_PASS")

MY_LAT = 18.47186
MY_LONG = -69.89232

def iss_close():
    if 13.0 <= iss_position[0] <= 23.0 and -74.0 <= iss_position[1] <= -64.0:
        return True
    return False

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()

data = response.json()

latitude = float(data["iss_position"]["latitude"])
longitude = float(data["iss_position"]["longitude"])

iss_position = (latitude, longitude)

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
}

response_0 = requests.get("https://api.sunrise-sunset.org/v2", params=parameters)
response_0.raise_for_status()

data = response_0.json()
sunrise = int(data["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["sunset"].split("T")[1].split(":")[0])

time = dt.datetime.now()

if iss_close() and (time.hour <= sunrise or time.hour >= sunset):
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email, to_addrs="tonysmith0730@outlook.com",
                            msg="Look up!")
