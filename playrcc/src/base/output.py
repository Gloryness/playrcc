import re
from string import punctuation

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTextEdit

class OutputSender:
    def __init__(self, output: QTextEdit):
        self.output = output
        self.spans = ['<span>']

    def sendMouseToEnd(self):
        """
        Move the Text Cursor to the end
        """
        cursor = self.output.textCursor().document().find("------------------------------------------", 2)
        cursor.movePosition(cursor.StartOfLine, cursor.MoveAnchor, 85)
        self.output.setTextCursor(cursor)

    def addspan(self):
        if self.spans:
            if self.spans[-1] == '<span>':
                return self.addendspan()
            elif self.spans[-1] == '</span>':
                return self.addstartspan()
        else:
            return self.addstartspan()

    def addendspan(self):
        if self.spans:
            if self.spans[-1] == '<span>':
                self.spans.append('</span>')
                return '</span>'
            return ''
        return ''

    def addstartspan(self):
        if self.spans:
            if self.spans[-1] == '</span>':
                self.spans.append('<span>')
                return f'<span style= \" font-size:{self.size}pt;'
            return ''
        else:
            self.spans.append('<span>')
            return f'<span style= \" font-size:{self.size}pt;'

    def send_html(self, text: str, size=8, bold=False, italic=False, underline=False, newlinesbefore=0, newlinesafter=1, color="#000000"):
        """
        Insert HTML into the Output Text

        :param text: Output text
        :param size: Font size
        :param bold: Use bold
        :param italic: Use italic
        :param underline: Use underline
        :param newlinesbefore: How many new lines to put before the text
        :param newlinesafter: How many new lines to put after the text
        :param color: Output colour in STR or QColor
        :return: HTML
        """
        self.size = size
        self.sendMouseToEnd()

        html = []

        before = []
        after = []

        for _ in range(newlinesbefore): before.append("<br />")
        for _ in range(newlinesafter): after.append("<br />")

        if bold:
            html.append("font-weight:600")

        if italic:
            html.append("font-style:italic")

        if underline:
            html.append("text-decoration: underline")

        bold_ = re.findall(f'BOLD=\[[a-zA-Z0-9 \]{punctuation}]*]', text)
        italic_ = re.findall(f'ITALIC=\[[a-zA-Z0-9 \]{punctuation}]*]', text)
        underline_ = re.findall(f'UNDERLINE=\[[a-zA-Z0-9 \]{punctuation}]*]', text)
        color_ = re.findall(f'COLOR=\(\S*, [a-zA-Z0-9 \]{punctuation}]*\)', text)
        types_ = re.findall(f'TYPES=\[\([a-zA-Z0-9 \]{punctuation}]*\), [a-zA-Z0-9 \]{punctuation.replace("[", "")}]*]', text)


        if bold_:
            for i in bold_:
                txt = bold_[bold_.index(i)].replace("BOLD=", "").lstrip('[').rstrip(']')
                a, b, c = self.addendspan(), self.addspan(), self.addspan()
                text = text.replace(i, f'{a}{b} font-weight:600\">{txt}{c}')
        if italic_:
            for i in italic_:
                txt = italic_[italic_.index(i)].replace("ITALIC=", "").lstrip('[').rstrip(']')
                a, b, c = self.addendspan(), self.addspan(), self.addspan()
                text = text.replace(i, f'{a}{b} font-style:italic\">{txt}{c}')
        if underline_:
            for i in underline_:
                txt = underline_[underline_.index(i)].replace("UNDERLINE=", "").lstrip('[').rstrip(']')
                a, b, c = self.addendspan(), self.addspan(), self.addspan()
                text = text.replace(i, f'{a}{b} text-decoration: underline\">{txt}{c}')
        if color_:
            for i in color_:
                colourAndText = color_[color_.index(i)].replace("COLOR=", "").lstrip('(').rstrip(')')
                colourAndText = colourAndText.split(', ')
                a, b, c = self.addendspan(), self.addspan(), self.addspan()
                text = text.replace(i, f'{a}{b} color: {colourAndText[0]}\">{colourAndText[1]}{c}')
        if types_:
            for i in types_:
                types = types_[types_.index(i)].replace("TYPES=", "").lstrip('[').rstrip(']')
                types = types.rsplit(', ', maxsplit=1)
                a, b, c = self.addendspan(), self.addspan(), self.addspan()
                result = []
                if types[0].__contains__('BOLD'):
                    result.append('font-weight:600')
                if types[0].__contains__('ITALIC'):
                    result.append('font-style:italic')
                if types[0].__contains__('UNDERLINE'):
                    result.append('text-decoration: underline')
                if types[0].__contains__('#'):
                    result.append('color:'+types[0][types[0].index('#'):types[0].index('#')+7])
                text = text.replace(i, f'{a}{b} {"; ".join(result)}\">{types[-1]}{c}')

        assert isinstance(color, (QColor, str))
        if isinstance(color, QColor):
            color = color.name()

        html.append(f"font-size:{size}pt")
        html.append(f"color:{color}")

        fullhtml = f"{''.join(before)}<span style=\" {'; '.join(html)}\">{text}</span>{''.join(after)}"
        self.output.insertHtml(fullhtml)
        self.spans.clear()
        self.spans.append('<span>')

        return fullhtml

    def send_text(self, text: str):
        """
        Insert Plain Text into the Output Text

        :param text: Output text
        :return: HTML
        """
        self.sendMouseToEnd()

        fulltext = f"<span>{text}</span><br />"
        self.output.insertHtml(fulltext)

        return fulltext