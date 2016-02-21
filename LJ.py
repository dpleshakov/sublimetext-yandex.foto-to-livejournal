import re


CLEAR_RULES = [
    (r'<br\s*/>', '\n'),
    (r'</?lj-cut>', ''),
    (r'</?cut\s?.*?>', ''),
    (r'<!--more-->', ''),
    (r'(title|alt|border)=".*?"', ''),
    (r'^(?!.*^<).*\n', ''),
    (r' {2,}', ' '),
    (r'\n{2,}', '\n'),
    (r'^\n+', ''),
    (r'\n+$', '')
]

COUNT_RULES = [
    (r'</?a.*?>', ''),
    (r'<img ', '<img style="border: 2px solid black;" width="1100" ')
]


def _make_rules(text, rules):
    for pattern, string in rules:
        text = re.sub(pattern, string, text)
    return text


def clear(text):
    return _make_rules(text, CLEAR_RULES)


def count(text):
    lines = text.split('\n')
    for index in range(len(lines)):
        lines[index] = _make_rules(lines[index], COUNT_RULES)
        lines[index] = '\n' + str(index + 1) + ". \n" + lines[index]
    return '\n'.join(lines)


def main():
	result = ""
	with open('test.txt', 'r') as h_file:
		result = clear(h_file.read())

	result = count(result)
	print(result)


if __name__ == '__main__':
	main()
