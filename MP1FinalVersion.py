import cx_Oracle
from tkinter import *
import datetime
import random
import sys

'''
CMPUT 291 B1 WINTER 2017 Miniproject1
GROUP MEMNER: Donglin Han
GROUP MEMBER: Zhi Li
Group MEMBER: Shan Lu

Description:
	This is a python program, user can use the program to access U of A database and retrieve information from it. This program is about user, user’s tweet, user’s followee’s tweet, user can login and sign up. User can compose, 	reply, retweet a tweet. User can also follow other users, see other user’s detailed  information, and manage favourate user list.

HOW TO RUN: in terminal run: python3 MP1FinalVersion.py
            then user need to enter his/her csid and passward 
'''


class LoginScreen:

    def __init__(self, master):
        self.master = master
        self.master.geometry('200x100')
        master.title("Login Screen")
        self.login_button = Button(master, text = "Log In", command = self.login_buttonCallback)
        self.login_button.place(x= 20, y = 30)
        self.signup_button = Button(master, text = "Sign Up", command = self.signup_buttonCallback)
        self.signup_button.place(x= 100, y = 30)
        self.exit_button = Button(master, text = "Exit", command = self.exit_buttonCallback)
        self.exit_button.pack(side = BOTTOM)

    def login_buttonCallback(self):
        # Go to Log In window
        loginroot = Toplevel(self.master)
        login_window = Login(loginroot)
        
    def signup_buttonCallback(self):
        # Go to Sign Up window
        signuproot = Toplevel(self.master)
        signup_window = Signup(signuproot)
        

    def exit_buttonCallback(self):
        # Exit the program
        self.master.destroy()

class Login:

    def __init__(self, master):
        self.master = master
        self.master.geometry('300x200')
        master.title("Login")
        # focus on the Login window
        self.master.focus_set()
        # Prohibits any other window to accept events
        self.master.grab_set()
        self.usrnlabel = Label(master, text = "User id: ")
        self.usrnlabel.pack()
        self.usrnentry = Entry(master)
        self.usrnentry.pack()
        self.usrpswlabel = Label(master, text = "Password: ")
        self.usrpswlabel.pack()
        self.usrpswentry = Entry(master, show = '*')
        self.usrpswentry.pack()
        self.invalid_label_frame = LabelFrame(self.master)
        self.invalid_label_frame.pack()
        self.clogin = Button(master, text = "Log in", command = self.cloginCallback)
        self.clogin.pack(side = BOTTOM)

    def cloginCallback(self):
        # Get user entered username and password
        enteredusrn = self.usrnentry.get()
        enteredpsw = self.usrpswentry.get()

        # Check valid user id and password
        usrpsw_curs = con.cursor()
        usrpsw_curs.execute("SELECT usr, pwd FROM users")

        valid_usr = float("inf")
        for row in usrpsw_curs:
            print(row[0], row[1].rstrip())
            if str(row[0]) == enteredusrn and row[1].rstrip() == enteredpsw:
                valid_usr = row[0]
                break
        usrpsw_curs.close()

        # If get valid username and psw, open main page
        if valid_usr != float("inf"):
            mainpageroot = Toplevel(self.master.master) # parent is root
            mainpage = mainPage(mainpageroot, valid_usr)
            # After login, close the Login window
            self.master.destroy()
        else:
            # Show invalid username or psw
            self.invalid_label = Label(self.invalid_label_frame, text = "Invalid username or password", fg = "#ff0000", relief = RAISED)
            self.invalid_label.grid(row = 0)
            # clear two entries
            self.usrnentry.delete(0, 'end')
            self.usrpswentry.delete(0, 'end')
class Signup:

    def __init__(self, master):
        self.master = master
        self.master.geometry('500x400')
        master.title("Signup")
        #focus on the login window
        self.master.focus_set()
        #prohibits any other window to accept events
        self.master.grab_set()
        self.usrid = None
       
        self.usrnlabel = Label(master, text = "Name: ")
        self.usrnlabel.pack()
        self.usrnentry = Entry(master)
        self.usrnentry.pack()
        
        self.usrmaillabel = Label(master, text = "Email:")
        self.usrmaillabel.pack()
        self.usrmailentry = Entry(master)
        self.usrmailentry.pack()  
        
        self.usrcitylabel = Label(master, text = "City: ")
        self.usrcitylabel.pack()
        self.usrcityentry = Entry(master)
        self.usrcityentry.pack()  
       
        self.usrtimelabel = Label(master, text = "Timezone: ")
        self.usrtimelabel.pack()
        self.usrtimeentry = Entry(master)
        self.usrtimeentry.pack() 
        self.invalid_label_frame = LabelFrame(self.master)
        self.invalid_label_frame.pack()        
              
        
        self.usrpswlabel = Label(master, text = "Password: ")
        self.usrpswlabel.pack()
        self.usrpswentry = Entry(master, show = '*')
        self.usrpswentry.pack()
        self.csignup = Button(master, text = "Sign up", command = self.csignupCallback)
        self.csignup.pack()

    def csignupCallback(self):
        # Check valid username and password
        # if invalid, show invalid info
        # if valid, give unique userid
        # Get user entered username and password
        usrn = self.usrnentry.get()
        usrmail = self.usrmailentry.get()
        usrcity = self.usrcityentry.get()
        usrtime = self.usrtimeentry.get()
        usrpsw = self.usrpswentry.get()
        if len(usrpsw)>4:
            self.invalid_label = Label(self.invalid_label_frame, text = "Invalid user info", fg = "#ff0000", relief = RAISED)
            self.invalid_label.grid(row = 0)
            # clear  entries
            self.usrnentry.delete(0, 'end')
            self.usrmailentry.delete(0,'end')
            self.usrcityentry.delete(0,'end')
            self.usrtimeentry.delete(0,'end')
            self.usrpswentry.delete(0, 'end')
        else:
            print(usrn)
            print(usrmail)
            print(usrcity)
            print(usrtime)
            print(usrpsw)
                    
            #This method creates a unique usr ID when a signup screen shows up
            # Condition is true if a usr ID already exists in table.
            exits = True
            Allusrid = []
            usrid_curs = con.cursor()
            usrid_curs.execute        
            while exits == True:
                usrid_curs.execute('select usr from users')
                raw= usrid_curs.fetchall()
                for usr in raw:
                    Allusrid.append(usr[0])
                    # Randomize usr ID
                    self.usrid = random.randrange(0,99999)
                    # If usr ID already exists in table
                    if self.usrid in Allusrid:
                        exits = True
                    else:
                        exits = False     
                            
            print(self.usrid)
            try: 
                users_curs = con.cursor()
                users_curs.execute("INSERT INTO users VALUES (:1,:2,:3,:4,:5,:6)", (self.usrid, usrpsw,usrn,usrmail,usrcity,usrtime))
                con.commit() 
                users_curs.execute("Select * from users")
                for row in users_curs:
                    print(row)            
                users_curs.close()       
                self.master.destroy()
                # After sign up , goto main page
                mainpageroot = Toplevel(self.master.master) # parent is root
                mainpage = mainPage(mainpageroot, self.usrid)            
                
            except cx_Oracle.DatabaseError as exc:
                error, = exc.args
                print(sys.stderr, "Oracle code:", error.code)
                print(sys.stderr, "Oracle message:", error.message)
                self.invalid_label = Label(self.invalid_label_frame, text = "Invalid user info", fg = "#ff0000", relief = RAISED)
                self.invalid_label.grid(row = 0)
                # clear  entries
                self.usrnentry.delete(0, 'end')
                self.usrmailentry.delete(0,'end')
                self.usrcityentry.delete(0,'end')
                self.usrtimeentry.delete(0,'end')
                self.usrpswentry.delete(0, 'end')                
            ## After sign up , goto main page
            #mainpageroot = Toplevel(self.master.master) # parent is root
            #mainpage = mainPage(mainpageroot, self.usrid)            
            
        
        
      
        
             
