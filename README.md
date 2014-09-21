rpi-lights
==========


```
  sudo apt-get install build-essential python-dev upstart
  git clone https://github.com/tmikoss/rpi-lights.git ~/rpi-lights
```

```
  scp config/upstart.conf root@raspberrypi.local.net:/etc/init/rpi-lights.conf
  ./deploy.sh
```
