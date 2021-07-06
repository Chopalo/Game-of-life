import tkinter as tk
import random as rd
import math as mt


LIVE=1
DEAD=0
IsRunning=False
class Cellular():
    def __init__(self,pos,status):
        self.pos=pos
        self.status=status

class Population():
    def __init__(self,n):

        self.MapppingConsole=[]
        self.c=int(mt.sqrt(n))
        self.pop=[]
        for i in range(self.c):
            self.pop.append([ 0 for x in range(self.c)])
            self.MapppingConsole.append([ 0 for x in range(self.c)])
        self.EmptyConfiguration_GOL()

    def  EmptyConfiguration_GOL(self):
        for i in range(self.c):
            for j in range(self.c):
                self.pop[i][j] = Cellular([i, j],DEAD)
                self.MapppingConsole[i][j]=0

    def law(self,Acel,CellAround):
        isBord=( (Acel.pos[0]==0 and Acel.pos[1]<self.c) or (Acel.pos[0]==self.c-1 and Acel.pos[1]<self.c) or (Acel.pos[0]<self.c and Acel.pos[1]==0) or (Acel.pos[0]<self.c and Acel.pos[1]==self.c-1) )
        if(isBord):
            Acel.status=DEAD
            return
        if(Acel.status==LIVE):
            if (CellAround < 2):
                Acel.status = DEAD
            elif(CellAround>3):
                Acel.status=DEAD
            elif(CellAround==2 or CellAround==3):
                Acel.status=LIVE
        elif(Acel.status==DEAD and CellAround==3):
            Acel.status=LIVE

    def lawMapping(self,Acel,x,y):
        CellAround=0
        for i in range(Acel.pos[0] - 1, Acel.pos[0] + 2):
            for j in range(Acel.pos[1] - 1, Acel.pos[1] + 2):
                if (self.pop[i][j].pos == Acel.pos):
                    pass
                else:
                    CellAround = CellAround + self.pop[i][j].status
        return CellAround

    def Evolution(self):
        for x in range(1,self.c-1):
            for y in range(1,self.c-1):
                self.MapppingConsole[x][y]=self.lawMapping(self.pop[x][y],x,y)


class AppRandom():
    def __init__(self,x,y,name,npop):
        self.window=tk.Tk()
        geo=str(x)+"x"+str(y)
        self.window.geometry(geo)
        self.window.title(name)
        self.MainCanvas=Canva(x,y,self.window,npop)
        self.MainCanvas.UpdateGOL()

        self.window.protocol("WN_DELETE_WINDOW",self.closing)
        self.window.mainloop()
    def closing(self,fen):
        fen.destroy()

class Canva_editor():
    def __init__(self,x,y,window,n):
        self.x=x
        self.y=y
        self.xp=int(x/int(mt.sqrt(n)))
        self.yp=int(y/int(mt.sqrt(n)))
        self.wn=window
        self.sqN=0
        self.OwnPop = Population(n)
        self.SquareList=[]
        self.CANV_PLATE=tk.Canvas(window,width=x,height=y,bg="white")
        self.InitGOL(self.CANV_PLATE)
        self.CANV_PLATE.grid()

    def InitGOL(self,can):
        for x in range(0,self.x,self.xp):
            for y in range(0,self.y,self.yp):
                #print(x,y)
                nam = str(int(x/self.xp)) + "," + str(int(y/self.yp))
                rc=can.create_rectangle(y,x,y+self.yp,x+self.xp,fill="white",outline="black",tags=nam)
                self.SquareList.append(rc)
                self.sqN=self.sqN+1
    def ResetGOL(self):
        print("reset")
        a=0
        for x in range(self.OwnPop.c):
            for y in range(self.OwnPop.c):
                #print(x,y)
                self.CANV_PLATE.itemconfig(self.SquareList[a],outline="black",fill="white")
                self.OwnPop.pop[x][y].status=DEAD
                self.OwnPop.MapppingConsole[x][y]=0
                a=a+1
    def UpdateGOL(self):
        global IsRunning
        if(not IsRunning):
            return
        a=0
        self.OwnPop.Evolution()
        for x in range(self.OwnPop.c):
            for y in range(self.OwnPop.c):
                self.OwnPop.law(self.OwnPop.pop[x][y], self.OwnPop.MapppingConsole[x][y])
                if(self.OwnPop.pop[x][y].status==LIVE):
                    self.CANV_PLATE.itemconfig(self.SquareList[a],outline="white",fill="black")
                else:
                    self.CANV_PLATE.itemconfig(self.SquareList[a],outline="black", fill="white")
                a=a+1
        self.wn.after(10,self.UpdateGOL)


