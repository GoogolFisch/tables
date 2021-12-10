from io import StringIO
from typing import Union


def bytearray2Int(array:bytearray) -> int:
	o = 0
	for e in array:o = (o << 8) + int(e)
	return o
def bytearray2Str(array:bytearray) -> str:
	o = ""
	for e in array:o += chr(e)
	return o
def int2bytearray(num:int) -> list:
	o = [];e = num
	while e & 0xff_ff:o.insert(0,e & 0xff);e = e >> 8
	return o
def str2bytearray(string:str) -> list:
	return [ord(o) for o in string]

class Colum:
	math = __import__("math")
	content = ""
	filled = False
	prevalue = None
	color = 15
	pos = 0
	def __init__(self,pos:int,content:Union[None,str]=None,color:int=15) -> None:
		self.pos = pos
		self.color = color
		if content is not None:
			self.content = content
			self.filled  = True
		else:content = str()

	def addCon(self,What:str,color:int=0) -> None:
		self.content  = What
		self.filled   = True
		self.prevalue = None
		self.color    = color
	
	def setColor(self,color:int):
		self.color  = color
		self.filled = True
	
	def GetCon(self) -> str:
		return self.content
	
	def reset(self) -> None:
		self.prevalue = None
		
	def isMath(self) -> bool:
		return self.content[:1] == "="

	def evaling(self,board,pos,error:bool=True):
		try:
			def get(x:int,y:int,math:bool=False):
				a = board.GetConDown(x,y)
				if math and a.isMath() and a.prevalue is not None:
					return a.prevalue
				elif math and a.isMath():
					b = a.evaling(board,[x,y],error)
					a.prevalue = b
					return b
				else:
					return a.__str__()
			x,y = pos[0],pos[1]
			math = self.math
			self.prevalue = eval(self.content[1:],{"math":math,"x":x,"y":y,"get":get})
			a = str(self.prevalue)
			return " " * (8 - len(a[:8])) + a[:8]
		except Exception as e:
			if error:
				a = str(e).replace("\n","")
				return " " * (8 - len(a[:8])) + a[:8]
			else    :
				return " " * (8 - len(self.content[:8])) + self.content[:8]

	def __str__(self) -> str:
		a = self.content[:8]
		return " " * (8 - len(a)) + a
	
	def GetColor(self) -> str:
		return str([30,31,32,33,34,35,36,37,90,91,92,93,94,95,96,97][self.color & 0xf])

class Row:
	content = None
	filled = False
	pos = 0
	def __init__(self,pos:int,content:Union[None,list]=None) -> None:
		self.pos = pos
		if content is not None:
			self.content = content
			self.filled  = True
		else:self.content = list()

	def addCon(self,What:Colum) -> None:
		self.content.insert(0,What)
		self.content.sort(key = lambda x:x.pos)
		a = -1
		for x in self.content:
			if a >= x.pos:
				self.content.remove(x)
			a = x.pos
		self.filled = True
	
	def search(self,start,end,index) -> Colum:
		diff = (end - start) // 2
		if diff >= 1:
			if   self.content[start + diff].pos == index	:return self.content[start + diff]
			elif self.content[start + diff].pos < index	:return self.search(start + diff,end        ,index)
			else												:return self.search(start       ,end - diff ,index)
		elif diff == 0:
			if len(self.content) and self.content[start + diff].pos == index:
				return self.content[start + diff]
			else:
				return Colum(index)
		else:
			return Colum(index)


	def GetCon(self,index:int) -> Colum:
		return self.search(0,len(self.content),index)
	def __str__(self) -> str:
		return str(self.pos) + "\t[" + "|".join([str(x) for x in self.content]) + "]"

	def rem(self,index:int) -> bool:
		"""False if nothing happend"""
		a = self.GetCon(index)
		if a.filled:
			self.content.remove(a)
			return True
		else:
			return False


