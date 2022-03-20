from dotenv import dotenv_values
from sqlalchemy import exc
import sqlalchemy as db
import logging
import os


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
    DB_LOG_ACTIVE = True if DB_URI != "" else False

    if DB_LOG_ACTIVE:
        try:
            engine = db.create_engine(DB_URI)
            connection = engine.connect()
            metadata = db.MetaData()
            logging.info('Database activated.')
        except Exception as e:
            logging.error(f'Database error: {e}')
    else:
        logging.warning('Database not specified.')