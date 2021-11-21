import sys
import sqlite3
import translators as ts
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDialog, QDialogButtonBox
from PyQt5 import uic
from PyQt5.QtWidgets import QInputDialog
from random import randint

AUTO_TRANSLATE = ["Google", "Bing", "Tencent"]
LANGUAGE = ['Английский', 'Немецкий']


class Lern_2(QDialog):
    def __init__(self, id, word, tr, tr_lang):
        super().__init__()
        self.id = id
        self.word = word
        self.tr = tr
        self.tr_lang = tr_lang
        uic.loadUi('design/lern_2.ui', self)
        self.translate.setText(self.tr)
        self.question.setText(f"Знаете как переводится слово '{self.word}'?")
        self.translate.hide()
        self.btn_know.hide()
        self.btn_dont_know.hide()
        self.show_translate.clicked.connect(self.show_tr)

    def show_tr(self):
        self.translate.show()
        self.btn_know.show()
        self.btn_dont_know.show()
        self.btn_know.clicked.connect(self.know)
        self.btn_dont_know.clicked.connect(self.dont_konw)

    def know(self):
        if self.tr_lang == 'en':
            self.con = sqlite3.connect('db/ru_en.db')
        elif self.tr_lang == 'de':
            self.con = sqlite3.connect('db/ru_de.db')
        self.cur = self.con.cursor()
        self.result = self.cur.execute("""UPDATE words
    SET coeff = 2
    WHERE id = ?""", (self.id,))
        self.con.commit()
        self.con.close()
        self.close()

    def dont_konw(self):
        self.close()


class Lern_3(QDialog):
    def __init__(self, id, word, tr, tr_lang, other):
        super().__init__()
        self.id = id
        self.word = word
        self.tr = tr
        self.tr_lang = tr_lang
        self.other = other
        uic.loadUi('design/lern_3.ui', self)
        self.question.setText(f"Как переводится слово '{self.word}'?")
        while len(self.other) != 4:
            self.other.append('')
        number = randint(1, 4)
        if number == 1:
            self.answer1.setText(self.tr)
            self.answer2.setText(self.other[0])
            self.answer3.setText(self.other[1])
            self.answer4.setText(self.other[2])
            self.answer1.clicked.connect(self.right_ans)
            self.answer2.clicked.connect(self.false_ans)
            self.answer3.clicked.connect(self.false_ans)
            self.answer4.clicked.connect(self.false_ans)

        elif number == 2:
            self.answer2.setText(self.tr)
            self.answer4.setText(self.other[0])
            self.answer3.setText(self.other[1])
            self.answer1.setText(self.other[2])
            self.answer2.clicked.connect(self.right_ans)
            self.answer1.clicked.connect(self.false_ans)
            self.answer3.clicked.connect(self.false_ans)
            self.answer4.clicked.connect(self.false_ans)
        elif number == 3:
            self.answer3.setText(self.tr)
            self.answer1.setText(self.other[0])
            self.answer4.setText(self.other[1])
            self.answer2.setText(self.other[2])
            self.answer3.clicked.connect(self.right_ans)
            self.answer2.clicked.connect(self.false_ans)
            self.answer1.clicked.connect(self.false_ans)
            self.answer4.clicked.connect(self.false_ans)
        else:
            self.answer4.setText(self.tr)
            self.answer3.setText(self.other[0])
            self.answer1.setText(self.other[1])
            self.answer2.setText(self.other[2])
            self.answer4.clicked.connect(self.right_ans)
            self.answer2.clicked.connect(self.false_ans)
            self.answer3.clicked.connect(self.false_ans)
            self.answer1.clicked.connect(self.false_ans)

        if not bool(self.answer1.text()):
            self.answer1.hide()
        if not bool(self.answer2.text()):
            self.answer2.hide()
        if not bool(self.answer3.text()):
            self.answer3.hide()
        if not bool(self.answer4.text()):
            self.answer4.hide()

        if self.tr_lang == 'en':
            self.con = sqlite3.connect('db/ru_en.db')
        elif self.tr_lang == 'de':
            self.con = sqlite3.connect('db/ru_de.db')
        self.cur = self.con.cursor()

    def right_ans(self):
        result = self.cur.execute("""UPDATE words
        SET coeff = 3
        WHERE id = ?""", (self.id,))
        self.con.commit()
        self.con.close()
        self.close()
    def false_ans(self):
        result = self.cur.execute("""UPDATE words
        SET coeff = 1
        WHERE id = ?""", (self.id,))
        self.con.commit()
        self.con.close()
        self.close()


