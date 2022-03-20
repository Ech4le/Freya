# Freya

Freya is Python library for Raspberry Pi plant auto watering device. After installation, daemon will periodically get environment values from DHT sensors, water level sensors and ground humidity sensor to decide, is watering needed.  

To do:  
- [ ] freydaemon script
- [ ] freyctl script 
- [ ] install script
- [ ] smtp relay for alerts

## Installation

Use git to download latest version - [click](https://github.com/Ech4le/Freya), then run install script.

```bash
git clone https://github.com/Ech4le/Freya
bash install.sh
```

## Env options

```bash
WAIT_INTERVAL = INTERVAL OF WAITING BETWEEN MEASURES
HUM_TRIG = BELOW THIS GROUND HUMIDITY VALUE, INJETION WILL BE TRIGGERED
INJECT_VALUE = VALUE OF WATER TO INJECT (liters)
INJECT_LOCK = MINIMUM TIME OF INTERVAL BETWEEN INJECTIONS
DB_URI = "sqlite:///db.sqlite" URI TO DATABASE
PUMP_MAX_FLOW = MAXIMUM FLOW OF POMP (liters)
```

## Usage

```bash
# Enable and run Freya daemon service
sudo systemctl start freya.service
sudo systemctl enable freya.service

# Check Freya version
freyctl --version

# Check info about ground and air conditions
freyctl status
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
