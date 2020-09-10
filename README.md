# MongoDB ~~Com~~TimePass
![timepass](assets/timepass-logo.png)

Just a mongodb related project to pass time *(Thus MongoDB TimePass Ba-dum-tss! 😁)* and learn about mongodb profiling, schema generation etc.

## Features:
1. Explore MongoDB instances ( Collections, Databases, Paginated queries, filters, projection ) ✅
2. Insertion, Update, Delete ( *TODO* ) 📝
3. Schema Analysis ( *TODO* ) 📝
4. Profiling based graphs ( *TODO* ) 📝

## Run Instructions

### 1. I like docker 🐳
```python
git clone 

docker-compose up --build 😊
```
**Note: By default COPY is commented out from Dockerfile and the code is mounted as volume in docker-compose.yml to work with hot-reload of streamlit.
You must uncomment COPY from Dockerfile and remove volume mounts from docker-compose.yml at the time of deployment.**

### 2. I hate docker 🔪🐳🔪 I will mess up my host system! 🎉

```python
pip install -r requirements.txt

streamlit run main.py 😞
```
