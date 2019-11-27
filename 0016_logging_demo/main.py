import os
import sys
from argparse import ArgumentParser

from loguru import logger

from .calculation import add, square


def parse_arguments():
    parser = ArgumentParser()

    parser.add_argument('--debug', dest='debug', action='store_true')
    parser.set_defaults(debug=False)

    return parser.parse_args()


def set_logger(debug):
    if debug:
        logging_level = 'DEBUG'
    else:
        logging_level = 'INFO'

    # 移除原始的logger配置
    logger.remove()

    # 添加目标为sys.stdout的logger handler
    logger.add(
        sys.stdout,
        level=logging_level,
        colorize=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> <level>{message}</level>"
    )

    # 添加目标为log.txt的logger handler
    logger.add(
        "{}/log.txt".format(os.path.dirname(os.path.abspath(__file__))),
        level=logging_level,
        colorize=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> <level>{message}</level>",
        rotation='1mb',  # 如果想保留最近一段时间的记录可以用， retention="10 days"
        serialize=True
    )


if __name__ == '__main__':
    args = parse_arguments()

    set_logger(args.debug)

    z = add(2, 4)
    square(z)
