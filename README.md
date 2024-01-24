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
