from config.settings import settings


def ctc(*args):  # Content Type Creator
    alen = len(args)
    content_type = ''
    for i in range(alen):
        content_type += f'{args[i]}{settings.SEP if i < alen - 1 else ""}'
    return content_type
