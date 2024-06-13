def callback(val):
	#print(val)
	t,h,m,p= val.decode('utf-8').split(";")
	print(f'TempC : {t} C')	
	print(f'Humidity : {h} %')	
	print(f'Soil Moisture : {m} %')	
	print("----------")

if __name__ == "__main__":
	grass = "28:CD:xx:xx:xx:xx"
	vetgy = "28:CD:xx:xx:xx:xx"
	ble = BLEDevice()
	ble.start()
	ble.connect(vetgy)
	if ble.isConected():
		ble.readHnd(9,callback)
		ble.writeHnd(int('c',16),'P1')
		time.sleep(5)
		ble.writeHnd(int('c',16),'P0')
		time.sleep(2)
		ble.readHnd(9,callback)
		time.sleep(2)
		ble.readHnd(9,callback)
		ble.disconnect()
		ble.stop()
		
