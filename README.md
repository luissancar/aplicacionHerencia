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


# Ampliar las vistas  
Debemos localizar los elementos XML y luego introducir modificaciones en esos puntos. 
Una vista heredada se ve así:  

~~~  

<record id="view_form_herencia_inherited" model="ir.ui.view">
              <field name="name">Herencia aplicacion</field>
              <field name="model">aplicacionejemplo01.task</field>  //modelo del padre
              <field name="inherit_id" ref="aplicacionEjemplo01.view_form_aplicacion_ejemplo01_task"/>
              <field name="arch" type="xml">
                <field name="name" position="after">
                  <field name="user_id" />
                </field>..........
              </field>
          </record>
          ~~~  
El campo inherit_id identifica la vista que será ampliada, a través de la referencia de su identificador externo usando el atributo especial ref. 


Tener atributos "name" en los elementos es importante porque los hace mucho más fácil de seleccionar como puntos de extensión. Una vez que el punto de extensión es localizado, puede ser modificado o puede tener elementos XML agregados cerca de él.  

Para agregar el campo date_deadline antes del campo is_done, debemos escribir:  
~~~  
<field name="is_done" position="before">
    <field name="date_deadline" />
</field>
~~~  
Agregar campos nuevos, cerca de campos existentes es hecho frecuentemente, por lo tanto la etiqueta <field> es usada frecuentemente como el localizador.   

El atributo de posición usado con el elemento localizador es opcional, y puede tener los siguientes valores: - after: Este es agregado al elemento padre, después del nodo de coincidencia. - before: Este es agregado al elemento padre, antes del nodo de coincidencia. - inside (el valor predeterminado): Este es anexado al contenido del nodo de coincidencia. - replace: Este reemplaza el nodo de coincidencia. Si es usado con un contenido vacío, borra un elemento. - attributes: Este modifica los atributos XML del elemento de coincidencia (más detalles luego de esta lista).  

La posición del atributo nos permite modificar los atributos del elemento de coincidencia. Esto es hecho usando los elementos   
~~~  
<attribute name="attr-name"> con los valores del atributo nuevo.
~~~  
En el formulario de Tareas, tenemos el campo Active, pero tenerlo visible no es muy útil. Quizás podamos esconderlo de la usuaria y el usuario. Esto puede ser realizado configurando su atributo invisible:  

~~~  
<field name="active" position="attributes">
    <attribute name="invisible">1<attribute/>
</field>
~~~  
Configurar el atributo invisible para esconder un elemento es una buena alternativa para usar el localizador de reemplazo para eliminar nodos. Debería evitarse la eliminación, ya que puede dañar las extensiones de modelos que pueden depender del nodo eliminado.  

Finalmente, podemos poner todo junto, agregar los campos nuevos, y obtener la siguiente vista heredada completa para ampliar el formulario de tareas por hacer:  
~~~  

<?xml version="1.0" encoding="UTF-8"?>
    <openerp>
        <data>
          <record id="view_form_herencia_inherited" model="ir.ui.view">
              <field name="name">Herencia aplicacion</field>
              <field name="model">aplicacionejemplo01.task</field>
              <field name="inherit_id" ref="aplicacionEjemplo01.view_form_aplicacion_ejemplo01_task"/>
              <field name="arch" type="xml">
                <field name="name" position="after">
                  <field name="user_id" />
                </field>
                <field name="is_done" position="before">
                  <field name="date_deadline" />
                </field>
                <field name="name" position="attributes">
                  <attribute name="string">I have to…</attribute>
                </field>
              </field>
          </record>
        </data>
    </openerp>

~~~  
Esto debe ser agregado al archivo herenciaview.xml en nuestro módulo  
Debemos agregar el atributo datos al archivo descriptor __openerp__.py:  
~~~  
'data': ['herenciaview.xml'],
~~~  






###### http://fundamentos-de-desarrollo-en-odoo.readthedocs.io/es/latest/capitulos/herencia-extendiendo-funcionalidad-aplicaciones-existentes.html
