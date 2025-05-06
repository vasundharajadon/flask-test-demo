from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

DETAILS_FILE = 'details.txt'

def get_next_user_id():
    if not os.path.exists(DETAILS_FILE) or os.stat(DETAILS_FILE).st_size == 0:
        return 1
    with open(DETAILS_FILE, 'r') as f:
        lines = f.readlines()
        last_line = lines[-1]
        last_id = int(last_line.split(',')[0])
        return last_id + 1

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = get_next_user_id()
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        with open(DETAILS_FILE, 'a') as f:
            f.write(f"{user_id},{name},{email},{password}\n")
        
        return redirect('/')
    
    return render_template('register.html')
@app.route('/users')
def users():
    users = []
    if os.path.exists(DETAILS_FILE):
        with open(DETAILS_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) >= 4:
                    users.append({
                        'id': parts[0],
                        'name': parts[1],
                        'email': parts[2],
                        'password': parts[3]
                    })
    return render_template('users.html', users=users)



if __name__ == '__main__':
    app.run(debug=True)