# Contain manage lists button
class mainPage:
    def __init__(self, master, usr):
        self.master = master
        master.title("Main Page")
        # user's usr
        self.usr = usr
        stw_curs = con.cursor()
        stw_curs.execute(" select t.text from tweets t where t.writer=2")
        for row in stw_curs:
            print(row[0])        
        stw_curs.close()
        self.index = 0
        self.lens = 0
        # A listbox frame, and listbox pointer
        self.itembigframe, self.itemslist = FiveItemListCreator(self.master)
        self.itemslist.config(width = 100)
        self.useridlabel = Label(self.master, text="usrid: "+str(self.usr))
        self.useridlabel.pack()

        # The selecttw button allows user to see more info about the selected tweets
        self.selecttwbutton = Button(self.itembigframe, text = 'Select Tweet', command = self.selecttwbuttonCallback)
        self.selecttwbutton.pack(side = RIGHT)

        # A list containing the tid of tweets in the tweetslist box
        self.tidlist = []

        self.querytweets()

        # PreviousFiveButton and NextFiveButton allow user to see five more tweets if available
        # Previous, Next Buttons frame
        self.prevnextbuttonframe = Frame(self.master)
        self.prevnextbuttonframe.pack()
        self.testbutton1 = Button(self.prevnextbuttonframe, text = "previous 5",command=self.previousfive_buttonCallback)
        self.testbutton1.pack(side = LEFT)
        self.testbutton2 = Button(self.prevnextbuttonframe, text = "next 5",command=self.nextfive_buttonCallback)
        self.testbutton2.pack(side = RIGHT)
        
        # input frame for users to search both tweets and users
        self.searchlabel = Label(master, text = "Search:")
        self.searchlabel.pack()
        self.searchentry = Entry(master)
        self.searchentry.pack()
        #serach for tweets button frame and search for users button frame
        self.searchtwusbuttonframe=Frame(self.master)
        self.searchtwusbuttonframe.pack()
        self.testbutton3=Button(self.searchtwusbuttonframe, text="search for tweets",command = self.searchtw)
        self.testbutton3.pack(side=LEFT)
        self.testbutton4=Button(self.searchtwusbuttonframe,text="search for users",command = self.searchus)
        self.testbutton4.pack(side=RIGHT)
        #input frame for users to compose a tweet
        self.ctweetlabel=Label(master,text="Compose tweet:")
        self.ctweetlabel.pack()
        self.compostcontent=Entry(master)
        self.compostcontent.pack()
        #ctweet button
        self.ctweetbuttonframe=Frame(self.master)
        self.ctweetbuttonframe.pack()
        #self.compostcontent = Entry(self.ctweetbuttonframe)
        #self.compostcontent.pack()
        self.testbutton5=Button(self.ctweetbuttonframe,text="compose",command = self.compose)
        self.testbutton5.pack(side=BOTTOM)
        #list of followers button to see more info of the followers
        self.listflwerbuttonframe=Frame(self.master)
        self.listflwerbuttonframe.pack()
        self.testbutton6=Button(self.listflwerbuttonframe, text="List of followers",command=self.listflwer_buttonCallback)
        self.testbutton6.pack(side=BOTTOM)
        # Manage user's lists
        self.managelist_button = Button(self.master, text = "Manage List", command = self.managelist_buttonCallback)
        self.managelist_button.pack()
        #LOG OUT BUTTON
        self.logoutbuttonframe=Frame(self.master)
        self.logoutbuttonframe.pack()
        self.testbutton7=Button(self.logoutbuttonframe, text="Log out",command=self.logout)
        self.testbutton7.pack(side = BOTTOM)
    #going to list of followers table
    def listflwer_buttonCallback(self):
        # Open a window for List of followers
        listflwerroot = Toplevel(self.master)
        # Pass the current user name to the class
        listflwer = ListOfFollowers(listflwerroot, self.usr)
            
    def logout(self):
        self.master.destroy()
        

     
    
    def nextfive_buttonCallback(self):
        i = self.lens//5
        i+=1
        i = i*5
        self.index+=5
        print('i is '+str(i))
        print('index is '+str(self.index))
        if self.index<i:
           self.itemslist.delete(0,4)
           tw_curs = con.cursor()
           tw_curs.execute("""
                        SELECT t.tid, t.writer, t.tdate, t.text, t.replyto
                        FROM tweets t, (SELECT retweets.tid FROM retweets, follows WHERE retweets.usr = follows.flwee AND follows.flwer = :1
                                        UNION ALL
                                        SELECT tweets.tid FROM tweets, follows WHERE tweets.writer = follows.flwee AND follows.flwer = :2) a
                        WHERE t.tid = a.tid
                        ORDER BY t.tdate DESC""", (self.usr, self.usr))
           a=0
           for row in tw_curs:
               if a>=self.index and a<self.index+5:
                   #self.tidlist.insert(a-5+self.index,row[0])
                   self.itemslist.insert(a-5+self.index, "tid: "+ str(row[0]) + " writer: " + str(row[1]) + " tdate: " + str(row[2]) + " text: " + row[3].rstrip() + " replyto: " + str(row[4]))
               a+=1
        else:
            self.index-=5
    def previousfive_buttonCallback(self):
        if self.index!=0:
           self.index-=5
           self.itemslist.delete(0,4)
           tw_curs = con.cursor()
           tw_curs.execute("""
                        SELECT t.tid, t.writer, t.tdate, t.text, t.replyto
                        FROM tweets t, (SELECT retweets.tid FROM retweets, follows WHERE retweets.usr = follows.flwee AND follows.flwer = :1
                                        UNION ALL
                                        SELECT tweets.tid FROM tweets, follows WHERE tweets.writer = follows.flwee AND follows.flwer = :2) a
                        WHERE t.tid = a.tid
                        ORDER BY t.tdate DESC""", (self.usr, self.usr))

           i=0
           for row in tw_curs:
               if i<self.index+5 and i>=self.index:
                   #self.tidlist.insert(i+self.index,row[0])
                   self.itemslist.insert(i+self.index, "tid: "+ str(row[0]) + " writer: " + str(row[1]) + " tdate: " + str(row[2]) + " text: " + row[3].rstrip() + " replyto: " + str(row[4]))
               i+=1
           tw_curs.close()
    def searchus(self): 
        # Open a window for search users
        searchusersroot = Toplevel(self.master)
        # Pass the current list name to the class
        searchusers = SearchUsersW(searchusersroot, self.usr)
     
    def searchtw(self):
        lists = []
        lists2 = []
        items = []
        times = []
        md = []
        realtimes = []
        realitems = []
        a = self.searchentry.get().rstrip()
        strList = a.split()
        datelist = []
        print(strList)
        for strings in strList:
            if strings[0] == '#':
                mtw_curs = con.cursor()
                mtw_curs.execute("SELECT mentions.tid, t.text, extract(year from t.tdate),extract (month from t.tdate),extract(day from t.tdate), t.tdate FROM mentions, tweets t WHERE mentions.term like '%"+strings[1:]+"%' AND t.tid = mentions.tid")
                for row in mtw_curs:
                    lists.append(row[0])
                    datelist.append(row[5])
                    items.append(row[1])
                    time = row[2]*365+row[3]*30+row[4]
                    times.append(time)
                    md.append(time)
                    #    print(time)
                    #  print(row[1])
                                                        
                mtw_curs.close()
                #lens = len(times)
                #for n in range(0,lens):
                    #mins= n
                                
                    #for a in range(n+1,lens):
                        #if times[mins]>times[a]:
                            #mins = a
                            #tem = times[n]
                            #times[n] = times[mins]
                            #times[mins] = tem
                            #indexs = md.index(times[n])
                            ## print(times[indexs])
                            ##  print(items[indexs])
                            #realitems.append(items[indexs])            

            else:
                stw_curs = con.cursor()
                stw_curs.execute(" select t.tid,t.text,extract(year from t.tdate),extract (month from t.tdate),extract(day from t.tdate), t.tdate from tweets t where t.text like '%"+strings+"%'")
                for row in stw_curs:
                    #.....
                    lists.append(row[0])
                    datelist.append(row[5])
                    items.append(row[1])
                                     
                    time = row[2]*365+row[3]*30+row[4]
                    times.append(time)
                    md.append(time)
                    #    print(time)
                    #  print(row[1])
                stw_curs.close()
        
        #Save tid as dict key and tdate as dict value
        twd_dict = dict()
        for i in range(len(lists)):
            twd_dict[lists[i]] = datelist[i]
        
        # Sort the dict by date value
        import operator
        sortedtid = sorted(twd_dict.items(), key = operator.itemgetter(1), reverse = True)
        
        print("Sorted tid list")
        tidlistss = []
        for i in sortedtid:
            print(i[0])
            tidlistss.append(i[0])
        
        tww_curs = con.cursor()
        for i in sortedtid:
            tww_curs.execute("SELECT t.tid, t.text, t.tdate from tweets t WHERE t.tid = :ttid", {"ttid": i[0]})
            for row in tww_curs:
                realitems.append("tid: " + str(row[0]) + " text: " + row[1].rstrip() + " tdate: " + str(row[2]))
                
        tww_curs.close()
        
        for i in realitems:
            print(i)
        
                     
        #print("tid:")
        #for i in lists:
            #print(i)
            
        
        #lens = len(times)
        #for n in range(0,lens):
            #mins= n
            
            #for a in range(n+1,lens):
                #if times[mins]>times[a]:
                    #mins = a   
                    #tem = times[n]
                    #times[n] = times[mins]
                    #times[mins] = tem
                    #indexs = md.index(times[n])
                    ## print(times[indexs])
                    ##  print(items[indexs])
                    #realitems.append(items[indexs])       
                
        #print("realtiems")
        #for i in realitems:
            #print(i)
            #stw_curs = con.cursor()
            #stw_curs.execute(" select t.tid,t.text,extract(year from t.tdate),extract (month from t.tdate),extract(day from t.tdate) from tweets t where t.text like '%"+strings+"%'")
            #for row in stw_curs:
                ##.....
                #lists.append(row[0])
                #if strings[0] == '#':
                   #lists2.append(row[0])
                #items.append(row[1])
                #time = row[2]*365+row[3]*30+row[4]
                #print(time)
                #times.append(time)
                #md.append(time)
                #print(row[1])
            #stw_curs.close()
            #if strings[0] == '#' and len(lists2)==0:
                 #stw_curs = con.cursor()
                 #stw_curs.execute(" select t.tid,t.text,extract(year from t.tdate),extract (month from t.tdate),extract(day from t.tdate) from tweets t where t.text like '%"+strings[1:]+"%'")
                 #for row in stw_curs:
                 ##.....
                     #lists.append(row[0])
                     #items.append(row[1])
                     
                     #time = row[2]*365+row[3]*30+row[4]
                     #times.append(time)
                     #md.append(time)
                 ##    print(time)
                   ##  print(row[1])
                 #stw_curs.close()
            #lens = len(times)
            #for n in range(0,lens):
                #mins= n
                
                #for a in range(n+1,lens):
                    #if times[mins]>times[a]:
                        #mins = a
                #tem = times[n]
                #times[n] = times[mins]
                #times[mins] = tem
                #indexs = md.index(times[n])
               ## print(times[indexs])
              ##  print(items[indexs])
                #realitems.append(items[indexs])
            ##for n in range(0,lens):
                ##oldindex = times.index(realtimes[n])
                ##realitems.append(items[oldindex])
      
      
        searchtwroot =Toplevel(self.master)
        searchtweets=SearchTw(searchtwroot,self.usr,realitems, tidlistss, lists)
    def compose(self):
        a = ComposeButton(self.master,0, self.compostcontent, 111, self.usr)
        intext = self.compostcontent.get().rstrip()
        print(intext)
        newtid = a.tidCreator()
        twdate = datetime.date.today()
        composereply_curs = con.cursor()
        composereply_curs.execute("INSERT INTO tweets VALUES (:1, :2, :3, :4,:5)", (newtid, self.usr, twdate, intext,None))

                    # Process the hashtags in the tweet
        a.processhashtags(newtid)

        con.commit()
        composereply_curs.close()

    def querytweets(self):
        # Query all tweets or retweets from users who are being followed into the listbox, ordered based on date from latest to oldest
        tw_curs = con.cursor()
        tw_curs.execute("""
                        SELECT t.tid, t.writer, t.tdate, t.text, t.replyto
                        FROM tweets t, (SELECT retweets.tid FROM retweets, follows WHERE retweets.usr = follows.flwee AND follows.flwer = :1
                                        UNION ALL
                                        SELECT tweets.tid FROM tweets, follows WHERE tweets.writer = follows.flwee AND follows.flwer = :2) a
                        WHERE t.tid = a.tid
                        ORDER BY t.tdate DESC""", (self.usr, self.usr))
        a = 0
        for row in tw_curs:
            print(row[0], row[1], row[2], row[3].rstrip(), row[4])
            self.tidlist.append(row[0])
            if a<5:
               self.itemslist.insert(END, "tid: " + str(row[0]) + " writer: " + str(row[1]) + " tdate: " + str(row[2]) + " text: " + row[3].rstrip() + " replyto: " + str(row[4]))
            a+=1
            self.lens+=1
        tw_curs.close()
    
    def selecttwbuttonCallback(self):
        print("self.index")
        print(self.index)        
        # Open the window to see more info about the selected tweet
        selectedtwindex = self.itemslist.curselection()
        if len(selectedtwindex) != 0:
            # Tweet text and tid of the selected tweet
            twtid = self.tidlist[selectedtwindex[0] + self.index]
            text_curs = con.cursor()
            text_curs.execute("SELECT tweets.text FROM tweets WHERE tweets.tid = :sltwtid", {"sltwtid": twtid})
            for row in text_curs:
                twtext = row[0].rstrip()
                break
            text_curs.close()
            # Test selected tweet
            print(twtid, twtext)
            # Open the tweet info window (allow user to see the number of retweets, and # replies of the selected tweet)
            # User can also compose a relpy or retweet the selected tweet
            tweetinforoot = Toplevel(self.master)
            tweetinfo = Tweetinfo(tweetinforoot, twtext, twtid, self.usr)


    def managelist_buttonCallback(self):
        # Go to list page (a listing of all lists)
        listsroot = Toplevel(self.master)
        lists = Lists(listsroot, self.usr)

