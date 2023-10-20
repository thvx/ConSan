import pyodbc

class ConexionSQLServer:
    def __init__(self, servidor, base_de_datos):
        self.server = servidor
        self.database = base_de_datos
        self.conex = None

    def establecerConexion(self):
        try:
            self.conex = pyodbc.connect('DRIVER={SQL Server};'f'SERVER={self.server};'f'DATABASE={self.database}; Trusted_Connection=yes;')
        except Exception as e:
            print(f"Error al establecer la conexión con la base de datos: {str(e)}")
            return None
        
    def cerrarConexion(self):
        if self.conex:
            self.conex.close()
        
    def setDatosUsuario(self, datos):
        self.datos_usuario = datos
        
    def insertarUsuario(self):
        self.establecerConexion()
        if self.conex:
            cursor = self.conex.cursor()
            cursor.execute("INSERT INTO Usuario (ID_Usuario, Nombre, Apellido, TipoDocumento, NDocumento, NombreDeUsuario, Contrasena, Correo, NumeroDeCelular, Administrador, FotoPerfil, FechaCreacion) VALUES (?,?,?,?,?,?,?,?,?,?,?,?);", self.datos_usuario)
            cursor.commit()
            self.cerrarConexion()
    
    def setUUIDUsuario(self, UUID):
        self.UUID_usuario = UUID
    
    def encontrarUUIDUsuario(self):
        self.establecerConexion()
        if self.conex:
            cursor = self.conex.cursor()
            cursor.execute(f"SELECT ID_Usuario FROM Usuario WHERE ID_Usuario='{self.UUID_usuario}';")
            encontrado_usuario = cursor.fetchone()
            self.cerrarConexion()
            return encontrado_usuario
    
    def setLoginUsuario(self, correo, contrasena):
        self.correo = correo
        self.contrasena = contrasena

    def autenticarUsuario(self):
        self.establecerConexion()
        if self.conex:
            cursor = self.conex.cursor()
            cursor.execute(f"SELECT Correo, Contrasena FROM Usuario WHERE Correo='{self.correo}' AND Contrasena='{self.contrasena}';")
            esencial_usuario = cursor.fetchone()
            self.cerrarConexion()
            return esencial_usuario

        
    def devolverUsuario(self):
        try:
            self.establecerConexion()
            if self.conex:
                cursor = self.conex.cursor()
                cursor.execute(f"SELECT * FROM Usuario WHERE Correo='{self.correo}' AND Contrasena='{self.contrasena}';")
                datos_usuario = cursor.fetchone()
                self.cerrarConexion()
                return datos_usuario
        except:
            print(f"Error al establecer la conexión con la base de datos.")
            return None
        
        
    def setUUIDPublicacion(self, UUID):
        self.UUID_publicacion = UUID
        
    def encontrarUUIDPublicacion(self):
            self.establecerConexion()
            if self.conex:
                cursor = self.conex.cursor()
                cursor.execute(f"SELECT ID_Publicacion FROM Publicacion WHERE ID_Publicacion='{self.UUID_publicacion}';")
                encontrado_publicacion = cursor.fetchone()
                self.cerrarConexion()
                return encontrado_publicacion
        
    def setDatosPublicacion(self, datos):
        self.datos_publicacion = datos
    
    def insertarDenuncia(self):
            self.establecerConexion()
            if self.conex:
                cursor = self.conex.cursor()
                cursor.execute("INSERT INTO Publicacion(ID_Publicacion, MotivosDenuncia, Descripcion, ID_Usuario, FechaDenuncia, FechaCreacion, Relevancia) VALUES(?,?,?,?,?,?,?);", self.datos_publicacion)
                cursor.commit()
                self.cerrarConexion()
    
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