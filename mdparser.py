#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re, sys
from html import escape

class Stack:
    def __init__(self):
        self._stack = []

    def empty(self):
        return len(self._stack) == 0

    def push(self, el):
        self._stack.append(el)

    def pop(self):
        if not self.empty():
            self._stack.pop()

    def top(self):
        if not self.empty():
            return self._stack[-1]

    def size(self):
        return len(self._stack)

class PythonParser:
    def __init__(self, codeblock):
        '''
        TODO
        '''
        self._codeblock = codeblock

    def _set_keyword_list(self):
        self._keyword_list = ['None', 'False', 'True', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield']

    def run(self):
        pass

    def parse(self):
        """
        空格和换行符是分割符
        被单引号''包围, 或者被双引号""包围的内容，是一块整体

        1. keyword -> pl-k
        2. function -> pl-en
        2. comment -> pl-c
        3. string -> pl-s
        5. digit -> pl-c1
        6. 普通变量 -> pl-v
        """
        pass

class MarkdownParser:
    def __init__(self, filename='readme.md'):
        self._set_stack()
        self._set_params()
        self._set_template()
        self._set_content_buf(filename)

    def print_todo(self):
        todo = """[TODO]:
        1. 空行
        2. code color style map
        """
        print(todo)

    def interpretation_rules(self):
        """
        _ul_stack 为空时
            无 indent
                _code_block_stack 为空，则解释为 <p></p>
                _code_block_stack 非空, 则解释为 codeblock
            [暂不支持]有 indent 则解释为 codeblock

        _ul_stack 不为空
            若 _code_block_stack 为空, 说明是 list
            若 _code_block_stack 非空, 说明是 codeblock
        """

        """
        支持的 marker


        [Done]
        hyper link    [text](link)
        image link    ![img](link)
        heading 后面的 <hr>
        quotation     > something
        整体页面格式（margin, padding）

        [Done]
        #   header1
        ##  header2
        ### header3
        ####    header4

        [Done]
        paragraph

        [Done]
        段落中的 `highlight`, 颜色暂定为红色 #dd0055

        [Done]
        *   ul

        [done]
        <br>

        ```python
        高亮颜色暂时不支持
        <div class="highlight highlight-source-lang">
            <pre>
            ...codeblock
            </pre>
        </div>
        ```

        [暂时不支持 ol]
        暂时只支持序号为 0~9 的ol, 其他的序号将归为 plain paragraph
        0.  ol
        1.  ol
        2.  ol
        3.  ol
        x...ol
        9.  ol

        暂时不支持 斜体*italic* 和 粗体 **bold**
        暂时不支持表格
        默认4空格缩进
        必须写一行空一行

        允许的 html tag 只有 <br>
        """

    def _set_params(self):
        self._std_indent = 4

    def _set_content_buf(self, filename='readme.md'):
        self.filename = filename
        with open(filename, encoding='utf-8') as f:
            self.md_content = f.read().split('\n')

        # 末尾增加类似EOF的东西，方便一致性处理
        self.md_content.append('#')
        # 从 md_content[-1] 开始扫描和parse line
        # 扫完一个 line, 就 md_content.pop()
        self.md_content.reverse()
        # 并把 parse 后的 line 放到新的数组中, parsed_content.append(line)
        self.parsed_content = []

    def _set_stack(self):
        self._ul_stack = Stack()
        self._code_block_stack = Stack()

    def _set_template(self):
        self.heading_template = "<h%(heading_font_size)d>%(heading_content)s</h%(heading_font_size)d>"
        self.paragraph_template = "<p>%(paragraph_content)s</p>"
        self.li_template = "<li>%(li_content)s</li>"

    def set_heading_font(self, line):
        line = escape(line)
        for ix in range(len(line)):
            if line[ix] != '#':
                # ix = cnt_sharp, and heading_font_size = cnt_sharp
                heading_font_size = ix
                heading_content = line[ix:].lstrip(' ')
                '''
                增加 if, 因为我们之前在 _set_content_buf 中增加了一个 # 作为 EOF
                这个 EOF 仅用于调用 _end_ul 从而对 ul 收尾, 而不能生成实际的 <h1>
                '''
                heading_dict = {
                    'heading_font_size': heading_font_size,
                    'heading_content': heading_content
                }
                heading = self.heading_template % heading_dict
                self.parsed_content.append(heading)
                break

    def _html_escape(self, line):
        if line == '<br>':
            return line
        else:
            return escape(line)

    def parse_codeblock_header(self, line, indent=0):
        if self._code_block_stack.empty():
            self._code_block_stack.push(line)
            language = line[3:]
            content = '<div class="highlight highlight-source-' + language + '"><pre>'
            self.parsed_content.append(content)
        else:
            self._code_block_stack.pop()
            content = '</pre></div>'
            self.parsed_content.append(content)

    def parse_ul(self, line, indent=0):
        """
        TODO
        连续的 * 属于同一个 <ul>, 都是 <li>
        直到遇到 indent - std_indent 的内容, 才停止 </ul>
        如果 stack.empty(), 说明是开头, 把 * 去掉，然后 push(indent)
        添加 </ul> 的工作交给 paragraph, 和 header,
        这里只在 stack 里面记录 indent

        或者每次都在 parsed_content 末尾先加上 </ul>
        下次进来如果 indent 相同, 那么把末尾的 </ul> 先 pop 再
        *   123
        *   456
            789
            *   123
            123
        """
        if self._ul_stack.empty():
            '添加 <ul>'
            self._ul_stack.push(indent)
            self.parsed_content.append('<ul><li>')
        else:
            if self._ul_stack.top() == indent:
                """
                *   123
                *   234
                """
                '对上面的 li 收尾 </li>, 再加新的 <li>'
                self.parsed_content.append('</li><li>')
            elif self._ul_stack.top() < indent:
                """
                *   456
                    789
                    *   123
                """
                '添加 <ul><li>'
                self._ul_stack.push(indent)
                self.parsed_content.append('<ul><li>')
            else:
                # 大于
                """
                *   456
                    *   123
                *   789
                """
                '先对前面进行收尾'
                self._end_ul(indent)
                '然后添加 </li><li>'
                self.parsed_content.append('</li><li>')

        line = line.lstrip('*').lstrip(' ')
        self.parse_paragraph(line, indent + self._std_indent)

    def _end_ul(self, indent):
        '先对前面进行收尾'
        while ( (not self._ul_stack.empty()) and self._ul_stack.top() > indent ):
            self._ul_stack.pop()
            self.parsed_content.append('</li></ul>')

    def parse_paragraph(self, line, indent=0):
        if line.startswith('```'):
            paragraph = self.parse_codeblock_header(line, indent)
        else:
            if self._code_block_stack.empty():
                # paragraph
                blockquote = False
                if line.startswith('>'):
                    blockquote = True
                    line = line[1:]
                line = self._html_escape(line)

                line = self.parse_highlight(line)
                line = self.parse_link(line)
                paragraph = '<p>' + line + '</p>'
                if blockquote:
                    paragraph = '<blockquote>' + paragraph + '</blockquote>'
                self.parsed_content.append(paragraph)
            else:
                # codeblock
                paragraph = line + '\n'
                self.parsed_content.append(paragraph)

    def parse_highlight(self, line):
        # self._re_highlight_pattern = re.compile(r'`{1}(.*?)`{1}')
        # self._re_highlight_repl = r'<code>\1</code>'
        # paragraph_content = self._re_highlight_pattern.sub(self._re_highlight_repl, line)
        # s = '`hello`, `world`, this is `l``.'
        pattern = r'`(.*?)`'
        repl = r'<code>\1</code>'
        # 可以用 split + 拼接 实现同样的功能
        line = re.sub(pattern, repl, line)
        return line

    def parse_link(self, line):
        pattern_img_link = r'!\[(.*?)\]\((.*?)\)'
        repl = r'<a href="\2"><img src="\2" alt="\1"></a>'
        line = re.sub(pattern_img_link, repl, line)

        pattern_link = r'\[(.*?)\]\((.*?)\)'
        repl = r'<a href="\2" rel="nofollow">\1</a>'
        line = re.sub(pattern_link, repl, line)
        return line

    def classify_and_parse_content(self, line, indent=0):
        len_line = len(line)
        if len_line > 0:
            ch = line[0]
            if ch == '*':
                self.parse_ul(line, indent + self._std_indent)
            # elif ch.isdigit() and len_line > 1 and line[1] == '.':
                # 'self.parse_ol()'
            else:
                if ch == ' ':
                    indent += self._std_indent
                    if self._std_indent < len_line:
                        sub_line = line[self._std_indent:]
                        self.classify_and_parse_content(sub_line, indent)
                    else:
                        # 不符合规范，暂时不支持
                        'self.parse_paragraph(line, indent)'
                else:
                    if line == '':
                        print('blank')
                    # '先对前面进行收尾'
                    self._end_ul(indent)
                    self.parse_paragraph(line, indent)

    def parse_md_content(self):
        while len(self.md_content):
            line = self.md_content[-1]
            self.md_content.pop()
            if len(line) > 0:
                if line == 'exit':
                    return
                ch = line[0]
                indent = 0
                if ch == '#':
                    '先对前面进行收尾'
                    self._end_ul(indent)
                    self.set_heading_font(line)
                else:
                    'classify_and_parse_content 与 parse_md_content 分开'
                    '方便 classify_and_parse_content 的递归调用'
                    self.classify_and_parse_content(line, indent)
            else:
                if not self._code_block_stack.empty():
                    self.parsed_content.append('\n')

    def make_html_content(self):
        with open('template.html', encoding='utf-8') as f:
            template = f.read()

        title = self.filename.rstrip('.md')
        content = {
            'title': title,
            'content': ''.join(self.parsed_content)
        }
        html_content = template % content
        html_filename = title + '.html'
        with open(html_filename, 'w', encoding='utf-8') as f:
            f.write(html_content)

    def run(self):
        self.parse_md_content()
        self.make_html_content()
        # self.print_todo()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        parser = MarkdownParser(filename)
        parser.run()
    else:
        print('Usage:\n  python3 mdparser.py [filename]\n')
