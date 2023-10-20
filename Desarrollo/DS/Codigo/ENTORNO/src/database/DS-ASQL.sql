--Creaci�n de la base de dato(ejecutar solo una vez)
CREATE DATABASE DB_DenunciaSeguro
--Utilizar siempre que se quiera usar la base de datos de DenunciaSeguro
USE DB_DenunciaSeguro

--Creaci�n de las tablas(ejecutar solo una vez)
-- Tabla de Usuarios
CREATE TABLE Usuario (
    ID_Usuario VARCHAR(50) PRIMARY KEY,
    Nombre VARCHAR(50),
    Apellido VARCHAR(80),
    TipoDocumento VARCHAR(30),
    NDocumento VARCHAR(10),
    NombreDeUsuario VARCHAR(35) UNIQUE,
    Contrasena VARCHAR(255),
    Correo VARCHAR(255),
    NumeroDeCelular VARCHAR(9),
    Administrador BIT,  -- Campo que indica si el usuario es administrador (true=1/false=0)
    FotoPerfil VARCHAR(255), -- Agregar (DEFAULT 'URL_de_la_imagen_predeterminada',) cuando tengamos el link de la imagen predise�ada
    FechaCreacion DATETIME
);
-- Tabla Publicacion
CREATE TABLE Publicacion (
    ID_Publicacion VARCHAR(50) PRIMARY KEY,
    MotivosDenuncia VARCHAR(255),
    Descripcion TEXT,
    ID_Usuario VARCHAR(50),  -- Referencia al ID del usuario que cre� la publicaci�n
    FechaDenuncia DATE,
    FechaCreacion DATETIME,
    Relevancia INT DEFAULT 0,
    FOREIGN KEY (ID_Usuario) REFERENCES Usuario(ID_Usuario)
);
-- Tabla de Im�gen (asociada a las publicaciones)
CREATE TABLE Imagen (
    ID_Imagen VARCHAR(50) PRIMARY KEY,
    URLImagen VARCHAR(255),
    ID_Publicacion VARCHAR(50),
    FOREIGN KEY (ID_Publicacion) REFERENCES Publicacion(ID_Publicacion)
);
-- Tabla de Comentarios
CREATE TABLE Comentarios (
    ID_Comentario  VARCHAR(50) PRIMARY KEY,
    TextoComentario TEXT,
    ID_Usuario VARCHAR(50),
    ID_Publicacion VARCHAR(50),
    FechaCreacion DATE,
    FOREIGN KEY (ID_Usuario) REFERENCES Usuario(ID_Usuario),
    FOREIGN KEY (ID_Publicacion) REFERENCES Publicacion(ID_Publicacion)
);

-- INSERT INTO Publicacion(ID_Publicacion, MotivosDenuncia, Descripcion, ID_Usuario, FechaDenuncia, FechaCreacion, Relevancia) VALUES('3862d1dc-add8-49d9-bb64-793fe766cf29', ' - Corrupción - Abuso de poder - Seguridad Ciudadana', 'xddd', '1203120', '2022-02-22', '2023-10-20 16:42:46', 0);