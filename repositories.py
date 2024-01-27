from datetime import datetime

from sqlalchemy import Select, func, select

from database import session_maker
from models import DKR


class DKRRepository:
    model = DKR

    def _filter_by_date(
            self,
            queryset: Select,
            start_date: datetime,
            finish_date: datetime,
    ) -> Select:
        return queryset.where(
            self.model.Data_Vvoda >= start_date,
            self.model.Data_Vvoda <= finish_date
        )

    def _filter_by_oblast(
            self,
            queryset: Select,
            oblast: str,
    ) -> Select:
        return queryset.where(self.model.Oblast == oblast)

    def _filter_by_rayon(
            self,
            queryset: Select,
            rayon: str,
    ) -> Select:
        return queryset.where(self.model.Rayon == rayon)

    def _filter_by_forma22(
            self,
            queryset: Select,
            forma22: list[str],
    ) -> Select:
        return queryset.where(self.model.Forma22.in_(forma22))

    def _filter_by_svovlech(
            self,
            queryset: Select,
            svovlech: list[int],
    ) -> Select:
        return queryset.where(self.model.SVovlech.in_(svovlech))

    def _get_report_queryset(self) -> Select:
        query = select(
            self.model.Oblast,
            self.model.Rayon,
            self.model.Forma22,
            self.model.SVovlech,
            func.count(self.model.Area_ga).label('Area_ga count'),
            func.sum(self.model.Area_ga).label('Area_ga sum'),
        ).group_by(
            self.model.Oblast
        ).group_by(
            self.model.Rayon
        ).group_by(
            self.model.Forma22
        ).group_by(
            self.model.SVovlech
        ).order_by(
            self.model.Oblast,
            self.model.Rayon,
            self.model.Forma22,
            self.model.SVovlech,
        )
        return query

    def get_report_data(
            self,
            start_date: datetime = None,
            finish_date: datetime = None,
            forma22: list[str] = None,
            oblast: str = None,
            rayon: str = None,
            svovlech: list[int] = None,
    ) -> list[dict]:
        queryset = self._get_report_queryset()
        if start_date is not None and finish_date is not None:
            queryset = self._filter_by_date(queryset, start_date, finish_date)
        if forma22 is not None:
            queryset = self._filter_by_forma22(queryset, forma22)
        if oblast is not None:
            queryset = self._filter_by_oblast(queryset, oblast)
        if rayon is not None:
            queryset = self._filter_by_rayon(queryset, rayon)
        if svovlech is not None:
            queryset = self._filter_by_svovlech(queryset, svovlech)

        print(queryset)
        with session_maker() as session:
            result = session.execute(queryset).mappings().fetchall()
        return result

    def get_oblast_list(self) -> list:
        queryset = select(
            self.model.Oblast
        ).distinct(
            self.model.Oblast
        ).order_by(
            self.model.Oblast
        )
        with session_maker() as session:
            result = session.scalars(queryset).all()
        return result

    def get_rayon_list_by_oblast(self, oblast: str) -> list[str]:
        queryset = select(
            self.model.Rayon
        ).distinct(
            self.model.Rayon
        ).where(
            self.model.Oblast == oblast
        ).order_by(
            self.model.Rayon
        )
        with session_maker() as session:
            result = session.scalars(queryset).all()
        return result