def FiveItemListCreator(master):
    # Big frame contain item select button and item listbox
    itembigframe = Frame(master)
    itembigframe.pack(side = TOP)
    # The frame to show items
    itemframe = Frame(itembigframe)
    itemframe.pack(side = LEFT)
    # Allow user to scroll the listbox horizontally, in case the item length exceed the listbox's width
    itemscrollbar = Scrollbar(itemframe, orient = HORIZONTAL)
    itemscrollbar.pack(side = BOTTOM, fill = X)
    # the listbox containing user's items (tweets or searched users)
    itemslist = Listbox(itemframe, height = 5, xscrollcommand = itemscrollbar.set, selectmode = SINGLE)
    itemslist.pack(side = TOP, fill = BOTH, expand = 1)
    itemscrollbar.config(command = itemslist.xview)

    return itembigframe, itemslist

class SearchTw:
    def __init__(self, master, usr,items, tidlistss, twids):
        self.master = master
        self.items = items
        self.lists = twids
        master.title("Search Tweets result")
        # user's usr
        self.usr = usr
        self.index = 0
        self.lens = 0
        # A listbox frame, and listbox pointer
        self.itembigframe, self.itemslist = FiveItemListCreator(self.master)
        self.itemslist.config(width = 80)
        
        self.tidlist = []
        
        # A list containing the tid of tweets in the tweetslist box
        self.tidlistss = tidlistss
                
        for i in self.tidlistss:
            print(i)        
      
        # The selecttw button allows user to see more info about the selected tweets
        self.selecttwbutton = Button(self.itembigframe, text = 'Select Tweet', command = self.selecttwbuttonCallback)
        self.selecttwbutton.pack(side = RIGHT)
        
        self.querytweets()

        # PreviousFiveButton and NextFiveButton allow user to see five more tweets if available
        # Previous, Next Buttons frame
        self.prevnextbuttonframe = Frame(self.master)
        self.prevnextbuttonframe.pack()
        self.testbutton1 = Button(self.prevnextbuttonframe, text = "previous 5",command=self.previousfive_buttonCallback)
        self.testbutton1.pack(side = LEFT)
        self.testbutton2 = Button(self.prevnextbuttonframe, text = "next 5",command=self.nextfive_buttonCallback)
        self.testbutton2.pack(side = RIGHT)
        
    def selecttwbuttonCallback(self):
        # Open the window to see more info about the selected tweet
        selectedtwindex = self.itemslist.curselection()
        
        print("In selectbutton")
        for i in self.tidlistss:
            print(i)
        print("self.index")
        print(self.index)
            
        if len(selectedtwindex) != 0:
            print(selectedtwindex[0])
            # Tweet text and tid of the selected tweet
            twtid = self.tidlistss[selectedtwindex[0] + self.index]
            text_curs = con.cursor()
            text_curs.execute("SELECT tweets.text FROM tweets WHERE tweets.tid = :sltwtid", {"sltwtid": twtid})
            for row in text_curs:
                twtext = row[0].rstrip()
                break
            text_curs.close()
            # Test selected tweet
            print(twtid, twtext)
            # Open the tweet info window (allow user to see the number of retweets, and # replies of the selected tweet)
            # User can also compose a relpy or retweet the selected tweet
            tweetinforoot = Toplevel(self.master)
            tweetinfo = Tweetinfo(tweetinforoot, twtext, twtid, self.usr)

    def querytweets(self):
        self.lens = len(self.lists)
       # self.tidlist=[]
     #   self.itemslist.delete(0,lens)
        for n in range(0,self.lens):
            self.tidlist.insert(n, self.lists[n])
            if n<=4:
                self.itemslist.insert(n,self.items[n])        
    def nextfive_buttonCallback(self):
        i = self.lens//5
        i+=1
        i = i*5
        self.index+=5
        print('i is '+str(i))
        print('index is '+str(self.index))
        if self.index<i:
           self.itemslist.delete(0,4)
           a=0
           for row in range(0,5):
                   #self.tidlist.insert(a-5+self.index,row[0])
                   if row+self.index < self.lens:
                      self.itemslist.insert(a,self.items[row+self.index])
                      a+=1
        else:
            self.index-=5
    def previousfive_buttonCallback(self):
        if self.index!=0:
           self.index-=5
           self.itemslist.delete(0,4)
    

           i=0
           for row in range(0,5):
                   #self.tidlist.insert(i+self.index,row[0])
                   self.itemslist.insert(i,self.items[row+self.index])
                   i+=1

