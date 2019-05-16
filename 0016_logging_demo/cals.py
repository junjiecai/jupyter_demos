import logging

logger = logging.getLogger(__name__)


def cal(i):
    logger.info('run cal')
    return 10 / i
