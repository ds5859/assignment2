from flask import Flask, render_template, request, url_for, flash, redirect, session
from forms import RegistrationForm, LoginForm, SpellForm
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect
import subprocess
#from subprocess import PIPE
app = Flask(__name__)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['SECRET_KEY'] = '4a6542b7886a0d46a36c1bf51f9a11ac720dde847d4b0a9b'

#csrf.init_app(app)

# initializing user dictionary with root account
users = {'root': {'pword': 'toor', '2fa': 1234567890}} 

class User(UserMixin):
    pass

@login_manager.user_loader
def load_user(uname):
    if uname not in users:
        return
    user = User()
    user.id = uname
    return user
"""
@login_manager.request_loader
def request_loader(request):
    uname = request.form.get('uname')
    if uname not in users:
        return
    user = User()
    user.id = uname
    if users[form.uname.data]['2fa'] == "":  
        user.is_authenticated = (bcrypt.check_password_hash(users[uname]['pword'], form.pword.data)) 
    else:
        if not form.twofa.data:
            return
        else:
            user.is_authenticated = (bcrypt.check_password_hash(users[uname]['pword'], form.pword.data) and (users[uname]['2fa'] == form.twofa.data))
    #BREAKING when user who has 2fa tries logging in with a blank 2fa field
    #if not form.twofa.data:
       # if users[form.uname.data]['2fa'] is None:
            #user.is_authenticated = (bcrypt.check_password_hash(users[uname]['pword'], form.pword.data) and bcrypt.check_password_hash(users[uname]['2fa'], form.twofa.data))
        #    user.is_authenticated = (bcrypt.check_password_hash(users[uname]['pword'], form.pword.data)) 
    #else: 
        #user.is_authenticated = (bcrypt.check_password_hash(users[uname]['pword'], form.pword.data)) 
      # user.is_authenticated = (bcrypt.check_password_hash(users[uname]['pword'], form.pword.data) and bcrypt.check_password_hash(users[uname]['2fa'], form.twofa.data))
    return user
"""
@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'

#@csrf.error_handler
###@app.errorhandler(CSRFProtect)
#def csrf_error(reason):
    #return render_template('csrf_error.html', reason=reason), 400

@app.route('/') #main page
@app.route('/index') #alt main page
def main():
    return render_template('home.html', pagename = 'Main Page')

@app.route('/logout')
#@login_required
def logout():
    print(current_user)
    logout_user()
    flash('Logged Out Successfully', 'success')
    return redirect(url_for('main'))