class Tweetinfo:
    # Show more info about the selected tweet
    def __init__(self, master, twtext, twtid, userid):
        self.master = master
        master.title("Selected Tweet")
        textlabel = Label(self.master, text = "Text: ").pack()
        # selected tweet's text
        self.twtext = Label(self.master, text = twtext, relief=RAISED)
        self.twtext.pack()
        # selected tweet's tid
        self.twtid = twtid
        # user's usr
        self.userid = userid

        # The number of retweets of the selected tweet
        self.numretweetsframe = Frame(self.master)
        self.numretweetsframe.pack()
        numretweetslabel = Label(self.numretweetsframe, text = "Number of retweets: ").pack(side = LEFT)
        self.numretw = IntVar()
        self.numretweets = Message(self.numretweetsframe, textvariable = self.numretw, relief=RAISED)

        # Query the number of retweets of the selected tweet
        numretw_curs = con.cursor()
        numretw_curs.execute("SELECT NVL(COUNT(*), 0) FROM retweets WHERE retweets.tid = :twtid", {"twtid": self.twtid})
        for row in numretw_curs:
            self.numretw.set(row[0])
        self.numretweets.pack(side = RIGHT)
        numretw_curs.close()

        # The number of replies of the selected tweet
        self.numreplyframe = Frame(self.master)
        self.numreplyframe.pack()
        numreplylabel = Label(self.numreplyframe, text = "Number of replies: ").pack(side = LEFT)
        self.numreply = IntVar()
        self.numreplymsg = Message(self.numreplyframe, textvariable = self.numreply, relief=RAISED)

        # Query the number of replies to the selected tweet
        numreply_curs = con.cursor()
        numreply_curs.execute("SELECT NVL(COUNT(*), 0) FROM tweets WHERE tweets.replyto = :twtid", {"twtid": self.twtid})
        for row in numreply_curs:
            self.numreply.set(row[0])
        self.numreplymsg.pack(side = RIGHT)
        numreply_curs.close()

        # Compose a reply to the selected tweet
        self.replytwframe = Frame(self.master)
        self.replytwframe.pack()
        replylabel = Label(self.replytwframe, text = "Reply: ").pack(side = LEFT)
        self.composetw = Entry(self.replytwframe)
        self.composetw.pack(side = RIGHT)
        replyindi = 1
        # Create a compose button used to compose a reply
        self.creplybutton = ComposeButton(self.master,1, self.composetw, replyindi, self.userid, self.numreply, self.twtid)

        # Retweet button, retweet the selected tweet
        self.retweetbu = Button(self.master, text = "Retweet", command = self.retweetbuCallback)
        self.retweetbu.pack()

    def retweetbuCallback(self):
        # Retweet this selected tweet
        try:
            retw_curs = con.cursor()
            retw_curs.execute("INSERT INTO retweets VALUES (:1, :2, :3)", (self.userid, self.twtid, datetime.date.today()))
            con.commit()
            retw_curs.close()

            # Increment the number of retweet field by 1
            self.numretw.set(self.numretw.get() + 1)
        except cx_Oracle.DatabaseError as exc:
            error, = exc.args
            print(sys.stderr, "Oracle code:", error.code)
            print(sys.stderr, "Oracle message:", error.message)

        # Test retweet
        testretw_curs = con.cursor()
        testretw_curs.execute("SELECT * FROM retweets")
        for row in testretw_curs:
            print(row)
        testretw_curs.close()


