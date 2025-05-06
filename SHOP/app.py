from flask import Flask, render_template, redirect, url_for, request, session
app = Flask(__name__)
app.secret_key = 'your_secret_key'
users = {}
lists = {}
products = {}

@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        user_lists = lists.get(username, [])
        user_products = products.get(username, [])
        return render_template('main.html', lists=user_lists, products=user_products)
    else:
        return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    error_message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            error_message = 'Lietotajs jau ir izveidots'
        else:
            users[username] = password
            session['username'] = username  
            return redirect(url_for('index')) 

    return render_template('register.html', error_message=error_message)
@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            error_message = 'Nepareizi dati'
    return render_template('login.html', error_message=error_message)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/create_list', methods=['POST'])
def create_list():
    if 'username' not in session:
        return redirect(url_for('login'))
    list_name = request.form['list_name']
    username = session['username']
    if username not in lists:
        lists[username] = []
    new_list = {'id': len(lists[username]) + 1, 'list_name': list_name}
    lists[username].append(new_list)

    return redirect(url_for('index'))

@app.route('/delete_list/<int:list_id>')
def delete_list(list_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    lists[username] = [lst for lst in lists[username] if lst['id'] != list_id]
    return redirect(url_for('index'))

@app.route('/add_product/<int:list_id>', methods=['POST'])
def add_product(list_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    product_name = request.form['product_name']
    if username not in products:
        products[username] = []
    new_product = {'id': len(products[username]) + 1, 'list_id': list_id, 'product_name': product_name}
    products[username].append(new_product)

    return redirect(url_for('index'))

@app.route('/delete_product/<int:product_id>')
def delete_product(product_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    products[username] = [prod for prod in products[username] if prod['id'] != product_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)

