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

![image](https://github.com/mram23/Proyecto-Ingenieria-de-Datos-YouTube/assets/132526921/7411ad77-bf6f-4758-bc35-cacdd3eb0bc6)
