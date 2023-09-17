from flask import Flask, request, render_template
import pyodbc
import uuid
import random

class ConexionSQLServer:
    def __init__(self, servidor, base_de_datos, nombre_usuario, contrasena):
        self.server = servidor
        self.database = base_de_datos
        self.username = nombre_usuario
        self.password = contrasena
        self.conex = None

    def establecerConexion(self):
        try:
            # Establece la conexión
            self.conex = pyodbc.connect(f'DRIVER={{SQL Server}};'f'SERVER={self.server};'f'DATABASE={self.database};'f'UID={self.username};'f'PWD={self.password};')
            return self.conn
        except Exception as e:
            print(f"Error al establecer la conexión con la base de datos: {str(e)}")
            return None

    def cerrarConexion(self):
        if self.conex:
            self.conex.close()
'''
MODO DE USO DE LA CLASE ConexionSQLServer

# Crear una instancia de la clase ConexionSQLServer
conexion_sql = ConexionSQLServer(
    servidor='tu_servidor_sql',
    base_de_datos='tu_base_de_datos',
    nombre_usuario='tu_usuario',
    contrasena='tu_contraseña'
)

# Establecer la conexión

conex = conexion_sql.establecerConexion()
if conex:
    # Realizar operaciones de base de datos aquí
    cursor = conex.cursor()
    cursor.execute("SELECT * FROM tu_tabla")
    ..............

    # Cerrar la conexión cuando haya terminado
#   conexion_sql.cerrarConexion()
'''

app = Flask(__name__)

@app.route('/')
def inicio():
	return render_template('index.html')

@app.route('/registro-usuario', methods = ['GET','POST'])
def registroUsuario():
	msg = ''
	erroneo = False
	if request.method == 'POST':
		nombre = request.form['nombre']
		apellidos = request.form['apellidos']
		DNI = request.form['DNI']
		usuario = request.form['usuario']
		correo = request.form['correo']
		direccion = request.form['direccion']
		num_celular = request.form['num_celular']
		administrador = request.form['administrador']
		foto_perfil = request.form['foto_perfil']
		fecha_creac = request.form['fecha_creac']
		contrasena = request.form['contrasena']
		datos_esenciales = (nombre, apellidos)
		for dato_esencial in datos_esenciales:
			if dato_esencial.isdigit():
				erroneo = True
		if not erroneo:
			ID_usuario = uuid.uuid4()
			msg = 'Registro con éxito'
			# *********************************************************************************************
			# A partir de aquí se realiza la conexión a DB para mandar los datos a la tabla correspondiente
			# *********************************************************************************************
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
	# ******************************************************************************************************
	# Aquí se debe validar con la BBDD y permitir el acceso a la plataforma en caso los datos sean correctos.
	# ******************************************************************************************************
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