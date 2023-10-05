from flask import Flask, request, render_template, redirect, url_for, session
from consultas.consulta import ConexionSQLServer
import uuid
from datetime import datetime

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
		nombre = request.form['nombres']
		apellidos = request.form['apellidos']
		DNI = request.form['numero-documento']
		usuario = request.form['usuario']
		contrasena = request.form['contrasena']
		correo = request.form['correo']
		direccion = request.form['direccion']
		num_celular = request.form['celular']
		administrador = 0 
		foto_perfil = '010101' # DEBE SER OPCIONAL (PROVISIONAL)
		fecha_creac = datetime.now()
		fecha_creac = fecha_creac.strftime("%Y-%m-%d %H:%M:%S")
		datos_esenciales = (nombre, apellidos)
		for dato_esencial in datos_esenciales:
			if dato_esencial.isdigit():
				erroneo = True
			
		if not erroneo:
			while not verificado:
				ID_usuario = uuid.uuid4()
				SQL = ConexionSQLServer('DESKTOP-0QQGSJL', 'DS-BBDD')
				SQL.getUUIDUsuario(ID_usuario)
				if SQL.encontrarUUIDUsuario() == None:
					array = (ID_usuario, nombre, apellidos, DNI, usuario, contrasena, correo, direccion, num_celular, administrador, foto_perfil, fecha_creac)
					SQL.getDatosUsuario(array)
					SQL.insertarUsuario()
					msg = 'Registro con éxito'
					verificado = True
		else:
			msg = 'Los datos no pueden ser numéricos'
	else:
		msg = 'Método HTTP incorrecto'
	return render_template('login.html', msg)

@app.route('/login')
def loginUsuario():
	msg = ''
	correo = request.form['correo']
	contrasena = request.form['contrasena']
	SQL = ConexionSQLServer('DESKTOP-0QQGSJL', 'DS-BBDD')
	SQL.getLoginUsuario(correo, contrasena)
	if SQL.autenticarUsuario != None:
		datos_usuario = SQL.devolverUsuario()
		session['ID_usuario'] = datos_usuario[0] 
		session['nombre'] = datos_usuario[1] 
		session['apellido'] = datos_usuario[2] 
		session['DNI'] = datos_usuario[3]
		session['usuario'] = datos_usuario[4] 
		session['correo'] = datos_usuario[6]
		session['direccion'] = datos_usuario[7]
		session['celular'] = datos_usuario[8]
		session['admin'] = datos_usuario[9]
		session['foto_perfil'] = datos_usuario[10]
		msg = 'Logeado con éxito'
		return redirect(url_for('registroDenuncia')) # FALTA DEFINIR PANTALLA PRINCIPAL
	else:
		msg = 'Correo o contraseña incorrectos'
	return render_template('login.html', msg)

@app.route('/logout')
def cerrarSesion():
	session.clear()
	return redirect(url_for('inicio'))

@app.route('/registro-denuncia', methods = ['GET', 'POST'])
def registroDenuncia():
	msg = ''
	verificado = False
	if request.method == 'POST':
		
		titulo = request.form['titulo']
		descripcion = request.form['descripcion']
		ID_usuario = session['ID_usuario']
		fecha_creac = datetime.now()
		fecha_creac = fecha_creac.strftime("%Y-%m-%d %H:%M:%S")
		relevancia = 0
		URL_imagen = request.form['URL_imagen'] # FALTA ACORDAR CUANDO SON VARIAS IMAGENES
		while not verificado:
			ID_publicacion = uuid.uuid4()
			SQL = ConexionSQLServer('DESKTOP-0QQGSJL', 'DS-BBDD')
			SQL.getUUIDPublicacion(ID_publicacion)
			if SQL.encontrarUUIDPublicacion() == None:
				array = (ID_publicacion, titulo, descripcion, ID_usuario, fecha_creac, relevancia)
				SQL.getDatosPublicacion(array)
				SQL.insertarDenuncia()
				msg = 'Registro con éxito'
				verificado = True
		# FALTA INSERTAR IMAGENES EN LA TABLA
	else:
		msg = 'Método HTTP incorrecto'
	return render_template('registrarDenuncia.html', msg)

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