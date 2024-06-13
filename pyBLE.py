import pexpect
import time

class BLEDevice():
	def __init__(self):
		self._callbacks = []
		self._remoteAddr = None
		self._child = None
		self._timeout = 10
		self._connect = False
		self._cmds = [""]


	def isConected(self):
		return self._connect
		
	def start(self):
		try:
			self._child = pexpect.spawn(f"gatttool -I")
			print("Device started")
		except Exception as error:
			print(f"An exception occured : {error}")
			self._child = None			
			
	def stop(self):
		try:
			self._child.sendline('exit')
			self._child = None
		except Exception as error:
			print(f"An exception occured : {error}")
	
	def connect(self,remoteAddr):
		try:
			self._child.sendline(f"connect {remoteAddr}")
			self._child.expect("Connection successful",timeout=self._timeout)
			self._connect = True
			self._remoteAddr = remoteAddr
		except Exception as error:
			print(f"An exception occured : {error}")
			self._connect = False
				
	def disconnect(self):
		'''
		disconnect from current connected device		
		'''
		try:
			self._child.sendline("disconnect")
			self._connect = False
			self._remoteAddr = None
			print("Disconnect to remote device.")
		except:
			pass
			
	def writeHnd(self,hnd,val):
		'''
		hnd : 10 base int
		val : string 
		'''
		try:
			val = val.encode('utf-8').hex()
			self._child.sendline(f"char-write-req 0x{hnd:04x} {val}")
			self._child.expect('Characteristic value was written successfully')
			print("value was written successfully.")
		except Exception as error:
			print(f"An exception occured : {error}")
		
				
	def readHnd(self,hnd,callback):
		'''
		hnd : 10 base int
		callback : function requires hnd and value
		'''		
		try:
			self._child.sendline(f"char-read-hnd 0x{hnd:04x}")
			self._child.expect(f"Notification handle = 0x{hnd:04x} value: ",timeout=self._timeout)
			self._child.expect("\r\n",timeout=self._timeout)
			val = self._child.before		
			
			#_, _, hex_value = msg.strip().split(" ",maxsplit=5)[3:]
			
			#value = bytearray.fromhex(hex_value)
			callback(bytes.fromhex(val.decode('utf-8')))		
		except Exception as error:
			print(f"An exception occured : {error}")		
			
# ---------------------------------------------------------------		
