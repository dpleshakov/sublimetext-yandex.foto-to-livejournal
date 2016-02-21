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
    (r'<img ', '<img style="border: 2px solid black;" width="1100" '),
    (r'\n{2,}', '\n'),
]


def _make_rules(text, rules):
    for pattern, string in rules:
        text = re.sub(pattern, string, text)
    return text


class LjPrepareTextCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        all_file_region = sublime.Region(0, self.view.size())
        text = self.view.substr(all_file_region)
        text = _make_rules(text, CLEAR_RULES)
        self.view.replace(edit, all_file_region, text)


class LjCountLinesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            if not region.empty():
                text = self.view.substr(region) + '\n'
                self.view.replace(edit, region, '')
                self.view.insert(edit, 0, text)
        self.view.sel().clear()

        all_file_region = sublime.Region(0, self.view.size())
        text = self.view.substr(all_file_region)
        text = _make_rules(text, COUNT_RULES)
        lines = text.split('\n')
        first_line = lines[0]
        lines = lines[1:]
        for index in range(len(lines)):
            lines[index] = str(index + 1) + ". \n" + lines[index]
            if index != len(lines):
                lines[index] += '\n'
        
        lines.insert(0, '<lj-cut text="Читать дальше">')
        lines.insert(0, '<a href=""><b>Оглавление</b></a>\n')
        lines.insert(0, first_line + '\n')
        lines.append('</lj-cut>')
        lines.append('<lj-like buttons="repost,facebook,twitter,google,vkontakte,livejournal" />')
        text = '\n'.join(lines)

        self.view.replace(edit, all_file_region, text)


if __name__ == '__main__':
	main()
