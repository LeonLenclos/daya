# Lucy

A tamagochi-like bot made with pygame. For the *Turing Test* show.

![lucy](sprite/normal/base/0/0.png)

[Plus de détails](https://github.com/LeonLenclos/turing-test/blob/master/contenu/robots/lucy.md)

## Usage

```
pip install pygame
cd lucy
python3 main.py -h
python3 main.py
```

### Keyboard

- <kbd>Space</kbd> : feed
- Long press on <kbd>Space</kbd> : reset
- <kbd>R</kbd> : reset
- <kbd>D</kbd> : dance

### Button


On a raspberrypi with a button that connect GPIO 18 to the Ground(GND). Run lucy with the raspberry option : `python3 main.py --raspberry`.

You can now use the button !

- Press the button : feed
- Long press on the button : reset

### OSC

Run lucy with the serve-at option : `python3 main.py --serve-at localhost`.

You can now send OSC messages to the port `4242` of the given adress :

- `/feed` : feed
- `/dance` : dance
- `/reset` : reset
