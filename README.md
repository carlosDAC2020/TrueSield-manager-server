# Fake News Detector

Detector de noticias falsas usando inteligencia artificail 

## Requerimientos
- ***Adicion de medios:*** gestion(CRUD) de  medios de comunicacion y sus correspondientes RSS para la iptencion den noticias (***Admin***) .
- ***Obtencion y validacion de prompt:*** al usuario ingresar el prompt de una noticia este se debe vaidar en el siguiente orden.
    1. Obtencion del prompt por formulario.
    2. Validar si es un titular o un comentario (***IA***).
    3. Separacion del prompt en palabras clave (***IA***).
    4. Busqueda de palabras clave en noticias recientes.
    5. Retorno de resultados de evaliacion.


envio de items 

items | vaids | apis activas |  tiempo
  100 |    1  |      3       | 17.4033
  200 |    1  |      3       | 25.0467
  300 |    1  |      3       | 34.3806
  400 |    1  |      3       | 42.9203
  500 |    1  |      3       | 49.1278
