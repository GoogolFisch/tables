import sys
import os
import color,reader,RC

# color.init()
if sys.platform.startswith("linux") or sys.platform == "darwin":
# 	Men = RC.Board()
	osp = "lin"
elif sys.platform in ("win32", "cygwin"):
# 	Men = RC.Board()
	osp = "win"
else:print("Error");exit(1)
Men = RC.Board()


class Main:
	def __init__(self):
		self.size = os.get_terminal_size()
		self.tabelSize = (self.size.columns // 9 - 1,self.size.lines - 3)
		self.matrix = []
		self.edit_tab = [0,0]
		self.slow_tab = [0,0]
		self.copy = ""

	def editTab(self,pos):
		x,y = pos[0],pos[1]
		data = Men.GetConDown(x,y).content
		editing = len(data)
		print(end="\033[47m\033[30m" + " " * 64 + "\b" * 64 + data,flush=True)
		while True:
			self.size = os.get_terminal_size()
			self.tabelSize = (self.size.columns // 9 - 1,self.size.lines - 3)
			#
			try:key = reader.readkey()
			except Exception:continue
			if   key is None:continue
			elif key is None:continue
			elif key == reader.key.ESC:
				print(end=color.Fore.RESET + color.Back.RESET)
				return
			elif key == reader.key.LEFT:
				if editing > 0:
					editing -=1
					print(end=reader.key.LEFT)
			elif key == reader.key.RIGHT:
				if editing < len(data):
					editing +=1
					print(end=reader.key.RIGHT)
			elif key == reader.key.ENTER:
				print(end=color.Fore.RESET + color.Back.RESET + " " * (self.tabelSize[0] * 9) + "\b" * (self.tabelSize[0] * 9))
				if data != "":Men.addConCol(y,RC.Colum(x,data))
				return
			elif (key == reader.key.BACKSPACE2 and osp == "win") or (key == reader.key.BACKSPACE and osp == "lin"):
				if editing > 0:
					data = data[:editing - 1] + data[editing:]
					editing -= 1
					print("\b" + data[editing:],end="  \b\b" + "\b" * (len(data) - editing),flush=True)
			elif len(key) == 1 and key in " =^1234567890!\"§$%&/()={?}[]\\<|>qw°easdyxcrtzfghvbnuiojklmpQWERTZUIOPASDFGHJKLYXCVBNM@,.-+#*'~-,.;:":
				if len(data) < 0xff:
					data = data[:editing] + key + data[editing:]
					print(data[editing:],end="\b" * len(data[editing + 1:]),flush=True)
					editing += 1
		
	def display(self):
		print(end="\033[1;1Hexel_not" + color.Back.RESET + color.Fore.RESET)
		for x in range(self.slow_tab[0],self.slow_tab[0] + self.tabelSize[0]):
			a = str(x)
			print(end="|" + " " * (8 - len(a)) + a)
		for y in range(self.slow_tab[1],self.slow_tab[1] + self.tabelSize[1]):
			a = str(y)
			print(end="\n" + " " * (8 - len(a)) + a)
			b = Men.GetCon(y)
			for x in range(self.slow_tab[0],self.slow_tab[0] + self.tabelSize[0]):
				c = b.GetCon(x)
				print(end=color.Fore.RESET + "|\033[" + c.GetColor() + "m")
				if c.isMath():
					print(end=c.evaling(Men,[x,y]))
				else:
					print(end=c.__str__())
		#
		edit = Men.GetConDown(self.edit_tab[0],self.edit_tab[1])
		print(end="\n-------->" + color.Fore.BLACK + color.Back.WHITE + edit.content + color.Fore.RESET + color.Back.RESET)
		print(end=" " * (self.size[0] - len(edit.content)))
		#
		print(end=f"\033[{(self.edit_tab[1] - self.slow_tab[1] + 2)};{(self.edit_tab[0] - self.slow_tab[0] + 1) * 9 + 1}H")
		if edit.isMath():
			edit = edit.evaling(Men,self.edit_tab)
		else:
			edit = str(edit)
		print(
			end=color.Back.GREEN + color.Fore.BLACK + edit + "\b" * len(edit) + color.Back.RESET + color.Fore.RESET,flush=True
		)
	

	def Console(self):
		data = ":"
		editing = len(data)
		print(end=color.Fore.GREEN + color.Back.BLACK + " " * 64 + "\b" * 64 + data,flush=True)
		while True:
			self.size = os.get_terminal_size()
			self.tabelSize = (self.size.columns // 9 - 1,self.size.lines - 3)
			#
			#
			try:key = reader.readkey()
			except Exception:continue
			if key is None:continue
			elif key == reader.key.ESC:
				print(end=color.Fore.RESET + color.Back.RESET)
				return (False,)
			elif key == reader.key.LEFT:
				if editing > 0:
					editing -=1
					print(end=reader.key.LEFT)
			elif key == reader.key.RIGHT:
				if editing < len(data):
					editing +=1
					print(end=reader.key.RIGHT)
			elif key == reader.key.ENTER:
				print(end=color.Fore.RESET + color.Back.RESET)
				if data[0:1] == ":":
					if   data[1:3] == "s ":
						a = Men.saveS()
						with open(data[3:],"wb")as f:f.write(a)
					elif data[1:3] == "l ":
						with open(data[3:],"rb")as f:Men.loadS(f.read())
					elif data[1:4] == "a":
						p = data.split(" ")
						self.edit_tab[0] = min(0xff_ff,max(0,int(p[1])))
						self.edit_tab[1] = min(0xff_ff,max(0,int(p[2])))
						self.slow_tab[0] = min(0xff_ff,max(0,self.edit_tab[0] - 2))
						self.slow_tab[1] = min(0xff_ff,max(0,self.edit_tab[1] - 2))
					elif data[1:3] == "m ":
						a = Men.GetConDown(self.edit_tab[0],self.edit_tab[1])
						a.setColor(int(data[3:],2))
					elif data[1:2] == "c":self.copy = Men.GetConDown(self.edit_tab[0],self.edit_tab[1]).content
					elif data[1:2] == "p":Men.addConCol(self.edit_tab[1],RC.Colum(self.edit_tab[0],self.copy))
					elif data[1:2] == "q":return (True,)
					else:
						print(end="\a")
				return (False,)
			elif key == reader.key.BACKSPACE2:
				if editing > 0:
					data = data[:editing - 1] + data[editing:]
					editing -= 1
					print("\b" + data[editing:],end="  \b\b" + "\b" * (len(data) - editing),flush=True)
			elif len(key) == 1 and key in " =12345^°67890!\"§$%&/()={?}[]\\<|>qweasdyxcrtzfghvbnuiojklmpQWERTZUIOPASDFGHJKLYXCVBNM@,.-+#*'~-,.;:":
				if len(data) < 0xff:
					data = data[:editing] + key + data[editing:]
					print(data[editing:],end="\b" * len(data[editing + 1:]),flush=True)
					editing += 1
			# else:
			# 	print([hex(ord(d)) for d in key])

	def onTab(self):
		self.display()
		while True:
			self.size = os.get_terminal_size()
			self.tabelSize = (self.size.columns // 9 - 1,self.size.lines - 3)
			#
			#
			try:key = reader.readkey()
			except Exception:continue
			if   key is None:continue
			elif key == reader.key.CTRL_C:	return
			elif key == reader.key.CTRL_D:	print("\n"+str(Men));return
			elif key == reader.key.ESC   :
				for itY in Men.content:
					for itX in itY.content:
						itX.prevalue = None
				self.display()
			elif key == reader.key.BACKSPACE2:
				a = Men.GetCon(self.edit_tab[1])
				a.rem(self.edit_tab[0])
				if len(a.content) == 0:
					Men.rem(self.edit_tab[1])
				self.display()

			elif key == reader.key.ENTER :
				print(end=f"\033[{self.tabelSize[1] + 2};1H > > > > ")
				self.editTab(self.edit_tab)
				print(end=f"\033[{str(self.edit_tab[1] + 1)};{str(self.edit_tab[0] + 1)}H")
				self.display()
			
			elif key == ":":
				print(end=f"\033[{self.tabelSize[1] + 2};1HConsole >")
				a = self.Console()
				print(end=f"\033[{str(self.edit_tab[1] + 1)};{str(self.edit_tab[0] + 1)}H")
				self.display()
				if a[0]:
					print(f"\033[{self.size[1]};1H")
					return

			elif key == reader.key.UP   :
				if self.edit_tab[1] > 0:
					self.edit_tab[1] -= 1
					if self.slow_tab[1] > 0 and self.edit_tab[1] - self.slow_tab[1] < 2:
						self.slow_tab[1] -= 1
				self.display()
			elif key == reader.key.DOWN :
				if self.edit_tab[1] < 0xff_ff:
					self.edit_tab[1] += 1
					if self.slow_tab[1] < 0xff_ff and self.edit_tab[1] - self.slow_tab[1] > self.tabelSize[1] - 3:
						self.slow_tab[1] += 1
				self.display()
			elif key == reader.key.LEFT :
				if self.edit_tab[0] > 0:
					self.edit_tab[0] -= 1
					if self.slow_tab[0] > 0 and self.edit_tab[0] - self.slow_tab[0] < 2:
						self.slow_tab[0] -= 1
				self.display()
			elif key == reader.key.RIGHT:
				if self.edit_tab[0] < 0xff_ff:
					self.edit_tab[0] += 1
					if self.slow_tab[0] < 0xff_ff and self.edit_tab[0] - self.slow_tab[0] > self.tabelSize[0] - 3:
						self.slow_tab[0] += 1
				self.display()
			# else:
			# 	if key != None:
			# 		print([hex(ord(d)) for d in key])
			# 	else:
			# 		print(None)

if __name__ == '__main__':
	os.system("cls")
	MainClass = Main()
	MainClass.onTab()