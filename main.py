from flask import Flask, redirect, url_for, render_template
from flask_mysqldb import MySQL


app = Flask(__name__)

#Conexion DB
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'proyectoflask'

mysql =  MySQL(app)






@app.route('/')
def index():

    edad = 101
    personas = ['David','Esteban','Juan', 'Roberto']

    return render_template('index.html',
                           edad =edad,
                           personas = personas,
                            dato1 = "valor1", 
                            dato2 = "valor2",
                              lista = ["uno", "dos", "tres"]
                             )


@app.route('/informacion')
@app.route('/informacion/<string:nombre>')
def informacion(nombre = None):

    texto = ""
    if nombre != None:
        texto = f"bienvenido {nombre}"
       
    return  render_template('informacion.html', texto = texto)


@app.route('/contacto')
@app.route('/contacto/<redireccion>')
def contacto(redireccion = None):

    if redireccion is not None:
        return redirect(url_for('lenguajes'))

    return render_template('contacto.html')


@app.route('/Lenguajes-de-programacion')
def lenguajes():
    return render_template('lenguajes.html')

@app.route('/insertar-coche')
def insertar_coche():
    cursor = mysql.connection.cursor()
    cursor.execute(f"INSERT INTO coches VALUES(NULL, 'Lambo', 'Gallardo', 100000, 'angeles')")
    cursor.connection.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)