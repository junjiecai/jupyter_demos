import argparse
import logging
from logging.handlers import RotatingFileHandler

from logging_demo.cals import cal


def create_logger(level):
    logger = logging.getLogger('test')
    logger.setLevel(level)

    file_handler = RotatingFileHandler('commong_log.txt', maxBytes=1024 * 2, backupCount=2, mode='w')
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    error_handler = logging.FileHandler('error_log.`txt', mode='w')
    error_handler.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(asctime)s - %(name)s -  %(message)s')
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)

    return logger


def main(logging_level):
    logger = create_logger(logging_level)
    logger.info('Start looping')

    for i in range(1000)[::-1]:
        logger.debug(i)
        try:
            cal(i)
        except Exception as e:
            logger.error('Wow! error orrcured', exc_info=True)

    logger.info('End of loop')


if __name__ == '__main__':
    # define
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--logging_level', type=int)

    args = parser.parse_args()
    logging_level = args.logging_level

    main(logging_level)