class ComposeButton:
    # The button used to compose a tweet or reply
    def __init__(self, master,createornot, textentry, replyindicator, userid, numreply = None, replytwtid = None):
        self.master = master
        # The entry text
        self.textentry = textentry

        # The reply indicator indicating whether a text in the entry is a reply (1) or a tweet(0)
        self.replyindicator = replyindicator
        # The user id
        self.userid = userid

        if replytwtid != None:
            # The replyto tw tid
            self.replytwtid = replytwtid

        if numreply != None:
            # The number of reply field
            self.numreply = numreply
        if createornot == 1:
            self.button = Button(self.master, text = "Compose", command = self.composetwreCallback)
            self.button.pack()

    def composetwreCallback(self):
        ''' Function used to compose a tweet or reply, put nonempty string in input entry into database
            tweet can hashtags with # before each hashtag, also store the hashtag info to table mentions, and hashtags if needed.
        '''
        if len(self.textentry.get().rstrip()) > 0:
            # Text is not a empty string, can put into database

            # Create a unique tid for the new tweet
            newtid = self.tidCreator()
            # The tweet date
            twdate = datetime.date.today()

            if self.replyindicator == 1:
                try:
                    # The text in the entry is a reply, put this reply into database, replytwtid is not None
                    composereply_curs = con.cursor()

                    composereply_curs.execute("INSERT INTO tweets VALUES (:1, :2, :3, :4, :5)", (newtid, self.userid, twdate, self.textentry.get().rstrip(), self.replytwtid))

                    # Process the hashtags in the tweet
                    self.processhashtags(newtid)

                    con.commit()
                    composereply_curs.close()

                    # Increment the number of relpy field by 1
                    self.numreply.set(self.numreply.get() + 1)

                    # Clear the text entry
                    self.textentry.delete(0, 'end')
                except cx_Oracle.DatabaseError as exc:
                    error, = exc.args
                    print(sys.stderr, "Oracle code:", error.code)
                    print(sys.stderr, "Oracle message", error.message)

                # Test the new tweets table, check if the database is updated
                test_curs = con.cursor()
                test_curs.execute("SELECT * FROM tweets")
                for row in test_curs:
                    print(row)
                test_curs.close()

            #elif self.replyindicator == 0:
                ## The text in the entry is a tweet, put this tweet into database (replyto field is null)
                #try:
                    #composetw_curs = con.cursor()
                    #composetw_curs.execute("INSERT INTO tweets VALUES (:1, :2, :3, :4, null)", (newtid, self.userid, twdate, self.textentry.get().rstrip()))
                    ## Process the hashtags in the tweet
                    #self.processhashtags(newtid)

                    #con.commit()
                    #composetw_curs.close()

                    ## Clear the text entry
                    #self.textentry.delete(0, 'end')

                #except cx_Oracle.DatabaseError as exc:
                    #error, = exc.args
                    #print(sys.stderr, "Oracle code:", error.code)
                    #print(sys.stderr, "Oracle message", error.message)

                ## Test the new tweets table, check if the database is updated
                #test_curs = con.cursor()
                #test_curs.execute("SELECT * FROM tweets")
                #for row in test_curs:
                    #print(row)
                #test_curs.close()
            #else:
                #print("Compose error.")
        else:
            print("Empty string in the text entry")

    def tidCreator(self):
        # Query tid from tweets table in descending order, get the current maximum tid, the newtid is 1 plus the current maximum tid
        tidcreator_curs = con.cursor()
        tidcreator_curs.execute("SELECT tweets.tid FROM tweets ORDER BY tweets.tid DESC")

        for row in tidcreator_curs:
            # Test
            print(row[0])
            newtid = row[0] + 1
            print(newtid)
            break
        tidcreator_curs.close()
        return newtid

    def processhashtags(self, newtid):
        '''
            Get the hashtags of the tweet, put them into hashtags and mentions tabels

            Argus:
                newtid: the tid of the new tweet
        '''

        # Also need to check the text in text entry to see if there are # marks,
        #if yes, update mentions table, if necessary, update hashtags table
        twtextck = self.textentry.get().rstrip()
        # A list containing the hashtags in the tw text
        hashtaglist = []
        # 1 - Indicate need to save the char in the string to hashtagvar list
        newhashtagflag = 0
        for a in twtextck:
            if a == '#':
                # encounter the # symbol, needing to save the following char into hashtagvar (empty list)
                # Check if in the saving char to hashtagvar state
                if newhashtagflag == 1:
                    # if yes, append the previous hashtagvar to the hashtaglist
                    if len(hashtagvar) != 0:
                        hashtaglist.append(hashtagvar)
                #empty string
                hashtagvar = ''
                newhashtagflag = 1
            elif a == ' ':
                if newhashtagflag == 1:
                    # finish saving the hashtagvar, save it to hashtaglist
                    if len(hashtagvar) != 0:
                        hashtaglist.append(hashtagvar)
                    # go to not saving char into hashtagvar state
                    newhashtagflag = 0
            else:
                if newhashtagflag == 1:
                    # save the char to hashtagvar
                    hashtagvar = hashtagvar + a
        if newhashtagflag == 1:
            # Append the last hashtagvar to hashtaglist
            if len(hashtagvar) != 0:
                hashtaglist.append(hashtagvar)

        # hashtag list for this tweet test
        print("hashtag list for this tweet test")
        for hashtag in hashtaglist:
            print(hashtag)
        print("finish hashtag list for this tweet test")

        # Put every hashtags in hashtaglist into table hashtags if the hashtag is not already in table hashtags
        # the set of hashtags already in the hashtags table
        alhashtags = set()
        hasht_curs = con.cursor()
        hasht_curs.execute("SELECT hashtags.term FROM hashtags")
        print("Already hashtags test")
        for row in hasht_curs:
            print(row[0].rstrip())
            # Put the hashtags into alhashtags set
            alhashtags.add(row[0].rstrip())
        hasht_curs.close()
        print("finish Already hashtags test")

        for hashtag in hashtaglist:
            if hashtag not in alhashtags and len(hashtag) <= 10:
                # Put this hash tag into hashtags table
                try:
                    puthashtag_curs = con.cursor()
                    puthashtag_curs.execute("INSERT INTO hashtags VALUES (:hasht)", {"hasht": hashtag})
                    con.commit()
                    puthashtag_curs.close()
                except cx_Oracle.DatabaseError as exc:
                    error, = exc.args
                    print(sys.stderr, "Oracle code:", error.code)
                    print(sys.stderr, "Oracle message", error.message)

        # Test hashtags table
        testhash_curs = con.cursor()
        testhash_curs.execute("SELECT * FROM hashtags")
        for row in testhash_curs:
            print(row)
        testhash_curs.close()

        # Put every hashtags in hashtaglist into table mentions
        for hashtag in hashtaglist:
            try:
                putmen_curs = con.cursor()
                putmen_curs.execute("INSERT INTO mentions VALUES (:1, :2)", (newtid, hashtag))
                con.commit()
                putmen_curs.close()
            except cx_Oracle.DatabaseError as exc:
                error, = exc.args
                print(sys.stderr, "Oracle code:", error.code)
                print(sys.stderr, "Oracle message", error.message)

        # Test mentions table
        testmen_curs = con.cursor()
        testmen_curs.execute("SELECT * FROM mentions")
        for row in testmen_curs:
            print(row)
        testmen_curs.close()

class Lists:
    def __init__(self, master, usr):
        self.master = master
        master.title("Listing of lists")
        # Show user's all lists
        self.usr = usr
        # A listing of lists
        self.listframe = Frame(self.master)
        self.listframe.pack(side = LEFT)
        self.listscrollbar = Scrollbar(self.listframe, orient = VERTICAL)
        self.listscrollbar.pack(side = RIGHT, fill = Y)
        self.listoflists = Listbox(self.listframe, yscrollcommand = self.listscrollbar.set, selectmode = SINGLE)
        self.listoflists.pack(side = LEFT, fill = BOTH, expand = 1)
        self.listscrollbar.config(command = self.listoflists.yview)

        # Query user's lists name
        lists_curs = con.cursor()
        lists_curs.execute("SELECT lname, owner FROM lists WHERE owner = :usr_id", {"usr_id": self.usr})
        for row in lists_curs:
            print(row[0].rstrip(), row[1])
            # Put lists into listbox
            self.listoflists.insert(END, row[0].rstrip())
        lists_curs.close()

        # select button, Allow user to see what's inside that selected list
        self.selectbutton = Button(self.master, text = "Select", command = self.selectbuttonCallback)
        self.selectbutton.pack(side = TOP)
        
        # The button allowing user to see the lists that includes him/her
        self.seelistsonbutton = Button(self.master, text = "Lists include the user", command = self.seelistsonbuttonCallback)
        self.seelistsonbutton.pack()
        

        # Create List button
        self.createlistbutton = Button(self.master, text = "Create List", command = self.createlistbuttonCallback)
        self.createlistbutton.pack(side = BOTTOM)

    def selectbuttonCallback(self):
        # Open a window to show the selected list contents
        selectedlistindex = self.listoflists.curselection()
        if len(selectedlistindex) != 0:
            listname = self.listoflists.get(selectedlistindex[0])
            # Open the selected list (allow user to add or delete members from that list)
            selectedlistroot = Toplevel(self.master)
            selectedlist = selectedList(selectedlistroot, self.usr, listname)
            
        
    def seelistsonbuttonCallback(self):
        # Open a window showing the lists contain the user
        listsonroot = Toplevel(self.master)
        listson = Listson(listsonroot, self.usr)    

    def createlistbuttonCallback(self):
        # Open a window that allows user to create a new list
        createlistroot = Toplevel(self.master)
        creatlist = Createlist(createlistroot, self.usr, self.listoflists)
        
class Listson:
    def __init__(self, master, usr):
        # The list of lists' name containing the user
        self.master = master
        master.title("Lists include the user")
        self.usr = usr
        self.listsonbox = Listbox(self.master)
        self.listsonbox.pack()

        # Query the listname that includes the user
        includes_curs = con.cursor()
        includes_curs.execute("SELECT includes.lname FROM includes WHERE includes.member = :userid", {"userid": self.usr})
        for row in includes_curs:
            self.listsonbox.insert(END, row[0].rstrip())
        includes_curs.close()

