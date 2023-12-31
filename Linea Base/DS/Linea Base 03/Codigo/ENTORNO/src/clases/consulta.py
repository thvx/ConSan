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
    
    def setNombreUsuario(self, usuario):
        self.usuario = usuario

    def encontrarNombreUsuario(self):
        self.establecerConexion()
        if self.conex:
            cursor = self.conex.cursor()
            cursor.execute(f"SELECT NombreDeUsuario FROM Usuario WHERE NombreDeUsuario='{self.usuario}';")
            encontrado_usuario = cursor.fetchone()
            self.cerrarConexion()
            return encontrado_usuario
        
    def setCorreo(self, correo):
        self.correo = correo

    def encontrarCorreo(self):
        self.establecerConexion()
        if self.conex:
            cursor = self.conex.cursor()
            cursor.execute(f"SELECT Correo FROM Usuario WHERE Correo='{self.correo}';")
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
                cursor.execute("INSERT INTO Publicacion(ID_Publicacion, MotivosDenuncia, Descripcion, ID_Usuario, FechaDenuncia, FechaCreacion, Relevancia, Estatus) VALUES(?,?,?,?,?,?,?, ?);", self.datos_publicacion)
                cursor.commit()
                self.cerrarConexion()
    
    def mostrarTabla(self):
            self.establecerConexion()
            if self.conex:
                cursor = self.conex.cursor()
                cursor.execute("SELECT P.ID_Publicacion, U.Nombre + ' ' + U.Apellido AS Nombre, P.MotivosDenuncia, P.FechaDenuncia, P.Estatus FROM Publicacion P INNER JOIN Usuario U ON P.ID_Usuario = U.ID_Usuario;")
                datos = cursor.fetchall()
                self.cerrarConexion
                return datos

    def datosDenuncia(self):
        return None
      
    def actualizarEstatusPublicacion(self, id_publicacion, nuevo_estatus):
        self.establecerConexion()
        if self.conex:
            cursor = self.conex.cursor()
            try:
                cursor.execute("UPDATE Publicacion SET Estatus = ? WHERE ID_Publicacion = ?", (nuevo_estatus, id_publicacion))
                self.conex.commit()  # Confirmar la actualización en la base de datos
                return True
            except Exception as e:
                print(f"Error al actualizar el estatus de la publicación: {str(e)}")
                return False
            finally:
                self.cerrarConexion()
        return False

    def obtenerDenunciasPrincipales(self):
             self.establecerConexion()
             if self.conex:
                 cursor = self.conex.cursor()
                 cursor.execute("SELECT TOP 3 * FROM Publicacion;")
                 denuncias_principales = cursor.fetchall()
                 self.cerrarConexion()
                 return denuncias_principales
             
    def obtenerDenunciasUsuario(self, usuario_id):
             self.establecerConexion()
             if self.conex:
                 cursor = self.conex.cursor()
                 cursor.execute("SELECT MotivosDenuncia, Descripcion, Estatus FROM Publicacion WHERE ID_Usuario = ?;", usuario_id)
                 denuncias_usuario = cursor.fetchall()
                 self.cerrarConexion()
                 return denuncias_usuario
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