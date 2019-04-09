def three_x_cubed_plus_7(x):
    return 3 * x * x * x + 7


def triple_up(x):
    if len(x) <= 3:
        return x
    return [[x[0], x[1], x[2]], triple_up(x[3:])]


def mystery_code(x):
    if len(x) == 1:
        return x
    if str.isalpha(x[0]):
        if str.isupper(x[0]):
            index = ord(x[0]) + 32
            if index > 109:
                index = index - 13
            else:
                index = index + 13
            return chr(index) + mystery_code(x[1:])
        else:
            index = ord(x[0]) - 32
            if index > 77:
                index = index - 13
            else:
                index = index + 13
            return chr(index) + mystery_code(x[1:])
    else:
        return x[0] + mystery_code(x[1:])


def future_tense(x):
    time = ['yesterday', 'today', 'now']
    verb = {'was': 'be', 'were': 'be', 'is': 'be', 'am': 'be', 'are': 'be',
            'go': 'go', 'goes': 'go', 'went': 'go',
            'eat': 'eat', 'eats': 'eat', 'ate': 'eat',
            'have': 'have', 'has': 'have', 'had': 'have',
            'do': 'do', 'does': 'do', 'did': 'do'}
    out = []
    past_verb = list(verb.keys())
    for word in x:
        if str.isupper(word[0]):
            word = str.lower(word[0]) + word[1:]
            if word in time:
                out = out + ['Tomorrow']
            elif word in past_verb:
                out = out + ['will'] + [str.upper(verb[word][0]) + verb[word][1:]]
            elif word[-2:] == 'ed':
                out = out + ['will'] + [str.upper(verb[word][0]) + verb[word][1:-2]]
            else:
                out = out + [str.upper(word[0]) + word[1:]]
        else:
            if word in time:
                out = out + ['tomorrow']
            elif word in past_verb:
                out = out + ['will'] + [verb[word]]
            elif word[-2:] == 'ed':
                out = out + ['will'] + [word[:-2]]
            else:
                out = out + [word]
    return out