class AppEditor():
    def __init__(self,x,y,npop):
        IsRunning=False
        self.window = tk.Tk()
        self.previous_square_selected=[-1,-1]
        geo = str(x) + "x" + str(y)
        self.window.geometry(geo)
        self.window.title("Game of life")
        self.window.resizable(False, False)
        self.MainCanvas = Canva_editor(x, y, self.window, npop)
        self.MainCanvas.CANV_PLATE.bind('<ButtonPress-1>', self.ClickOnce)
        self.MainCanvas.CANV_PLATE.bind('<B1-Motion>', self.Click)
        self.MainCanvas.CANV_PLATE.bind('<Button-3>', self.ChangeStatusRun)
        self.MainCanvas.CANV_PLATE.bind_all('<R>', self.RESET_ALL)
        self.window.protocol("WN_DELETE_WINDOW", self.closing)
        self.window.mainloop()
    def InitGOL_sequential(self):
        return
    def closing(self):
        self.window.destroy()
    def ChangeStatusRun(self,event):
        global IsRunning
        IsRunning= not IsRunning
        if (IsRunning):
            self.window.title("Game of life - Running ...")
            self.MainCanvas.UpdateGOL()
        else:
            self.window.title("Game of life")
            self.MainCanvas.ResetGOL()
    def RESET_ALL(self,event):
        self.MainCanvas.ResetGOL()

    def Click(self,event):
        x=self.MainCanvas.CANV_PLATE.gettags( self.MainCanvas.CANV_PLATE.find_closest(event.x,event.y))
        id_item=x[0]
        if(len(x)==0 and not x[0][0].isdigit() and not x[0][1].isdigit()):
            return
        x = list(x)
        x = x[0]
        x = x.split(',')
        #x is the tag : tag=[pos.x,pos.y]
        x[1] = int(x[1])
        x[0] = int(x[0])
        if(x==self.previous_square_selected):
            return
        if(self.MainCanvas.CANV_PLATE.itemcget( id_item ,"fill") =="white"):
            self.MainCanvas.OwnPop.pop[int(x[0])][int(x[1])].status=LIVE
            self.MainCanvas.CANV_PLATE.itemconfig(id_item,fill="black",outline="white")
        else:
            self.MainCanvas.OwnPop.pop[int(x[0])][int(x[1])].status = DEAD
            self.MainCanvas.CANV_PLATE.itemconfig(id_item, fill="white", outline="black")
        self.previous_square_selected = [x[0], x[1]]

    def ClickOnce(self,event):
        x=self.MainCanvas.CANV_PLATE.gettags( self.MainCanvas.CANV_PLATE.find_closest(event.x,event.y))
        id_item=x[0]
        if(len(x)==0 and not x[0][0].isdigit() and not x[0][1].isdigit()):
            return
        x = list(x)
        x = x[0]
        x = x.split(',')
        #x is the tag : tag=[pos.x,pos.y]
        x[1] = int(x[1])
        x[0] = int(x[0])
        if(self.MainCanvas.CANV_PLATE.itemcget( id_item ,"fill") =="white"):
            self.MainCanvas.OwnPop.pop[int(x[0])][int(x[1])].status=LIVE
            self.MainCanvas.CANV_PLATE.itemconfig(id_item,fill="black",outline="white")
        else:
            self.MainCanvas.OwnPop.pop[int(x[0])][int(x[1])].status = DEAD
            self.MainCanvas.CANV_PLATE.itemconfig(id_item, fill="white", outline="black")
        self.previous_square_selected = [x[0], x[1]]

class MainApplication():
    def __init__(self):
        self.wind=tk.Tk()
        self.wind.geometry("400x200")
        self.wind.title("Option menu - Game of life")
        self.wind.resizable(False,False)
        self.TITLE=tk.Label(text="Game of life",fg="black",width=10,font=40)
        self.N=tk.Label(text="Number of square",font=10,width=50,fg="black")
        self.N_Entry=tk.Entry(self.wind,width=10)
        self.DIM = tk.Label(text="Dimension", width=50, fg="black",font=10)
        self.DIM_Entry=tk.Entry(self.wind,width=10)
        OK_button=tk.Button(text="Start", width=10, fg="black",font=10,command=self.Checking)

        empty = tk.Label(text="", width=5, fg="black", font=1)
        self.TITLE.pack()
        self.N.pack()
        self.N_Entry.pack()
        self.DIM.pack()
        self.DIM_Entry.pack()
        empty.pack()
        OK_button.pack()

        self.wind.mainloop()

    def Checking(self):
        try:
            self.wind.title("Option menu - Game of life")
            N=self.N_Entry.get()
            dimens=self.DIM_Entry.get()
            if(not str(N).isdigit() or not str(dimens).isdigit()):
                self.wind.title(" GOL error - You didn't put a number !!!!")
                return
            N=int(N)
            if(N<=0):
                self.wind.title(" GOL error - Nice try !!!!")
                return
            dimens=int(dimens)
            ratio=float((dimens*dimens)/N)
            if(dimens<200):
                self.wind.title(" the dimension is too short (dim>200) !!!!")
                return
            if(mt.sqrt(N).is_integer()):
                pass
                #print("happy sqrt")
            else:
                self.wind.title("N has to be equal to N=a*a (Ex. N=16) !!!!")
                #print("angry sqrt")
                return
            if(ratio.is_integer()):
                pass
                #print("happy ration")
            else:
                self.wind.title("Change the dimension !!!!")
                #print("angry ration")
                return

            AppEditor(dimens, dimens,N)
        except ValueError:
            print("some value error appears")
        except Exception:
            print("somme issues appears")
        except ZeroDivisionError:
            print("You find a way to get this :/ !!!!")






#AppEditor(1000,1000,1600)
MainApplication()