class Board:
	content = list()
	def __init__(self) -> None:
		pass
	
	def search(self,start,end,index) -> Colum:
		diff = (end - start) // 2
		if diff >= 1:
			if   self.content[start + diff].pos == index	:return self.content[start + diff]
			elif self.content[start + diff].pos < index	:return self.search(start + diff,end        ,index)
			else												:return self.search(start       ,end - diff ,index)
		elif diff == 0:
			if len(self.content) and self.content[start + diff].pos == index:
				return self.content[start + diff]
			else:
				return Row(index)
		else:
			return Row(index)

	def GetCon    (self,index:int		  ) -> Row  :return self.search(0,len(self.content),index)
	def GetConDown(self,indX :int,indY:int) -> Colum:return self.GetCon(indY).GetCon(indX)

	def addConCol(self,pos:int,What:Colum) -> None:
		a = self.search(0,len(self.content),pos)
		if not a.filled:
			self.addConRow(a)
		a.addCon(What)

	def addConRow(self,What:Row) -> None:
		self.content.insert(0,What)
		self.content.sort(key = lambda x:x.pos)
		a = -1
		for x in self.content:
			if a >= x.pos:
				self.content.remove(x)
			a = x.pos
	
	def rem(self,index:int) -> bool:
		"""False if nothing happend"""
		a = self.GetCon(index)
		if a.filled:
			self.content.remove(a)
			return True
		else:
			return False
	
	def loadS(self,string:bytearray):
		"""
		headder:
		- 8 bytes:type
		Data:
		- 2 bytes:length
		- Row length times:
		- - 2 bytes:y coord
		- - 2 bytes:length
		- - Colum length times:
		- - - 2 bytes:x coord
		- - - 1 byte :color
		- - - 1	byte :length
		- - - length bytes:string
		"""
		self.content = list()
		add = 0
		if string[add:add + 8] == bytearray([69,120,101,108,0,1,0,0]):
			add += 8
			rowLen = bytearray2Int(string[add:add + 2]);add += 2
			for rowIterate in range(rowLen):
				ypos = bytearray2Int(string[add:add + 2]);add += 2
				row = Row(ypos)
				colLen = bytearray2Int(string[add:add + 2]);add += 2
				for colIterate in range(colLen):
					xpos = bytearray2Int(string[add:add + 2]);add += 2
					length = bytearray2Int(string[add:add + 1]);add += 1
					col = Colum(xpos,bytearray2Str(string[add:add + length]))
					add += length
					row.addCon(col)
				self.addConRow(row)

			return True
		elif string[add:add + 8] == bytearray([69,120,101,108,0,1,0,1]):
			add += 8
			rowLen = bytearray2Int(string[add:add + 2]);add += 2
			for rowIterate in range(rowLen):
				ypos = bytearray2Int(string[add:add + 2]);add += 2
				row = Row(ypos)
				colLen = bytearray2Int(string[add:add + 2]);add += 2
				for colIterate in range(colLen):
					xpos = bytearray2Int(string[add:add + 2]);add += 2
					color = bytearray2Int(string[add:add + 1]);add += 1
					length = bytearray2Int(string[add:add + 1]);add += 1
					col = Colum(xpos,bytearray2Str(string[add:add + length]),color)
					add += length
					row.addCon(col)
				self.addConRow(row)

			return True
		else:
			return False
		

	def saveS(self) -> bytearray:
		"""
		headder:
		- 8 bytes:type
		Data:
		- 2 bytes:length
		- Row length times:
		- - 2 bytes:y coord
		- - 2 bytes:length
		- - Colum length times:
		- - - 2 bytes:x coord
		- - - 1 byte :color
		- - - 1	byte :length
		- - - length bytes:string
		"""
		# headder:
		out = [ord(x) for x in "Exel"] + [0,1,0,1]
		# next
		rowLen = len(self.content)
		out += [(rowLen >> 8) & 0xff,rowLen & 0xff]
		for rowIterate in self.content:
			ypos = rowIterate.pos
			out += [(ypos >> 8) & 0xff,ypos & 0xff]
			colLen = len(rowIterate.content)
			out += [(colLen >> 8) & 0xff,colLen & 0xff]
			for colIterate in rowIterate.content:
				xpos = colIterate.pos
				out += [(xpos >> 8) & 0xff,xpos & 0xff]
				out += [colIterate.color]
				colLen = len(colIterate.content[:256])
				out += [colLen]
				out += str2bytearray(colIterate.content[:256])
		return bytearray(out)

	
	def __str__(self) -> str:
		return "\n".join([str(d) for d in self.content])