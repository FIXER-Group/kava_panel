# kava_panel
![alt text](https://i.imgur.com/Q3ckJlJ.png)

## Table of contents
* [Requirements](#requirements)
* [Setup](#setup)
* [REST API](#REST-API)
* [Technologies](#technologies-used-in-project)
## Requirements
* Python 3.7
* Mongodb
## Setup

Remember to install mongodb server

First time setup

```sh
git clone https://github.com/androjus/kava_panel.git
```

Then install the dependencies:

```sh
cd kava_panel
sudo pip install -r requirements.txt
```

Once `pip` has finished downloading the dependencies:
```sh
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```
To run app use this command
```sh
uvicorn kava.asgi:application --host 0.0.0.0
```
And navigate to `http://your_vps_ip:8000/`.

# REST API

## Auth

Authorization is done by passing Token. Tokens are generated separately for each user added to the panel.
To get a token:

`Click on your login on the left > Edit profile > API Token`

    curl -H 'Authorization: Token put_in_this_place_your_token'

## Get list of stats

### Request

`GET /panel/api/stats`

    curl http://your_vps_ip:8000/panel/api/stats

### Response

    HTTP/1.1 200 OK
    allow: GET, HEAD, OPTIONS
    content-length: 292
    content-type: application/json
    date: Mon, 11 Jan 2021 21:51:02 GMT
    server: uvicorn
    vary: Accept
    x-content-type-options: nosniff
    x-frame-options: DENY

    {"cpu_percent":6.7,"cpu_per_core":[20.4,3.0,3.2,0.0,4.2,4.0],"cpu_name":"QEMU Virtual CPU version 2.5+","ram_percent":25.5,"ram_total":"31.37 GB","ram_usage":"7.71 GB","disk_percent":18.0,"disk_total":"182.03 GB","disk_usage":"32.68 GB","swap_percent":0.0,"swap_total":"4.0 GB","uptime":33.0}

## Get list of system info

### Request

`GET /panel/api/system`

    curl http://your_vps_ip:8000/panel/api/system

### Response

    HTTP/1.1 200 OK
    allow: GET, HEAD, OPTIONS
    content-length: 190
    content-type: application/json
    date: Mon, 11 Jan 2021 21:51:37 GMT
    server: uvicorn
    vary: Accept
    x-content-type-options: nosniff
    x-frame-options: DENY

    {"name":"Linux","release":"5.4.0-1028-kvm","version":"#29-Ubuntu SMP Thu Nov 26 06:52:24 UTC 2020","architecture":"x86_64","hostname":"androjus","ipadress":"x.x.x.x","processor":"x86_64"}
    
## Get list of processes

### Request

`GET /panel/api/process`

    curl http://your_vps_ip:8000/panel/api/process

### Response

    HTTP/1.1 200 OK
    allow: GET, HEAD, OPTIONS
    content-length: 9743
    content-type: application/json
    date: Mon, 11 Jan 2021 21:52:27 GMT
    server: uvicorn
    vary: Accept
    x-content-type-options: nosniff
    x-frame-options: DENY

    {"List":[{"pid":5899,"name":"java","cpu_percent":3.32,"memory_percent":15.36},{"pid":1665,"name":"java","cpu_percent":0.81,"memory_percent":8.14}...]}
    
## Kill process

### Request

`POST /panel/api/process`

    curl http://your_vps_ip:8000/panel/api/process -d 'pid=2020'

### Response

    HTTP/1.1 400 Bad Request
    allow: GET, POST, HEAD, OPTIONS
    content-length: 5
    content-type: application/json
    date: Wed, 13 Jan 2021 23:23:54 GMT
    server: uvicorn
    vary: Accept
    x-content-type-options: nosniff
    x-frame-options: DENY

    false

## Reboot machine

### Request

`POST /panel/api/reboot`

    curl http://your_vps_ip:8000/panel/api/reboot

### Response

`true`

## Technologies used in project:
* [Python3](https://www.python.org/)
* [Bootstarp4](https://www.themekita.com/ready-bootstrap-dashboard.html)
* [Chartjs](https://www.chartjs.org/)
* [Django 3.0.5](https://www.djangoproject.com/)
* [Django rest framework](https://www.django-rest-framework.org/)
* [Datatables](https://datatables.net/)
* [Line awesome icons](https://icons8.com/line-awesome)
* [Uvicorn](https://www.uvicorn.org/)
* [Whitenoise](http://whitenoise.evans.io/en/stable/)