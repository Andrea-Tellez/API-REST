## Creacion de imagen 
docker build -t api_rest:v1 .

## Creacion de contenedor basado en imagen

docker run -it - v "PWD"/home:/home/code --net=host --name api_rest -h andrea api_rest:v1