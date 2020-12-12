# kava_panel
![alt text](https://i.imgur.com/WNnJkfA.png)

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

# More to add....