class selectedList:
    def __init__(self, master,  usr, listname):
        self.master = master
        master.title(listname)
        self.listname = "{:<12}".format(listname)
        self.listnameframe = Frame(self.master)
        self.listnameframe.pack(side = TOP)
        namelabel = Label(self.listnameframe, text = "List Name: ")
        namelabel.pack(side = LEFT)
        listnlabel = Label(self.listnameframe, text = self.listname)
        listnlabel.pack(side = LEFT)
        
        #current user
        self.usr=usr
        
        # Create a listbox containing the members in the list
        self.memberlistframe = Frame(self.master)
        self.memberlistframe.pack(side = LEFT)
        self.listscrollbar = Scrollbar(self.memberlistframe, orient = VERTICAL)
        self.listscrollbar.pack(side = RIGHT, fill = Y)
        self.memberlist = Listbox(self.memberlistframe, yscrollcommand = self.listscrollbar.set, selectmode = SINGLE)
        self.memberlist.pack(side = LEFT, fill = BOTH, expand = 1)
        self.listscrollbar.config(command = self.memberlist.yview)

        # Query the memebers in the selected list, put into the memberlist (listbox)
        memberlist_curs = con.cursor()
        memberlist_curs.execute("SELECT includes.member, users.name FROM includes, users WHERE includes.lname = :listnm AND includes.member = users.usr", {"listnm":self.listname})
        for row in memberlist_curs:
            # put the member in the selected list into the memberlist listbox
            self.memberlist.insert(END, str(row[0]) + ' ' + row[1].rstrip())
        memberlist_curs.close()

        self.adddeleteBframe = Frame(self.master)
        self.adddeleteBframe.pack()
        # Button to add new member to the list
        self.addmember_button = Button(self.adddeleteBframe, text = "Add Member", command = self.addmember_buttonCallback)
        self.addmember_button.pack(side = TOP)
        # Button to delete member from the list
        self.deletemember_button = Button(self.adddeleteBframe, text = "Delete Member", command = self.deletemember_buttonCallback)
        self.deletemember_button.pack(side = BOTTOM)

    def addmember_buttonCallback(self):
        # Open a window for search users
        searchusersroot = Toplevel(self.master)
        # Pass the current list name to the class
        searchusers = SearchUsersW(searchusersroot, self.usr, self.listname)
            
    def deletemember_buttonCallback(self):
            # Delete the selected member from the list (In both database and memberlist box)
            selectedmemberindex = self.memberlist.curselection()
            if len(selectedmemberindex) != 0:
                selectedmemberusr = int(self.memberlist.get(selectedmemberindex[0]).split()[0])
                try:
                    # Delete the selected member from the database
                    deletemem_curs = con.cursor()
                    deletemem_curs.execute("SELECT lname, member FROM includes")
    
                    for row in deletemem_curs:
                        if row[0].rstrip() == self.listname.rstrip() and row[1] == selectedmemberusr:
                            deletemem_curs.execute("DELETE FROM includes WHERE lname = :1 AND member = :2", (row[0], row[1]))
                            break
                    con.commit()
                    deletemem_curs.close()
                except cx_Oracle.DatabaseError as exc:
                    error, = exc.args
                    print(sys.stderr, "Oracle code:", error.code)
                    print(sys.stderr, "Oracle message:", error.message)
    
                # Test new member in the list
                test_curs = con.cursor()
                test_curs.execute("SELECT lname, member FROM includes")
                for row in test_curs:
                    if row[0].rstrip() == self.listname:
                        print(row[0].rstrip(), row[1])
                test_curs.close()
    
                # Delete the selected member from the listbox
                self.memberlist.delete(selectedmemberindex)

class Createlist:
    def __init__(self, master, usr, listoflists):
        self.master = master
        master.title("Create a list")
        self.usr = usr
        self.listoflistsbox = listoflists

        self.listnameframe = Frame(self.master)
        self.listnameframe.pack(side = TOP)
        listnamelabel = Label(self.listnameframe, text = "List name: ")
        listnamelabel.pack(side = LEFT)

        self.listnameentry = Entry(self.listnameframe)
        self.listnameentry.pack(side = RIGHT)

        self.invalidlabel_frame = LabelFrame(self.master)
        self.invalidlabel_frame.pack()

        # Create button to confirm the new list
        self.createbutton = Button(self.master, text = "Create", command = self.createbuttonCallback)
        self.createbutton.pack(side = BOTTOM)

    def createbuttonCallback(self):
        # The new list's name
        newlistname = self.listnameentry.get()

        # Query all existing lists' name, check if the new list name is unique
        newlname_curs = con.cursor()
        newlname_curs.execute("SELECT lname FROM lists")
        checkflag = 0
        for row in newlname_curs:
            if row[0].rstrip() == newlistname:
                checkflag = 1
                # Show invalid message
                invalid_label = Label(self.invalidlabel_frame, text = "The list name has alreafy existed.", fg = "#ff0000", relief = RAISED)
                invalid_label.grid(row = 0)
                break

        if checkflag == 0 and len(newlistname) != 0:
            try:
                # Insert the new list into database
                newlname_curs.execute("INSERT INTO lists(lname, owner) VALUES (:1, :2)", (newlistname, self.usr))
                con.commit()
            except cx_Oracle.DatabaseError as exc:
                error, = exc.args
                print(sys.stderr, "Oracle code:", error.code)
                print(sys.stderr, "Oracle message:", error.message)

            # Test the new database
            test_curs = con.cursor()
            test_curs.execute("SELECT lname, owner FROM lists")
            for row in test_curs:
                print(row)
            test_curs.close()

            # Insert the new list into the listing of lists listbox
            self.listoflistsbox.insert(END, newlistname)

        newlname_curs.close()
        if checkflag == 0:
            self.master.destroy()

class SearchUsersW:
    # Start the user search process by opening an window to prompt for a key word
    def __init__(self, master, usr, listname = None):
        self.master = master
        master.title('Search Users')
        
        #current user
        self.usr=usr        
        
        self.searchframe = Frame(self.master)
        self.searchframe.pack()
        keywordlabel = Label(self.searchframe, text = 'Keyword: ').pack(side = LEFT)
        self.keywordentry = Entry(self.searchframe)
        self.keywordentry.pack(side = RIGHT)

        # self.listname is None if the search user operation is not called by add member button
        self.listname = listname

        # search users
        self.searchusersbu = SearchUsers(self.master, self.keywordentry, self.usr, self.listname)

class SearchUsers:
    def __init__(self, master, keywordentry, usr, listname = None):
        # Other features in the window and the actual method for search for user
        self.master = master
        # Create search user button, get the sorted list of users whose name or city matches
        self.searchusersbu = Button(self.master, text = 'Search For Users', command = self.searchusers)
        self.searchusersbu.pack()
        self.keywordentry = keywordentry

        # self.listname is None if the search user operation is not called by add member button
        self.listname = listname

        #current user
        self.usr=usr
        
    def searchusers(self):
        # Get text from the entry
        keywordtext = self.keywordentry.get().rstrip()

        # The input is not an empty string
        if len(keywordtext) != 0:
            # The dict, key is the user id of the user whose name matches the keyword, value is the user name length
            namematchdict = dict()
            # The dict, key is the user id of the user whose city matches the keyword (name not match), value is the city name length
            citymatchdict = dict()


            keywords = keywordtext.split()
            for keyword in keywords:
                susers_curs = con.cursor()
                susers_curs.execute('SELECT users.usr, users.name, users.city FROM users')                
                print("keyword is",keyword)
                for row in susers_curs:
                    # Check if the keyword in users.name
                    if keyword in row[1].rstrip():
                        print("keyword is",keyword,row,"in name")
                        namematchdict[row[0]] = len(row[1].rstrip())
                    elif keyword in row[2].rstrip():
                        print("keyword is",keyword,row,"in ciy")                        
                        # if the keyword does not match the user's name, check for city
                        citymatchdict[row[0]] = len(row[2].rstrip())
            susers_curs.close()


            # Sort the matched user id by their name length in ascending order
            import operator
            # Get the list of tuples (userid, user name length), ordered by user's name length ascending
            sorted_namematchdict = sorted(namematchdict.items(), key = operator.itemgetter(1))
            # Get the list of tuples (userid, city name length), ordered by user's city length ascending
            sorted_citymatchdict = sorted(citymatchdict.items(), key = operator.itemgetter(1))

            print('sorted by name length test')
            for i in sorted_namematchdict:
                print(i)

            print('sorted by city length test')
            for i in sorted_citymatchdict:
                print(i)

            # get the sorted list of users whose name or city matches
            orderedmatched_usr = []
            for i in sorted_namematchdict:
                orderedmatched_usr.append(i[0])
            for i in sorted_citymatchdict:
                if i[0] not in orderedmatched_usr:
                    orderedmatched_usr.append(i[0])

            print('sorted mathed user id by name length and city length')
            for i in orderedmatched_usr:
                print(i)

            # Open the window show the list of searched users,(5 prev, 5 next buttons)
            searcheduserlistroot = Toplevel(self.master)
            searcheduserlist = SearchedUsersList(searcheduserlistroot, orderedmatched_usr, self.usr, self.listname)

