from flask import Flask, request, render_template, redirect, url_for, session
from bbdd import ConexionSQLServer
import pyodbc
import uuid
import random

app = Flask(__name__)

@app.route('/')
def inicio():
	return render_template('index.html')

@app.route('/registro-usuario', methods = ['GET','POST'])
def registroUsuario():
	verificado = False
	msg = ''
	erroneo = False
	if request.method == 'POST':
		nombre = request.form['nombre']
		apellidos = request.form['apellidos']
		DNI = request.form['DNI']
		usuario = request.form['usuario']
		contrasena = request.form['contrasena']
		correo = request.form['correo']
		direccion = request.form['direccion']
		num_celular = request.form['num_celular']
		administrador = request.form['administrador']
		foto_perfil = request.form['foto_perfil']
		fecha_creac = request.form['fecha_creac']
		datos_esenciales = (nombre, apellidos)
		for dato_esencial in datos_esenciales:
			if dato_esencial.isdigit():
				erroneo = True
			
		if not erroneo:
			while not verificado:
				ID_usuario = uuid.uuid4()
				SQL = ConexionSQLServer(servidor, base_de_datos, nombre_usuario, contra)
				SQL.getUUID(ID_usuario)
				if SQL.encontrarUUID() == None:
					array = (ID_usuario, nombre, apellidos, DNI, usuario, contrasena, correo, direccion, num_celular, administrador, foto_perfil, fecha_creac)
					SQL.getDatosUuario(array)
					SQL.insertarUsuario()
					msg = 'Registro con éxito'
					verificado = True
		else:
			msg = 'Los datos no pueden ser numéricos'
	else:
		msg = 'Método HTTP incorrecto'
	return render_template('registro.html', msg)

@app.route('/login')
def loginUsuario():
	msg = ''
	correo = request.form['correo']
	contrasena = request.form['contrasena']
	SQL = ConexionSQLServer(servidor, base_de_datos, nombre_usuario, contra)
	SQL.getLoginUsuario(correo, contrasena)
	if SQL.autenticarUsuario != None:
		# UTILIZAR SESSION AQUÍ
		msg = 'Logeado con éxito'
		return redirect(url_for('registro-denuncia')) # FALTA DEFINIR PANTALLA PRINCIPAL
	else:
		msg = 'Correo o contraseña incorrectos'
	return render_template('login.html', msg)

@app.route('/registro-denuncia', methods = ['GET', 'POST'])
def registroDenuncia():
	msg = ''
	ID_publicacion = ''
	if request.method == 'POST':
		titulo = request.form['titulo']
		descripcion = request.form['descripcion']
		ID_usuario = request.form['ID_usuario']
		fecha_creacion = request.form['fecha_creacion']
		relevancia = request.form['relevancia']
		ID_publicacion = str(random.randint(100,1000)) + str(random.randint(100,1000)) + str(random.randint(100,1000)) + str(random.randint(100,1000))
		URL_imagen = request.form['URL_imagen']
		# ******************************************************************************************************
		# Aquí se debe validar con la BBDD que la ID no se repita con otra ID y subir los datos a la BBDD
		# ******************************************************************************************************
		msg = 'Registro con éxito'
	else:
		msg = 'Método HTTP incorrecto'
	return render_template('registrarDenuncia.html', msg, ID_publicacion)

@app.route('/seguimiento-denuncia', methods = ['GET', 'POST'])
def seguimientoDenuncia():
	msg = ''
	ID_publicacion = request.form['ID_publicacion']
	# ******************************************************************************************************
	# Aquí se debe buscar la ID en la BBDD y si está se prosigue con la muestra de datos
	# ******************************************************************************************************
	return render_template('buscarRegistro.html', msg)

if __name__ == '__main__':
	app.run(debug = True)