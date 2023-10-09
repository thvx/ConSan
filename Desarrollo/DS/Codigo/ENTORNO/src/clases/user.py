class User:
    def __init__(self, datos_usuario):
        self.ID_usuario = datos_usuario[0]
        self.nombre = datos_usuario[1]
        self.apellido = datos_usuario[2]
        self.DNI = datos_usuario[3]
        self.usuario = datos_usuario[4]
        self.correo = datos_usuario[6]
        self.direccion = datos_usuario[7]
        self.celular = datos_usuario[8]
        self.admin = datos_usuario[9]
        self.foto_perfil = datos_usuario[10]