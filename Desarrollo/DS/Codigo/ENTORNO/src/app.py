from flask import Flask, request, render_template, redirect, url_for, session
from clases.consulta import ConexionSQLServer
import uuid
from datetime import datetime
import os

PATH_FILE = os.path.join(os.getcwd(), 'static/files')
desktop='LAPTOP-A511R2N8'
bbdd = 'DB_DenunciaSeguro'
app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

@app.route('/')
def inicio():
    SQL = ConexionSQLServer(desktop, bbdd)
    denuncias_principales = SQL.obtenerDenunciasPrincipales()
    return render_template('index.html', denuncias=denuncias_principales)

@app.route('/registro-usuario/', methods = ['GET','POST'])
def registroUsuario():
	verificado = False
	msg = ''
	usuario = request.form.get('nombre-usuario', False)
	nombre = request.form.get('nombre', False)
	apellidos = request.form.get('apellidos', False)
	tipo_documento = request.form.get('tipo-documento', False)
	num_doc = request.form.get('numero-documento', False)
	contrasena = request.form.get('contrasena', False)
	correo = request.form.get('correo', False)
	num_celular = request.form.get('celular', False)
	confirm_contrasena = request.form.get('verificar-contrasena', False)

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
		foto_perfil = '010101'
		fecha_creac = datetime.now()
		while not verificado:
			ID_usuario = uuid.uuid4()
			SQL = ConexionSQLServer(desktop, bbdd)
			SQL.setNombreUsuario(usuario)
			SQL.setCorreo(correo)
			if SQL.encontrarNombreUsuario() is not None:
				msg = 'Ese nombre de usuario ya existe'
				return redirect(url_for('registroUsuario'))
			
			if SQL.encontrarCorreo() is not None:
				msg = 'Ese correo ya está registrado'
				return redirect(url_for('registroUsuario'))
			
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
		SQL = ConexionSQLServer(desktop, bbdd)
		SQL.setLoginUsuario(correo, contrasena)
		if SQL.autenticarUsuario() != None:
			datos_usuario = SQL.devolverUsuario()
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
			motivo = request.form.getlist('categoria')
			fecha = request.form.get('fechaHechos', False)
			descripcion = request.form.get('descripcionHechos', False)
			archivo = request.files.get('archivosHechos', False)
			anonimo = request.form.get('anonimo', False)
			if request.method == 'POST':
				fecha_creac = datetime.now()
				relevancia = 0
				while not verificado:
					ID_publicacion = uuid.uuid4()
					SQL = ConexionSQLServer(desktop, bbdd)
					SQL.setUUIDPublicacion(ID_publicacion)
					motivo_limpio = ''
					if anonimo == '1':
						relevancia = 1
					else:
						relevancia = 0
					for motivos in motivo:
						if motivo_limpio=='':
							motivo_limpio = motivos
						else:
							motivo_limpio = motivo_limpio + " - " + motivos
					if SQL.encontrarUUIDPublicacion() == None:
						estatus = 'ESPERA'
						array = (str(ID_publicacion), motivo_limpio, descripcion, session['ID_usuario'], fecha, fecha_creac, relevancia, estatus)
						print(array)
						if archivo.filename.endswith(".png"):
							SQL.setDatosPublicacion(array)
							SQL.insertarDenuncia()
							PATH_PUBLICACION = str(ID_publicacion)
							NEW_PATH = os.path.join(PATH_FILE, PATH_PUBLICACION)
							os.mkdir(NEW_PATH)
							FINAL_PATH = os.path.join(NEW_PATH, PATH_PUBLICACION + '.png')
							archivo.save(FINAL_PATH)
							msg = 'Registrado con éxito'
							verificado = True
						else:
							msg = 'El archivo que suba debe ser png'
							return render_template('registrarDenuncia.html')
			return render_template('registrarDenuncia.html')
	except KeyError:
		msg = 'Para acceder a esta página debes iniciar sesión'
		return redirect(url_for('loginUsuario'))
	

@app.route('/seguimiento-denuncia/', methods = ['GET', 'POST'])
def seguimientoDenuncia():
	msg = ''
	return render_template('seguimientoDenuncia.html') 

@app.route('/admin/', methods = ['GET', 'POST'])
def admin():
	msg = ''
	verificado = False
	try:
		if session['logged'] == True and session['admin'] == 1:
			SQL = ConexionSQLServer(desktop, bbdd)
			datos = SQL.mostrarTabla()

			return render_template('admin.html', datos=datos)
	except KeyError:
		msg = 'Para acceder a esta página debes contactar al servicio de atención'
		return redirect(url_for('loginUsuario'))

@app.route('/actualizar-estatus', methods=['POST'])
def actualizar_estatus():
    public_id = request.form.get('publicID')
    new_status = request.form.get('newStatus')

    # Llama a la función para actualizar el estatus
    SQL = ConexionSQLServer(desktop, bbdd)
    exito = SQL.actualizarEstatusPublicacion(public_id, new_status)

    if exito:
        return 'Actualización exitosa'
    else:
        return 'Error al actualizar el estatus'
	
if __name__ == '__main__':
	app.run(debug = True)
