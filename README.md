# Análisis de datos de YouTube
![subtitulo-removebg-preview](https://github.com/mram23/Proyecto-Ingenieria-de-Datos-YouTube/assets/132526921/e58ecb1f-7c29-4ee3-85dc-054d0ccc5c7e)

Si eres un apasionado del mundo de los datos o buscas tu entrada en este campo, este proyecto es tu puerta de acceso. Descubre el camino hacia nuevas oportunidades.
------------
Empecemos contextualizando la problemática y por qué se desarrolla este proyecto:
Tenemos un cliente que quiere llevar a cabo una campaña de marketing online y han decidido que su principal canal de publicidad será YouTube. Esto debido a que YouTube se encuentra en el top de sitios web más visitados en el mundo. Pero antes de invertir en la campaña, se requiere profundizar en los siguiente puntos:
- ¿Cómo clasificar los videos en función de sus comentarios y otras métricas?
- ¿Qué factores influyen en la popularidad de un video de YouTube?

> Nota:
YouTube utiliza la interacción de los usuarios para denomiar a un video como ***Tendencia***. Esto involucra variables como el número de visitas, cuántas veces el video ha sido compartido, la cantidad de comentarios y likes del video.

### Cómo desarrollaremos este proyecto
1. Nos encargaremos de la ingesta de datos, en este caso utilizaremos como fuente de datos el siguiente dataset [Trending YouTube Video Stadistics](https://www.kaggle.com/datasets/datasnaek/youtube-new?select=CA_category_id.json)
2. Al tener nuestra _data cruda_ lo que haremos es el pre-procesamiento. Para ello utilizaremos una función Lambda, y nos ayudaremos de un _ETL Job_ que nos permitirá construir un Flujo ETL para automatizar la _extracción, transformación y carga_ de la data a un Data Lake en buckets de AWS S3.
3. Finalmente, mostraremos los _insights_ más relevantes mediante un dashboard en AWS QuickSight.
> Nota:
Podemos entender un Data Lake como un repositorio centralizado donde almacenamos toda nuestra data, ya estructurada o no estructurada. En nuestro caso, el Data Lake que formaremos estará conformada por la _data cruda_, _data limpia_ y _data para análisis_.

#### Primer paso: Ingesta de Datos
> Nota:
Es conveniente como buena prácticar crear un usuario IAM con el permiso _AdministratorAccess_ y utilizarlo enves del logeo con la cuenta raíz. Asimismo, por cuestiones de seguridad se recomienda activar la autenticación multifactor (MFA).

Utilizando la interfaz de línea de comandos (AWS CLI), cargaremos nuestro dataset de Kaggle en el bucket de AWS S3 llamado _project-youtube-raw-useast1_. Esto mediante los siguientes comandos:
```python3
# Para copiar todos los datos de referencia JSON en la misma ubicación:
aws s3 cp . s3://project-youtube-raw-useast1/youtube/raw_statistics_reference_data/ --recursive --exclude "*" --include "*.json"

# Para copiar todos los archivos de datos en su respectiva ubicación, según la región que representa:
aws s3 cp CAvideos.csv s3://project-youtube-raw-useast1/youtube/raw_statistics/region=ca/
aws s3 cp DEvideos.csv s3://project-youtube-raw-useast1/youtube/raw_statistics/region=de/
aws s3 cp FRvideos.csv s3://project-youtube-raw-useast1/youtube/raw_statistics/region=fr/
aws s3 cp GBvideos.csv s3://project-youtube-raw-useast1/youtube/raw_statistics/region=gb/
aws s3 cp INvideos.csv s3://project-youtube-raw-useast1/youtube/raw_statistics/region=in/
aws s3 cp JPvideos.csv s3://project-youtube-raw-useast1/youtube/raw_statistics/region=jp/
aws s3 cp KRvideos.csv s3://project-youtube-raw-useast1/youtube/raw_statistics/region=kr/
aws s3 cp MXvideos.csv s3://project-youtube-raw-useast1/youtube/raw_statistics/region=mx/
aws s3 cp RUvideos.csv s3://project-youtube-raw-useast1/youtube/raw_statistics/region=ru/
aws s3 cp USvideos.csv s3://project-youtube-raw-useast1/youtube/raw_statistics/region=us/
```
> Nota:
Para correr estos comandos, es necesario que en el cmd nos encontremos en el directorio donde hemos descargado nuestro dataset de Kaggle.

Así tendremos como resultado:
![image](https://github.com/mram23/Proyecto-Ingenieria-de-Datos-YouTube/assets/132526921/cbd3b5f4-6107-4eff-aded-dbf6dd20e68a)
![image](https://github.com/mram23/Proyecto-Ingenieria-de-Datos-YouTube/assets/132526921/1dfa4e53-5b7b-45c8-8c73-4b632ce1818c)

Ahora que tenemos nuestra data cruda cargada en el bucket de AWS S3 llamado _project-youtube-raw-useast1_, lo que necesitamos es colectar esta data con ayuda de un _crawler_ del servicio de AWS Glue. El cual nos permitirá conocer la estructura (_schema_) y contenido de la data a partir de la fuente de datos que configuremos, que en este caso será el bucket _project-youtube-raw-useast1_. A continuación se muestra la configuración del _crawler de AWS Glue_:
![image](https://github.com/mram23/Proyecto-Ingenieria-de-Datos-YouTube/assets/132526921/07561b9a-5abe-4c60-a15b-9be10f22be13)

> Nota:
Para que el crawler pueda acceder a la data del bucket de AWS S3, es necesario asignarle los respectivos permisos necesarios al servicio, esto mediante un rol:
![image](https://github.com/mram23/Proyecto-Ingenieria-de-Datos-YouTube/assets/132526921/e519003d-51a6-4a8a-9d86-1502ca5317cf)

Así finalmente el resumen de a configuración de nuestro crawler es la siguiente:
![image](https://github.com/mram23/Proyecto-Ingenieria-de-Datos-YouTube/assets/132526921/e41c9c17-6b3f-4ec6-968d-0ad45b7914a3)

Y podemos ver los resultados de correr (ejecutar) este crawler, pues se ha creado una tabla nueva denominada _raw_statistics_reference_data_, asimismo observamos su schema:
![image](https://github.com/mram23/Proyecto-Ingenieria-de-Datos-YouTube/assets/132526921/9ac62d5b-d06d-44b9-a932-21e95755932a)

#### Segundo paso: Preprocesamiento y ETL Pipeline

Ahora, podemos hacer consultas dirigiendonos a la tabla _raw_statistics_reference_data_ que se encuentra en la base de datos _de_youtube_raw_ en AWS Glue. Lo que procederemos a hacer es el pre-procesamiento puesto que lo que necesitamos nosotros es la data que se encuentra dentro del arreglo _items_, y debido a que trabajamos con grandes volúmenes de datos es conveniente hacer una transformación a parquet.
![image](https://github.com/mram23/Proyecto-Ingenieria-de-Datos-YouTube/assets/132526921/40abd7c9-cdf4-42fb-bbc2-9bd63e401304)
Entonces, con ayuda de una función lambda que se activa cuandoe un nuevo objeto es creado en el bucket _project-youtube-raw-useast1_, se encarga de la transformación de json a parquet y el resultado es llevado al bucket de data limpia denominado _project-youtube-useast1-cleansed-data_ junto con la creación de la tabla _cleaned_statistics_reference_data_ en la base de datos que creamos previamente denominada _db_youtube_clean_ dentro de AWS Glue.

A continuación, se muestra la configuración de creación de la función lambda:![image](https://github.com/mram23/Proyecto-Ingenieria-de-Datos-YouTube/assets/132526921/f0feaa20-ad45-4fde-8b09-735144e5e772)
Y la función que utilizamos la pueden encontrar en el archivo [lambda_function.py](https://github.com/mram23/Proyecto-Ingenieria-de-Datos-YouTube/blob/4ca442609842752ab67412870c3f98e87aa0afb3/lambda_function.py)

> Nota:
Aquí también es necesario asignar un rol con los permisos necesarios, tal que la función lambda pueda acceder al bucket S3 y a la base de datos en AWS Glue donde se creará la nueva tabla _cleaned_statistics_reference_data_:
![image](https://github.com/mram23/Proyecto-Ingenieria-de-Datos-YouTube/assets/132526921/07e20677-aaca-48a4-931d-670df640926e)

También es necesario configurar las variables de entorno, que hemos asignado en el código:
![image](https://github.com/mram23/Proyecto-Ingenieria-de-Datos-YouTube/assets/132526921/700cab47-8cc2-4f8c-81b8-9aa718382dd9)
OJO: La base de datos _db_youtube_cleaned_ la creamos antes de testear el código para que la ejecución sea exitosa.

Y como utilizamos algunas librerías como awswrangler y pandas, es necesario configurar un _layer_ donde es que se importan las librerías a utilizar. En este caso, es necesario usar _AWSSDKPandas-Python38_: ![image](https://github.com/mram23/Proyecto-Ingenieria-de-Datos-YouTube/assets/132526921/426a9f1f-b714-4655-859c-d0424463f045)

¿Cómo haremos para automatizar que esta función lambda se active cada que se crea un objeto nuevo?
Esto se logra tras configurar un _trigger_ (estimulante/disparador), el cual será el evento tipo _All object create events_: ![image](https://github.com/mram23/Proyecto-Ingenieria-de-Datos-YouTube/assets/132526921/706b0bff-0e82-47ac-8b23-32665b5edcdc)

Entonces cada que se crea un nuevo objeto en el bucket, la función se activa. Aquí podemos ver cómo quedó el diagrama de la función Lambda:
![image](https://github.com/mram23/Proyecto-Ingenieria-de-Datos-YouTube/assets/132526921/49d76685-dcee-4279-919a-6251706f6bfa)

Y el output tras eliminar y volver a subir los archivos al folder _raw_statistics_reference_data_, en el bucket _project-youtube-raw-useast1_:
![image](https://github.com/mram23/Proyecto-Ingenieria-de-Datos-YouTube/assets/132526921/061b4170-1e4f-4480-a2b1-6621be304f22)
Y es que esta data que se encuentra en AWS S3, con ayuda de la función lambda que crea la nueva tabla _cleaned_statistics_reference_data_ en la base de datos _db_youtube_cleaned_ puede ser consultada mediante queries mediante AWS Athena

Hasta el momento solo hemos trabajado con la data que se encuentra en la carpeta _raw_statistics_reference_data_, es momento de hacerlo con _raw_statistics_. Para ello, lo primero que haremos es crear un _crawler_ que colecte la data de esta carpeta encontrada en el bucket _project-youtube-raw-useast1_. Tras ejecutarlo, notamos que en la tabla _raw_statistics_ dentro de la base de datos _de_youtube_raw_ detecta la partición por región:
![image](https://github.com/mram23/Proyecto-Ingenieria-de-Datos-YouTube/assets/132526921/022c8d54-f68e-4c31-a9ac-2a221d9c0102)

Ahora, esa tabla es de la data cruda ingestada, lo que necesitamos es pre-procesarla (hacer algunos cambios en el tipo de dato de algunas variables y transformar de formato csv a parquet). El resultado será almacenado dentro del bucket _project-youtube-useast1-cleansed-data_ y con esta data se creará la tabla _raw_statistics_ pero dentro de la base de datos _db_youtube_cleaned_ en AWS Glue. Esto mediante un _ETL Job_ creado a partir del siguiente [script](https://github.com/mram23/Proyecto-Ingenieria-de-Datos-YouTube/blob/5d567ff8492babc83b8437d37791e0fabff90300/etljob_script.py). Como resultado tenemos en la carpeta _raw_statistics_ del bucket _project-youtube-useast1-cleansed-data_:
![image](https://github.com/mram23/Proyecto-Ingenieria-de-Datos-YouTube/assets/132526921/fde14eb8-c91b-404d-aba3-ae6e6a5ee4f9)

Y procedemos a correr un crawler para colectar esta _data limpia_:![image](https://github.com/mram23/Proyecto-Ingenieria-de-Datos-YouTube/assets/132526921/a374cf47-9541-4bd2-b71b-db0993f5222f)

#### Tercer paso: Presentación de insights en AWS QuickSight

En primer lugar, procedemos a desarrollar un ETL Pipeline (Extract, Transform, Load - Pipeline: diseño, flujo, plan) que permita pre-procesar la data que tenemos ya limpia, con el fin de obtener una versión final que podamos utilizar para hacer los reportes (analítica). En este caso queremos combinar las tablas _raw_statistics_ y _cleaned_statistics_reference_data_ de la base de datos _db_youtube_cleaned_:
![image](https://github.com/mram23/Proyecto-Ingenieria-de-Datos-YouTube/assets/132526921/d0e3c199-4445-497c-9d30-70d8a6ca587a)
El resultado del inner join está dirigido hacia un nuevo bucket S3 que servirá para la parte de analítica y reporte. Entonces, es conveniente crear también una base de datos y su respectiva tabla para la capa de analytics, incluyendo la partición por _region_:
![image](https://github.com/mram23/Proyecto-Ingenieria-de-Datos-YouTube/assets/132526921/bb9fb639-e046-4f15-be7b-de7113bea73d)

Finalmente, tras habernos logeado en AWS QuickSight podemos tener un gráfico como el siguiente:
![image](https://github.com/mram23/Proyecto-Ingenieria-de-Datos-YouTube/assets/132526921/18875522-e4ba-4457-a840-3802626ca4ec)

Y esta es la arquitectura final del proyecto que hemos desarrollado:
![image](https://github.com/mram23/Proyecto-Ingenieria-de-Datos-YouTube/assets/132526921/280988f1-b628-414b-9725-3134c8da151b)
