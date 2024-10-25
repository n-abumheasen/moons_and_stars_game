from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key for session management

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/instructions')
def instructions():
    return render_template('instructions.html')

@app.route('/start')
def start_game():
    session['secret_number'] = random.randint(1, 50)
    session['attempts'] = 5
    session['guesses'] = []  # To store user guesses
    return redirect(url_for('game'))

@app.route('/game', methods=['GET', 'POST'])
def game():
    # Check if attempts exist in the session
    if 'attempts' not in session:
        return redirect(url_for('start_game'))  # Redirect to start the game if attempts are not set

    if request.method == 'POST':
        guess = request.form.get('guess', type=int)
        if session['attempts'] > 0:
            session['guesses'].append(guess)  # Store the guess
            session['attempts'] -= 1  # Reduce attempts
            
            if guess == session['secret_number']:
                return redirect(url_for('win', number=session['secret_number']))
            elif session['attempts'] == 0:
                return redirect(url_for('lose', number=session['secret_number']))
            elif guess < session['secret_number']:
                result = "Your guess is too low."
            else:
                result = "Your guess is too high."
        else:
            return redirect(url_for('lose', number=session['secret_number']))
    else:
        result = None  # Reset result for GET request

    return render_template('game.html', result=result, attempts=session['attempts'], guesses=session['guesses'])

@app.route('/win/<int:number>')
def win(number):
    return render_template('win.html', number=number)

@app.route('/lose/<int:number>')
def lose(number):
    return render_template('lose.html', number=number)

@app.route('/play-again')
def play_again():
    session.clear()  # Clear session variables
    return redirect(url_for('start_game'))

if __name__ == "__main__":
    # Update host to allow external access on the local network
    app.run(debug=True)
