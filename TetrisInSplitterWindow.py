import wx
import random


class TetrisInSplitterFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(630, 800) )
        
        self.initpos = 420
        self.sp = wx.SplitterWindow(self)
        self.board = Board(self.sp, style=wx.SUNKEN_BORDER)
        self.info = Info(self.sp, style=wx.SUNKEN_BORDER)
        self.board.SetBackgroundColour("pink")
        self.info.SetBackgroundColour("sky blue")
        self.sp.SplitVertically(self.board, self.info, self.initpos)
        self.sp.SetMinimumPaneSize(100)
        
        self.ShowNextPiece = Shape()
        # self.board.SetFocus()
        
        # self.Music = wx.Sound('E:\Lab7\s.mp3')
        
        self.board.start()
        
        self.Centre()
        self.Show(True)  
        
        
        

class Info(wx.Panel):
    BoardWidth = 6
    BoardHeight = 25
    def __init__(self, parent, style):
        wx.Panel.__init__(self, parent) 
        
        self.upspeedButton = wx.Button(self, -1, "Up Speed", pos=(15, 700))
        self.lowerButton = wx.Button(self, -1, "Lower Speed", pos=(100, 700))
        self.Bind(wx.EVT_BUTTON, self.OnUpSpeed, self.upspeedButton)
        self.Bind(wx.EVT_BUTTON, self.OnLowerSpeed, self.lowerButton)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        
        temp = wx.StaticText(self, -1,"ComingNext:", pos=(20, 40))
        temp.SetFont(wx.Font(25, wx.SCRIPT, wx.NORMAL, wx.NORMAL, False))
        temp.SetForegroundColour(wx.Colour(255, 255, 255))
        temp = wx.StaticText(self, -1,"Number of lines removed:",pos=(5,360))
        temp.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False))
        temp = wx.StaticText(self,-1,"Your Score:",pos=(5,420))
        temp.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False))
        
    def OnUpSpeed(self,event):
         if Board.Speed >= 100:
              Board.Speed = Board.Speed -50 
              self.GetParent().GetParent().board.timer.Start(Board.Speed)
          
    def OnLowerSpeed(self,event):
         Board.Speed = Board.Speed +50 
         self.GetParent().GetParent().board.timer.Start(Board.Speed)
              
    def squareWidth(self):
        return self.GetClientSize().GetWidth() / Info.BoardWidth  
          
    def squareHeight(self):
        return self.GetClientSize().GetHeight() / Info.BoardHeight
    
    def OnPaint(self, event):
        dc = wx.PaintDC(self)           
        size = self.GetClientSize()
        boardTop = size.GetHeight() - Info.BoardHeight * self.squareHeight()
        
        # dc.DrawText("Coming next:",20,40)
       
        # temp = wx.StaticText(self, -1,"Coming next:", pos=(20, 40))
        # temp.SetFont(wx.Font(5, wx.SWISS, wx.NORMAL, wx.BOLD, False))
        
        # dc.DrawText("Number of lines removed:",5,380)
        dc.DrawText("%d"%(self.GetParent().GetParent().board.numLinesRemoved),90,400)
        # dc.DrawText("Your Score:",5,420)
        dc.DrawText("%d"%(self.GetParent().GetParent().board.Score),90,460)
        #linesRemoved=wx.StaticText(self, -1, "", pos=(100, 400))
        #linesRemoved.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.BOLD, False))
        #linesRemoved.SetForegroundColour(wx.Colour(0, 0, 0, 255))
        #linesRemoved.SetLabel(u"%d"%(self.GetParent().GetParent().board.numLinesRemoved))
      
        
        if self.GetParent().GetParent().ShowNextPiece.shape() != Tetrominoes.NoShape:
            for i in range(4):
                x = self.GetParent().GetParent().ShowNextPiece.x(i)
                y = self.GetParent().GetParent().ShowNextPiece.y(i)
                self.drawSquare(dc, 0 + x * self.squareWidth()+70,
                    boardTop + (Info.BoardHeight + y - 1) * self.squareHeight()-600,
                    self.GetParent().GetParent().ShowNextPiece.shape())
                    
    def drawSquare(self, dc, x, y, shape):
        colors = ['#000000', '#CC6666', '#66CC66', '#6666CC',
                  '#CCCC66', '#CC66CC', '#66CCCC', '#DAAA00']

        light = ['#000000', '#F89FAB', '#79FC79', '#7979FC', 
                 '#FCFC79', '#FC79FC', '#79FCFC', '#FCC600']

        dark = ['#000000', '#803C3B', '#3B803B', '#3B3B80', 
                 '#80803B', '#803B80', '#3B8080', '#806200']

        pen = wx.Pen(light[shape])
        pen.SetCap(wx.CAP_PROJECTING)
        dc.SetPen(pen)

        dc.DrawLine(x, y + self.squareHeight() - 1, x, y)
        dc.DrawLine(x, y, x + self.squareWidth() - 1, y)

        darkpen = wx.Pen(dark[shape])
        darkpen.SetCap(wx.CAP_PROJECTING)
        dc.SetPen(darkpen)

        dc.DrawLine(x + 1, y + self.squareHeight() - 1,
            x + self.squareWidth() - 1, y + self.squareHeight() - 1)
        dc.DrawLine(x + self.squareWidth() - 1, 
        y + self.squareHeight() - 1, x + self.squareWidth() - 1, y + 1)

        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.SetBrush(wx.Brush(colors[shape]))
        dc.DrawRectangle(x + 1, y + 1, self.squareWidth() - 2, 
                         self.squareHeight() - 2)

               
     
                         
