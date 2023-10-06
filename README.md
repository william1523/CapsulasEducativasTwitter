# CapsulasEducativasTwitter


Este software tiene como meta aportar a la creación de guiones de cápsulas educativas que,

aporten a la formación de la población; para esto, se creó un modelo que, permite obtener datos de la red social Twitter

/ X mediante un proceso de automatización de búsquedas, las cuales se realizan sobre la página web de Twitter usando

Selenium Web Driver. Una vez obtenidos los datos, se realiza el proceso de limpieza y pre-procesamiento; los datos

limpios se procesan con el modelo de asignación latente de Dirichlet (LDA) para obtener las palabras claves;

finalmente, usando el modelo “text-davinci-003” de GPT-3 mediante el API de OpenAI, se realiza la generación de

contenido para la cápsula educativa; para lo cual, se asigna un contexto, y el uso de las palabras clave identificadas.

## Requerimientos:

-   Contar con cuenta en Twitter (https://twitter.com/)
-   Registrarse en OpenAI, para poder usar su API se requiere el token asignado (<https://chat.openai.com/auth/login>)
-   Python 3.9 o superior
-   Navegador Google Chrome

## Requerimientos de Software

Este software fue desarrollado en Python usando el framework django. Fue desarrollado con Python 3.9, por lo que se recomienda esta misma versión o una superior.

Una vez descargado las fuentes, se recomienda crear un entorno virtual, puede hacerlo mediante un comando similar al siguiente: python -m venv envcap (<https://docs.python.org/3/library/venv.html>)

Activar el entorno virtual, ejemplo .\\envcap\\Scripts\\Activate.ps1

Instalar las dependencias del proyecto, pude usar el comando python -m pip install -r .\\requirements.txt

Luego instalar modelo de spacy requerido con el comando: python -m spacy download es_core_news_sm

Definir credenciales para poder realizar búsquedas de twitter en la línea 139, del archivo models.py ubicado en la ruta CapsulasEducativasTwitter\\twitter debe reemplazar los textos “usuario” y “clave” con el nombre de usuario y contraseña que se usa para el inicio de sesión en Twitter.

c=searchBySelenium(usr="usaurio",pwd="clave")

Definir key para uso de api de OpenApi, se debe ubicar el archivo CapsulasEducativasTwitter\\twitter\\util\\openaiapi.py e ingresar el key proporcionado en la línea 14

openai.api_key = '' \#introducir OPENAI_API_KEY

Ejecutar el software con el comando

python.exe .\\manage.py runserver --insecure

.