@app.route('/register', methods=["POST", "GET"]) #registration page
def register():
    gradescope = ''
    if current_user.is_authenticated:
        flash('Already Logged In', 'info')
        return redirect(url_for('main'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.uname.data in users:
            gradescope = 'failure'
            flash('Registration Error. Please select a different User Name', 'danger')
            return render_template('register.html', title = 'Success', pagename = 'Registration Page', gradescope = gradescope, form = form)
        else:
            if not form.twofa.data:
                hash_pword = bcrypt.generate_password_hash(form.pword.data).decode('utf-8')
                #users[form.uname.data] = {'pword': form.pword.data, '2fa': form.twofa.data}
                users[form.uname.data] = {'pword': hash_pword, '2fa': ""}
                flash(f'Account created for {form.uname.data}. Please Login.', 'success')
                print(users)
                gradescope = 'success'
                #return redirect(url_for('login'))
                return render_template('register.html', title = 'Success', pagename = 'Registration Page', gradescope = gradescope, form = form)
            else:
                #TODO: hash and salt passwords and 2fa
                #TODO: if user already exists? if form.uname.data in users
                hash_pword = bcrypt.generate_password_hash(form.pword.data).decode('utf-8')
                #hash_twofa = bcrypt.generate_password_hash(form.twofa.data).decode('utf-8')
                #users[form.uname.data] = {'pword': form.pword.data, '2fa': form.twofa.data}
                users[form.uname.data] = {'pword': hash_pword, '2fa': form.twofa.data}
                flash(f'Account created for {form.uname.data} with 2-Factor Authentication. Please Login.', 'success')
                print(users)
                gradescope = 'success'
                #return redirect(url_for('login'))
                return render_template('register.html', title = 'Success', pagename = 'Registration Page', gradescope = gradescope, form = form)
    return render_template('register.html', title = 'Register', pagename = 'Registration Page', form = form)

@app.route('/login', methods=["POST", "GET"]) #login page
def login():
    #if current_user.is_authenticated:
        #flash('Already Logged In', 'info')
        #return redirect(url_for('main'))
    gradescope = ''
    form = LoginForm()
    if form.validate_on_submit():
        if form.uname.data in users:
            uname = form.uname.data
            if users[form.uname.data]['2fa'] == "":
                if (bcrypt.check_password_hash(users[form.uname.data]['pword'], form.pword.data)): # and not form.twofa.data)
                #if ((users[form.uname.data]['pword'] == form.pword.data) and (users[form.uname.data]['2fa'] == form.twofa.data)):
                #if form.uname.data == 'test123' and form.twofa.data == '123456789' and form.pword.data == 'test123':
                    #login_user(form.uname.data, remember=form.remember.data)
                    #User.curr_user = form.uname.data
                    #login_user(curr_user, remember=form.remember.data)
                    user = User()
                    user.id = uname
                    login_user(user, remember=form.remember.data)
                    flash('Logged in successfully', 'success')
                    #return 'Logged in as: ' + current_user.id
                    print(login_user(user))
                    print(user)
                    print(user.id)
                    #return redirect(url_for('main'))
                    gradescope = 'Success'
                    return render_template('login.html', title = 'Login', pagename = 'Login Page', gradescope = gradescope, form = form)
                else:
                    flash('Unsuccessful Login', 'danger')
                    gradescope = 'Incorrect'
                    return render_template('login.html', title = 'Login', pagename = 'Login Page', gradescope = gradescope, form = form)
            #else if not form.twofa.data:
                #flash('Unsuccessful Login', 'danger')
            else:
                if (bcrypt.check_password_hash(users[form.uname.data]['pword'], form.pword.data) and (users[form.uname.data]['2fa'] == form.twofa.data)):
                #if ((users[form.uname.data]['pword'] == form.pword.data) and (users[form.uname.data]['2fa'] == form.twofa.data)):
                #if form.uname.data == 'test123' and form.twofa.data == '123456789' and form.pword.data == 'test123':
                    #login_user(form.uname.data, remember=form.remember.data)
                    #User.curr_user = form.uname.data
                    #login_user(curr_user, remember=form.remember.data)
                    user = User()
                    user.id = uname
                    login_user(user, remember=form.remember.data)
                    flash('Logged in successfully', 'success')
                    #return 'Logged in as: ' + current_user.id
                    print(login_user(user))
                    print(user)
                    print(user.id)
                    gradescope = 'Success'
                    #return redirect(url_for('main'))
                    return render_template('login.html', title = 'Login', pagename = 'Login Page', gradescope = gradescope, form = form)
                else:
                    flash('Unsuccessful Login', 'danger')
                    gradescope = 'Incorrect'
                    return render_template('login.html', title = 'Login', pagename = 'Login Page', gradescope = gradescope, form = form)
        else:
            flash('Unsuccessful Login. No such User.', 'danger')
            gradescope = 'Incorrect'
            return render_template('login.html', title = 'Login', pagename = 'Login Page', gradescope = gradescope, form = form)
    return render_template('login.html', title = 'Login', pagename = 'Login Page', form = form)

    #return "Test Login Page"

@app.route('/spell_check', methods=["POST", "GET"]) #spellchecker
@login_required
def spell():
    form = SpellForm()
    #if login_user(user) == False:
        #flash('Please Log In', 'danger')
        #return redirect(url_for('login'))

    if form.validate_on_submit(): 
        flash('Submitted Successfully', 'success')
        inputtext = form.inputtext.data 
        with open('userinput.txt', 'w') as f:
            f.write(form.inputtext.data)
            f.close()

        #print(inputtext)

        # copy input to new text file
        # pipe input to new field
        # run subprocess 
        # pipe output to new field
        # delete text file
        spellout = subprocess.run(['./a.out', 'userinput.txt', 'wordlist.txt'], check=True, stdout=subprocess.PIPE, universal_newlines=True) #use if using python3.6
        #spellout = subprocess.run(['./a.out', 'userinput.txt', 'wordlist.txt'], capture_output=True, text=True) # stderr=subprocess.DEVNULL

        with open('mispelled.txt', 'w') as g:
            g.write(spellout.stdout)
            g.close()
        with open('mispelled.txt', 'r') as g:
            mispelled = g.read().replace('\n', ', ').strip().strip(',')
            g.close()
        
        #spellout2 = spellout.stdout
        print(spellout.stdout)
        # return form.inputtext.data 
        # TODO: delete files
    #else:
        #flash('No Input Detected', 'danger')
        #return mispelled
        return render_template('spell_check.html', title = 'Spell Checker', pagename = 'Spell Check Page', textout = inputtext, misspelled = mispelled, form = form)

    #take input from user - validate
    #open new input file - take user input and put in file
    #run subprocess
    #ouput to va
    
    return render_template('spell_check.html', title = 'Spell Checker', pagename = 'Spell Check Page', form = form)


if __name__ == '__main__':
    app.run(debug=True)


