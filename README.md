# kava_panel
![alt text](https://i.imgur.com/FtdndbN.jpg)

## Setup

The first thing to do is to clone the repository:

```sh
git clone https://github.com/androjus/kava_panel.git
```

Then install the dependencies:

```sh
sudo pip install -r requirements.txt
```

Once `pip` has finished downloading the dependencies:
```sh
cd kava_panel
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
    content-length: 304
    content-type: application/json
    date: Mon, 11 Jan 2021 21:24:08 GMT
    server: uvicorn
    vary: Accept
    x-content-type-options: nosniff
    x-frame-options: DENY

    {"cpu_percent":20.5,"cpu_per_core":[20.0,17.2,20.3,20.3],"cpu_name":"AMD Athlon(tm) II X4 631 Quad-Core Processor","ram_percent":85.9,"ram_total":"4.0 GB","ram_usage":"3.43 GB","disk_percent":96.7,"disk_total":"921.66 GB","disk_usage":"891.37 GB","swap_percent":67.1,"swap_total":"10.25 GB","uptime":0.0}

## Get list of system info

### Request

`GET /panel/api/system`

    curl http://your_vps_ip:8000/panel/api/system

### Response

    HTTP/1.1 200 OK
    allow: GET, HEAD, OPTIONS
    content-length: 196
    content-type: application/json
    date: Mon, 11 Jan 2021 21:22:52 GMT
    server: uvicorn
    vary: Accept
    x-content-type-options: nosniff
    x-frame-options: DENY

    {"name":"Windows","release":"10","version":"10.0.16299","architecture":"AMD64","hostname":"DESKTOP-M8J9S0I","ipadress":"95.49.16.98","processor":"AMD64 Family 18 Model 1 Stepping 0, AuthenticAMD"}
    
## Get list of processes

### Request

`GET /panel/api/process`

    curl http://your_vps_ip:8000/panel/api/process

### Response

    HTTP/1.1 200 OK
    allow: GET, HEAD, OPTIONS
    content-length: 15082
    content-type: application/json
    date: Mon, 11 Jan 2021 21:25:33 GMT
    server: uvicorn
    vary: Accept
    x-content-type-options: nosniff
    x-frame-options: DENY

    {"List":[{"pid":0,"name":"System Idle Process","cpu_percent":28.72,"memory_percent":0.0}...]}
    
## Get list of network connections

### Request

`GET /panel/api/network`

    curl http://your_vps_ip:8000/panel/api/network

### Response

    HTTP/1.1 200 OK
    allow: GET, HEAD, OPTIONS
    content-length: 16957
    content-type: application/json
    date: Mon, 11 Jan 2021 21:29:46 GMT
    server: uvicorn
    vary: Accept
    x-content-type-options: nosniff
    x-frame-options: DENY

    {"List":[{"Protocol":"tcp","Local_address":"192.168.1.16:1128","Remote_address":"44.242.24.237:443","Status:":"ESTABLISHED","PID":11140,"Name":"chrome.exe"}...]}
