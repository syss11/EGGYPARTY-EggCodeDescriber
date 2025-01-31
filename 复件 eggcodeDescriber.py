from PySide6.QtCore import QRect,Slot,QPoint

from PySide6.QtGui import QPixmap,QPainter,QImage,QColor,Qt,QPen
from PySide6.QtWidgets import QApplication,QWidget,QLineEdit,QLabel,QPushButton,QTextEdit
import sys
import re #分字符串用
OFFSET=17
color_dict={"B":QColor(101,110,255),"X":QColor('black'),"R":QColor('red'),"Y":QColor(255,182,6),"G":QColor(95,209,8),"W":QColor('white'),"b":QColor('blue'),"x":QColor('black'),"r":QColor('red'),"y":QColor('yellow'),"g":QColor('green'),"w":QColor('white'),"P":QColor('purple'),
"V":QColor(255,192,203),"L":QColor(135,206,250)
}
b_front=None
initial_picture={}



def apart_string(method,string):
	delimiters = '['+method+"]"
	# 分割
	sp= re.split(delimiters, string)
	return sp


maxh=0#计算高度的max值，函数里用
whi=QPen(QColor("white"))
bla=QPen(QColor("black"))
class Eggcode():
	def __init__(self):
		self.name=""
		self.children=[]
		self.parent=None
		self.pur=False
		#图形化后的外观
		
		self.m_rect=QRect()
		self.x=0
		self.y=0
		self.hight=20
		self.width=5
		self.color="B"#决定颜色的字符键
		self.right_livel=0#缩进层级，默认为0，蛋码套在控制积木时+1级
		
		
	def addchild(self,child):
		self.children.append(child)
		child.parent=self

	def appendtext(self,text):
		if len(self.children)==0:
			self.children.append(text)
			return 
		if isinstance(self.children[-1],Eggcode):
			self.children.append("")
		self.children[-1]+=text
		
	def ReWidth(self):
		sum_w=0
		for ch in self.children:
			if isinstance(ch,str):
				sum_w+=len(ch)*OFFSET
			else:
				sum_w+=ch.ReWidth()
				
		self.width=sum_w
		return sum_w
		
	
			
		
		
	def init_color(self):

		try:
			first=self.children[0]
			if isinstance(first,str):
				if first[0]=="#":
					self.color=first[1]
					self.children[0]=first[2:]
				else:
					if self.parent==None:
						self.color="B"
					else:
						self.color="G"
			else:
				if self.parent==None:
					self.color="B"
				else:
					self.color="G"

				#X是无颜色的黑色积木表明获取颜色失败
		except:
			raise ValueError("?")
		if self.pur:
			self.color="P"
						
		for ch in self.children:
			if isinstance(ch,Eggcode):
				ch.init_color()
			
			
	#流程：先计算所有图形属性，然后开始遍历列表确定上下顺序。图形属性的计算：
	#偏移量，宽度，高度。
	def DETERmine_pos(self,addition,xx,yy):
		#xx+=self.right_livel*20
		self.x=xx+self.right_livel*20
		self.y=yy
		
		for ch in self.children:
			if isinstance(ch,str):
				addition+=len(ch)*OFFSET
			else:
				addition+=ch.DETERmine_pos(0,xx+addition,yy)
				#addition+=len(ch)*OFFSET
		
		return addition
		
	def Giveheight(self,startyy):
		global maxh
		maxh=0
		have=[]
		
		self.Rehight(have,0,startyy)#Max全局
		return 10*maxh
	def Rehight(self,have_list,lower_value,startyy):
		global maxh
		self.y=startyy+lower_value*5
		for ch in self.children:
			if isinstance(ch,Eggcode):
				ch.Rehight(have_list,lower_value+1,startyy)
			
		if maxh<lower_value:
			maxh=lower_value
			for had in have_list:
				had.hight+=10
				
		self.hight=30+10*(maxh-lower_value)
		have_list.append(self)
		
		return lower_value
		
	def Paint_execute(self,qpainter:QPainter):
		global whi,bla
		if self.pur:
			self.m_rect.setX(self.x)
		else:
			self.m_rect.setX(self.x)#dont
		
		self.m_rect.setY(self.y)
		self.m_rect.setWidth(self.width)
		self.m_rect.setHeight(self.hight)
		print("Success",self.x,self.y,self.width,self.hight)#dhdhhdhdhdhdhdhdhhf
		
		textpo=QPoint(self.m_rect.bottomLeft())
		print(textpo.x(),textpo.y())#&hhhhhhh&g

		qpainter.setBrush(color_dict[self.color])

		textpo.setX(textpo.x()+0)
		qpainter.drawRect(self.m_rect)
		#矩形！
		textpo.setY(textpo.y()-(self.hight-15)/2)

		
		for ch in self.children:

			if isinstance(ch,str):
				qpainter.setPen(bla)
				qpainter.drawText(textpo,ch)
				qpainter.setPen(whi)
				qpainter.drawText(QPoint(textpo.x()+1,textpo.y()-1),ch)
				textpo.setX(textpo.x()+len(ch)*OFFSET)
			else:
				textpo.setX(textpo.x()+ch.Paint_execute(qpainter))
			
		return self.width







