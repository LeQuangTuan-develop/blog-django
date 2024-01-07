DEFAULT_LANG = 'en'
SUPPORT_LANG = ['ja', 'es', 'cn']
LANG = [DEFAULT_LANG] + SUPPORT_LANG
DOMAIN_DIDIVU = 1
DOMAIN_FXEATER = 2
STATUS_TYPE_DRAFT = 1
STATUS_TYPE_PUBLISHED = 2


CL_MAP = {
    'en': [
        'description',
        'html_string',
        'name',
        'sub_title',
    ],
    'ja': [
        'description_ja',
        'html_string_ja',
        'name_ja',
        'sub_title_ja',
    ],
    'cn': [
        'description_cn',
        'html_string_cn',
        'name_cn',
        'sub_title_cn',
    ],
    'es': [
        'description_es',
        'html_string_es',
        'name_es',
        'sub_title_es',
    ]
}
