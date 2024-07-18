"# dash_app_pali" 

Se modificó la estructura del programa, ahora
está separado en 3 carpetas:

- callbacks: es la carpeta que contiene un archivo de callback por cada conjunto de páginas
- pages: contiene la estructura y elementos de las páginas 
- utils: guarda archivos con funciones auxiliares que se utilizan en el resto de la página.

Esta estructura debería permitir tener más ordenadas las cosas.

# Agregados desde la ultima version
## Paginas
- Páginas de Fourier transform with sliding window: Permite seleccionar un valor constante en una de las dimensiones,
valor de comienzo, fin, tamaño de ventana y paso de ventana. Realiza la FFT en la ventana móvil y muestra amplitud y fase
(como desventaja los tiempos de actualización de la página son lentos y podría complicar la interactividad de la misma).
Al 25-8-20223 funciona con los tiempos setteados en mi pc, habría que probar cómo lo ves vos pali, en local y en el server.


- Página para cargar datos propios: permite cargar los datos propios, seleccionar rango de B, valor de V y ver Traza y 
transformada, además de la reconstrucción. Tiene un toggle que permite elegir el barrido ascendente o  descendente en B
Permite descargar los datos

## Modificaciónes en páginas existentes
- Se modifico la interacción de los slide-bars en grafico 3d ahora el pajama plot y el 3d están linkeados (se modifican juntos)
- Se agregaron en las páginas botones de descarga que permiten obtener lso datos procesados y mostrados en pantalla.



# Pendientes al 25-8-2023 [prioridad]: 
    [1] -verificar los nuevos tipos de datos.
    
    [99]-generar video de la visualización de fourier con los rangos setteados,
    la idea es poder descargarlo a posteriori si es necesario darle tiempo de procesamiento

    [500]- Quiero modificar la página de 3d plot a ver si se puede optimizar un poco para que sea viable en servidor.