egglist=[]

class MainWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.start_X=10
		self.prepare=False
		self.beautiful=QPixmap("eggbk.jpg").scaled(400,800)
		#加载图片
		initial_picture["B"]=QPixmap("frb.png").scaled(40,40)
		
		
		self.coverrect=QRect(10,300,340,400)
		
		self.allofc=[]#存储allof_maincodes
		self.inputer=QTextEdit(self)
		self.inputer.setGeometry(50,50,250,200)
		
		self.ok=QPushButton(self)
		self.ok.setGeometry(300,255,45,45)
		self.ok.setText("OK")
		self.ok.setPalette(QColor('yellow'))
		self.ok.clicked.connect(self.ret)
		
		
		self.exitbutton=QPushButton(self)
		self.exitbutton.setGeometry(5,255,45,45)
		self.exitbutton.setText("Quit")
		self.exitbutton.setPalette(QColor('red'))
		self.exitbutton.clicked.connect(self.exitme)
		
		self.outputer=QLabel(self)
		self.outputer.setGeometry(100,240,200,50)
		self.outputer.setText("输入蛋码表达式……")
		
		self.left=QPushButton(self)
		self.left.setGeometry(5,150,45,45)
		self.left.setText("<")
		self.left.setPalette(QColor('white'))
		self.left.clicked.connect(self.leftroll)
		
		self.lleft=QPushButton(self)
		self.lleft.setGeometry(300,150,45,45)
		self.lleft.setText(">")
		self.lleft.setPalette(QColor('white'))
		self.lleft.clicked.connect(self.rightroll)
		
	def leftroll(self):
		self.start_X-=20
		self.update()
	def rightroll(self):
		self.start_X+=20
		self.update()
	def paintEvent(self,event):
		p=QPainter(self)
		#p.setPen(QPen('white'))
		p.drawPixmap(QPoint(0,0),self.beautiful)
		p.drawRect(self.coverrect)
		
		if self.prepare:

			
			startx=self.start_X
			starty=300
			for eggs in egglist:
				
				eggs.DETERmine_pos(0,startx,starty)
				eggs.ReWidth()

				starty+=eggs.Giveheight(starty)
				#self.outputer.setText("al")
				if not eggs.pur:
					pass
					#p.drawPixmap(QPoint(eggs.x,eggs.y),initial_picture[eggs.color].scaled(30,eggs.hight))
				p.setBrush(QColor('purple'))
				for pow in range(eggs.right_livel):
					p.drawRect(QRect(startx+pow,eggs.y,24,eggs.hight))
				
				
				eggs.Paint_execute(p)
				
				starty+=30#后续计算h时加这里
				
		
		
	def exitme(self):
		sys.exit(2)
	
		
	def trigger_save(self):
		self.update()
		
		
	def ret(self):#处理总函数
		text=self.inputer.toPlainText()
		self.outputer.setText("处理完成")
		global egglist

		egglist=self.operate_input(text)
		for egg in egglist:
			egg.init_color()
		self.prepare=True
		self.update()

		
		
	def operate_input(self,treat):#接受字符串，返回allof列表
		allof_maincodes=[]
		obj_stack=[]
		
		power=0#缩进层级
		nowtimes=0
		line_num=0
		if ";" in treat:
			
			aparted_treat=apart_string(r";{}",treat)
		else:
			aparted_treat=apart_string("；｛｝",treat)
		
		for i in treat:
			nowtimes+=1
			if i == ";" or i=="；":
				line_num+=1
				nowtimes=0
				obj_stack.clear()
				continue
			if i=="{" or i =="｛":
				allof_maincodes[line_num].pur=True
				line_num+=1
				nowtimes=0
				obj_stack.clear()
				
				power+=1
				continue
			
			if i=="}" or i =="｝":
				line_num+=1
				nowtimes=0
				obj_stack.clear()
				
				power-=1
				insert=Eggcode()
				insert.children=["end"]
				insert.pur=True
				insert.right_livel=power
				
				allof_maincodes.append(insert)
				#line_num+=1
				continue
			
			
			if i =="(" or i=="（" :
				newobj=Eggcode()
				newobj.right_livel=power
			
				if len(obj_stack)!=0:
					obj_stack[-1].addchild(newobj)
				obj_stack.append(newobj)
				
			elif i == ")" or i=="）":
				if nowtimes==len(aparted_treat[line_num]):
					
					allof_maincodes.append(obj_stack[0])
					
				obj_stack.pop()
			
			else:#是字母
				if len(obj_stack)>0:
					obj_stack[-1].appendtext(i)
				else:
					self.outputer.setText("语法错误或括号不成对！")
		
		return allof_maincodes




app=QApplication([])

mainw=MainWindow()
mainw.show()
app.exec()


	
