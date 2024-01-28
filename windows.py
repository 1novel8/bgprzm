from datetime import datetime
from multiprocessing import Process
from tkinter import (Button, Checkbutton, IntVar, Label, StringVar, Tk,
                     messagebox)
from tkinter.ttk import Combobox

from tkcalendar import DateEntry

from enums import Forma22Enum, SVovlechEnum
from services import ExcelReportService


class MainWindow:
    def __init__(self) -> None:
        self.service = ExcelReportService()

        #  general
        self.width = 900
        self.height = 700
        self.root = Tk()
        self.root.title("ИНФОРМАЦИЯ О ВОВЛЕЧЕНИИ ЗЕМЕЛЬ")
        self.root.geometry(f"{self.width}x{self.height}")

        #  button
        self.generate_report_button = Button(
            self.root,
            text="Создать отчет",
            command=self._generate_report_clicked,
        )
        self.generate_report_button.place(x=self.width * 0.45, y=self.height * 0.9)

        # date
        self.use_date = IntVar(value=0)
        self.use_date_checkbutton = Checkbutton(
            self.root,
            text="Использовать дату",
            variable=self.use_date,
            command=self._use_date_checkbutton_clicked
        )
        self.use_date_checkbutton.place(x=self.width * 0.4, y=self.height * 0.03)
        self.start_date_label = Label(self.root, text="Дата начала")
        self.start_date_label.place(x=self.width * 0.1, y=self.height * 0.05)
        self.start_date_entry = DateEntry(self.root, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.start_date_entry['state'] = 'disabled'
        self.start_date_entry.place(x=self.width * 0.1, y=self.height * 0.1)
        self.finish_date_label = Label(self.root, text="Дата окончания")
        self.finish_date_label.place(x=self.width * 0.7, y=self.height * 0.05)
        self.finish_date_entry = DateEntry(self.root, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.finish_date_entry['state'] = 'disabled'
        self.finish_date_entry.place(x=self.width * 0.7, y=self.height * 0.1)

        # forma22
        self.forma22_checkbuttons = []
        self.forma22_checkbuttons_values = []
        self.forma22_lable = Label(self.root, text="Forma22")
        self.forma22_lable.place(x=self.width * 0.01, y=self.height * 0.15)
        for i, key in enumerate(Forma22Enum.get_keys()):
            value = IntVar(value=1)
            checkbutton = Checkbutton(
                self.root,
                text=self._limit_text_length(Forma22Enum.get_value(key)),
                variable=value,
            )
            checkbutton.place(x=self.width * 0.01, y=self.height * 0.18 + self.height * (i * 0.03))
            self.forma22_checkbuttons_values.append(value)
            self.forma22_checkbuttons.append(checkbutton)

        # Oblast
        self.oblast_lable = Label(self.root, text='Область')
        self.oblast_lable.place(x=self.width*0.52, y=self.height * 0.15)
        self.oblast_value = StringVar(value='Все')
        self.oblast_list = self._get_oblast_list()
        self.oblast_list.append('Все')
        self.oblast_combobox = Combobox(self.root, textvariable=self.oblast_value, values=self.oblast_list)
        self.oblast_combobox.place(x=self.width*0.58, y=self.height * 0.15)
        self.oblast_combobox.bind("<<ComboboxSelected>>", self._oblast_combobox_selected)

        # Rayon
        self.rayon_lable = Label(self.root, text='Район')
        self.rayon_lable.place(x=self.width*0.75, y=self.height * 0.15)
        self.rayon_value = StringVar(value='Все')
        self.rayon_list = ['Все']
        self.rayon_combobox = Combobox(self.root, textvariable=self.rayon_value, values=self.rayon_list)
        self.rayon_combobox.place(x=self.width*0.80, y=self.height * 0.15)

        # SVovlech
        self.svovlech_checkbuttons = []
        self.svovlech_checkbuttons_values = []
        self.svovlech_lable = Label(self.root, text="Svovlech")
        self.svovlech_lable.place(x=self.width * 0.51, y=self.height * 0.21)
        for i, key in enumerate(SVovlechEnum.get_info_keys()):
            value = IntVar(value=1)
            checkbutton = Checkbutton(
                self.root,
                text=self._limit_text_length(SVovlechEnum.get_info_value(key)),
                variable=value,
            )
            checkbutton.place(x=self.width * 0.51, y=self.height * 0.25 + self.height * (i * 0.03))
            self.svovlech_checkbuttons_values.append(value)
            self.svovlech_checkbuttons.append(checkbutton)

    def _oblast_combobox_selected(self, event) -> None:
        self.rayon_list = ['Все', ]
        if self.oblast_value.get() != 'Все':
            self.rayon_list.extend(self.service.repository.get_rayon_list_by_oblast(oblast=self.oblast_value.get()))
        self.rayon_combobox.set('Все')
        self.rayon_combobox['values'] = self.rayon_list

    def _get_oblast_list(self) -> list[str]:
        return self.service.repository.get_oblast_list()

    def _use_date_checkbutton_clicked(self) -> None:
        if self.use_date.get() == 0:
            self.finish_date_entry['state'] = 'disabled'
            self.start_date_entry['state'] = 'disabled'
        else:
            self.finish_date_entry['state'] = 'enabled'
            self.start_date_entry['state'] = 'enabled'

    def _generate_report_clicked(self) -> None:
        prompt = self._generate_prompt()
        if prompt is None:
            return
        self._show_info_message('Запрос принят. Скоро ваш отчет появится в папке output.')
        generate_report_process = Process(
            target=self.service.generate_report,
            kwargs=prompt
        )
        generate_report_process.start()

    def _generate_prompt(self) -> dict | None:
        prompt = {}
        # date
        if self.use_date.get() == 1:
            start_date = self._convert_datetime(self.start_date_entry.get_date())
            finish_date = self._convert_datetime(self.finish_date_entry.get_date())
            if start_date > finish_date:
                self._show_error_message('Дата начала не может быть больше чем дата окончания')
                return
            prompt['start_date'] = start_date
            prompt['finish_date'] = finish_date
        # forma22
        forma22_prompt = self._get_forma22_prompt()
        if forma22_prompt is None:
            self._show_error_message('Вы должны выбрать хотя бы 1 признак Форма22')
            return None
        prompt['forma22'] = forma22_prompt
        # svovlech
        svovlech_prompt = self._get_svovlech_prompt()
        if svovlech_prompt is None:
            self._show_error_message('Вы должны выбрать хотя бы 1 признак SVovlech')
            return None
        svovlech_prompt.append(0)
        prompt['svovlech'] = svovlech_prompt
        # rayon
        if self.rayon_value.get() not in self.rayon_list:
            self._show_error_message('Район выбран некорректно')
            return None
        if self.rayon_value.get() != 'Все':
            prompt['rayon'] = self.rayon_value.get()
        # oblast
        if self.oblast_value.get() not in self.oblast_list:
            self._show_error_message('Область выбрана некорректно')
            return None
        if self.oblast_value.get() != 'Все':
            prompt['oblast'] = self.oblast_value.get()

        return prompt

    def _get_svovlech_prompt(self) -> list | None:
        svovlech_prompt = list()
        for i, key in enumerate(SVovlechEnum.get_info_keys()):
            if self.svovlech_checkbuttons_values[i].get() == 1:
                svovlech_prompt.append(key)
        if len(svovlech_prompt) == 0:
            return None
        svovlech_prompt.append(0)
        return svovlech_prompt

    def _get_forma22_prompt(self) -> list | None:
        forma22_prompt = list()
        for i, key in enumerate(Forma22Enum.get_keys()):
            if self.forma22_checkbuttons_values[i].get() == 1:
                forma22_prompt.append(key)
        if len(forma22_prompt) == 0:
            return None
        return forma22_prompt

    @staticmethod
    def _convert_datetime(date) -> datetime:
        return datetime(year=date.year, month=date.month, day=date.day)

    @staticmethod
    def _show_error_message(message) -> None:
        messagebox.showerror("Ошибка", f"{message}")

    @staticmethod
    def _show_info_message(message) -> None:
        messagebox.showinfo("Информация", f"{message}")

    @staticmethod
    def _limit_text_length(text, max_length=70):
        if len(text) > max_length:
            return text[:max_length - 3] + "..."
        return text

    def run(self) -> None:
        self.root.mainloop()
