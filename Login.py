
import PySimpleGUI as sg
import json, os, sys, smtplib, ssl, random





BORDER_COLOR = '#B2BEB5'
DARK_HEADER_COLOR = '#FFFFFF'
BACKGROUND= '#FFFFFF'


# ----------- Creating All Required Windows -----------------

# ---------------- Front-End-Functions ----------------

# Login Interface
def win_Login():
    try:
        # Interface Layout
        # -------------------------------------------------------------------
        Left_Column = [[sg.Text('Or Are you New User?',font=25), sg.Text(' ' * 10)],
                       [sg.Text('Then',font=25), sg.Button(' Sign Up ',font=25)]]

        Right_Column = [[sg.Text(' ' * 13), sg.Button(' Forget Email? ',font=25)],
                        [sg.Text(' ' * 13), sg.Button(' Forget Password? ',font=25)]]

        layout = [[sg.Text('Email : ',font=2), sg.InputText(key='in1', do_not_clear=False)],
                  [sg.Text('Password : ',font=25), sg.InputText(key='in2', do_not_clear=False, password_char='*')],
                  [sg.Button(' Log In ',font=25)],
                  [sg.Text('_' * 60)],
                  [sg.Column(Left_Column), sg.VSeperator(), sg.Column(Right_Column)]]

        window = sg.Window('Login', layout, margins=(150, 150))
        # -------------------------------------------------------------------

        # Defining Button Connections and Acceptable Data Logic
        # -------------------------------------------------------------------
        event, values = window.Read()
        if (event == ' Log In '):
            email = str(values['in1'])

            Is_space = email.isspace()
            if not email:
                sg.Popup('No Input Data!!')
                window.close()
                win_Login()
            elif Is_space == True:
                sg.popup('Email Cannot contain Spaces!!')
                window.close()
                win_Login()
            elif Is_space == False:
                if email.endswith('@gmail.com') == False:
                    sg.Popup('Invalid Email!!')
                    window.close()
                    win_Login()
                else:
                    with open('datafile.py', 'r') as f:
                        dic = json.load(f)
                    gemail = list(dic.keys())[0]
                    if (email != gemail):
                        sg.Popup('Incorrect Email!!')
                        window.close()
                        win_Login()
                    elif (email == gemail):
                        passwd = str(values['in2'])
                        evalue = dic[email]
                        cr_pass = pass_decoder(evalue)
                        if (passwd.isspace() == True):
                            sg.Popup('Password cannot contain Spaces!!')
                            window.close()
                            win_Login()
                        elif passwd == cr_pass:
                            sg.Popup("Login Succ")
                            window.close()
                            os.system('python DPC.py')
                            
                        elif (passwd != cr_pass):
                            sg.Popup('Incorrect Password!!')
                            window.close()
                            win_Login()
                        else:
                            win_Invalid_Input()
                            window.close()
                            win_Login()
                    else:

                        window.close()
                        win_Login()
            else:
                sg.Popup('Something Went Wrong!!')
                window.close()
                win_Login()
        elif event == sg.WIN_CLOSED:
            window.close()
            i = False
            return i
        elif (event == ' Sign Up '):
            window.close()
            win_UserAvailable()
            win_Login()
        elif (event == ' Forget Email? '):
            window.close()
            sec_ques_check()
        elif (event == ' Forget Password? '):
            window.close()
            code, get_email = verify()
            win_Verify(code, get_email)
        else:
            window.close()
            win_Login()
    except Exception as err:
        sg.Popup(err)
        win_Invalid_Input()
        window.close()
        win_Login()