class Board(wx.Panel):
    BoardWidth = 12
    BoardHeight = 20
    Speed = 300
    ID_TIMER = 1
    def __init__(self, parent, style):
        wx.Panel.__init__(self, parent, style=wx.WANTS_CHARS) #you can use arrow keys after adding style = wx.WANTS_CHARS
    
        self.timer = wx.Timer(self, Board.ID_TIMER)
        self.isWaitingAfterLine = False
        self.curPiece = Shape()
        self.nextPiece = Shape() 
        self.nextPiece.setRandomShape()
        self.curX = 0
        self.curY = 0
        self.numLinesRemoved = 0
        self.Score = 0
        self.board = []

        self.isStarted = False
        self.isPaused = False

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.Bind(wx.EVT_TIMER, self.OnTimer, id=Board.ID_TIMER)

        self.clearBoard()

    def shapeAt(self, x, y):
        return self.board[(y * Board.BoardWidth) + x]

    def setShapeAt(self, x, y, shape):
        self.board[(y * Board.BoardWidth) + x] = shape

    def squareWidth(self):
        return self.GetClientSize().GetWidth() / Board.BoardWidth

    def squareHeight(self):
        return self.GetClientSize().GetHeight() / Board.BoardHeight

    def start(self):
        if self.isPaused:
            return

        self.isStarted = True
        self.isWaitingAfterLine = False
        self.numLinesRemoved = 0
        self.Score = 0
        self.clearBoard()
        
        wx.MessageBox(u"Hello!Welcome to Tetris World!\nHere are some information you may need:\nw:rotate\na/d:left/right move\ns:one line down\nspace:drop down\np:pause\nHope you enjoy!^.^",
                      u"Hello",wx.OK | wx.ICON_INFORMATION, self)
        
        # self.GetParent().GetParent().Music.Play(wx.SOUND_ASYNC)
        
        self.newPiece()
        self.timer.Start(Board.Speed)

    def pause(self):
        if not self.isStarted:
            return

        self.isPaused = not self.isPaused
        # statusbar = self.GetParent().statusbar

        if self.isPaused:
            self.timer.Stop()
            # statusbar.SetStatusText('paused')
        else:
            self.timer.Start(Board.Speed)
            # statusbar.SetStatusText(str(self.numLinesRemoved))
        self.Refresh()

    def clearBoard(self):
        for i in range(Board.BoardHeight * Board.BoardWidth):
            self.board.append(Tetrominoes.NoShape)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)        

        size = self.GetClientSize()
        boardTop = size.GetHeight() - Board.BoardHeight * self.squareHeight()
        
        for i in range(Board.BoardHeight):
            for j in range(Board.BoardWidth):
                shape = self.shapeAt(j, Board.BoardHeight - i - 1)
                if shape != Tetrominoes.NoShape:
                    self.drawSquare(dc,
                        0 + j * self.squareWidth(),
                        boardTop + i * self.squareHeight(), shape)

        if self.curPiece.shape() != Tetrominoes.NoShape:
            for i in range(4):
                x = self.curX + self.curPiece.x(i)
                y = self.curY - self.curPiece.y(i)
                self.drawSquare(dc, 0 + x * self.squareWidth(),
                    boardTop + (Board.BoardHeight - y - 1) * self.squareHeight(),
                    self.curPiece.shape())


    def OnKeyDown(self, event):
        if not self.isStarted or self.curPiece.shape() == Tetrominoes.NoShape:
            event.Skip()
            return

        keycode = event.GetKeyCode()

        if keycode == ord('P') or keycode == ord('p'):
            self.pause()
            return
        if self.isPaused:
            return
        elif keycode == ord('A') or keycode == ord('a'):
            self.tryMove(self.curPiece, self.curX - 1, self.curY)
        elif keycode == ord('D') or keycode == ord('d'):
            self.tryMove(self.curPiece, self.curX + 1, self.curY)
        #elif keycode == wx.WXK_DOWN:
            #self.tryMove(self.curPiece.rotatedRight(), self.curX, self.curY)
        elif keycode == ord('W') or keycode == ord('w'):
            self.tryMove(self.curPiece.rotatedLeft(), self.curX, self.curY)
        elif keycode == ord('S') or keycode == ord('s'):
            self.oneLineDown()
        elif keycode == wx.WXK_SPACE:
            self.dropDown()
        else:
            event.Skip()

    def OnTimer(self, event):
        if event.GetId() == Board.ID_TIMER:
            if self.isWaitingAfterLine:
                self.isWaitingAfterLine = False
                self.newPiece()
            else:
                self.oneLineDown()
        else:
            event.Skip()

    def dropDown(self):
        newY = self.curY
        while newY > 0:
            if not self.tryMove(self.curPiece, self.curX, newY - 1):
                break
            newY -= 1

        self.pieceDropped()

    def oneLineDown(self):
        if not self.tryMove(self.curPiece, self.curX, self.curY - 1):
            self.pieceDropped()

    def pieceDropped(self):
        for i in range(4):
            x = self.curX + self.curPiece.x(i)
            y = self.curY - self.curPiece.y(i)
            self.setShapeAt(x, y, self.curPiece.shape())

        self.removeFullLines()

        if not self.isWaitingAfterLine:
            self.newPiece()


    def removeFullLines(self):
        numFullLines = 0

        # statusbar = self.GetParent().statusbar

        rowsToRemove = []

        for i in range(Board.BoardHeight):
            n = 0
            for j in range(Board.BoardWidth):
                if not self.shapeAt(j, i) == Tetrominoes.NoShape:
                    n = n + 1

            if n == 12:
                rowsToRemove.append(i)

        rowsToRemove.reverse()
        
        for m in rowsToRemove: 
            for k in range(m, Board.BoardHeight):
                for l in range(Board.BoardWidth):
                        self.setShapeAt(l, k, self.shapeAt(l, k + 1))

            numFullLines = numFullLines + len(rowsToRemove)
            
            
            if numFullLines > 0:
                #if numFullLines == 1:
                    #self.Score += 10
                #else :
                    #self.Score += numFullLines*20
                #self.numLinesRemoved += numFullLines
                # statusbar.SetStatusText(str(self.numLinesRemoved)) 
                self.isWaitingAfterLine = True
                self.curPiece.setShape(Tetrominoes.NoShape)
                self.Refresh()
        
        if len(rowsToRemove) != 0:
            self.numLinesRemoved += len(rowsToRemove)
            if len(rowsToRemove) == 1:
                self.Score += 10
            else:
                self.Score += len(rowsToRemove)*20
            self.GetParent().GetParent().info.Refresh()
            
    
    def newPiece(self):
        # self.curPiece = self.nextPiece (it's wrong!)   # the original one has problem!!
                                                         # self.curPiece will always be the same as self.nextPiece
        self.curPiece.setShape(self.nextPiece.shape())   # this is the proper way!   
        # statusbar = self.GetParent().statusbar
        self.nextPiece.setRandomShape()
        
        self.GetParent().GetParent().ShowNextPiece = self.nextPiece
        # self.GetParent is a SpiltterWindow, and SpiltterWIndow's parent is TetrisInSplitterFrame!
        self.GetParent().GetParent().info.Refresh()
        
        self.curX = Board.BoardWidth / 2 + 1
        self.curY = Board.BoardHeight - 1 + self.curPiece.minY()

        if not self.tryMove(self.curPiece, self.curX, self.curY):
            self.curPiece.setShape(Tetrominoes.NoShape)
            self.timer.Stop()
            self.isStarted = False
            wx.MessageBox(u"Sorry! Game Over!",u"Game Over",wx.OK | wx.ICON_INFORMATION, self)
            self.GetParent().GetParent().Close()   #Once the game is over, the program will quit

    def tryMove(self, newPiece, newX, newY):
        for i in range(4):
            x = newX + newPiece.x(i)
            y = newY - newPiece.y(i)
            if x < 0 or x >= Board.BoardWidth or y < 0 or y >= Board.BoardHeight:
                return False
            if self.shapeAt(x, y) != Tetrominoes.NoShape:
                return False

        self.curPiece = newPiece
        self.curX = newX
        self.curY = newY
        self.Refresh()
        return True


    def drawSquare(self, dc, x, y, shape):
        colors = ['#000000', '#CC6666', '#66CC66', '#6666CC',
                  '#CCCC66', '#CC66CC', '#66CCCC', '#DAAA00']

        light = ['#000000', '#F89FAB', '#79FC79', '#7979FC', 
                 '#FCFC79', '#FC79FC', '#79FCFC', '#FCC600']

        dark = ['#000000', '#803C3B', '#3B803B', '#3B3B80', 
                 '#80803B', '#803B80', '#3B8080', '#806200']

        pen = wx.Pen(light[shape])
        pen.SetCap(wx.CAP_PROJECTING)
        dc.SetPen(pen)

        dc.DrawLine(x, y + self.squareHeight() - 1, x, y)
        dc.DrawLine(x, y, x + self.squareWidth() - 1, y)

        darkpen = wx.Pen(dark[shape])
        darkpen.SetCap(wx.CAP_PROJECTING)
        dc.SetPen(darkpen)

        dc.DrawLine(x + 1, y + self.squareHeight() - 1,
            x + self.squareWidth() - 1, y + self.squareHeight() - 1)
        dc.DrawLine(x + self.squareWidth() - 1, 
        y + self.squareHeight() - 1, x + self.squareWidth() - 1, y + 1)

        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.SetBrush(wx.Brush(colors[shape]))
        dc.DrawRectangle(x + 1, y + 1, self.squareWidth() - 2, 
        self.squareHeight() - 2)




