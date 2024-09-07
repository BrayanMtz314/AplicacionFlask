from flask import Flask, flash, redirect, request, url_for, render_template
from flask_mysqldb import MySQL


app = Flask(__name__)

app.secret_key = 'clave_secreta-flask'

#Conexion DB
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'proyectoflask'

mysql =  MySQL(app)






@app.route('/')
def index():
    return render_template('index.html')


@app.route('/informacion')
@app.route('/informacion/<string:nombre>')
def informacion(nombre = None):

    texto = ""
    if nombre != None:
        texto = f"bienvenido {nombre}"
       
    return  render_template('informacion.html', texto = texto)



@app.route('/crear-coche', methods =[ 'GET', 'POST'] )
def crear_coche():
    if request.method == 'POST':
        
        marca = request.form['marca']
        modelo = request.form['modelo']
        precio = request.form['precio']
        ciudad = request.form['ciudad']
        
    
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO coches VALUES(NULL, %s , %s, %s, %s)", (marca, modelo, precio, ciudad))
        cursor.connection.commit()
        flash('Has creado el coche correctamente!!')
        return redirect(url_for('index'))
    
    
    return render_template('crear_coche.html')

@app.route('/coches')
def coches():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM coches ORDER BY id DESC")
    coches = cursor.fetchall()
    cursor.close()
    
    return render_template('coches.html', coches = coches)

@app.route('/coche/<coche_id>')
def coche(coche_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM coches WHERE id = %s", (coche_id))
    coches = cursor.fetchall()
    cursor.close()
    
    if coches: 
        return render_template('coche.html', coche=coches[0])
    else:
        return "Coche no encontrado", 404  
    
@app.route('/borrar-coche/<coche_id>')
def borrar_coche(coche_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM coches WHERE id = %s", (coche_id))
    mysql.connection.commit()
    flash('el coche ha sido eliminado!!')
    return redirect(url_for('coches'))   


@app.route('/editar-coche/<coche_id>', methods = ['GET', 'POST'])
def editar_coche(coche_id):
    if request.method == 'POST':
        
        marca = request.form['marca']
        modelo = request.form['modelo']
        precio = request.form['precio']
        ciudad = request.form['ciudad']
        
    
        cursor = mysql.connection.cursor()
        cursor.execute("""
                       UPDATE coches
                       SET marca = %s,
                            modelo = %s,
                            precio = %s,
                            ciudad = %s
                        WHERE id = %s
                       """, (marca, modelo, precio, ciudad, coche_id)),
        cursor.connection.commit()
        flash('Has editado el coche correctamente!!')
        return redirect(url_for('coches'))
             
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM coches WHERE id = %s", (coche_id))
    coches = cursor.fetchall()
    cursor.close()
    
    if coches: 
        return render_template('crear_coche.html', coche=coches[0])
    else:
        return "Coche no encontrado", 404  



if __name__ == '__main__':
    app.run(debug=True)