class Lern_4(QDialog):
    def __init__(self, id, word, tr, tr_lang):
        super().__init__()
        self.id = id
        self.word = word
        self.tr = tr
        self.tr_lang = tr_lang
        uic.loadUi('design/lern_4.ui', self)
        self.error.hide()
        self.question.setText(f"Как переводится слово '{self.word}'?")
        self.btn_ok.clicked.connect(self.run)

    def run(self):
        if bool(self.answer.text()):
            text = self.answer.text().lower()
            if text == self.tr.lower():
                k = 4
            else:
                k = 2
            if self.tr_lang == 'en':
                self.con = sqlite3.connect('db/ru_en.db')
            elif self.tr_lang == 'de':
                self.con = sqlite3.connect('db/ru_de.db')
            self.cur = self.con.cursor()
            self.result = self.cur.execute("""UPDATE words
                SET coeff = ?
                WHERE id = ?""", (k, self.id,))
            self.con.commit()
            self.con.close()
            self.close()

        else:
            self.error.show()
            self.error.setText('Вы не ввели слово')


class AddNewWordWindow(QDialog):
    def __init__(self, tr_lang, tr_machine):
        super().__init__()
        self.tr_lang = tr_lang
        self.tr_machine = tr_machine
        uic.loadUi('design/add_new_word.ui', self)
        self.ok_btn.clicked.connect(self.add)

    def add(self):
        if self.tr_lang == 'en':
            self.con = sqlite3.connect('db/ru_en.db')
        elif self.tr_lang == 'de':
            self.con = sqlite3.connect('db/ru_de.db')
        self.cur = self.con.cursor()
        word = self.word.text()
        translate = self.translate.text()
        oth_translate = self.other_translate.text()
        example = self.example.text()
        if not bool(translate):
            if self.tr_machine == 'Google':
                translate = ts.google(word, from_language=self.tr_lang, to_language='ru')
            elif self.tr_machine == 'Bing':
                translate = ts.bing(word, from_language=self.tr_lang, to_language='ru')
            elif self.tr_machine == 'Tencent':
                translate = ts.bing(word, from_language=self.tr_lang, to_language='ru')

        if not bool(oth_translate):
            oth_translate = None

        if not bool(example):
            example = None
        if bool(word) and bool(translate):
            add = self.cur.execute(f"""INSERT INTO words(base_word, 
            translation_word, coeff, more_translation, example) VALUES(?, ?, 1, ?, ?)""",
                                   (word, translate, oth_translate, example,))
            self.con.commit()
            self.close()
        else:
            self.error.setText('Вы не ввели слово')

    def closeEvent(self, event):
        try:
            self.con.close()
        except AttributeError:
            pass


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('design/lern.ui', self)
        self.change_tr.triggered.connect(self.change_translate_machine)
        self.language.addItems(LANGUAGE)
        self.add_new_word.clicked.connect(self.add_word)
        self.lern_words.clicked.connect(self.lern)
        self.tr_machine = AUTO_TRANSLATE[0]

    def change_translate_machine(self):
        self.tr_machine = QInputDialog.getItem(self, "Выберите автоматический перводчик",
                                               "Выберите автоматический перводчик", AUTO_TRANSLATE,
                                               AUTO_TRANSLATE.index(self.tr_machine), False)[0]

    def add_word(self):
        self.tr_lang = self.get_lang()
        self.new_word_win = AddNewWordWindow(self.tr_lang, self.tr_machine)
        self.new_word_win.show()

    def lern(self):
        self.tr_lang = self.get_lang()
        if self.tr_lang == 'en':
            self.con = sqlite3.connect('db/ru_en.db')
        elif self.tr_lang == 'de':
            self.con = sqlite3.connect('db/ru_de.db')
        self.cur = self.con.cursor()
        for i in range(1, 4):
            result = self.cur.execute("""SELECT id, base_word, translation_word FROM words
    WHERE coeff = ?""", (i,)).fetchall()
            if bool(result):
                break
        id, word, tr = result[randint(1, len(result)) - 1]
        if i == 1:
            self.Lern = Lern_2(id, word, tr, self.tr_lang)
            self.Lern.show()
        elif i == 2:
            other = []
            for n in result:
                if n[2] != tr:
                    other.append(n[2])
                if len(other) == 4:
                    break
            self.Lern = Lern_3(id, word, tr, self.tr_lang, other)
            self.Lern.show()
        elif i == 3:
            self.Lern = Lern_4(id, word, tr, self.tr_lang)
            self.Lern.show()

    def get_lang(self):
        lang = self.language.currentText()
        if lang == 'Английский':
            tr_lang = 'en'
        elif lang == 'Немецкий':
            tr_lang = 'de'
        return tr_lang

    def closeEvent(self, event):
        try:
            self.con.close()
        except AttributeError:
            pass


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
