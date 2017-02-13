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

Creamos el fichero herencia_model.py
~~~  
from openerp import models, fields, api
class HerenciaModel(models.Model):
    _inherit = 'aplicacionejemplo01.task''
    user_id = fields.Many2one('res.users', 'Responsible')
    date_deadline = fields.Date('Deadline')

~~~   

En __init__.py
~~~   
from . import herencia_model
~~~   

# Modificar los campos existentes  
Para modificar un campo existente agregaremos un campo con el mismo nombre, y configurando los valores de los atributos que serán modificados.  

Por ejemplo, para agregar un comentario de ayuda a un campo name, podríamos agregar esta línea en el archivo herencia_model.py:

name = fields.Char(help="Campo modificado")  


# Modificar los métodos del modelo  
Para agregar métodos nuevos se declararán las funciones dentro de la clase heredada.

Para ampliar la lógica existente, un método puede ser sobreescrito declarando otro método con el mismo nombre, y el método nuevo reemplazará al anterior. Pero este puede extender el código de la clase heredada, usando la palabra clave de Python super() para llamar al método padre.  

Es mejor evitar cambiar la función distintiva del método (esto es, mantener los mismos argumentos) para asegurarnos que las llamadas a este sigan funcionando adecuadamente.

La acción original de Clear All Done ya no es apropiada para nuestro módulos de tareas compartidas, ya que borra todas las tareas sin importar a quien le pertenecen. Necesitamos modificarla para que borre solo las tareas del usuario actual.

Para esto, se sobreescribirá el método original con una nueva versión que primero encuentre las tareas completadas del usuario actual, y luego las desactive:
~~~   
@api.multi
def do_clear_done(self):
    domain = [('is_done', '=', True), '|', ('user_id', '=', self.env.uid), ('user_id', '=', False)]
    done_recs = self.search(domain)
    done_recs.write({'active': False})
    return True
~~~       
Primero se listan los registros finalizados sobre los cuales se usa el método search con un filtro de búsqueda. El filtro de búsqueda sigue una sintaxis especial de Odoo referida como domain.

El filtro "domain" usado es definido en la primera instrucción: es una lista de condiciones, donde cada condición es una tupla.

Estas condiciones son unidas implícitamente con un operador AND (& en la sintaxis de dominio). Para agregar una operación OR se usa una "tubería" (|) en el lugar de la tupla, y afectara las siguientes dos condiciones.   
El dominio usado aquí filtra todas las tareas finalizadas('is_done', '=', True) que también tengan al usuario actual como responsable ('user_id','=',self.env.uid) o no tengan fijado un usuario ('user_id', '=', False).

Lo que acabamos de hacer fue sobrescribir completamente el método padre, reemplazándolo con una implementación nueva.  

Pero esto no es lo que usualmente querremos hacer. En vez de esto, ampliaremos la lógica actual y agregaremos operaciones adicionales. De lo contrario podemos dañar operaciones existentes. La lógica existente es insertada dentro de un método sobrescrito usando el comando super() de Python para llamar a la versión padre del método.  

Veamos un ejemplo de esto: podemos escribir una versión mejor de do_toggle_done() que solo ejecute la acción sobre las Tareas asignadas a nuestro usuario:  
~~~   
@api.one
def do_toggle_done(self):
    if self.user_id != self.env.user:
        raise Exception('Only the responsible can do this!')
    else:
        return super(TodoTask, self).do_toggle_done()
~~~           
