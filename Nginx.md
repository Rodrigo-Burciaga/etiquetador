# Nginx

------------

## ¿Qué es y por qué Nginx?
Es un servidor web/proxy inverso ligero de alto rendimiento y un proxy para protocolos de correo electrónico.

NGINX fue lanzado oficialmente en octubre del 2004. El creador del software, Igor Sysoev, comenzó su proyecto en el 2002 como un intento de solucionar el problema C10k. C10k es el reto de gestionar diez mil conexiones al mismo tiempo. Hoy en día, los servidores web tienen que manejar un número aún mas grande de conexiones. Por esa razón, NGINX ofrece una arquitectura asíncrona y controlada por eventos, característica que hace de NGINX uno de los servidores más confiables para la velocidad y la escalabilidad.


Para ***DeepDaemon*** es de gran importancia Nginx, debido a que es el servidor principal y el punto de acceso para todos los microservicios que actualmente  tienen salida al usuario final.

## Arquitectura DeepDaemon

## Instalación y configuraciones

### Instalación

La instalación del servidor nginx varia mucho del sistema operativo (Familia en la que está basada) que se esté usando, para una instalación especifica consultar  la [documentación oficial.](https://docs.nginx.com/nginx/admin-guide/installing-nginx/installing-nginx-open-source/)

Una vez que ha sido instalado, verificamos en nuestro sistema operativo que el servidor esté funcionando; en linux basta con ejecutar el siguiente comando:

```sh
# service nginx status
```

[create an anchor](#Nginx)