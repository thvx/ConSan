import pyodbc

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
        
    def getDatosUuario(self, datos):
        self.datos_usuario = datos
        
    def insertarUsuario(self):
        try:
            conex = self.establecerConexion()
            if conex:
                cursor = conex.cursor()
                cursor.execute("INSERT INTO Usuario(ID_Usuario, Nombre, Apellido, DNI, NombreDeUsuario, Contrasena, Correo, Direccion, NumeroDeCelular, Administrador, FotoPerfil, FechaCreacion) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)", self.datos_usuario)
                cursor.commit()
                self.cerrarConexion()
        except:
            print(f"Error al establecer la conexión con la base de datos: {str(e)}")
            return None
    
    def getUUID(self, UUID):
        self.UUID = UUID
    
    def encontrarUUID(self):
        try:
            conex = self.establecerConexion()
            if conex:
                cursor = conex.cursor()
                cursor.execute(f"SELECT ID_Usuario FROM Usuario WHERE ID_USUARIO = {self.UUID}")
                encontrado = cursor.fetchone()
                self.cerrarConexion()
                return encontrado
        except:
            print(f"Error al establecer la conexión con la base de datos: {str(e)}")
            return None
    
    def getLoginUsuario(self, correo, contrasena):
        self.correo = correo
        self.contrasena = contrasena

    def autenticarUsuario(self):
        try:
            conex = self.establecerConexion()
            if conex:
                cursor = conex.cursor()
                cursor.execute(f"SELECT Correo, Contrasena FROM Usuario WHERE Correo = {self.correo} AND Contrasena = {self.contrasena}")
                datos_usuario = cursor.fetchone()
                self.cerrarConexion()
                return datos_usuario
        except:
            print(f"Error al establecer la conexión con la base de datos: {str(e)}")
            return None
    
    def registrarDenuncia(self):
        return None
    
    def buscarDenuncia(self):
        return None
    
    def datosDenuncia(self):
        return None

    
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