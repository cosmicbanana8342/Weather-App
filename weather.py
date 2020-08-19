from tkinter import *
from PIL import ImageTk,Image
import tkinter as tk
import requests
import json
import datetime as dt
from tkinter import messagebox
import io
import base64
from urllib.request import urlopen

root = Tk()
root.title('Simple Weather App')
root.iconbitmap('multimedia/icons/icon.ico')
# root.geometry('520x400+400+100')
root.geometry('1000x620+120+40')
root.configure(background='#6666ff')
# root.attributes('-alpha', 0.8)

# Making main_frame global so that it can be used by each function
global main_frame

'''Variable which decides whether it is initial search or a new search, it will 
further decide whether to create a new canvas or edit the existing one'''
flag = 0

# Callbacks for radiobuttons
def pin_enable():
	pincode_entry.config(state="normal")
	pincode_entry.update()
	city_entry.config(state="disabled")
	city_entry.update()
	pincode_entry.focus()
	# pincode_entry.insert(0,'e.g. 110005')			# Placeholder

def city_enable():
	city_entry.config(state="normal")
	city_entry.update()
	pincode_entry.config(state="disabled")
	pincode_entry.update()
	city_entry.focus()
	# city_entry.insert(0, 'e.g. Allahabad')			# Placeholder

# Functions to disappear placeholders on click
def userText(event):
	city_entry.delete(0,END)
	usercheck=True

def passText(event):
	pincode_entry.delete(0, END)
	passcheck=True

# Function to call fetch_data function when enter key is pressed
def callback(event):
	fetch_data()

