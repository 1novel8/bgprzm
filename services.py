from datetime import datetime

import xlsxwriter
from xlsxwriter import Workbook
from xlsxwriter.worksheet import Worksheet

from enums import Forma22Enum, SVovlechEnum
from repositories import DKRRepository


class ExcelReportService:

    def __init__(self) -> None:
        self.repository = DKRRepository()
        self.default_info = {
            'A1:S1': 'ИНФОРМАЦИЯ О ВОВЛЕЧЕНИИ ЗЕМЕЛЬ ПОД ДРЕВЕСНО-КУСТАРНИКОВОЙ РАСТИТЕЛЬНОСТЬЮ',
            'A3:B3': 'за период',
            'A4:B4': 'Республика, Область, район',
            'A7:A10': 'Наименование административно-территориальной единицы (района, города областного подчинения)',
            'B7:B10': 'Категория землепользователя по Форме 22',
            'C7:D9': 'Всего земель под древесно-кустарниковой растительностью по данным ЗИС',
        }
        self.total_info = [
            'обследовано местным исполнительным комитетом',
            'не обследовано местным исполнительным комитетом',
        ]
        self.svovlech_row = {}
        self.svovlech_ends: int
        self.ws: Worksheet
        self.wb: Workbook

    def generate_report(self, **kwargs) -> None:
        self._create_file()
        statistics_row = self.repository.get_report_data(**kwargs)
        self._create_hat(**kwargs)
        self._fill_table(statistics_row)
        self.wb.close()

    def _create_hat(
            self,
            start_date: datetime = None,
            finish_date: datetime = None,
            forma22: list[str] = None,
            oblast: str = None,
            rayon: str = None,
            svovlech: list[int] = None,
    ) -> None:
        hat_format = self.wb.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'text_wrap': True,
        })
        for key in self.default_info:
            self.ws.merge_range(key, self.default_info[key], cell_format=hat_format)

        if start_date is not None and finish_date is not None:
            self.ws.write(2, 2, start_date.strftime(format='%d/%m/%Y'))
            self.ws.write(2, 3, finish_date.strftime(format='%d/%m/%Y'))
        if oblast is not None:
            self.ws.write(3, 2, oblast)
        if rayon is not None:
            self.ws.write(3, 3, rayon)

        self.ws.write(9, 2, 'количество контуров')
        self.ws.write(9, 3, 'площадь, га')

        svovlech_i = 4
        for key in svovlech:
            if key == 0:
                continue
            self.ws.merge_range(8, svovlech_i, 8, svovlech_i + 1, SVovlechEnum.get_info_value(key), hat_format)
            self.ws.write(9, svovlech_i, 'количество контуров')
            self.ws.write(9, svovlech_i + 1, 'площадь, га')
            self.svovlech_row[key] = svovlech_i
            svovlech_i += 2

        self.svovlech_ends = svovlech_i - 2
        for val in self.total_info:
            self.ws.merge_range(7, svovlech_i, 8, svovlech_i + 1, val, hat_format)
            self.ws.write(9, svovlech_i, 'количество контуров')
            self.ws.write(9, svovlech_i + 1, 'площадь, га')
            svovlech_i += 2
        for i in range(self.svovlech_ends+6):
            self.ws.write(10, i, f'{i+1}')
        self.ws.merge_range(7, 4, 7, self.svovlech_ends+1,
                            'по результатам уточнения местного исполнительного комитета', hat_format)
        self.ws.merge_range(6, 4, 6, self.svovlech_ends + 5,
                            'из них', hat_format)

    def _create_file(self) -> None:
        file_name = f'./output/{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.xlsx'
        workbook = xlsxwriter.Workbook(file_name)
        worksheet = workbook.add_worksheet()
        self.ws = worksheet
        self.wb = workbook

    def _set_file_format(self) -> None:
        main_format = self.wb.add_format({
            'align': 'left',
            'valign': 'vcenter',
        })
        self.ws.set_column(2, 25, width=10, cell_format=main_format)
        self.ws.set_column(0, 1, width=20, cell_format=main_format)
        self.ws.set_row(8, 40)
        self.ws.set_row(9, 30)

    def _fill_table(self, statistics: list[dict]) -> None:
        oblast = None
        rayon = None
        forma22 = None
        unprocessed_count = 0
        unprocessed_sum = 0
        rayon_starts_i = 12
        i = 10

        for row in statistics:
            if oblast != row['Oblast']:
                oblast = row['Oblast']
                i += 1
                self.ws.write(i, 0, oblast)
                forma22 = None

            if rayon != row['Rayon']:
                forma22 = None
                i += 1
                if rayon is not None:
                    self._set_column_sum_formulas(start=rayon_starts_i, end=i)
                self.ws.write(i, 0, row['Rayon'])
                rayon_starts_i = i
                rayon = row['Rayon']

            if forma22 != row['Forma22']:
                i += 1
                self.ws.write(i, 1, f'{row['Forma22']} - {Forma22Enum.get_value(row['Forma22'])}')
                self._set_row_sum_formulas(row=i)
                self.ws.write(i, self.svovlech_ends + 4, unprocessed_count)
                self.ws.write(i, self.svovlech_ends + 5, unprocessed_sum)
                unprocessed_count = 0
                unprocessed_sum = 0
                forma22 = row['Forma22']

            if row['SVovlech'] != 0:
                self._write_svovlech_values(i, row['SVovlech'], row['Area_ga count'], row['Area_ga sum'])
            else:
                unprocessed_count += row['Area_ga count']
                unprocessed_sum += row['Area_ga sum']
        self._set_column_sum_formulas(start=rayon_starts_i, end=i + 1)
        self._set_file_format()

    def _set_column_sum_formulas(self, start, end) -> None:
        for col_num in range(self.svovlech_ends + 4):
            self.ws.write_formula(start, col_num + 2,
                                  f'=SUM({chr(67 + col_num)}{start + 2}:{chr(67 + col_num)}{end})')

    def _set_row_sum_formulas(self, row) -> None:
        sum_formula = '='
        count_formula = '='
        for j in self.svovlech_row.values():
            count_formula += f'{chr(65 + j)}{row + 1}+'
            sum_formula += f'{chr(65 + j + 1)}{row + 1}+'
        count_formula = count_formula[:-1]
        sum_formula = sum_formula[:-1]
        self.ws.write_formula(row, self.svovlech_ends + 2, count_formula)
        self.ws.write_formula(row, self.svovlech_ends + 3, sum_formula)
        self.ws.write_formula(row, 2,
                              f'={chr(67 + self.svovlech_ends)}{row + 1}+{chr(69 + self.svovlech_ends)}{row + 1}')
        self.ws.write_formula(row, 3,
                              f'={chr(68 + self.svovlech_ends)}{row + 1}+{chr(70 + self.svovlech_ends)}{row + 1}')

    def _write_svovlech_values(self, row: int, svovlech: int, count_: int, sum_: float):
        self.ws.write(row, self.svovlech_row[svovlech], count_)
        self.ws.write(row, self.svovlech_row[svovlech] + 1, sum_)
