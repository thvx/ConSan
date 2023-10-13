from flask import Flask, request, render_template, redirect, url_for, session
from clases.consulta import ConexionSQLServer
import uuid
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

@app.route('/')
def inicio():
	return render_template('index.html')

@app.route('/registro-usuario/', methods = ['GET','POST'])
def registroUsuario():
	verificado = False
	msg = ''
	erroneo = False
	usuario = request.form.get('nombre-usuario', False)
	nombre = request.form.get('nombre', False)
	apellidos = request.form.get('apellidos', False)
	tipo_documento = request.form.get('tipo-documento', False)
	num_doc = request.form.get('numero-documento', False)
	contrasena = request.form.get('contrasena', False)
	correo = request.form.get('correo', False)
	num_celular = request.form.get('num_celular', False)
	confirm_contrasena = request.form.get('confirmar-contrasena', False)

	if request.method == 'POST':
		datos_esenciales = (nombre, apellidos)
		for dato_esencial in datos_esenciales:
			if dato_esencial.isdigit():
				msg = 'Los datos no pueden ser numéricos'
				return redirect(url_for('registroUsuario'))
		
		if contrasena != confirm_contrasena:
			msg = 'Las contraseñas deben coincidir'
			return redirect(url_for('registroUsuario'))
		
		if len(contrasena) < 8:
			msg = 'La contraseña no debe tener menos de 8 digitos'
			return redirect(url_for('registroUsuario'))

		administrador = 0 
		foto_perfil = '010101' # DEBE SER OPCIONAL (PROVISIONAL)
		fecha_creac = datetime.now()
		fecha_creac = fecha_creac.strftime("%Y-%m-%d %H:%M:%S")
		while not verificado:
			ID_usuario = uuid.uuid4()
			SQL = ConexionSQLServer('DESKTOP-0QQGSJL', 'DS-BBDD')
			SQL.setUUIDUsuario(ID_usuario)
			if SQL.encontrarUUIDUsuario() == None:
				array = (str(ID_usuario), nombre, apellidos, tipo_documento, num_doc, usuario, contrasena, correo, num_celular, administrador, foto_perfil, fecha_creac)
				SQL.setDatosUsuario(array)
				SQL.insertarUsuario()
				msg = 'Registro con éxito'
				verificado = True
		return redirect(url_for('loginUsuario'))
	return render_template('registroUsuario.html')

@app.route('/login/', methods=['GET', 'POST'])
def loginUsuario():
	msg = ''
	correo = request.form.get('correo', False)
	contrasena = request.form.get('contrasena', False)
	if request.method == 'POST':
		SQL = ConexionSQLServer('DESKTOP-0QQGSJL', 'DS-BBDD')
		SQL.setLoginUsuario(correo, contrasena)
		print(correo)
		print(contrasena)
		if SQL.autenticarUsuario() != None:
			datos_usuario = SQL.devolverUsuario()
			print(datos_usuario)
			session['ID_usuario'] = datos_usuario[0]
			session['nombre'] = datos_usuario[1] 
			session['apellido'] = datos_usuario[2] 
			session['tipo_documento'] = datos_usuario[3]
			session['num_documento'] = datos_usuario[4]
			session['usuario'] = datos_usuario[5] 
			session['correo'] = datos_usuario[7]
			session['celular'] = datos_usuario[8]
			session['admin'] = datos_usuario[9]
			session['foto_perfil'] = datos_usuario[10]
			session['logged'] = True
			msg = 'Logeado con éxito'
			if session['admin'] == 1:
				return redirect(url_for('admin'))
			elif session['admin'] == 0:
				return redirect(url_for('registroDenuncia'))
		else:
			msg = 'Correo o contraseña incorrectos'
	return render_template('inicioSesion.html')

@app.route('/logout/')
def cerrarSesion():
	session.clear()
	return redirect(url_for('inicio'))

@app.route('/registro-denuncia/', methods = ['GET', 'POST'])
def registroDenuncia():
	msg = ''
	verificado = False
	try:
		if session['logged'] == True and session['admin'] == 0:
			'''
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
			'''
			return render_template('registrarDenuncia.html')
	except:
		msg = 'Para acceder a esta página debes iniciar sesión'
		return redirect(url_for('loginUsuario'))

@app.route('/seguimiento-denuncia/', methods = ['GET', 'POST'])
def seguimientoDenuncia():
	msg = ''
	return render_template('seguimientoDenuncia.html', msg) 

@app.route('/admin/', methods = ['GET', 'POST'])
def admin():
	msg = ''
	return render_template('admin.html', msg) 

if __name__ == '__main__':
	app.run(debug = True)