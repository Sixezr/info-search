import pymorphy2

inverted_index_file = 'inverted_index/inverted_index.txt'
morph = pymorphy2.MorphAnalyzer()


class Command:
    AND = 'and'
    OR = 'or'
    NOT = 'not'
    L_BR = '('
    R_BR = ')'


def get_inverted_index():
    inverted_index = dict()
    with open(inverted_index_file, 'r', encoding='utf-8') as file:
        lines = file.read().splitlines()
        for l in lines:
            inverted_index[l.split(" ", 1)[0]] = set(eval(l.split(" ", 1)[1]))
    return inverted_index


def searh(query):
    expr = query.strip().split()
    inverted_index = get_inverted_index()
    result = Command.L_BR
    for i, e in enumerate(expr):
        match e:
            case Command.AND:
                result += ").intersection("
            case Command.OR:
                result += ").union("
            case Command.NOT:
                result += ").difference("
            case Command.L_BR | Command.R_BR:
                result += e
            case _:
                lemma = morph.parse(e)[0].normal_form
                if lemma in inverted_index.keys():
                    result += str(inverted_index[lemma])
                else:
                    result += "set()"
    return eval(result + Command.R_BR)


if __name__ == "__main__":
    while True:
        query = input("Enter query: ").lower()
        if query == 'exit':
            exit()

        try:
            result = searh(query)
            print(f'Found {len(result)} files: {result}')
        except:
            print('Error')
