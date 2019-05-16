import html
import re

from IPython.display import HTML


def _split_by(string, sub_string):
    n = string.find(sub_string) + len(sub_string)
    return string[:n], string[n:]


def _get_color_span(p, s, color_captured_group=False):
    black_string = StyledSpan(s, 'black', None, False)
    r = re.search(p, s)
    if r is None:
        return black_string.render()
    span = r.span()

    matched_string = s[span[0]:span[1]]

    blue_string = StyledSpan(matched_string, 'black', None, True)
    black_string.sub_colored_strings = [blue_string]

    if color_captured_group:
        green_strings = [StyledSpan(captured, 'red', None, False) for captured in r.groups()]
        blue_string.sub_colored_strings = green_strings

    return black_string.render()


class StyledSpan:
    def __init__(self, string, color, sub_colored_strings=None, border=False):
        self.string = string
        self.color = color
        self.sub_colored_strings = sub_colored_strings or []
        self.border = border

    def render(self):
        border_style = 'border: 1px solid red' if self.border else ''
        if len(self.sub_colored_strings) == 0:
            return "<span style='font-size:18px;color:{};{}'>{}</span>".format(self.color, border_style, self.string)
        else:
            strs = []
            # string = html.escape(self.string)
            string = self.string
            for sub_colored_string in self.sub_colored_strings:
                first_part, last_part = _split_by(string, sub_colored_string.string)
                first_part = first_part.replace(sub_colored_string.string, sub_colored_string.render(), 1)
                strs.append(first_part)
                string = last_part
            strs.append(last_part)

            string = "<span style='font-size:18px;color:{};{}'>{}</span>".format(self.color, border_style,
                                                                                 ''.join(strs))
            return string


def search_pattern(patterns, strings, color_captured_group=False):
    html_string = ''
    for string in strings:
        string = html.escape(string)
        html_string += '<td style="font-size:18px">{}</td>'.format(string)
        for pattern in patterns:
            html_string += "<td>{}</td>".format(_get_color_span(pattern, string, color_captured_group))
        html_string = '<tr>' + html_string + '</tr>'
    header = '<tr><th></th>{}</tr>'.format(
        ''.join(['<th style="font-size:18px">{}</th>'.format(pattern) for pattern in patterns]))
    html_string = '<table>' + header + html_string + '</table>'
    return HTML(html_string)
