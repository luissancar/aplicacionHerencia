# Ejemplo Herencia Odoo  
- Crearemos la estructura básica para el módulo.
__openerp__.py  :  
~~~  
{
    'name': 'Herencia aplicacionEjemplo01',
    'description': 'Herencia.',
    'author': 'luissancar',
    'depends': ['aplicacionEjemplo01'],
}

~~~   
__init.__py  (en principio vacio)  

Instalamos la aplicación.  

# Ampliando el modelo  
Los modelos nuevos son definidos a través de las clases Python. Ampliarlos también es hecho a través de las clases Python, pero usando un mecanismo específico de Odoo.

Para aplicar un modelo usamos una clase Python con un atributo __inherit. Este identifica el modelo que será ampliado. La clase nueva hereda todas las características del modelo padre, y solo necesitamos declarar las modificaciones que queremos introducir.


Para modificar un modelo de Odoo obtenemos una referencia a la clase de registro y luego ejecutamos los cambios en ella. Esto significa que esas modificaciones también estarán disponibles en cualquier otro lado donde el modelo sea usado.

