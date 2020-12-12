# kava_panel

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/androjus/kava_panel.git
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```

Once `pip` has finished downloading the dependencies:
```sh
(env)$ cd kava_panel
(env)$ hypercorn kava.asgi:application
```
And navigate to `http://127.0.0.1:8000/`.

# More to add....
