--Creaci�n de la base de dato(ejecutar solo una vez)
CREATE DATABASE DB_DenunciaSeguro
--Utilizar siempre que se quiera usar la base de datos de DenunciaSeguro
USE DB_DenunciaSeguro

--Creaci�n de las tablas(ejecutar solo una vez)
-- Tabla de Usuarios
CREATE TABLE Usuario (
    ID_Usuario INT PRIMARY KEY,
    Nombre VARCHAR(50),
    Apellido VARCHAR(80),
    DNI VARCHAR(8),
    NombreDeUsuario VARCHAR(35) UNIQUE,
    Contrasena VARCHAR(20),
    Correo VARCHAR(255),
    Direccion VARCHAR(255),
    NumeroDeCelular VARCHAR(9),
    Administrador BIT,  -- Campo que indica si el usuario es administrador (true=1/false=0)
    FotoPerfil VARCHAR(255), -- Agregar (DEFAULT 'URL_de_la_imagen_predeterminada',) cuando tengamos el link de la imagen predise�ada
    FechaCreacion DATE
);
-- Tabla Publicacion
CREATE TABLE Publicacion (
    ID_Publicacion INT PRIMARY KEY,
    TituloDePublicacion VARCHAR(150),
    Descripcion TEXT,
    ID_Usuario INT,  -- Referencia al ID del usuario que cre� la publicaci�n
    FechaCreacion DATE,
    Relevancia INT DEFAULT 0,
    FOREIGN KEY (ID_Usuario) REFERENCES Usuario(ID_Usuario)
);
-- Tabla de Im�gen (asociada a las publicaciones)
CREATE TABLE Imagen (
    ID_Imagen INT PRIMARY KEY,
    URLImagen VARCHAR(255),
    ID_Publicacion INT,
    FOREIGN KEY (ID_Publicacion) REFERENCES Publicacion(ID_Publicacion)
);
-- Tabla de Comentarios
CREATE TABLE Comentarios (
    ID_Comentario  INT PRIMARY KEY,
    TextoComentario TEXT,
    ID_Usuario INT,
    ID_Publicacion INT,
    FechaCreacion DATE,
    FOREIGN KEY (ID_Usuario) REFERENCES Usuario(ID_Usuario),
    FOREIGN KEY (ID_Publicacion) REFERENCES Publicacion(ID_Publicacion)
);