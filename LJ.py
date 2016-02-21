import re
import sublime
import sublime_plugin


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


def prepare(text):
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
		result = prepare(h_file.read())

	result = count(result)
	print(result)


class LjPrepareCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        all_file_region = sublime.Region(0, self.view.size())
        text = self.view.substr(all_file_region)
        text = prepare(text)
        self.view.replace(edit, all_file_region, text)


if __name__ == '__main__':
	main()