# Signup Interface
def win_Signup():
    try:
        # Interface Layout
        # -------------------------------------------------------------------
        layout = [[sg.Text('Enter Email : ',font=25), sg.InputText(key='in1', do_not_clear=False)],
                  [sg.Text('Create Password : ',font=25), sg.InputText(key='in2', password_char='*', do_not_clear=False)],
                  [sg.Text('ReEnter Password : ',font=25), sg.InputText(key='in3', password_char='*', do_not_clear=False)],
                  [sg.Button('Back to Login',font=25), sg.Button(' Sign Up ',font=25)]]

        window = sg.Window('Sign Up', layout, margins=(150, 150))
        # -------------------------------------------------------------------

        # Backend Logic
        # -------------------------------------------------------------------
        event, values = window.Read()
        if(event == 'Back to Login'):
            window.close()
            win_Login()
        
        elif (event == ' Sign Up '):
            global email
            email = str(values['in1'])
            email = email.lower()
            passwd = str(values['in2'])
            rpasswd = str(values['in3'])
            if not passwd or not email:
                sg.Popup('Please Fill up all Entries!!')
                window.close()
                win_Signup()
            elif (email.isspace() == True) or (passwd.isspace() == True):
                sg.Popup('Space is not valid!!')
                window.close()
                win_Signup()
            elif email.endswith('@gmail.com') == False:
                sg.Popup('Invalid Email!!')
                window.close()
                win_Signup()
            elif (len(passwd) < 8):
                sg.Popup('Password Length must be of 8 charcters!!')
                window.close()
                win_Signup()
            elif (passwd == rpasswd):
                global passd
                passd = pass_encoder(passwd)
                window.close()
                last_step(True, email, passd)
            else:
                win_Error()
                window.close()
                win_Signup()
        elif event == sg.WIN_CLOSED:
            window.close()
            i = False
            return i
        else:
            window.close()
            win_Signup()
    except Exception as err:
        window.close()


# Verify Window Interface
def win_Verify(code, get_email):
    try:
        # Interface Layout
        # -------------------------------------------------------------------
        layout = [[sg.Text('OTP sent to your registered Email ID...')],
                  [sg.Text('Enter OTP : '), sg.InputText(key='in1')],
                  [sg.Button(' Verify ')],
                  [sg.Text("Didn't recieved OTP?"), sg.Button(' Resend OTP ')]]

        window = sg.Window('Verifying', layout, margins=(250, 150))
        # -------------------------------------------------------------------

        # Backend Logic
        # -------------------------------------------------------------------
        event, values = window.Read()
        if (event == ' Verify '):
            in_otp = str(values['in1'])
            if (in_otp.isspace() == True):
                sg.Popup('Otp cannot contain space!!')
                window.close()
                win_Verify(code, get_email)
            else:
                in_otp = int(values['in1'])
                pass
            if not in_otp:
                sg.Popup('Please Enter OTP!!')
                window.close()
                win_Verify(code, get_email)
            elif (in_otp == code):
                window.close()
                win_resetpass()
            else:
                sg.Popup('Incorrect OTP!!')
                window.close()
                win_Login()
        elif (event == ' Resend OTP '):
            send_otp(code, get_email)
            window.close()
            win_Verify(code, get_email)
        elif (event == sg.WIN_CLOSED):
            window.close()
        else:
            window.close()
            win_Verify()
    except Exception as err:
        sg.Popup(err)
        win_Verify()


