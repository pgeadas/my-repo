# -*- coding: cp1252 -*-
from matplotlib.mlab import FormatInt
import os
import wx
from SGA_BC import *


class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(400,450))

        self.CreateStatusBar() # A StatusBar in the bottom of the window

        quoteList = ['Número de Gerações:', 'Tamanho da População:', 'Número de Pontos:',  'Target:',
         'Tamanho do Torneio/Roleta:', 'Probabilidade de Crossover (0 a 1):', 'Número de Pontos de Crossover:', 'Probabilidade de Mutação: (0 a 1)', 'Percentagem de Elites (0 a 1):', 'Modo de Selecção (1-Torneio, 2-Roleta):','1-Partiçoes iguais, 2-Partições Aleatorias', '1-Mutacao Normal, 2-Mutacao Gaussiana\n']
        #defaultValues = [1000, 50, 10, [0,75,500,25] , 3, 0.5, 3, 0.1, 0.3, 1]

        defaultValues = [4, 10, 5, [150,75,200,25] , 3, 0.5, 1, 0.1, 0.2, 1,2,1]

        self.buttons = []
        self.tFields = []
        self.quotes = []
        self.grid = wx.GridBagSizer(hgap=5, vgap=13)
        self.grid2 = wx.GridBagSizer(hgap=1, vgap=8)
        self.grid3 = wx.GridBagSizer(hgap=1, vgap=8)

        self.logger = wx.TextCtrl(self, size=(300,300), style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.buttons.append(wx.Button(self, -1, " Start Work!"))
        font1 = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, u'Arial')

        # Setting up the menu.
        filemenu= wx.Menu()

        # wx.ID_ABOUT and wx.ID_EXIT are standard ids provided by wxWidgets.
        menuOpen = filemenu.Append(wx.ID_OPEN, "Open File","Open File")
        menuAbout = filemenu.Append(wx.ID_ABOUT, "About"," Credits")
        menuExit = filemenu.Append(wx.ID_EXIT,"Exit"," Terminate the program")

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        # Set events.
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)

        self.Bind(wx.EVT_BUTTON, self.OnClickStart,self.buttons[0])

        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer2.Add(self.buttons[0], 1, wx.ALIGN_LEFT| wx.ALIGN_BOTTOM)

        x=0
        for i in range(0, 12):
            self.tFields.append(wx.TextCtrl(self,0, `defaultValues[i]`))
            self.grid2.Add(self.tFields[i], pos=(x,0))

            self.quotes.append(wx.StaticText(self, label=quoteList[i]))
            self.quotes[i].SetForegroundColour((255,255,255)) # set text color
            self.quotes[i].SetFont(font1)# change font parameters
            #self.quotes[i].SetBackgroundColour((0,0,0)) # set text back color
            self.grid.Add(self.quotes[i], pos=(x,0))
            x=x+1


        self.grid3.Add(self.logger,pos=(0,0))

        # Use some sizers to see layout options
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.grid, 0, wx.ALL, 5)
        self.sizer.Add(self.grid2, 0, wx.ALL, 5)
        self.sizer.Add(self.grid3, 0, wx.ALL, 5)
        self.sizer.Add(self.sizer2, 1, wx.EXPAND)

        #Layout sizers
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)

        self.Show()

        self.Show(True)


    def OnAbout(self,e):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog( self, "Elaborado por:\n\nPedro Geadas\n2006131902\npmrg@student.dei.uc.pt ", "About", wx.OK)
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.

    def OnExit(self,e):
        self.Close(True)  # Close the frame.

    def OnOpen(self,e):
        """ Open a file"""
        self.dirname = ''
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(os.path.join(self.dirname, self.filename), 'r')
            self.logger.SetValue(f.read())
            f.close()
        dlg.Destroy()


    def OnClickStart(self,event):

        #o segundo parametro, numero de individuos, tem que ser par
        #o terceiro parametro (numero de pontos) tem que ser maior que o numero de divisios de cross_over (parametro -3)
        #o numero de pontos (3 parametro) ainda nao inclui o ultimo
        # o parametro -1, diz nos qual o modo de seleccao ( 1 = torneio, 2 = roleta )
        alphabet = []
        str = ''

        #parametro 1
        try:
            num_ger = atoi(self.tFields[0].GetLineText(0))
            if(num_ger<=0):
                self.logger.AppendText("O numero de gerações tem que ser positivo!\n")
                return 1
        except Exception:
            self.logger.AppendText("O numero de gerações tem que ser um inteiro!\n")
            return 1

        #parametro 5
        try:
            size_tourn = atoi(self.tFields[4].GetLineText(0))
            if(size_tourn<=0):
                self.logger.AppendText("O tamanho do torneio tem que ser positivo!\n")
                return 1
        except Exception:
            self.logger.AppendText("O tamanho do torneio tem que ser um inteiro!\n")
            return 1

        #parametro 2
        try:
            size_pop = atoi(self.tFields[1].GetLineText(0))
            if(size_pop%2 != 0):
                self.logger.AppendText("O tamanho da população tem que ser par!\n")
                return 1
            elif(size_pop<=0):
                self.logger.AppendText("O tamanho da população tem que ser positivo!\n")
                return 1
            elif(size_pop<=size_tourn):
                self.logger.AppendText("O tamanho da população tem que ser >= que o tamanho do torneio!\n")
                return 1
        except Exception:
            self.logger.AppendText("O tamanho da população tem que ser um inteiro!\n")
            return 1

        #parametro 7
        try:
            n_crossover = atoi(self.tFields[6].GetLineText(0))
            if(n_crossover<=0):
                self.logger.AppendText("O numero de crossovers tem que ser positivo!\n")
                return 1
        except Exception:
            self.logger.AppendText("O numero de crossovers tem que ser um inteiro!\n")
            return 1

       #parametro 3
        try:
            num_pontos = atoi(self.tFields[2].GetLineText(0))
            if(num_pontos<=0):
                self.logger.AppendText("O numero de pontos tem que ser positivo!\n")
                return 1

            elif(num_pontos <= n_crossover):
             self.logger.AppendText('Nº crossover maior que o numero de pontos!!\n')
             return 1
        except Exception:
            self.logger.AppendText("O numero de pontos tem que ser um inteiro!\n")
            return 1


        #parametro 4
        try:
            d = self.tFields[3].GetLineText(0)
            if(d[0] != '[' or d[-1]!= ']'):
                self.logger.AppendText("Inserir na forma:  [xi,yi,xf,yf]  \n")
                return 1

            str = d[1:-1]
            points = str.split(',',3)
            for p in points:
                alphabet.extend([float(p)])

            if(alphabet[-1]>=alphabet[1]):
                self.logger.AppendText("Target: O valor de [yf] tem que ser inferior a [yi]!!\n")
                return 1
            elif(alphabet[0]>=alphabet[2]):
                self.logger.AppendText("Target: O valor de [xf] tem que ser inferior a [xi]!!\n")
                return 1

        except Exception:
            self.logger.AppendText("Inserir na forma:  [x1,y1,x2,y2]  \n")
            
            return 1



        #parametro 6, 8 e 9
        try:
            prob_cross = atof(self.tFields[5].GetLineText(0))
            prob_muta = atof(self.tFields[7].GetLineText(0))
            elites = atof(self.tFields[8].GetLineText(0))
            if(prob_cross<0 or prob_cross>1):
                self.logger.AppendText("Probabilidade de Crossover!\nInsira um valor entre 0 e 1!!\n")
                return 1
            elif(prob_muta<0 or prob_muta>1):
                self.logger.AppendText("Probabilidade de Mutação!\nInsira um valor entre 0 e 1!!\n")
                return 1
            elif(elites<0 or elites>1):
                self.logger.AppendText("Percentagem de Elites!\nInsira um valor entre 0 e 1!!\n")
                return 1
        except Exception:
            self.logger.AppendText("Insira um valor entre 0 e 1!!!\n")
            return 1


        #parametro 10
        try:
            mode = atoi(self.tFields[9].GetLineText(0))
            if(mode !=1 and mode != 2):
                self.logger.AppendText("Opções:\n1- Torneio\n2- Roleta\n")
                return 1
        except Exception:
            self.logger.AppendText("-Opções:\n1- Torneio\n2- Roleta\n")
            return 1

        #parametro 11
        try:
            spacement = atoi(self.tFields[10].GetLineText(0))
            if(spacement !=1 and spacement != 2):
                self.logger.AppendText("Opções:\n1-Partiçoes iguais, 2-Partições Aleatorias\n")
                return 1
        except Exception:
            self.logger.AppendText("-Opções:\n1-Partiçoes iguais, 2-Partições Aleatorias\n")
            return 1

                #parametro 12
        try:
            mut_type = atoi(self.tFields[11].GetLineText(0))
            if(mut_type !=1 and mut_type != 2):
                self.logger.AppendText('1-Mutacao Normal, 2-Mutacao Gaussiana\n')
                return 1
        except Exception:
            self.logger.AppendText('-1.Mutacao Normal, 2.Mutacao Gaussiana\n')
            return 1

       # f = open('population.txt','w')

        times = 30
        results = sga(num_ger, size_pop, num_pontos, alphabet, size_tourn, prob_cross, n_crossover, prob_muta, elites, mode,spacement,mut_type, times)
        
        
        
        print "That's it!"
        # Process data: best by generation
        ylabel('Fitness')
        xlabel('Generation')
        title('Weasel')
        p1 = plot(results[0], 'r-s', label="Best")
        legend(loc='upper right')
        show()

        x_cor = []
        y_cor = []
       # print results[1]
       # print results[2]
        for i in range(len(results[1])):
            if(i%2 ==0):
                x_cor.extend([results[1][i]])
            else:
                y_cor.extend([results[1][i]])

        ylabel('Y')
        xlabel('X')
        title('Brachistochrone Curve')
        p2 = plot(x_cor, y_cor, label="Best")
        legend(loc='upper right')
        show()


#app = wx.App(1, 'filespec.txt') #redirects stdout to the file 'filespec'
app = wx.App(0)
frame = MainWindow(None, "Introdução à Inteligência Artificial - TP2 ")
app.MainLoop()