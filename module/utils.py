from .constant import *


def get_support_lang(params):
    default_lang = 'en'
    query_lang = ''
    try:
        if 'lang' in params:  # type: ignore
            query_lang = params['lang']  # type: ignore
    except Exception as e:
        print('error get_support_lang')

    return query_lang if query_lang in LANG else default_lang
