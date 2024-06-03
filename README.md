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

