import logging


from . import logger # must be first import before you get loggers




__all__ = ['tgbot', 'db_service', 'kwork_parser_service']


tgbot = logging.getLogger('tgbot')
db_service = logging.getLogger('services.db_service')
kwork_parser_service = logging.getLogger('services.kwork_parser_service')

