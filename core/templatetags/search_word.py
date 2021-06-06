from django.template import Library

register = Library()

def search_word(word, search):
    found = word.find(search)

    if found >= 0:
        return True
    return False

register.filter('search_word', search_word)