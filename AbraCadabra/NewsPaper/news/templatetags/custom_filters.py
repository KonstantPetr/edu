from django import template

register = template.Library()


@register.filter()
def censor(value):
    if not type(value) is str:
        raise TypeError('value type not str')
    with open('forbidden_words', encoding='utf-8') as forbidden_words:
        forbidden_words = forbidden_words.read().split()
        text_words = value.split()
        for word in text_words:
            if word.lower() in forbidden_words:
                value = value.replace(word[1:], "*" * (len(word) - 1))

    return value
