from datetime import datetime, timedelta
from time import sleep
from dotenv import dotenv_values
from sqlalchemy.orm import declarative_base, sessionmaker
from db_app import init_db, Readings
import sqlalchemy as db
import logging
import os


def check_env():
    hum = 15.0  # Swap with real device reading
    temp = 27.2  # Swap with real device reading
    lux = 62503  # Swap with real device reading
    water_temp = 25.2  # Swap with real device reading
    water_level = 80  # Swap with real device reading
    vals = {
        'hum': hum,
        'temp': temp,
        'lux': lux,
        'water_temp': water_temp,
        'water_level': water_level
    }
    return vals


def check_gnd_hum():
    val = 15.0  # Swap with real device reading
    logging.debug(f'Water sensor gathered: {val}.')
    return val


def infuse(val, MAX_FLOW):
    flow_per_sec = round(MAX_FLOW / 3600, 5)
    time_needed = round(val / flow_per_sec, 1)
    logging.info(f'Injecting {int(val * 1000)} ml.')
    sleep(time_needed)
    logging.info('Injection done.')


if __name__ == "__main__":
    installation_path = '/home/nsl/Pulpit/Freya/'

    logging.basicConfig(
        filename='example.log',
        level=logging.INFO, 
        format= '[%(asctime)s] %(levelname)s - %(message)s',
        datefmt='%d-%m-%Y-%H:%M:%S'
    )
    logging.info('FreyDaemon activated.')
    logging.info(f'Installation path: {installation_path}')
    
    config = dotenv_values(os.path.join(installation_path, '.env'))
    DB_URI = config['DB_URI']
    PUMP_MAX_FLOW = int(config['PUMP_MAX_FLOW'])
    DB_LOG_ACTIVE = True if DB_URI != "" else False
    WAIT_INTERVAL = int(config['WAIT_INTERVAL'])
    HUM_TRIG = int(config['HUM_TRIG'])
    INJECT_VALUE = float(config['INJECT_VALUE'])
    INJECT_LOCK = int(config['INJECT_LOCK'])
    LAST_INJECT = datetime.now() - timedelta(hours=5)

    if DB_LOG_ACTIVE:
        try:
            engine = init_db()
            metadata = db.MetaData()
            Session = sessionmaker(bind=engine)
            session = Session()

            logging.info('Database activated.')
        except Exception as e:
            logging.error(f'Database error: {e}')
    else:
        logging.warning('Database not specified.')

    while True:
        ## Gather data from sensors
        gnd_hum = check_gnd_hum()
        env_vals = check_env()

        ## If db is connected, send metrics
        if DB_LOG_ACTIVE:
            new_readings = Readings(
                created_at=datetime.now(), 
                ground_hum = gnd_hum,
                air_hum = env_vals['hum'],
                air_temp = env_vals['temp'],
                lux = env_vals['lux'],
                water_temp = env_vals['water_temp'],
                water_level = env_vals['water_level'],
            )
            session.add(new_readings)
            session.commit()
        
        ## If injection isn't locked, and ground humidity is low - begin injection
        if gnd_hum < HUM_TRIG and datetime.now() - LAST_INJECT > timedelta(seconds=INJECT_LOCK):
            infuse(INJECT_VALUE, PUMP_MAX_FLOW)
            LAST_INJECT = datetime.now()
        
        ## If ground humidity is low but injection is locked - send warning
        elif gnd_hum < HUM_TRIG:
            logging.warning('Requested locked injection.')

        ## Save energy bruh
        sleep(WAIT_INTERVAL)
