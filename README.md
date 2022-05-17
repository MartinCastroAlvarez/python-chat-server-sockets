# Chat server

![wallpaper](./wallpaper.jpeg)

## Demo

[Click here](./martincastroalvarez-uc3.mp4)

## Architecture

![architecture](./architecture.png)

## References

- [Threading](https://docs.python.org/3/library/threading.html)

## Instructions

### Start the server
```bash
python3 server.py --host 2018 --host "0.0.0.0"
```
```bash
Nuevo client: ('127.0.0.1', 54462)
Nuevo client: ('127.0.0.1', 54464)
Nuevo client: ('127.0.0.1', 54466)
54462 a b c
54464 lorem ipsum
54466 dolor sit amet
```

### Create a client
```bash
python3 client.py --host 2018 --host "0.0.0.0"
```
```bash
Escuchando mensajes del servidor...
54462 a b c
lorem ipsum 
54464 lorem ipsum
54466 dolor sit amet
```
