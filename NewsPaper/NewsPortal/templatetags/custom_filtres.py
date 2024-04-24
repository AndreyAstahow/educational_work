from django import template

register = template.Library()

@register.filter()
def censor(value):
    val = value.split()
    text = []
    for i in val:
        if i.istitle():
            text.append(i[0] + '*' * (len(i) - 1))
        else:
            text.append(i)
    return f'{" ".join(text)}'

@register.filter()
def censor_forbidden(value):
    forbidden_words = ['Четыре', 'Lorem', 'Ipsum']
    val = value.split()
    text = []
    for word in val:
        if word in forbidden_words:
            text.append(word[0] + '*' * (len(word) - 2) + word[-1])
        else:
            text.append(word)
    return f'{" ".join(text)}'