def fetch_data():
	global icon_url
	global bg
	global photo_icon
	global photo_weather
	global flag
	global canvas

	if (var.get()==1):
		city = city_entry.get()
		try:
			api_request_1 = requests.get("https://api.opencagedata.com/geocode/v1/google-v3-json?address="+city+"&key=b3970ffbe4114688a43efd5cf96736c2")
			api_1 = json.loads(api_request_1.content)
			
			
			lat = api_1['results'][0]['geometry']['location']['lat']
			lng = api_1['results'][0]['geometry']['location']['lng']
			address = api_1['results'][0]['formatted_address']

			#including date, day and time
			x = dt.datetime.now()
			date_time = x.strftime("%a, %d %B %I:%M %p")

			url = "http://api.openweathermap.org/data/2.5/weather?lat="+str(lat)+"&lon="+str(lng)+"&appid=9a46b1b95df36905735d9e5e0bd322c2&units=metric"
			# print(url)
			api_request_2 = requests.get(url)
			api_2 = json.loads(api_request_2.content)

			temp = api_2['main']['temp']
			desc = api_2['weather'][0]['description']
			sunrise = api_2['sys']['sunrise']
			sunset = api_2['sys']['sunset']
			cur_time = api_2['dt']
			icon_id = api_2['weather'][0]['icon']
			icon_url = "http://openweathermap.org/img/wn/"+icon_id+"@2x.png"

			# print("temp:", temp)
			# print("desc:", desc)
			# print("sunrise:", sunrise)
			# print("sunset:", sunset)
			# print("cur_time:", cur_time)
			# print("icon_id", icon_id)
			# print("icon_url", icon_url)

			# Clearing canvas for new data
			if (flag == 1):
				canvas.destroy()

			# Create canvas and set the background image according to time
			canvas = Canvas(root, width = 615, height = 300)  
			canvas.pack(pady=15)
			if (cur_time>sunrise and cur_time<sunset):
				bg = ImageTk.PhotoImage(Image.open("multimedia/day2.png"))
			else:
				bg = ImageTk.PhotoImage(Image.open("multimedia/night2.png"))
			canvas.create_image(0, 0, anchor=NW, image=bg)

			# Location pin icon
			nav_icon = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAC40lEQVRoQ+2VzWsTURTFz32TFNtMAi782igUdFFUsDOTpC4FQZAu9E9wI6IbQVBE+2FxoaArERH8EwQXXaggFAQ7k860UDdCQVz5iaAkwdJk3pWkJE1Ka1rem5jCzHLmvXvP75z73hB2+EM7XD9igP+dYJxAnICiA/EIKRqovD1OQNlCxQJxAooGKm+PE9jMwpLj7JcUHgYRCySWTM/7pmz3BgW0J1DOWmdDIcYT/QMOJZPgMIQsl8AMlwQmzdm5lzpBtAKU8vZDw8xcTezZB65WwNVqXWv162ewlKu6CfdN17+uC0IbQDlr36RM+i4ZCYS/f6Fm+eYPXzO94IEOCC0AfyzrYKUvsWQYoo8rlY66pJTLhqTBVBB86bi4wwItAOWsPc6EifZe8idIvABLgjTOQfDutu/EN0w3uNcTACXHfg2B0w0xDPkRRnUk/W7xe+1d2bIOhAbNCsKhpmCiadOdG+0JgKJjByQw3BBDwMWU5z9tFVfM2ZcJeNR8x/DMgp/vCYBSznkD8KkmAMvRVGF+ug0g75wn5udrKdGrtDd3picAijlnisC3muIIT9Kuf6lVXCk3/AwQF1rWTKZdf9252T6OlkO87DiDK4I/CCBZkyABNsDjIRuPEYZESbrCjDFR+wusfq8kKXGk33U/bV9y+w4tALWSxZxzh8C3tyKIGBOpgj+5lbWd1mgD4KGhvnJmVwAWR//VNGS5kBnIZGlmZvU3rfhoA6hfl3lrOAzZE0IkNtIlgRUB6Zje/KKi7rXbWFehRp31B7q1PoHHUl4wpbOn1gRqwuqjlBrwIXCsVShLzJspM6drdBq1tQPUR2nEPhFWZaExSvXREWybs8F7ne7XakUCsP5WimJ0Ik2gPkqWlSwT+UyoRjE6kQPUUzh5fC8Mg9NvF37oHp2uAEQluv1m60aXCHtEdogj1NxWOgboltOb9YkTiBNQdCAeIUUDlbfHCShbqFggTkDRQOXtfwFbB+YxW/eOLQAAAABJRU5ErkJggg=="
			icon_byt = urlopen(nav_icon).read()
			nav_icon_b64 = base64.encodebytes(icon_byt)
			photo_icon = tk.PhotoImage(data=nav_icon_b64)  
			canvas.create_image(1,-6, anchor=NW, image=photo_icon)

			if (desc=="clear sky"):
				if (cur_time>sunrise and cur_time<sunset):
					icon_url = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAFdElEQVR4Xu2aW2xUVRSG/7XPmenQFqFEegU0QktpgdC0AvoCtNgLsQFNqiYkJgSj0ZhGfEB80EBi1AQTTXgwUR588JL0AWswWKQFjFwS6TW0ttSaYFo608RyqTPt0JlzljmQCgkW9j6XYZLOeerDWv+/1rfXPpc9Jczxi+Z4/0gBSE3AHCeQ2gJzfABSN8HUFkhtgTlOILUF5vgAePsUYAbdPL95eTxAjxmgfA282GS+KoR2haOxkcyNlZeI9psPcxE82QITXZVPE9AgmHcA9PhsDTJTkJh/YI2OZKxrayUCJxqGqwAiF7aWMRkfk6Bq5UYY5wWLvfMqWs8o5zpIcAUAt5f7wmLhJwLc6KCWW6lE+HqekfEaVRyddKolk+8YwI2+mkW+6HQTE1XJGErFMHdQjHekbzw9IhXvIMgRgPFjdY+kZUfPkqDVDmqYJZVHYE6sz6joCLqvfUfRNgBuatAihePNxHjWwwJ/S+8xN9Gu01GvPGwDiLRXvQ/BB7wqbEbXNPnL+RWnXvXKxxaAye6nCtgIDIEo4FVhd3SZp2OxsqwNZ3q88LIFINy5+TBB7PaioP/TZDZbMstP13nhpwwg1FOdPd+IWzcm4WZBJvlxQ5TguliDKZGDacqCSTp85gT8fA1TKPggHFj2Rc2KgmE3fZUBRC5U7YbGh90qIoYFGPHVI+TbCgP+B8oyzF+ZzAN1K5e0PTBYIkAZQLir8qhbd/6g7xlc9u2UavyeXhg/R+P08vY1OWMSfc4aog6gc8tVAmU5MbXGfdD/Ov7WNjiRATOCwjAaqlcXnLUrpASA2+vTJ0UkYtfMymNo6E97G1e1Micy/+Uy4x9TNzZtKyzosiOoBCB6bvMKIyD+sGM0kzPkfwUhvdKJxL25hDF9KlZetW7pFVVhJQDW1x40s1PVZCb+uliL3sA+u+n3zWOgubY49zlVcTUA7eV5EAtGVU1uj76OzsDBW484zy5Gfc2q3B9V9JUAWO//k8vHb4Kg3W0SRwau6WswScsQp0wInkaAx7DQ6MU8vv0tM64/iX7/HpXalGOZ+VTtqjyl/aUEwKoo0lX5JxhPWH8blI5hXz2Cet0sjzLGIqMTS2PNGPY979qN7z5kOGqIou2l2UOy9NQBdFQeAuFN641tINAIa/XlLuu0S9lOTvruKAONNaW5h2QTlSsKd26pmhAlrX1p78B6nifbZRJ9VbcyZ5dsXcoATnZ3lxqBrIsm0pRzZYtyEkfgC9XFeetlNZSbOP578DsIeknWINFxDPTUFueuk/VVAnD80mgxs+gjl78EZYuVifMUwE99ox8JTXjzJiPTnUQME07UrsyVPpZXm4CBYBtASs9ZiZrdDTHpYE1Jzl5ZUSUALZeCvcRUKiv+MOLYiL9YW7qkSdZbDcBAqIeAtbLiDyHuxnTYzK+vyJf+UUUJwPGBsWMAe3I25wYshvl5bXH+GypaSgB+6g+9KwgfqhgkLJYRhs8oUT0zVALQ1j1cEA/oQ0AijsPV0BmmuWdbSf5nalk2Xs5bBkKfEvCWqpGX8UTmkXNFeQ37iZT/10BpAqwmjvSEstPTuJdAi71sSlbb+gQe1MN1jYWFN2Vz7o5TBmAlt3T/VUoB/0mAsu2YupVj3fQGtcgeu81bddgCYCWeGLy8Km74mwWJIrcaktUx2RzUWNtXXZLzvWzObHG2AViCTcxaZn9op9DoPWKscFrM/fM5ajL/QgLfTBTlffsCkeGGnyMAMwUwM7VeHFkd0/UyXROPMtiVgwLDMKOaJoIcN0djU+hQecGRheMKAFmzZIxLAUjGVUlkTakJSCTtZPRKTUAyrkoia0pNQCJpJ6NXagKScVUSWVNqAhJJOxm9/gW+x7lQ2DDK3wAAAABJRU5ErkJggg=="
					weather_icon = icon_url
					weather_byt = urlopen(weather_icon).read()
					weather_icon_b64 = base64.encodebytes(weather_byt)
					photo_weather = tk.PhotoImage(data=weather_icon_b64)  
					canvas.create_image(238,99, anchor=NW, image=photo_weather)

				else:
					icon_url = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAFWklEQVR4Xu2ZX0wcVRTGvzMLy9+2SNeFBVoQpbtrW4otqRhbtdawSExDKTZKTDTRWBZNAxSTojHZGNP6Uhq1FOTZaoKBhQdtaSXWh/oimpq2dCHV/tG2LLVtAm3sssxcMxRSwLB7Z3aW2cjM63znnO/85tyduXcJi/yiRd4/DADGBCxyAsYSWOQDYPwIGkvAWAKLnICxBBb5AET/LVD/Zkc6zPH7SaKeO8x/or19VzCWoEd9CXg8HmHUv+4egHgAF0HkWWo9/aXH45FiAUTUAchNNri9FwHkzWj4eEBg1S0tlTf1hrAwAGq7z4Mxx5xmL02Ipmc/a992RU8ICwPA7R0DkPqfRol8AZI26TkJUQdQV+dNEwK4Pf9Tpm+aWyt26jUFUQfQ4O7ZBkg9oRokoPxA6/ajekCIOoA97u6vGdgroZujU82tFZv+dwCmxv8qgORwzTETFR48VHEmnE7r+1GdgIbarjYw2sVjmhhrOtBW+QmPVktN1ADU7ep6ShDoFMD5tUnM23y4slJu7vshf35QRBFByoIgpEOSbgkEv8DifnvB+fBQzAN4723voxMCThIhh9dsQqp54Lm3NvQwxnYQaFWIuD/A0CPGTTSXF+T8xZt/Pp3mE1Dv7swnCCcBrOAxJ5gIj5WsRO4TNkkwkcATM6UJAPgCAbzvWpd5V0HcLKmmABpqvW+A4QCAdB5DSWmJKHpxFZZaU3jk82nOiyZWVV5gG1CTJGIAk5udG+u2QEQTCFt5TaQ8lIiNL6+FOSmONySUbgxM2uJyZv2iNBkXgNrajtQkFl9NkK4yCMNgZGFAHgNzErEqgLKVFE5INaNk51okLjErCQunHWGi8HTZauuFcMKZ97kAyAENbu/vAPKVJJ9Pu2G7E5aVaVqkmruef/7JnlHiIeLeaisBsA9AU6SubXYLCssKIk0zfzzDbpcz83PeAtwAGmu6rBKRPF5LQiVPXpaIhJT7o33vTgD/jMo/1g+uza8XITktidefGt2N5XcysouLievkiRuA7GRPTddeRrR/rqu4BBPyi3OQ/bgF5uTZ6zpwdxx/nhnB5dPXsMSSjI1Va9Q0pSiGMaoqc2Z08gQpAnD/eKvoW4CVTSfPW5+F/I3ZiE8I/Ws+ERQRGBtHSnpUn/6ULdbpctiqNAcgJ5zc4NxDHwjr7ZtzIQOIweuKy5GZy+NL0QRMJ2xs7E1xlmT+mrMmI9QnK0/9qGmYGFxetnrFrXAFVAE4MXTNKUnCWQBKPl3DedH0PhOFAp5vAlUAen3DRwBUa+pY42RRA9A3+Hf2BJu4DMCksWdN08VRXM5Wu0U+jAl5KZ6A4+eHX2WEr8Il1vc+3XY5Mrg2ZIoB9PqGPwDwsb4Nhq3+g8uR+XxYFfdpzYxMx3zXPyLQhzzJddMQGlz2zIM89dVMwG4An/Ik10kTYGIwi+cVKPtTDmDo2jOQhB91ai5sWQJrK3XY3GGFUwLFADrOnTMvMy2/BMDGW2QBdSPB8YDjpcLcEP9EzXajGIAcfnzw+juM0aEFbIynlASiHS57RjePeFqjCkB/P4u/meofBPCIkmLR1BKxd0vtthalNVQBkIsc9fkLCayPAIvSohrrx0Gs3mW3HVaTVzUAuVjvwPAaCOgDYFVTPPIYGiSIr5U6svrV5ooIwCSEC8NWBLEXhBoAC7HZl19eg4ywb3SV9chOIlFt86peg/MVOzZwwwaSqonwJMDkU+KIDvsf1JEblEYIdB1EZxnE71z2LF8kTc+MjXgCtDKiVx4DgF7kY6WuMQGx8iT08mFMgF7kY6WuMQGx8iT08mFMgF7kY6WuMQGx8iT08vEvygljUHEc6C0AAAAASUVORK5CYII="
					weather_icon = icon_url
					weather_byt = urlopen(weather_icon).read()
					weather_icon_b64 = base64.encodebytes(weather_byt)
					photo_weather = tk.PhotoImage(data=weather_icon_b64)  
					canvas.create_image(238,99, anchor=NW, image=photo_weather)
			else:
				weather_icon = icon_url
				weather_byt = urlopen(weather_icon).read()
				weather_icon_b64 = base64.encodebytes(weather_byt)
				photo_weather = tk.PhotoImage(data=weather_icon_b64)  
				canvas.create_image(200,80, anchor=NW, image=photo_weather)

			if (cur_time>sunrise and cur_time<sunset):
				canvas.create_text(42,9, anchor=NW, text=address,font=('Helvetica',11,'bold'))
				canvas.create_text(252,165, anchor=NW, text=desc,font=('Helvetica',12,'bold'))
				canvas.create_text(208,85, anchor=NW, text=date_time,font=('Helvetica',12,'bold'))
				canvas.create_text(295,113, anchor=NW, text=str(int(temp))+"°C",font=('Helvetica',27,'bold'))
				# Outer rectangle
				canvas.create_rectangle(175,80,435,190)
			
			else:
				canvas.create_text(42,9, anchor=NW, text=address,font=('Helvetica',11,'bold'), fill="white")
				canvas.create_text(252,165, anchor=NW, text=desc,font=('Helvetica',12,'bold'), fill="white")
				canvas.create_text(208,85, anchor=NW, text=date_time,font=('Helvetica',12,'bold'), fill="white")
				canvas.create_text(295,113, anchor=NW, text=str(int(temp))+"°C",font=('Helvetica',27,'bold'), fill="white")
				# Outer rectangle
				canvas.create_rectangle(175,80,435,190, outline="white")

			flag = 1

		except:
			messagebox.showinfo('Something went wrong!', 'Make sure you entered valid data and have a stable internet connection')
		
	if (var.get()==2):
		pincode = pincode_entry.get()
		try:
			url = "http://api.openweathermap.org/data/2.5/weather?zip="+pincode+",in&appid=9a46b1b95df36905735d9e5e0bd322c2&units=metric"
			# print(url)
			api_request_2 = requests.get(url)
			api_2 = json.loads(api_request_2.content)

			lat = api_2['coord']['lat']
			lng = api_2['coord']['lon']
			address = api_2['name']
			temp = api_2['main']['temp']
			desc = api_2['weather'][0]['description']
			sunrise = api_2['sys']['sunrise']
			sunset = api_2['sys']['sunset']
			cur_time = api_2['dt']
			icon_id = api_2['weather'][0]['icon']
			icon_url = "http://openweathermap.org/img/wn/"+icon_id+"@2x.png"

			#including date, day and time
			x = dt.datetime.now()
			date_time = x.strftime("%a, %d %B %I:%M %p")

			api_request_1 = requests.get("https://api.opencagedata.com/geocode/v1/json?q="+str(lat)+"+"+str(lng)+"&key=b3970ffbe4114688a43efd5cf96736c2")
			api_1 = json.loads(api_request_1.content)

			city = api_1['results'][0]['components']['state_district']
			country = api_1['results'][0]['components']['country']

			# Clearing canvas for new data
			if (flag == 1):
				canvas.destroy()

			# Create canvas and set the background image according to time
			canvas = Canvas(root, width = 615, height = 300)  
			canvas.pack(pady=15)
			if (cur_time>sunrise and cur_time<sunset):
				bg = ImageTk.PhotoImage(Image.open("multimedia/day2.png"))
			else:
				bg = ImageTk.PhotoImage(Image.open("multimedia/night2.png"))
			canvas.create_image(0, 0, anchor=NW, image=bg)

			# Location pin icon
			nav_icon = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAC40lEQVRoQ+2VzWsTURTFz32TFNtMAi782igUdFFUsDOTpC4FQZAu9E9wI6IbQVBE+2FxoaArERH8EwQXXaggFAQ7k860UDdCQVz5iaAkwdJk3pWkJE1Ka1rem5jCzHLmvXvP75z73hB2+EM7XD9igP+dYJxAnICiA/EIKRqovD1OQNlCxQJxAooGKm+PE9jMwpLj7JcUHgYRCySWTM/7pmz3BgW0J1DOWmdDIcYT/QMOJZPgMIQsl8AMlwQmzdm5lzpBtAKU8vZDw8xcTezZB65WwNVqXWv162ewlKu6CfdN17+uC0IbQDlr36RM+i4ZCYS/f6Fm+eYPXzO94IEOCC0AfyzrYKUvsWQYoo8rlY66pJTLhqTBVBB86bi4wwItAOWsPc6EifZe8idIvABLgjTOQfDutu/EN0w3uNcTACXHfg2B0w0xDPkRRnUk/W7xe+1d2bIOhAbNCsKhpmCiadOdG+0JgKJjByQw3BBDwMWU5z9tFVfM2ZcJeNR8x/DMgp/vCYBSznkD8KkmAMvRVGF+ug0g75wn5udrKdGrtDd3picAijlnisC3muIIT9Kuf6lVXCk3/AwQF1rWTKZdf9252T6OlkO87DiDK4I/CCBZkyABNsDjIRuPEYZESbrCjDFR+wusfq8kKXGk33U/bV9y+w4tALWSxZxzh8C3tyKIGBOpgj+5lbWd1mgD4KGhvnJmVwAWR//VNGS5kBnIZGlmZvU3rfhoA6hfl3lrOAzZE0IkNtIlgRUB6Zje/KKi7rXbWFehRp31B7q1PoHHUl4wpbOn1gRqwuqjlBrwIXCsVShLzJspM6drdBq1tQPUR2nEPhFWZaExSvXREWybs8F7ne7XakUCsP5WimJ0Ik2gPkqWlSwT+UyoRjE6kQPUUzh5fC8Mg9NvF37oHp2uAEQluv1m60aXCHtEdogj1NxWOgboltOb9YkTiBNQdCAeIUUDlbfHCShbqFggTkDRQOXtfwFbB+YxW/eOLQAAAABJRU5ErkJggg=="
			icon_byt = urlopen(nav_icon).read()
			nav_icon_b64 = base64.encodebytes(icon_byt)
			photo_icon = tk.PhotoImage(data=nav_icon_b64)  
			canvas.create_image(1,-6, anchor=NW, image=photo_icon)

			if (desc=="clear sky"):
				if (cur_time>sunrise and cur_time<sunset):
					icon_url = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAFdElEQVR4Xu2aW2xUVRSG/7XPmenQFqFEegU0QktpgdC0AvoCtNgLsQFNqiYkJgSj0ZhGfEB80EBi1AQTTXgwUR588JL0AWswWKQFjFwS6TW0ttSaYFo608RyqTPt0JlzljmQCgkW9j6XYZLOeerDWv+/1rfXPpc9Jczxi+Z4/0gBSE3AHCeQ2gJzfABSN8HUFkhtgTlOILUF5vgAePsUYAbdPL95eTxAjxmgfA282GS+KoR2haOxkcyNlZeI9psPcxE82QITXZVPE9AgmHcA9PhsDTJTkJh/YI2OZKxrayUCJxqGqwAiF7aWMRkfk6Bq5UYY5wWLvfMqWs8o5zpIcAUAt5f7wmLhJwLc6KCWW6lE+HqekfEaVRyddKolk+8YwI2+mkW+6HQTE1XJGErFMHdQjHekbzw9IhXvIMgRgPFjdY+kZUfPkqDVDmqYJZVHYE6sz6joCLqvfUfRNgBuatAihePNxHjWwwJ/S+8xN9Gu01GvPGwDiLRXvQ/BB7wqbEbXNPnL+RWnXvXKxxaAye6nCtgIDIEo4FVhd3SZp2OxsqwNZ3q88LIFINy5+TBB7PaioP/TZDZbMstP13nhpwwg1FOdPd+IWzcm4WZBJvlxQ5TguliDKZGDacqCSTp85gT8fA1TKPggHFj2Rc2KgmE3fZUBRC5U7YbGh90qIoYFGPHVI+TbCgP+B8oyzF+ZzAN1K5e0PTBYIkAZQLir8qhbd/6g7xlc9u2UavyeXhg/R+P08vY1OWMSfc4aog6gc8tVAmU5MbXGfdD/Ov7WNjiRATOCwjAaqlcXnLUrpASA2+vTJ0UkYtfMymNo6E97G1e1Micy/+Uy4x9TNzZtKyzosiOoBCB6bvMKIyD+sGM0kzPkfwUhvdKJxL25hDF9KlZetW7pFVVhJQDW1x40s1PVZCb+uliL3sA+u+n3zWOgubY49zlVcTUA7eV5EAtGVU1uj76OzsDBW484zy5Gfc2q3B9V9JUAWO//k8vHb4Kg3W0SRwau6WswScsQp0wInkaAx7DQ6MU8vv0tM64/iX7/HpXalGOZ+VTtqjyl/aUEwKoo0lX5JxhPWH8blI5hXz2Cet0sjzLGIqMTS2PNGPY979qN7z5kOGqIou2l2UOy9NQBdFQeAuFN641tINAIa/XlLuu0S9lOTvruKAONNaW5h2QTlSsKd26pmhAlrX1p78B6nifbZRJ9VbcyZ5dsXcoATnZ3lxqBrIsm0pRzZYtyEkfgC9XFeetlNZSbOP578DsIeknWINFxDPTUFueuk/VVAnD80mgxs+gjl78EZYuVifMUwE99ox8JTXjzJiPTnUQME07UrsyVPpZXm4CBYBtASs9ZiZrdDTHpYE1Jzl5ZUSUALZeCvcRUKiv+MOLYiL9YW7qkSdZbDcBAqIeAtbLiDyHuxnTYzK+vyJf+UUUJwPGBsWMAe3I25wYshvl5bXH+GypaSgB+6g+9KwgfqhgkLJYRhs8oUT0zVALQ1j1cEA/oQ0AijsPV0BmmuWdbSf5nalk2Xs5bBkKfEvCWqpGX8UTmkXNFeQ37iZT/10BpAqwmjvSEstPTuJdAi71sSlbb+gQe1MN1jYWFN2Vz7o5TBmAlt3T/VUoB/0mAsu2YupVj3fQGtcgeu81bddgCYCWeGLy8Km74mwWJIrcaktUx2RzUWNtXXZLzvWzObHG2AViCTcxaZn9op9DoPWKscFrM/fM5ajL/QgLfTBTlffsCkeGGnyMAMwUwM7VeHFkd0/UyXROPMtiVgwLDMKOaJoIcN0djU+hQecGRheMKAFmzZIxLAUjGVUlkTakJSCTtZPRKTUAyrkoia0pNQCJpJ6NXagKScVUSWVNqAhJJOxm9/gW+x7lQ2DDK3wAAAABJRU5ErkJggg=="
					weather_icon = icon_url
					weather_byt = urlopen(weather_icon).read()
					weather_icon_b64 = base64.encodebytes(weather_byt)
					photo_weather = tk.PhotoImage(data=weather_icon_b64)  
					canvas.create_image(238,99, anchor=NW, image=photo_weather)

				else:
					icon_url = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAFWklEQVR4Xu2ZX0wcVRTGvzMLy9+2SNeFBVoQpbtrW4otqRhbtdawSExDKTZKTDTRWBZNAxSTojHZGNP6Uhq1FOTZaoKBhQdtaSXWh/oimpq2dCHV/tG2LLVtAm3sssxcMxRSwLB7Z3aW2cjM63znnO/85tyduXcJi/yiRd4/DADGBCxyAsYSWOQDYPwIGkvAWAKLnICxBBb5AET/LVD/Zkc6zPH7SaKeO8x/or19VzCWoEd9CXg8HmHUv+4egHgAF0HkWWo9/aXH45FiAUTUAchNNri9FwHkzWj4eEBg1S0tlTf1hrAwAGq7z4Mxx5xmL02Ipmc/a992RU8ICwPA7R0DkPqfRol8AZI26TkJUQdQV+dNEwK4Pf9Tpm+aWyt26jUFUQfQ4O7ZBkg9oRokoPxA6/ajekCIOoA97u6vGdgroZujU82tFZv+dwCmxv8qgORwzTETFR48VHEmnE7r+1GdgIbarjYw2sVjmhhrOtBW+QmPVktN1ADU7ep6ShDoFMD5tUnM23y4slJu7vshf35QRBFByoIgpEOSbgkEv8DifnvB+fBQzAN4723voxMCThIhh9dsQqp54Lm3NvQwxnYQaFWIuD/A0CPGTTSXF+T8xZt/Pp3mE1Dv7swnCCcBrOAxJ5gIj5WsRO4TNkkwkcATM6UJAPgCAbzvWpd5V0HcLKmmABpqvW+A4QCAdB5DSWmJKHpxFZZaU3jk82nOiyZWVV5gG1CTJGIAk5udG+u2QEQTCFt5TaQ8lIiNL6+FOSmONySUbgxM2uJyZv2iNBkXgNrajtQkFl9NkK4yCMNgZGFAHgNzErEqgLKVFE5INaNk51okLjErCQunHWGi8HTZauuFcMKZ97kAyAENbu/vAPKVJJ9Pu2G7E5aVaVqkmruef/7JnlHiIeLeaisBsA9AU6SubXYLCssKIk0zfzzDbpcz83PeAtwAGmu6rBKRPF5LQiVPXpaIhJT7o33vTgD/jMo/1g+uza8XITktidefGt2N5XcysouLievkiRuA7GRPTddeRrR/rqu4BBPyi3OQ/bgF5uTZ6zpwdxx/nhnB5dPXsMSSjI1Va9Q0pSiGMaoqc2Z08gQpAnD/eKvoW4CVTSfPW5+F/I3ZiE8I/Ws+ERQRGBtHSnpUn/6ULdbpctiqNAcgJ5zc4NxDHwjr7ZtzIQOIweuKy5GZy+NL0QRMJ2xs7E1xlmT+mrMmI9QnK0/9qGmYGFxetnrFrXAFVAE4MXTNKUnCWQBKPl3DedH0PhOFAp5vAlUAen3DRwBUa+pY42RRA9A3+Hf2BJu4DMCksWdN08VRXM5Wu0U+jAl5KZ6A4+eHX2WEr8Il1vc+3XY5Mrg2ZIoB9PqGPwDwsb4Nhq3+g8uR+XxYFfdpzYxMx3zXPyLQhzzJddMQGlz2zIM89dVMwG4An/Ik10kTYGIwi+cVKPtTDmDo2jOQhB91ai5sWQJrK3XY3GGFUwLFADrOnTMvMy2/BMDGW2QBdSPB8YDjpcLcEP9EzXajGIAcfnzw+juM0aEFbIynlASiHS57RjePeFqjCkB/P4u/meofBPCIkmLR1BKxd0vtthalNVQBkIsc9fkLCayPAIvSohrrx0Gs3mW3HVaTVzUAuVjvwPAaCOgDYFVTPPIYGiSIr5U6svrV5ooIwCSEC8NWBLEXhBoAC7HZl19eg4ywb3SV9chOIlFt86peg/MVOzZwwwaSqonwJMDkU+KIDvsf1JEblEYIdB1EZxnE71z2LF8kTc+MjXgCtDKiVx4DgF7kY6WuMQGx8iT08mFMgF7kY6WuMQGx8iT08mFMgF7kY6WuMQGx8iT08vEvygljUHEc6C0AAAAASUVORK5CYII="
					weather_icon = icon_url
					weather_byt = urlopen(weather_icon).read()
					weather_icon_b64 = base64.encodebytes(weather_byt)
					photo_weather = tk.PhotoImage(data=weather_icon_b64)  
					canvas.create_image(238,99, anchor=NW, image=photo_weather)
			else:
				weather_icon = icon_url
				weather_byt = urlopen(weather_icon).read()
				weather_icon_b64 = base64.encodebytes(weather_byt)
				photo_weather = tk.PhotoImage(data=weather_icon_b64)  
				canvas.create_image(200,80, anchor=NW, image=photo_weather)

			if (cur_time>sunrise and cur_time<sunset):
				canvas.create_text(42,9, anchor=NW, text=address+", "+city+", "+country,font=('Helvetica',11,'bold'))
				canvas.create_text(252,165, anchor=NW, text=desc,font=('Helvetica',12,'bold'))
				canvas.create_text(208,85, anchor=NW, text=date_time,font=('Helvetica',12,'bold'))
				canvas.create_text(295,113, anchor=NW, text=str(int(temp))+"°C",font=('Helvetica',27,'bold'))
				# Outer rectangle
				canvas.create_rectangle(175,80,435,190)
				
			else:
				canvas.create_text(42,9, anchor=NW, text=address+", "+city+", "+country,font=('Helvetica',11,'bold'), fill="white")
				canvas.create_text(252,165, anchor=NW, text=desc,font=('Helvetica',12,'bold'), fill="white")
				canvas.create_text(208,85, anchor=NW, text=date_time,font=('Helvetica',12,'bold'), fill="white")
				canvas.create_text(295,113, anchor=NW, text=str(int(temp))+"°C",font=('Helvetica',27,'bold'), fill="white")
				# Outer rectangle
				canvas.create_rectangle(175,80,435,190, outline="white")

			flag = 1

		except:
			messagebox.showinfo('Something went wrong!', 'Make sure you entered valid data and have a stable internet connection')



