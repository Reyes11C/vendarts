from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL



#Conexión con MySQL
app.config['MYSQL_HOST'] = 'vendarts.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER'] = 'vendarts'
app.config['MYSQL_PASSWORD'] = 'REYES11sq...'
app.config['MYSQL_DB'] = 'vendarts$vendarts_contac'
mysql = MySQL(app)


#Aquí se guardan los datos, dentro de la memoria de la app.
app.secret_key = 'mysecretkey'


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/mision_vision")
def mision_vision():
    return render_template("mision_vision.html")

@app.route("/productos")
def products():
    return render_template("products.html")

@app.route("/tienda")
def store():
    return render_template("store.html")

@app.route("/registrarvista")
def registrarvista():
    return render_template("registrarvista.html")

@app.route("/galeria")
def galeria():
    return render_template("Galeria.html")

@app.route("/vaso_decorado")
def vaso():
    return render_template("vaso.html")

@app.route("/mini_cazuela_arrocera")
def cazuela():
    return render_template("cazuela.html")

@app.route("/servilletero_decorativo")
def servilletero():
    return render_template("servilletero.html")

@app.route("/taza_azul")
def taza():
    return render_template("taza_azul.html")

#inicio de agregar contacto
@app.route('/add_artesano')
def add_artesano():
    #Consulta a la base de datos
    cur = mysql.connection.cursor()
    #se almacena en la variable cur
    cur.execute('SELECT * FROM contacts')
    #con fetch se obtienen todos los datos y se guardan en la variable datos
    data = cur.fetchall()
    return render_template("add_contact_artesano.html", contacts = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        nombre = request.form ['nombre']
        telefono = request.form['telefono']
        email = request.form['email']
        #obtenemos la conexion
        cur = mysql.connection.cursor()
        #escribimos la consulta
        cur.execute('INSERT INTO contacts (nombre, telefono, email) VALUES (%s, %s, %s)', (nombre, telefono, email))
        #ejecutamos la consulta
        mysql.connection.commit()
        #Mandamos mensaje entre vistas
        flash('CONTACTO AGREGADO CON EXITO. GRACIAS. :)')
        #despues de esto se han escriro los datos en MySQL y termina petición del navegador, es regresado al formulario
        return redirect(url_for('add_artesano'))

@app.route('/editar/<id>')
def editar_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', (id))
    data = cur.fetchall()
    print(data[0])
    return render_template('edit_contact.html', contact=data[0])

@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contacts
            SET nombre = %s,
                email = %s,
                telefono = %s
            WHERE id = %s
        """, (nombre, email, telefono, id))
        flash('LISTO, EL CONTACTO HA SIDO EDITADO CON EXITO.')
        mysql.connection.commit()
        return redirect(url_for('add_artesano'))

@app.route('/eliminar/<id>')
def eliminar_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('OK, EL CONTACTO HA SIDO ELIMINADO CON EXITO. ')
    return redirect(url_for('add_artesano'))
#fin de agregar contacto

# Login
@app.route('/')
@app.route('/login', methods=['POST', 'GET'])
def login():
    status = True
    if request.method == 'POST':
        email = request.form["email"]
        pwd = request.form["pass"]
        cur = mysql.connection.cursor()
        cur.execute("select * from contactos where EMAIL=%s and PASS=%s", (email, pwd))
        data = cur.fetchone()
        if data:
            session['logged_in'] = True
            flash('Ingreso exitoso','success')
            return redirect('/tienda')
        else:
            flash('Usuario incorrecto')
    return render_template("login.html")


# check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('NO AUTORIZADO','success')
            return redirect(url_for('login'))

    return wrap


# Registration
@app.route('/reg', methods=['POST', 'GET'])
def reg():
    status = False
    if request.method == 'POST':
        name = request.form["name"]
        email = request.form["email"]
        pwd = request.form["pass"]
        cur = mysql.connection.cursor()
        cur.execute("insert into contactos (NAME,PASS,EMAIL) values(%s,%s,%s)", (name, pwd, email))
        mysql.connection.commit()
        cur.close()
        flash('REGISTRO EXITOSO, AHORA PUEDES INGRESAR', 'success')
        return redirect('login')
    return render_template("reg.html", status=status)

# logout
@app.route("/logout")
def logout():
    session.clear()
    flash('INGRESAR', 'success')
    return redirect(url_for('login'))



def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(port = 3000, debug = True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