# Security Setup Interface
def sec_ques_setup():
    # List of Security Questions
    # -----------------------------------------------------------------------
    q1 = 'What was the name of your Elementry/Primary School?'
    q2 = 'What is your Favorite place in India?'
    q3 = 'In What City were you born?'
    q4 = 'What is the name of your First Grade Teacher?'
    q5 = 'What is the first name of your Best Friend?'

    List = [q1, q2, q3, q4, q5]

    # Interface Layout
    # -----------------------------------------------------------------------
    layout = [[sg.Text('Just One More Step!!\n')],
              [sg.Text('Please choose any Security Question and write it Answer..\n')],
              [sg.Text('First Question : '), sg.OptionMenu(List, key='sq1')],
              [sg.Text('Enter Answer : '), sg.InputText(key='in1')],
              [sg.Text('Second Question : '), sg.OptionMenu(List, key='sq2')],
              [sg.Text('Enter Answer : '), sg.InputText(key='in2')],
              [sg.Text('Third Question : '), sg.OptionMenu(List, key='sq3')],
              [sg.Text('Enter Answer : '), sg.InputText(key='in3')],
              [sg.Button(' Submit ')]]

    window = sg.Window('Security Setup', layout)
    # -----------------------------------------------------------------------

    # Backend Logic
    # -----------------------------------------------------------------------
    event, values = window.Read()
    if (event == ' Submit '):
        if (values['sq1'] != values['sq2']):  # you don't select same questions
            if (values['sq2'] != values['sq3']):
                if (values['sq1'] != values['sq3']):
                    if (not values['in1']) or (not values['in2']) or (not values['in3']):
                        sg.Popup('Answer Field cannot be Empty!!')
                        window.close()
                        sec_ques_setup()
                    elif ((values['in1'].isspace()) == False):
                        if ((values['in2'].isspace()) == False):
                            if ((values['in3'].isspace()) == False):
                                sq = {values['sq1']: values['in1'], values['sq2']: values['in2'],
                                      values['sq3']: values['in3']}
                                window.close()
                                return sq
                            else:
                                sg.Popup('Answer Field cannot be Empty!!')
                                window.close()
                                sec_ques_setup()
                        else:
                            sg.Popup('Answer Field cannot be Empty!!')
                            window.close()
                            sec_ques_setup()
                    else:
                        sg.Popup('Answer Field cannot be Empty!!')
                        window.close()
                        sec_ques_setup()
                else:
                    sec_Ques_Error()
                    window.close()
                    sec_ques_setup()
            else:
                sec_Ques_Error()
                window.close()
                sec_ques_setup()
        else:
            sec_Ques_Error()
            window.close()
            sec_ques_setup()
    elif (event == sg.WIN_CLOSED):
        sg.Popup("It's Compulsory to Setup Security Question")
        window.close()
        win_setup_Incomplete()
    else:
        sec_ques_setup()


# If you close the program accidentally while setup Process then next time it will start from where you left
def win_setup_Incomplete():
    # Interface Layout
    # -----------------------------------------------------------------------
    layout = [[sg.Text("You don't Proceed Next... If you want to setup later..")],
              [sg.Text('Then'), sg.Button(' Close ')],
              [sg.Text('')],
              [sg.Text('If you want to Setup Now..')],
              [sg.Text('Then'), sg.Button(' Continue ')]]

    window = sg.Window('Setup InComplete', layout)
    # -----------------------------------------------------------------------

    # Backend Logic
    # -----------------------------------------------------------------------
    event, values = window.Read()
    if (event == ' Close ' or event == sg.WIN_CLOSED):
        window.close()
        last_step(False, email, passd)
    elif (event == ' Continue '):
        window.close()
        sq = sec_ques_setup()
        last_step(True, email, passd, sq)
    else:
        window.close()
        win_setup_Incomplete()