# Main Frame
main_frame = Frame(root, background='#6666ff')
main_frame.pack(pady=(60,5))


# Radiobuttons
radio_frame = LabelFrame(main_frame, text="Select input mode", background='#6666ff', font=('Hobo Std',12))
radio_frame.grid(row=0, column=0, padx=50)

var = IntVar(root,"1")

# City name radiobutton
city_radio = Radiobutton(radio_frame, text="Place", variable=var, value=1, indicator=0, background = "#33d6ff", font=('calibre',10), command=city_enable)
city_radio.pack(padx=10, pady=10, ipadx=50, side = LEFT, expand = True, fill = BOTH)

# Pincode radiobutton
pincode_radio = Radiobutton(radio_frame, text="Pincode", variable=var, value=2, indicator=0, background = "#33d6ff", font=('calibre',10), command=pin_enable)
pincode_radio.pack(padx=10, pady=10, ipadx=50, side = LEFT, expand = True, fill = BOTH)

# Entry frame
input_frame = LabelFrame(main_frame, text="Enter your place or pincode and hit enter", background='#6666ff', font=('Hobo Std',12))
input_frame.grid(row=1, column=0, pady=5)

# City entry
city_lbl = Label(input_frame, text="Enter City", font=('Segoe Print',12), background='#6666ff')
city_lbl.pack(pady=5, side=LEFT)

city_entry = Entry(input_frame)
# city_entry.insert(0, 'e.g. Allahabad')			# Placeholder
# city_entry.bind("<Button>",userText)			# Disappear placeholder on click
city_entry.pack(side=LEFT)
city_entry.focus()

# Pincode entry
pincode_lbl = Label(input_frame, text="Enter Pincode", font=('Segoe Print',12), background='#6666ff')
pincode_lbl.pack(padx=(20,0), pady=5, side=LEFT)

pincode_entry = Entry(input_frame, state="disabled")
# pincode_entry.insert(0,'e.g. 110005')			# Placeholder
# pincode_entry.bind("<Button>",passText)			# Disappear placeholder on click
pincode_entry.pack(padx=(0,5), side=LEFT)

# Fetch data button
click_here=PhotoImage(file='multimedia/button.png')
styled_button=Button(root,image=click_here,command=fetch_data, borderwidth=0)
styled_button.config(highlightbackground='#6666ff', highlightthickness=0)
styled_button.pack()
root.bind('<Return>',callback)

root.mainloop()