class SearchedUsersList:
    def __init__(self, master, orderedmatched_usr, usr, listname = None):
        # The window show the list of searched users (user id, user name)
        # Has the select button able to select the user to see more info
        self.master = master
        master.title('Search Users Name List')
        
        #current user
        self.usr=usr

        # A listbox frame, and listbox pointer
        self.itembigframe, self.itemslist = FiveItemListCreator(self.master)

        # Select button able to select user to see more info
        self.selectusrbutton = Button(self.itembigframe, text = 'Select User', command = self.selectusrbuttonCallback)
        self.selectusrbutton.pack(side = RIGHT)

        # PreviousFiveButton and NextFiveButton allow user to see five more tweets if available
        # Previous, Next Buttons frame
        self.prevnextbuttonframe = Frame(self.master)
        self.prevnextbuttonframe.pack()
        self.button1 = Button(self.prevnextbuttonframe, text = "Previous five",command = self.previousButtonCallback)
        self.button1.pack(side = LEFT)
        self.button2 = Button(self.prevnextbuttonframe, text = "Next five",command = self.nextButtonCallBack)
        self.button2.pack(side = RIGHT)        
        
        # the ordered usr list
        self.orderedusr = orderedmatched_usr
        #Size of the searched list
        self.size = len(self.orderedusr)       
        print("Sorted List size is",self.size,"\n")        
        
        # Test searched user id list
        self.testorderedusr = []

        # Put the searched user id and user name into the self.itemslist listbox
        self.index=1
        self.queryUsrName(self.index)

        # self.listname is None if the search user operation is not called by add member button
        self.listname = listname

    def queryUsrName(self,index):
        # Search for user name
        currentCount = 0
        # Fill the list
        usrname_curs = con.cursor()
        for i in self.orderedusr:
            currentCount=currentCount+1
            if currentCount<(index+5):
                if currentCount>=index :
                    usrname_curs.execute('SELECT users.usr, users.name FROM users WHERE users.usr = :userid', {"userid": i})
                    for row in usrname_curs:
                        # Put the user id and name into the itemslist box
                        print(row[0], row[1].rstrip())#test
                        self.testorderedusr.append(row[0])#test
                        self.itemslist.insert(END, row[1].rstrip())
        usrname_curs.close()

        if self.testorderedusr == self.orderedusr:#test
            print('True1')#test
        else:#test
            print('False1')#test


    def selectusrbuttonCallback(self):
        # Call another class when a user is selected to see more info
        selectedusrindex = self.itemslist.curselection()
        print("selected index is",selectedusrindex)
        if len(selectedusrindex) != 0:
            # User's id and name
            usrid = self.orderedusr[selectedusrindex[0]+self.index-1]
            username = self.itemslist.get(selectedusrindex[0])
            
            # Test the selected user
            print("befor userinfo window",usrid, username)

            # Open another window to see more info about the selected user
            userinforoot = Toplevel(self.master)
            userinfo = Userinfo(userinforoot, usrid, self.usr, self.listname)
            
    def previousButtonCallback(self):
        # Create button to allow user to see the previous five items in the listbox
        print("Previous button clicked")
        if self.index - 5 > 0:
            # Clear the list first
            self.itemslist.delete(0, END)
            self.index = self.index -5
            self.queryUsrName(self.index)
        
    def nextButtonCallBack(self):
        # Create button to allow user to see the next five items in the listbox
        print("Next button clicked")
        if self.index + 5 <= self.size :
            self.itemslist.delete(0, END)
            self.index = self.index+5
            self.queryUsrName(self.index)