# Password Reset Interface
def win_resetpass():
    # Interface Layout
    # --------------------------------------------------------------------
    layout = [[sg.Text('Please Enter your New Password...')],
              [sg.Text('New Password : '), sg.InputText(key='in1', password_char='*')],
              [sg.Text('Confirm Password : '), sg.InputText(key='in2', password_char='*')],
              [sg.Button(' Reset ')]]

    window = sg.Window('Reset Password', layout)
    # --------------------------------------------------------------------

    # Backend Logic
    # -----------------------------------------------------------------------
    event, values = window.Read()
    if (event == sg.WIN_CLOSED):
        window.close()
    elif (event == ' Reset '):
        with open('datafile.py') as f:
            dic = json.load(f)
        ol_pass = list(dic.values())[0]
        o_pass = pass_decoder(ol_pass)
        if (not str(values['in1'])) or (not str(values['in2'])):
            window.close()
            sg.Popup('Please Enter your new Password!!')
            win_resetpass()
        elif (str(values['in1']).isspace() == True) or (str(values['in2']).isspace() == True):
            window.close()
            sg.Popup('Password cannot contain spaces!!')
            win_resetpass()
        elif (o_pass == str(values['in1'])):
            window.close()
            sg.Popup('You already used this password..\nPlease Enter another one!!')
            win_resetpass()
        elif (len(values['in1']) < 8):
            window.close()
            sg.Popup('Length of Password must be of 8 characters!!')
            win_resetpass()
        elif (str(values['in1']) == str(values['in2'])):
            with open('datafile.py', 'r') as f:
                data = json.load(f)
                email = list(data)[0]
            repass = str(values['in1'])
            relpass = pass_encoder(repass)
            data[email] = relpass
            with open('datafile.py', 'w') as fl:
                json.dump(data, fl)
            window.close()
            win_confirm()
            win_Login()
        else:
            window.close()
            win_resetpass()
    else:
        window.close()
        win_resetpass()


# Checking Security Question
def sec_ques_check():
    with open('datafile.py', 'r') as f:
        dic = json.load(f)
    List = list(dic)
    List.pop(0)
    List.pop(-1)

    # Interface Layout
    # -----------------------------------------------------------------------
    layout = [[sg.Text('Please choose any Security question and write it Answer..\n')],
              [sg.Text('First Question : '), sg.OptionMenu(List, key='sq1')],
              [sg.Text('Enter Answer : '), sg.InputText(key='in1')],
              [sg.Text('Second Question : '), sg.OptionMenu(List, key='sq2')],
              [sg.Text('Enter Answer : '), sg.InputText(key='in2')],
              [sg.Text('Third Question : '), sg.OptionMenu(List, key='sq3')],
              [sg.Text('Enter Answer : '), sg.InputText(key='in3')],
              [sg.Button(' Submit ')]]

    window = sg.Window('Verifying', layout)
    # -----------------------------------------------------------------------

    # Backend Logic
    # -----------------------------------------------------------------------
    event, values = window.Read()
    if (event == sg.WIN_CLOSED):
        window.close()
    elif (values['sq1'] != values['sq2']):
        if (values['sq2'] != values['sq3']):
            if (values['sq1'] != values['sq3']):
                if (not str(values['in1'])) or (not str(values['in2'])) or (not str(values['in3'])):
                    window.close()
                    sg.Popup('Please Write the all Answers!!')
                    sec_ques_check()
                elif ((dic[values['sq1']]) == str(values['in1'])):
                    if ((dic[values['sq2']]) == str(values['in2'])):
                        if ((dic[values['sq3']]) == str(values['in3'])):
                            window.close()
                            win_Fuser()
                        else:
                            win_Incorrect_Ans()
                            window.close()
                            win_Login()
                    else:
                        win_Incorrect_Ans()
                        window.close()
                        win_Login()
                else:
                    win_Incorrect_Ans()
                    window.close()
                    win_Login()
            else:
                sec_Ques_Error()
                window.close()
                sec_ques_check()
        else:
            sec_Ques_Error()
            window.close()
            sec_ques_check()
    else:
        sec_Ques_Error()
        window.close()
        sec_ques_check()


# Forget Username Interface
def win_Fuser():
    email = get_email()

    # Interface Layout
    # -----------------------------------------------------------------------
    layout = [[sg.Text('Your Email is '), sg.Text(email)],
              [sg.Text('Are you Also forget the Password?')],
              [sg.Button(' Recover Account ')],
              [sg.Text('If not, then '), sg.Button(' Log In ')]]

    window = sg.Window('Account Recovery', layout)
    # -----------------------------------------------------------------------

    # Backend Logic
    # -----------------------------------------------------------------------
    event, values = window.Read()
    if (event == sg.WIN_CLOSED):
        window.close()
    elif (event == ' Recover Account '):
        window.close()
        win_Verify()
    elif (event == ' LogIn '):
        window.close()
        win_Login()
    else:
        window.close()
        win_Login()


