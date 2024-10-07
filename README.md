# My Portfolio Webiste!!

This is my portfolio website made using Flask, Docker, and Nginx

## Installation

Make sure you have python3 and pip installed

Create and activate virtual environment using virtualenv
```bash
$ python3 -m venv python3-virtualenv
$ source python3-virtualenv/bin/activate
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all dependencies!

```bash
pip install -r requirements.txt
```

## Usage

***Create and fill in a .env file using the example.env template (make a copy using the variables inside of the template***
***The Basic Auth Username and Password will be used when accessing the POST and DELETE API endpoints***

### Running with Docker Locally

Run docker-compose. If you're using Docker Desktop and WSL2 like me, you might need to use sudo.
```bash
❯ sudo docker compose up -d --build
```

You should get a response like this in the terminal:
```bash
❯ sudo docker compose up -d --build
[sudo] password for mrsyn:
[+] Building 2.9s (10/10) FINISHED                                                                       docker:default
 => [myportfolio internal] load build definition from Dockerfile                                                   0.0s
 => => transferring dockerfile: 216B                                                                               0.0s
 => [myportfolio internal] load .dockerignore                                                                      0.0s
 => => transferring context: 2B                                                                                    0.0s
 => [myportfolio internal] load metadata for docker.io/library/python:3.9-slim-buster                              0.8s
 => [myportfolio 1/5] FROM docker.io/library/python:3.9-slim-buster@sha256:320a7a4250aba4249f458872adecf92eea88dc  0.0s
 => [myportfolio internal] load build context                                                                      0.3s
 => => transferring context: 9.27MB                                                                                0.3s
 => CACHED [myportfolio 2/5] WORKDIR /myportfolio                                                                  0.0s
 => CACHED [myportfolio 3/5] COPY requirements.txt .                                                               0.0s
 => CACHED [myportfolio 4/5] RUN pip3 install -r requirements.txt                                                  0.0s
 => [myportfolio 5/5] COPY . .                                                                                     1.3s
 => [myportfolio] exporting to image                                                                               0.4s
 => => exporting layers                                                                                            0.4s
 => => writing image sha256:9806f501eadc6a40b22f03cf5e8e2f4313b625e5b148bc33c022b35da3a68308                       0.0s
 => => naming to docker.io/library/portfolio-myportfolio                                                           0.0s
[+] Running 3/3
 ✔ Network portfolio_default  Created                                                                              0.0s
 ✔ Container mysql            Started                                                                              0.8s
 ✔ Container myportfolio      Started                                                                              1.2s
```

You'll now be able to access the website at `localhost:5000` or `127.0.0.1:5000` in the browser! 

### Running with Docker on your server

***Go to https://duckdns.org/ and add a domain name with the IP of your server and change the server_name in myportfolio.conf to whatever domain name you made***

Run docker-compose for production
```bash
❯ docker compose -f docker-compose.prod.yml up -d --build
```

You should get a response like this in the terminal:
```bash
❯ docker compose -f docker-compose.prod.yml up -d --build
[+] Building 0.9s (10/10) FINISHED
 => [myportfolio internal] load build definition from Dockerfile                                                   0.0s
 => => transferring dockerfile: 276B                                                                               0.0s
 => [myportfolio internal] load .dockerignore                                                                      0.0s
 => => transferring context: 2B                                                                                    0.0s
 => [myportfolio internal] load metadata for docker.io/library/python:3.9-slim-buster                              0.6s
 => [myportfolio 1/5] FROM docker.io/library/python:3.9-slim-buster@sha256:320a7a4250aba4249f458872adecf92eea88dc  0.0s
 => [myportfolio internal] load build context                                                                      0.2s
 => => transferring context: 353.30kB                                                                              0.2s
 => CACHED [myportfolio 2/5] WORKDIR /myportfolio                                                                  0.0s
 => CACHED [myportfolio 3/5] COPY requirements.txt .                                                               0.0s
 => CACHED [myportfolio 4/5] RUN pip3 install -r requirements.txt                                                  0.0s
 => CACHED [myportfolio 5/5] COPY . .                                                                              0.0s
 => [myportfolio] exporting to image                                                                               0.0s
 => => exporting layers                                                                                            0.0s
 => => writing image sha256:f4967dae53f8001260671392f6f42c70f9ae6db950eb5d76050db1bb776142d9                       0.0s
 => => naming to docker.io/library/portfolio-myportfolio                                                           0.0s
[+] Running 3/0
 ✔ Container mysql        Running                                                                                  0.0s
 ✔ Container myportfolio  Running                                                                                  0.0s
 ✔ Container nginx        Running                                                                                  0.0s
```

You'll now be able to access the website at the domain you made! 

### Flask only

Start flask server after setting it to development and setting mysql host to localhost
```bash
❯ export FLASK_ENV=development && export MYSQL_HOST=localhost
❯ flask run
```

You should get a response like this in the terminal:
```bash
❯ flask run
 * Serving Flask app 'app' (lazy loading)
 * Environment: development
 * Debug mode: on
<peewee.MySQLDatabase object at 0x7fbce0d812d0>
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 122-060-471
<peewee.MySQLDatabase object at 0x7fd49ba04220>
```

You'll now be able to access the website at `localhost:5000` or `127.0.0.1:5000` in the browser! 



## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