class Userinfo:
    def __init__(self, master, usrid, usr, listname = None):
        # The user info window, contains name, numbser of being followed, number of followers,
        # number of tweets, first three tweets and option to see more tweets and follow (and 
        # add to list if the class is being called by list user search method.
        self.master = master
        master.title("User Info")
        # The selected user's user id
        self.selectedusr = usrid
        print("selected user id is: ", self.selectedusr)
        #current user
        self.usr=usr        
        print("Current user is",self.usr)
        
        # User name
        self.getName()
        
        # Number of being followeed
        self.getfollowedN();
        
        # Number of followers
        self.getFollowerNumber();
        
        # Number of Tweets        
        self.getTweetsN();
        
        # Tweet List
        self.getTweetList();
        
        # See more tweets        
        self.seeMoreButton = Button(self.master, text = "See More", command = self.seeMoreButtonCallback)
        self.seeMoreButton.pack()        
        
        if(self.selectedusr == self.usr):
            infolabel = Label(self.master, text = "This is yourself")
            infolabel.pack()     
        
        # Follow button
        self.followButton = Button(self.master, text = "Follow", command = self.followButtonCallback)
        self.followButton.pack()
        
        if listname != None:
            # The current list name if the user add this selected user to the list
            self.listname = listname            
            self.addusertolist = Button(self.master, text = 'Add User to the List', command = self.addusertolistCallback)
            self.addusertolist.pack()

    def addusertolistCallback(self):
        # Add the user to the favourite list user is currently on 
        if self.listname != None:
            try:
                # Add the selected user into the list (include table)
                addtolist_curs = con.cursor()
                # Insert the new list into database
                addtolist_curs.execute("INSERT INTO includes(lname, member) VALUES (:1, :2)", (self.listname, self.selectedusr))
                con.commit()
                addtolist_curs.close()
            except cx_Oracle.DatabaseError as exc:
                error, = exc.args
                print(sys.stderr, "Oracle code:", error.code)
                print(sys.stderr, "Oracle message:", error.message)

            # Test the includes table
            testincludes_curs = con.cursor()
            testincludes_curs.execute('SELECT * FROM includes')
            for row in testincludes_curs:
                print(row[0].rstrip(), row[1])
            testincludes_curs.close()


    def getName(self):
        # Query the user name from the user id
        try:
            # find name
            name_curs = con.cursor()
            name_curs.execute("SELECT users.name FROM users WHERE users.usr = :userid", ({"userid": self.selectedusr}))
            
        except cx_Oracle.DatabaseError as exc:
            error, = exc.args
            print(sys.stderr, "Oracle code:", error.code)
            print(sys.stderr, "Oracle message:", error.message)            
        namelabel = Label(self.master, text = "User Name: ")
        namelabel.pack()
        for row in name_curs:
            self.selectedName =row[0].rstrip()
            print("User Name is : ",self.selectedName)       
            nlabel = Label(self.master, text = self.selectedName)
            nlabel.pack()        
        name_curs.close() 
        
    def getfollowedN(self):
        # Count how many being followed by the user
        try:
            # get counts
            fldnumber_curs = con.cursor()
            fldnumber_curs.execute("SELECT COUNT(*) FROM follows WHERE flwer = :userid", ({"userid": self.selectedusr}))
            
        except cx_Oracle.DatabaseError as exc:
            error, = exc.args
            print(sys.stderr, "Oracle code:", error.code)
            print(sys.stderr, "Oracle message:", error.message)            
        flabel = Label(self.master, text = "Number of being followed: ")
        flabel.pack()
        for row in fldnumber_curs:
            self.fldn =row[0]
            print("Number of being followed : ",self.fldn)       
            flabel = Label(self.master, text = self.fldn)
            flabel.pack()        
        fldnumber_curs.close() 
    
    def getFollowerNumber(self):
        # Get how many is following the user
        try:
            # get counts
            fler_curs = con.cursor()
            fler_curs.execute("SELECT COUNT(*) FROM follows WHERE flwee = :userid", ({"userid": self.selectedusr}))
            
        except cx_Oracle.DatabaseError as exc:
            error, = exc.args
            print(sys.stderr, "Oracle code:", error.code)
            print(sys.stderr, "Oracle message:", error.message)            
        flabel = Label(self.master, text = "Number of followers: ")
        flabel.pack()
        for row in fler_curs:
            self.fldn =row[0]
            print("Number of followers : ",self.fldn)       
            flabel = Label(self.master, text = self.fldn)
            flabel.pack()        
        fler_curs.close() 
    
    def getTweetsN(self):
        # Get number of tweets
        try:
            # get counts
            t_curs = con.cursor()
            t_curs.execute("SELECT COUNT(*) FROM tweets WHERE writer = :userid", ({"userid": self.selectedusr}))
            
        except cx_Oracle.DatabaseError as exc:
            error, = exc.args
            print(sys.stderr, "Oracle code:", error.code)
            print(sys.stderr, "Oracle message:", error.message)            
        flabel = Label(self.master, text = "Number of tweets: ")
        flabel.pack()
        for row in t_curs:
            self.fldn =row[0]
            print("Number of tweets : ",self.fldn)       
            flabel = Label(self.master, text = self.fldn)
            flabel.pack()        
        t_curs.close() 
                
    def getTweetList(self):
        # Get First three tweets composed by the user
        tlabel = Label(self.master, text = "First three tweet id and tweet:")
        tlabel.pack()        
        # Query tweets
        tweets_curs = con.cursor()
        tweets_curs.execute("SELECT tid, text FROM tweets WHERE writer = :usr_id order by tdate desc ", {"usr_id": self.selectedusr})
        self.t3index = 0
        for row in tweets_curs:
            if self.t3index < 3:
                self.t3index = self.t3index + 1
                print(row[0], row[1].rstrip())
                # show 3 tweets
                t=str(row[0]) + " " + row[1].rstrip()
                tlabel = Label(self.master, text = t)
                tlabel.pack()            
            else: break
        tweets_curs.close()
        if self.t3index != 3:
            tlabel = Label(self.master, text = "This user has less than three tweet to show.")
            tlabel.pack()                       
    
    def seeMoreButtonCallback(self):
        # Call ListOfTweets class to open an new window to see user's all tweets
        ListOfTweetsRoot = Toplevel(self.master)
        ListOfTweets(ListOfTweetsRoot, self.selectedusr, self.usr)
            
    def followButtonCallback(self):
        # Follow the selected user
        try:
            # Add the selected user into the list (include table)
            addtofollow_curs = con.cursor()
            # Insert the new list into database
            addtofollow_curs.execute("INSERT INTO follows(flwer, flwee,start_date) VALUES (:1, :2, :3)", (self.usr, self.selectedusr,datetime.date.today()))
            con.commit()
            addtofollow_curs.close()
            print(self.selectedusr, "is followed")
        except cx_Oracle.DatabaseError as exc:
            error, = exc.args
            print("User selected is already followed")
            print(sys.stderr, "Oracle code:", error.code)
            print(sys.stderr, "Oracle message:", error.message)
            
        
class ListOfFollowers:
    # A list view of current user's list of followers, able to select and see more info about 
    # the selected user.
    def __init__(self, master, usr):
        self.master = master
        #current user
        self.usr=usr        
        print("Current user is",self.usr)
        master.title("List of Followers")
        
        # A listing of lists
        self.listframe = Frame(self.master)
        self.listframe.pack(side = LEFT)
        self.listscrollbar = Scrollbar(self.listframe, orient = VERTICAL)
        self.listscrollbar.pack(side = RIGHT, fill = Y)
        self.listofflwer = Listbox(self.listframe, yscrollcommand = self.listscrollbar.set, selectmode = SINGLE)
        self.listofflwer.pack(side = LEFT, fill = BOTH, expand = 1)
        self.listscrollbar.config(command = self.listofflwer.yview)

        # Query follwer's name
        lists_curs = con.cursor()
        lists_curs.execute("SELECT u.usr, u.name FROM users u, follows f WHERE flwee = :usr_id AND f.flwer = u.usr", {"usr_id": self.usr})

        for row in lists_curs:
            print(row[0], row[1].rstrip())
            # Put followers into listbox
            self.listofflwer.insert(END, str(row[0]) + " " + row[1].rstrip())

        # select button, Allow user to see specific info of a selected user
        self.selectbutton = Button(self.master, text = "Select", command = self.selectbuttonCallback)
        self.selectbutton.pack(side = TOP)
        lists_curs.close()
        
    def selectbuttonCallback(self):
        # Open a window to show the selected user info
        selecteduserindex = self.listofflwer.curselection()
        print(selecteduserindex)
        if len(selecteduserindex) != 0:
            self.selectedUsrId = self.listofflwer.get(selecteduserindex[0]).partition(' ')[0]
            print(self.selectedUsrId)
            # Open the selected userinfo
            selecteduserroot = Toplevel(self.master)
            selecteduser = Userinfo(selecteduserroot, self.selectedUsrId, self.usr)

        
class ListOfTweets:
    # To show all the tweets composed by the selected user.
    def __init__(self, master, selectedusr, usr):
        self.master = master
        
        #current user
        self.usr=usr        
        print("Current user is",self.usr)
        master.title("List of More Tweets")
        
        self.selectedusr = selectedusr
        print("Selected user is",self.selectedusr)
        
        # A listing of tweets
        self.listframe = Frame(self.master)
        self.listframe.pack(side = LEFT)
        self.listscrollbar = Scrollbar(self.listframe, orient = VERTICAL)
        self.listscrollbar.pack(side = RIGHT, fill = Y)
        self.listoft = Listbox(self.listframe, yscrollcommand = self.listscrollbar.set, selectmode = SINGLE)
        self.listoft.config(width = 100)
        self.listoft.pack(side = LEFT, fill = BOTH, expand = 1)
        self.listscrollbar.config(command = self.listoft.yview)

        # Query tweets
        lists_curs = con.cursor()
        lists_curs.execute("SELECT tid, text FROM tweets WHERE writer = :usr_id", {"usr_id": self.selectedusr})

        for row in lists_curs:
            print(row[0], row[1].rstrip())
            # Put followers into listbox
            self.listoft.insert(END, str(row[0]) + " " + row[1].rstrip())

        # select button, Allow user to see specific info of a tweet
        self.selectbutton = Button(self.master, text = "Select", command = self.selectbuttonCallback)
        self.selectbutton.pack(side = TOP)
        lists_curs.close()
        
    def selectbuttonCallback(self):
        # Open a window to show the selected tweet info
        selecteduserindex = self.listoft.curselection()
        print(selecteduserindex)
        if len(selecteduserindex) != 0:
            self.selectedtId = self.listoft.get(selecteduserindex[0]).partition(' ')[0]
            t = self.listoft.get(selecteduserindex[0])
            self.ttext = t[t.find(" ")+1:]
            print("Slectedttext: ", self.ttext)
            print("selectedtID: ", self.selectedtId)
            # Open the selected tweet
            selectedtweetroot = Toplevel(self.master)
            selectedtweet = Tweetinfo(selectedtweetroot, self.ttext, self.selectedtId, self.usr)

if __name__ == "__main__":

    
    import getpass
    user = input('Enter user name: ')
    pswd = getpass.getpass('Enter password:')
    con = cx_Oracle.connect(user, pswd, "gwynne.cs.ualberta.ca:1521/CRS")
    
    root = Tk()
    # Main login in screen (Containing one Log In button and one Sign Up button)
    mainLoginScreen = LoginScreen(root)
    root.mainloop()