# ---------------- Popup Windows --------------------

def win_Error():
    text = 'Password is not Matching.. Please ReEnter it!!'
    sg.Popup(text)


def win_Invalid_Input():
    text = 'Incorrect Password or Email!!'
    sg.Popup(text)


def win_successful_signup():
    text = 'Signed Up Successfully'
    sg.Popup(text)


def sec_Ques_Error():
    text = 'Security Questions Cannot be same!!'
    sg.Popup(text)


def win_confirm():
    text = 'Password Changed!!'
    text1 = 'Click OK to Login'
    sg.Popup(text, text1)


def win_Incorrect_Ans():
    text = 'Incorrect Answer!!'
    sg.Popup(text)


def win_UserAvailable():
    # window.close()
    win_Signup()
    #text = "Can't Sign Up Again. User Already Existed"
    #sg.Popup(text)


# ----------------- Back-End-Functions -------------------

# Encoding Password
def pass_encoder(pss):
    evalue = []
    for char in pss:
        evalue.append(ord(char))
    return evalue

# Decoding Password
def pass_decoder(evalue):
    pss = ''
    for val in evalue:
        pss = pss + chr(val)
    return str(pss)

# Verify Function
def verify():
    code, get_email = otp_process()
    return code, get_email

# Send OTP to register EMail
def send_otp(otp, email):
    try:
        port = 465
        sender_email = 'abc@gmail.com'
        sender_email_pass = 'no@gmail.com'
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
            server.login(sender_email, sender_email_pass)
            message = ('Your OTP is {}').format(otp)
            server.sendmail(sender_email, email, message)
        return
    except Exception as err:
        sg.Popup(err)
        win_Login()


# Generating OTP
def otp_process():
    code = random.randint(111111, 999999)
    with open('datafile.py') as f:
        data = json.load(f)
    get_email = list(data)[0]
    send_otp(code, get_email)
    return code, get_email


# Backup Setup Process
def win_choice():
    try:
        with open('datafile.py', 'a+') as f:
            f.close()
        fsize = os.path.getsize('datafile.py')
        if fsize == 0:
            win_Signup()
        else:
            with open('datafile.py', 'r') as f:
                data = json.load(f)
            if (data['sqs'] == True):
                win_Login()
            else:
                second_last_step()
                last_step(True, email, passd)
    except Exception as err:
        print(err)
        win_choice()

# Saving Security Questions
def last_step(res, *arg):
    l = []
    for a in arg:
        l.append(a)

    email = l[0]
    epass = l[1]

    if (res == True):
        sec_ques = sec_ques_setup()
        dic = {email: epass}
        dic.update(sec_ques)
        dic.update({'sqs': True})
        with open('datafile.py', 'w') as fl:
            json.dump(dic, fl)
        win_successful_signup()
        win_Login()
    elif (res == False):
        dic = {email: epass}
        dic.update({'sqs': False})
        with open('datafile.py', 'w') as f:
            json.dump(dic, f)


def second_last_step():
    with open('datafile.py') as f:
        dic = json.load(f)
    global email, passd
    email = list(dic.keys())[0]
    passd = list(dic.values())[0]


# Check User is available or not
def file_checker():
    try:
        fsize = os.path.getsize('datafile.py')
        if fsize == 0:
            pass
        else:
            win_UserAvailable()
            win_Login()
    except Exception as err:
        sg.Popup(err)


# getting email from file
def get_email():
    with open('datafile.py') as f:
        data = json.load(f)
    email = list(data)[0]
    return email


# -------------------------- Main Program -------------------------

i = True
while i:
    try:
        # sg.theme('LightBrown1')
        i = win_choice()
    except Exception as err:
        print(err)
