from flask import Flask, render_template, request, url_for, flash, redirect, session
from forms import RegistrationForm, LoginForm, SpellForm
import subprocess
app = Flask(__name__)
app.config['SECRET_KEY'] = '4a6542b7886a0d46a36c1bf51f9a11ac720dde847d4b0a9b'

# initializing user dictionary with root account
users = {'root': {'pword': 'toor', '2fa': 1234567890}} 

@app.route('/') #main page
@app.route('/index') #alt main page
def main():
    return render_template('home.html', pagename = 'Main Page')

@app.route('/register', methods=["POST", "GET"]) #registration page
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        #TODO: hash and salt passwords and 2fa
        #TODO: if user already exists? if form.uname.data in users
        users[form.uname.data] = {'pword': form.pword.data, '2fa': form.twofa.data}
        flash(f'Account created for {form.uname.data}', 'success')
        print(users)
        return redirect(url_for('main'))
    return render_template('register.html', title = 'Register', pagename = 'Registration Page', form = form)

@app.route('/login', methods=["POST", "GET"]) #login page
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.uname.data in users:
            if ((users[form.uname.data]['pword'] == form.pword.data) and (users[form.uname.data]['2fa'] == form.twofa.data)):
            #if form.uname.data == 'test123' and form.twofa.data == '123456789' and form.pword.data == 'test123':
                flash('Logged in successfully', 'success')
                return redirect(url_for('main'))
            else:
                flash('Unsuccessful Login', 'danger')
        else:
            flash('Unsuccessful Login', 'danger')
    return render_template('login.html', title = 'Login', pagename = 'Login Page', form = form)

    #return "Test Login Page"

@app.route('/spell_check', methods=["POST", "GET"]) #spellchecker
def spell():
    form = SpellForm()

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
        spellout = subprocess.run(['./a.out', 'userinput.txt', 'wordlist.txt'], capture_output=True, text=True) # stderr=subprocess.DEVNULL
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





