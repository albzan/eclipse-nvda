# Eclipse Enhance
Este complemento para NVDA ofrece un soporte mejorado mientras se trabaja con el entorno de desarrollo Eclipse.

## Características del complemento:
### Características principales:
* Reproduce sonidos diferentes mientras usas el atajo **ctrl+. (punto)** de Eclipse para identificar si hay seleccionada una advertencia o un error.
* Reproduce sonidos diferentes cuando pulsas **ctrl+s** para indicar si el archivo guardado contiene errores o advertencias.
* Anuncia la conmutación de puntos de ruptura (breakpoints) mientras se pulsa **ctrl+shift+b**.

### Características adicionales de Braille:
* Muestra mensajes braille si el archivo guardado contiene errores o advertencias;
* Soluciona un problema que impide usar la tecla de retroceso de la pantalla braille para ir a la línea anterior

### Características de voz adicionales:
* Anuncia la línea actual mientras te desplazas con las teclas de depuración
* Anuncia la línea actual cuando pulsas ctrl+. y el cursor se mueve.
* Anuncia la línea actual al pulsar ctrl+shift+flechas arriba y abajo para saltar al método anterior o al siguiente
* Anuncia la línea actual al pulsar ctrl+shift+p teniendo seleccionado un paréntesis: este atajo salta al paréntesis correspondiente de apertura o de cierre

## Configuración de Eclipse
Para aprovechar todas las ventajas que te ofrece este complemento, tienes que configurar Eclipse para que resalte las advertencias y los errores en lugar de subrayarlos.
Para hacerlo, sigue estos pasos:

* Abre el entorno Eclipse
* Abre el menú Window (alt+w)
* Elige el elemento "Preferences"
* Navega a la presentación en árbol
* Navega a General, Editors, Text Editors, Anotations
* Pulsa tabulador para moverte a la lista de anotaciones

En cada anotación puedes elegir:

* Tres casillas de verificación (Vertical ruler, Overview ruler y Text As)
* Un cuadro combinado que indica cómo se presenta la anotación en el texto (disponible cuando se ha marcado la casilla Text As).

Configura las anotaciones de la siguiente manera::

* **Breackpoints**: casilla Text As marcada, y opción "highlighted" del cuadro combinado.
* **Errors**: casilla Text As marcada, y opción “highlighted” del cuadro combinado.
* **Info**: casilla Text As desmarcada
* **Matching tags**: casilla Text As desmarcada
* **Occurrences**: casilla Text As desmarcada
* **Search Results**: casilla Text As desmarcada
* **Warnings**: casilla Text As marcada, y opción “highlighted” del cuadro combinado.


## Derechos de copia de los sonidos
Los sonidos usados para indicar advertencias y errores están cubiertos por la licencia Creative Commons.

* [Visita esta página para el sonido de error](https://www.freesound.org/people/Autistic%20Lucario/sounds/142608/)
* [Visita esta página para el sonido de advertencia](https://www.freesound.org/people/ecfike/sounds/135125/)


## Autores:
* Alberto Zanella
* Alessandro Albano