class Tetrominoes(object):
    NoShape = 0
    ZShape = 1
    SShape = 2
    LineShape = 3
    TShape = 4
    SquareShape = 5
    LShape = 6
    MirroredLShape = 7




class Shape(object):
    coordsTable = (
        ((0, 0),     (0, 0),     (0, 0),     (0, 0)),
        ((0, -1),    (0, 0),     (-1, 0),    (-1, 1)),
        ((0, -1),    (0, 0),     (1, 0),     (1, 1)),
        ((0, -1),    (0, 0),     (0, 1),     (0, 2)),
        ((-1, 0),    (0, 0),     (1, 0),     (0, 1)),
        ((0, 0),     (1, 0),     (0, 1),     (1, 1)),
        ((-1, -1),   (0, -1),    (0, 0),     (0, 1)),
        ((1, -1),    (0, -1),    (0, 0),     (0, 1))
    )

    def __init__(self):
        self.coords = [[0,0] for i in range(4)]
        self.pieceShape = Tetrominoes.NoShape
        self.setShape(Tetrominoes.NoShape)

    def shape(self):
        return self.pieceShape

    def setShape(self, shape):
        table = Shape.coordsTable[shape]
        for i in range(4):
            for j in range(2):
                self.coords[i][j] = table[i][j]

        self.pieceShape = shape

    def setRandomShape(self):
        self.setShape(random.randint(1, 7))

    def x(self, index):
        return self.coords[index][0]

    def y(self, index):
        return self.coords[index][1]

    def setX(self, index, x):
        self.coords[index][0] = x

    def setY(self, index, y):
        self.coords[index][1] = y

    def minX(self):
        m = self.coords[0][0]
        for i in range(4):
            m = min(m, self.coords[i][0])
        return m

    def maxX(self):
        m = self.coords[0][0]
        for i in range(4):
            m = max(m, self.coords[i][0])
        return m

    def minY(self):
        m = self.coords[0][1]
        for i in range(4):
            m = min(m, self.coords[i][1])
        return m

    def maxY(self):
        m = self.coords[0][1]
        for i in range(4):
            m = max(m, self.coords[i][1])
        return m

    def rotatedLeft(self):
        if self.pieceShape == Tetrominoes.SquareShape:
            return self

        result = Shape()
        result.pieceShape = self.pieceShape
        for i in range(4):
            result.setX(i, self.y(i))
            result.setY(i, -self.x(i))

        return result

    #def rotatedRight(self):
        #if self.pieceShape == Tetrominoes.SquareShape:
            #return self

        #result = Shape()
        #result.pieceShape = self.pieceShape
        #for i in range(4):
            #result.setX(i, -self.y(i))
            #result.setY(i, self.x(i))

        #return result
if __name__ == '__main__':      
  app = wx.App()        
  TetrisInSplitterFrame(None, -1, 'Tetris')
  app.MainLoop()