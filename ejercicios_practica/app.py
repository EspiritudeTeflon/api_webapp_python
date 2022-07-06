'''
Flask [Python]
Ejercicios de práctica

Autor: Inove Coding School
Version: 2.0
 
Descripcion:
Se utiliza Flask para crear un WebServer que levanta los datos de
las personas registradas.

Ingresar a la siguiente URL para ver los endpoints disponibles
http://127.0.0.1:5000/
'''

# Realizar HTTP POST con --> post.py

import traceback
from flask import Flask, request, jsonify, render_template, Response, redirect, url_for

import utils
import persona

app = Flask(__name__)

# Indicamos al sistema (app) de donde leer la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///personas.db"
# Asociamos nuestro controlador de la base de datos con la aplicacion
persona.db.init_app(app)


@app.route("/")
def index():
    try:
        # Imprimir los distintos endopoints disponibles
        # Renderizar el temaplate HTML index.html
        print("Renderizar index.html")
        return render_template('index.html')
    except:
        return jsonify({'trace': traceback.format_exc()})


# ejercicio de practica Nº1
@app.route("/personas")
def personas():
    try:
        # Alumno:
        # Implementar la captura de limit y offset de los argumentos
        # de la URL
        # limit = ...
        # offset = ....
        limit_str = str(request.args.get('limit'))
        offset_str = str(request.args.get('offset'))

        limit = 0
        offset = 0

        if(limit_str is not None) and (limit_str.isdigit()):
            limit = int(limit_str)

        if(offset_str is not None) and (offset_str.isdigit()):
            offset = int(offset_str)
        
        # Debe verificar si el limit y offset son válidos cuando
        # no son especificados en la URL
    
        # Alumno: Pasarle al metodo report los valores de limit y offset
        data = persona.report(limit=limit, offset=offset)
        print("Renderizar tabla.html")
    
        #result = '''<h3>Alumno: Implementar la llamada
        #            al HTML tabla.html
        #           con render_template, recuerde pasar
         #           data como parámetro</h3>'''
        # Sacar esta linea cuando haya implementado el return
        # con render template
        return render_template("tabla.html", data = data)
    except:
        return jsonify({'trace': traceback.format_exc()})


# ejercicio de practica Nº2
@app.route("/registro", methods=['GET', 'POST'])
def registro():
    if request.method == 'GET':
        try:
            return render_template('registro.html')
        except:
            return jsonify({'trace': traceback.format_exc()})

    if request.method == 'POST':
        try:
            name = ""
            age = 0

            # Alumno:
            # Obtener del HTTP POST JSON el nombre y la edad
            # name = ...
            # age = ...
            name = str(request.form.get("name")).lower()
            age = str(request.form.get ("age"))

            # Alumno: descomentar la linea persona.insert una vez implementado
            # lo anterior:
            # persona.insert(name, int(age))
            persona.insert(name, int(age))
            
            # Como respuesta al POST devolvemos la tabla de valores
            # return redirect(url_for('personas'))
            return redirect(url_for('personas', name= name, age= age)) 
        except:
            return jsonify({'trace': traceback.format_exc()})


# ejercicio de practica Nº3
@app.route("/comparativa")
def comparativa():
    try:
        # Alumno:
        # Implementar una función en persona.py llamada "dashboard"
        # Lo que desea es realizar un gráfico de linea con las edades
        # de todas las personas en la base de datos

        # Para eso, su función "dashboard" debe devolver dos valores:
        # - El primer valor que debe devolver es "x", que debe ser
        # los Ids de todas las personas en su base de datos
        # - El segundo valor que debe devolver es "y", que deben ser
        # todas las edades respectivas a los Ids que se encuentran en "x"

        # Descomentar luego de haber implementado su función en persona.py:

        # x, y = persona.dashboard()
        # image_html = utils.graficar(x, y)
        # return Response(image_html.getvalue(), mimetype='image/png')
        
        x, y = persona.dashboard()
        image_html= utils.graficar(x,y)
        #return "Alumno --> Realice la implementacion" 
        return Response(image_html.getvalue(), mimetype= "image/png")
    except:
        return jsonify({'trace': traceback.format_exc()})


# Este método se ejecutará solo una vez
# la primera vez que ingresemos a un endpoint
@app.before_first_request
def before_first_request_func():
    # Crear aquí todas las bases de datos
    persona.db.create_all()
    print("Base de datos generada")


if __name__ == '__main__':
    print('Inove@Server start!')

    # Lanzar server
    app.run(host="127.0.0.1", port=5000)
