import xlwings as xw


def write_line(content: str, txt, newline=False, quote=True):
    if content.endswith('\\n'):
        content = content[:len(content) - 2]
        if quote:
            txt.write(content + '\"\n')
        else:
            txt.write(content + '\n')
        if newline:
            txt.write('\n')
    else:
        if quote:
            txt.write(content + '\"\n')
        else:
            txt.write(content + '\n')
        if newline:
            txt.write('\n')


print('xlsx转po工具 by mirage')
location = input('输入xlsx文件路径：')
app = xw.App(visible=False, add_book=False)
wb = app.books.open(location)
sht = xw.sheets[0]
length = len(sht.used_range.value) - 1
print('共有' + str(length) + '行')
f = open('output.po', 'a', encoding='utf-8')
f.write("""msgid ""
msgstr ""
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"

""")
for i in range(2, length + 2):
    print('正在处理第' + str(i) + '行')
    location = str(sht.range('A' + str(i)).value).replace('\n', '\\n')
    if location is not None and '' != location:
        write_line('#: ' + location, f, quote=False)
    msgctxt = str(sht.range('B' + str(i)).value).replace('\n', '\\n')
    if msgctxt is not None and '' != msgctxt:
        write_line('msgctxt \"' + msgctxt, f)
    source = str(sht.range('C' + str(i)).value).replace('\n', '\\n')
    if source is not None and '' != source:
        write_line('msgid \"' + source, f)
    target = str(sht.range('D' + str(i)).value).replace('\n', '\\n')
    if target is not None and '' != target:
        write_line('msgstr \"' + target, f, newline=True)
f.close()
wb.close()
