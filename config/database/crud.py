from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Dict, Union, Optional
from config.database.base import get_db, SessionLocal
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import Dict, List, Optional, Union, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from config.database.models import Password, Payment
import re
from collections import Counter


class PasswordCRUD:
    """CRUD операции для модели Password"""
    
    @staticmethod
    def create_record(
        db: Session,
        title: Optional[str] = None,
        password: Optional[str] = None,
        login: Optional[str] = None,
        url_site: Optional[str] = None,
        email: Optional[str] = None,
        notes: Optional[str] = None,
        key_words: Optional[Union[str, List[str]]] = None,
        creation_date: Optional[str] = None,
        change_date: Optional[str] = None
    ) -> Password:
        """Добавление записи пароля в базу данных"""
        
        # Создаем словарь с переданными значениями
        data = {}
        
        # Проверяем и добавляем каждое поле
        if title is not None and title.strip():
            data['title'] = title.strip()
            
        if password is not None and password.strip():
            data['password'] = password.strip()
            
        if login is not None and login.strip():
            data['login'] = login.strip()
            
        if url_site is not None and url_site.strip():
            data['url_site'] = url_site.strip()
            
        if email is not None and email.strip():
            data['email'] = email.strip()
            
        if notes is not None and notes.strip():
            data['notes'] = notes.strip()
            
        if key_words is not None:
            if isinstance(key_words, list):
                data['key_words'] = ', '.join(key_words)
            elif isinstance(key_words, str) and key_words.strip():
                data['key_words'] = key_words.strip()
        
        if creation_date is not None and creation_date:
            data['creation_date'] = creation_date
        else:
            data['creation_date'] = datetime.now().isoformat()
            
        if change_date is not None and change_date:
            data['change_date'] = change_date
            
        db_password = Password(**data)
        db.add(db_password)
        db.commit()
        db.refresh(db_password)
        return db_password
    
    @staticmethod
    def get_by_id(db: Session, password_id: int) -> Optional[Password]:
        """Получение записи по ID"""
        return db.query(Password).filter(Password.id == password_id).first()
    
    @staticmethod
    def get_all_data_by_id(db: Session, password_id: int) -> Union[Dict, None]:
        """Получение всех данных по ID в виде словаря"""
        password = db.query(Password).filter(Password.id == password_id).first()
        if password:
            return password.to_dict()
        return None
    
    @staticmethod
    def get_records(db: Session, *fields: str) -> List[tuple]:
        """Получение определенных полей из всех записей"""
        if not fields:
            # Если поля не указаны, выбираем все
            result = db.query(Password).all()
            return [tuple(p.to_dict().values()) for p in result]
        
        # Строим динамический запрос для выбранных полей
        columns = []
        for field in fields:
            if hasattr(Password, field):
                columns.append(getattr(Password, field))
        
        if columns:
            result = db.query(*columns).all()
            return result
        return []
    
    @staticmethod
    def get_all_records(db: Session) -> List[Password]:
        """Получение всех записей"""
        return db.query(Password).all()
    
    @staticmethod
    def update_record(
        db: Session,
        password_id: int,
        title: Optional[str] = None,
        password: Optional[str] = None,
        login: Optional[str] = None,
        url_site: Optional[str] = None,
        email: Optional[str] = None,
        notes: Optional[str] = None,
        key_words: Optional[Union[str, List[str]]] = None,
        creation_date: Optional[str] = None,
        change_date: Optional[str] = None
    ) -> Optional[Password]:
        """Обновление записи"""
        password_record = db.query(Password).filter(Password.id == password_id).first()
        if not password_record:
            return None
        
        # Устанавливаем дату изменения
        password_record.change_date = datetime.now().isoformat()
        
        # Обновляем поля только если они переданы и не пустые
        if title is not None:
            password_record.title = title.strip() if title.strip() else None
            
        if password is not None:
            password_record.password = password.strip() if password.strip() else None
            
        if login is not None:
            password_record.login = login.strip() if login.strip() else None
            
        if url_site is not None:
            password_record.url_site = url_site.strip() if url_site.strip() else None
            
        if email is not None:
            password_record.email = email.strip() if email.strip() else None
            
        if notes is not None:
            password_record.notes = notes.strip() if notes.strip() else None
            
        if key_words is not None:
            if isinstance(key_words, list):
                password_record.key_words = ', '.join(key_words)
            elif isinstance(key_words, str):
                password_record.key_words = key_words.strip() if key_words.strip() else None
        
        if creation_date is not None:
            password_record.creation_date = creation_date.strip() if creation_date.strip() else None
            
        if change_date is not None:
            password_record.change_date = change_date.strip() if change_date.strip() else None
        
        db.commit()
        db.refresh(password_record)
        return password_record
    
    @staticmethod
    def delete_by_id(db: Session, password_id: int) -> bool:
        """Удаление записи по ID"""
        password = db.query(Password).filter(Password.id == password_id).first()
        if password:
            db.delete(password)
            db.commit()
            return True
        return False

class PaymentCRUD:
    """CRUD операции для модели Payment"""
    
    @staticmethod
    def create_record(
        db: Session,
        title: Optional[str] = None,
        password: Optional[str] = None,
        login: Optional[str] = None,
        url_site: Optional[str] = None,
        email: Optional[str] = None,
        notes: Optional[str] = None,
        key_words: Optional[Union[str, List[str]]] = None,
        creation_date: Optional[str] = None,
        change_date: Optional[str] = None
    ) -> Payment:
        """Добавление записи платежа в базу данных"""
        
        # Создаем словарь с переданными значениями
        data = {}
        
        # Проверяем и добавляем каждое поле
        if title is not None and title.strip():
            data['title'] = title.strip()
            
        if password is not None and password.strip():
            data['password'] = password.strip()
            
        if login is not None and login.strip():
            data['login'] = login.strip()
            
        if url_site is not None and url_site.strip():
            data['url_site'] = url_site.strip()
            
        if email is not None and email.strip():
            data['email'] = email.strip()
            
        if notes is not None and notes.strip():
            data['notes'] = notes.strip()
            
        if key_words is not None:
            if isinstance(key_words, list):
                data['key_words'] = ', '.join(key_words)
            elif isinstance(key_words, str) and key_words.strip():
                data['key_words'] = key_words.strip()
        
        if creation_date is not None and creation_date.strip():
            data['creation_date'] = creation_date.strip()
        else:
            data['creation_date'] = datetime.now().isoformat()
            
        if change_date is not None and change_date.strip():
            data['change_date'] = change_date.strip()
            
        db_payment = Payment(**data)
        db.add(db_payment)
        db.commit()
        db.refresh(db_payment)
        return db_payment
    
    @staticmethod
    def get_by_id(db: Session, payment_id: int) -> Optional[Payment]:
        """Получение записи по ID"""
        return db.query(Payment).filter(Payment.id == payment_id).first()
    
    @staticmethod
    def get_all_data_by_id(db: Session, payment_id: int) -> Union[Dict, None]:
        """Получение всех данных по ID в виде словаря"""
        payment = db.query(Payment).filter(Payment.id == payment_id).first()
        if payment:
            return payment.to_dict()
        return None
    
    @staticmethod
    def get_records(db: Session, *fields: str) -> List[tuple]:
        """Получение определенных полей из всех записей"""
        if not fields:
            result = db.query(Payment).all()
            return [tuple(p.to_dict().values()) for p in result]
        
        columns = []
        for field in fields:
            if hasattr(Payment, field):
                columns.append(getattr(Payment, field))
        
        if columns:
            result = db.query(*columns).all()
            return result
        return []
    
    @staticmethod
    def get_all_records(db: Session) -> List[Payment]:
        """Получение всех записей"""
        return db.query(Payment).all()
    
    @staticmethod
    def update_record(
        db: Session,
        payment_id: int,
        title: Optional[str] = None,
        password: Optional[str] = None,
        login: Optional[str] = None,
        url_site: Optional[str] = None,
        email: Optional[str] = None,
        notes: Optional[str] = None,
        key_words: Optional[Union[str, List[str]]] = None,
        creation_date: Optional[str] = None,
        change_date: Optional[str] = None
    ) -> Optional[Payment]:
        """Обновление записи"""
        payment_record = db.query(Payment).filter(Payment.id == payment_id).first()
        if not payment_record:
            return None
        
        # Устанавливаем дату изменения
        payment_record.change_date = datetime.now().isoformat()
        
        # Обновляем поля только если они переданы и не пустые
        if title is not None:
            payment_record.title = title.strip() if title.strip() else None
            
        if password is not None:
            payment_record.password = password.strip() if password.strip() else None
            
        if login is not None:
            payment_record.login = login.strip() if login.strip() else None
            
        if url_site is not None:
            payment_record.url_site = url_site.strip() if url_site.strip() else None
            
        if email is not None:
            payment_record.email = email.strip() if email.strip() else None
            
        if notes is not None:
            payment_record.notes = notes.strip() if notes.strip() else None
            
        if key_words is not None:
            if isinstance(key_words, list):
                payment_record.key_words = ', '.join(key_words)
            elif isinstance(key_words, str):
                payment_record.key_words = key_words.strip() if key_words.strip() else None
        
        if creation_date is not None:
            payment_record.creation_date = creation_date.strip() if creation_date.strip() else None
            
        if change_date is not None:
            payment_record.change_date = change_date.strip() if change_date.strip() else None
        
        db.commit()
        db.refresh(payment_record)
        return payment_record
    
    @staticmethod
    def delete_by_id(db: Session, payment_id: int) -> bool:
        """Удаление записи по ID"""
        payment = db.query(Payment).filter(Payment.id == payment_id).first()
        if payment:
            db.delete(payment)
            db.commit()
            return True
        return False

# Класс-менеджер для работы с базой данных
class DatabaseManager:
    def __init__(self):
        self.password_crud = PasswordCRUD()
        self.payment_crud = PaymentCRUD()
    
    def get_session(self) -> Session:
        """Получение сессии базы данных"""
        return SessionLocal()
    
    # Методы для работы с паролями
    def add_password_record(
        self,
        title: Optional[str] = None,
        password: Optional[str] = None,
        login: Optional[str] = None,
        url_site: Optional[str] = None,
        email: Optional[str] = None,
        notes: Optional[str] = None,
        key_words: Optional[Union[str, List[str]]] = None,
        creation_date: Optional[str] = None,
        change_date: Optional[str] = None
    ) -> Password:
        """Добавление записи пароля"""
        with self.get_session() as db:
            return self.password_crud.create_record(
                db, title, password, login, url_site, email, 
                notes, key_words, creation_date, change_date
            )
    
    def get_password_by_id(self, password_id: int) -> Union[Dict, None]:
        """Получение пароля по ID"""
        with self.get_session() as db:
            return self.password_crud.get_all_data_by_id(db, password_id)
    
    def read_password_records(self, *fields: str) -> List[tuple]:
        """Чтение записей паролей"""
        with self.get_session() as db:
            return self.password_crud.get_records(db, *fields)
    
    def delete_password_by_id(self, password_id: int) -> bool:
        """Удаление пароля по ID"""
        with self.get_session() as db:
            return self.password_crud.delete_by_id(db, password_id)
    
    def update_password(
        self,
        password_id: int,
        title: Optional[str] = None,
        password: Optional[str] = None,
        login: Optional[str] = None,
        url_site: Optional[str] = None,
        email: Optional[str] = None,
        notes: Optional[str] = None,
        key_words: Optional[Union[str, List[str]]] = None,
        creation_date: Optional[str] = None,
        change_date: Optional[str] = None
    ) -> Optional[Password]:
        """Обновление пароля"""
        with self.get_session() as db:
            return self.password_crud.update_record(
                db, password_id, title, password, login, url_site, 
                email, notes, key_words, creation_date, change_date
            )
    
    # Методы для работы с платежами
    def add_payment_record(
        self,
        title: Optional[str] = None,
        password: Optional[str] = None,
        login: Optional[str] = None,
        url_site: Optional[str] = None,
        email: Optional[str] = None,
        notes: Optional[str] = None,
        key_words: Optional[Union[str, List[str]]] = None,
        creation_date: Optional[str] = None,
        change_date: Optional[str] = None
    ) -> Payment:
        """Добавление записи платежа"""
        with self.get_session() as db:
            return self.payment_crud.create_record(
                db, title, password, login, url_site, email, 
                notes, key_words, creation_date, change_date
            )
    
    def get_payment_by_id(self, payment_id: int) -> Union[Dict, None]:
        """Получение платежа по ID"""
        with self.get_session() as db:
            return self.payment_crud.get_all_data_by_id(db, payment_id)
    
    def update_payment(
        self,
        payment_id: int,
        title: Optional[str] = None,
        password: Optional[str] = None,
        login: Optional[str] = None,
        url_site: Optional[str] = None,
        email: Optional[str] = None,
        notes: Optional[str] = None,
        key_words: Optional[Union[str, List[str]]] = None,
        creation_date: Optional[str] = None,
        change_date: Optional[str] = None
    ) -> Optional[Payment]:
        """Обновление платежа"""
        with self.get_session() as db:
            return self.payment_crud.update_record(
                db, payment_id, title, password, login, url_site, 
                email, notes, key_words, creation_date, change_date
            )
    
    def delete_payment_by_id(self, payment_id: int) -> bool:
        """Удаление платежа по ID"""
        with self.get_session() as db:
            return self.payment_crud.delete_by_id(db, payment_id)
        
@dataclass
class PasswordStatistics:
    """Статистика паролей"""
    total_passwords: int
    added_today: int
    added_this_week: int
    added_this_month: int
    avg_password_length: float
    min_password_length: int
    max_password_length: int
    most_common_domains: List[Tuple[str, int]]
    password_strength_distribution: Dict[str, int]
    most_used_keywords: List[Tuple[str, int]]
    
@dataclass
class GeneralStatistics:
    """Общая статистика"""
    total_records: int
    passwords_count: int
    payments_count: int
    records_added_today: int
    records_added_this_week: int
    records_added_this_month: int
    most_active_day: Optional[str]
    most_active_month: Optional[str]
    
    
class StatistikManager:
    """Менеджер для работы со статистикой паролей и платежей"""
    
    def __init__(self):
        pass
    
    def get_session(self) -> Session:
        """Получение сессии базы данных"""
        return SessionLocal()
    
    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Парсинг даты из строки"""
        if not date_str:
            return None
        try:
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except:
            try:
                return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            except:
                return None
    
    def _get_date_ranges(self) -> Tuple[datetime, datetime, datetime]:
        """Получение диапазонов дат для фильтрации"""
        now = datetime.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = today_start - timedelta(days=now.weekday())
        month_start = today_start.replace(day=1)
        
        return today_start, week_start, month_start
    
    def _assess_password_strength(self, password: str) -> str:
        """Оценка силы пароля"""
        if not password:
            return "unknown"
        
        score = 0
        length = len(password)
        
        # Длина
        if length >= 12:
            score += 2
        elif length >= 8:
            score += 1
        
        # Наличие цифр
        if re.search(r'\d', password):
            score += 1
        
        # Наличие букв в нижнем регистре
        if re.search(r'[a-z]', password):
            score += 1
        
        # Наличие букв в верхнем регистре
        if re.search(r'[A-Z]', password):
            score += 1
        
        # Наличие специальных символов
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            score += 1
        
        if score >= 5:
            return "strong"
        elif score >= 3:
            return "medium"
        else:
            return "weak"
    
    def _extract_domain(self, url: Optional[str]) -> Optional[str]:
        """Извлечение домена из URL"""
        if not url:
            return None
        
        # Удаляем протокол
        domain = url.replace('https://', '').replace('http://', '').replace('www.', '')
        # Берем только домен до первого слеша
        domain = domain.split('/')[0]
        # Берем основной домен (последние 2 части)
        parts = domain.split('.')
        if len(parts) >= 2:
            return f"{parts[-2]}.{parts[-1]}"
        return domain
    
    def get_password_statistics(self) -> PasswordStatistics:
        """Получение детальной статистики по паролям"""
        with self.get_session() as db:
            # Получаем все пароли
            passwords = db.query(Password).all()
            
            if not passwords:
                return PasswordStatistics(
                    total_passwords=0, added_today=0, added_this_week=0,
                    added_this_month=0, avg_password_length=0.0,
                    min_password_length=0, max_password_length=0,
                    most_common_domains=[], password_strength_distribution={},
                    most_used_keywords=[]
                )
            
            today_start, week_start, month_start = self._get_date_ranges()
            
            # Базовая статистика
            total_passwords = len(passwords)
            added_today = 0
            added_this_week = 0
            added_this_month = 0
            
            # Анализ паролей
            password_lengths = []
            domains = []
            strength_distribution = {"weak": 0, "medium": 0, "strong": 0, "unknown": 0}
            all_keywords = []
            
            for password_record in passwords:
                # Анализ дат
                creation_date = self._parse_date(password_record.creation_date)
                if creation_date:
                    if creation_date >= today_start:
                        added_today += 1
                    if creation_date >= week_start:
                        added_this_week += 1
                    if creation_date >= month_start:
                        added_this_month += 1
                
                # Анализ длины паролей
                if password_record.password:
                    password_lengths.append(len(password_record.password))
                    
                    # Анализ силы пароля
                    strength = self._assess_password_strength(password_record.password)
                    strength_distribution[strength] += 1
                
                # Анализ доменов
                domain = self._extract_domain(password_record.url_site)
                if domain:
                    domains.append(domain)
                
                # Анализ ключевых слов
                if password_record.key_words:
                    keywords = [kw.strip() for kw in password_record.key_words.split(',')]
                    all_keywords.extend(keywords)
            
            # Вычисляем статистику длин паролей
            avg_length = sum(password_lengths) / len(password_lengths) if password_lengths else 0.0
            min_length = min(password_lengths) if password_lengths else 0
            max_length = max(password_lengths) if password_lengths else 0
            
            # Топ доменов
            domain_counter = Counter(domains)
            most_common_domains = domain_counter.most_common(10)
            
            # Топ ключевых слов
            keyword_counter = Counter(all_keywords)
            most_used_keywords = keyword_counter.most_common(10)
            
            return PasswordStatistics(
                total_passwords=total_passwords,
                added_today=added_today,
                added_this_week=added_this_week,
                added_this_month=added_this_month,
                avg_password_length=round(avg_length, 2),
                min_password_length=min_length,
                max_password_length=max_length,
                most_common_domains=most_common_domains,
                password_strength_distribution=strength_distribution,
                most_used_keywords=most_used_keywords
            )
    
    def get_general_statistics(self) -> GeneralStatistics:
        """Получение общей статистики"""
        with self.get_session() as db:
            # Подсчет записей
            passwords_count = db.query(Password).count()
            payments_count = db.query(Payment).count()
            total_records = passwords_count + payments_count
            
            today_start, week_start, month_start = self._get_date_ranges()
            
            # Подсчет добавленных записей
            passwords_today = 0
            passwords_week = 0
            passwords_month = 0
            
            payments_today = 0
            payments_week = 0
            payments_month = 0
            
            # Анализ паролей
            passwords = db.query(Password).all()
            date_counts = {}
            month_counts = {}
            
            for password in passwords:
                creation_date = self._parse_date(password.creation_date)
                if creation_date:
                    if creation_date >= today_start:
                        passwords_today += 1
                    if creation_date >= week_start:
                        passwords_week += 1
                    if creation_date >= month_start:
                        passwords_month += 1
                    
                    # Для поиска самого активного дня и месяца
                    date_key = creation_date.strftime('%Y-%m-%d')
                    month_key = creation_date.strftime('%Y-%m')
                    date_counts[date_key] = date_counts.get(date_key, 0) + 1
                    month_counts[month_key] = month_counts.get(month_key, 0) + 1
            
            # Анализ платежей
            payments = db.query(Payment).all()
            for payment in payments:
                creation_date = self._parse_date(payment.creation_date)
                if creation_date:
                    if creation_date >= today_start:
                        payments_today += 1
                    if creation_date >= week_start:
                        payments_week += 1
                    if creation_date >= month_start:
                        payments_month += 1
                    
                    date_key = creation_date.strftime('%Y-%m-%d')
                    month_key = creation_date.strftime('%Y-%m')
                    date_counts[date_key] = date_counts.get(date_key, 0) + 1
                    month_counts[month_key] = month_counts.get(month_key, 0) + 1
            
            # Находим самый активный день и месяц
            most_active_day = max(date_counts, key=date_counts.get) if date_counts else None
            most_active_month = max(month_counts, key=month_counts.get) if month_counts else None
            
            return GeneralStatistics(
                total_records=total_records,
                passwords_count=passwords_count,
                payments_count=payments_count,
                records_added_today=passwords_today + payments_today,
                records_added_this_week=passwords_week + payments_week,
                records_added_this_month=passwords_month + payments_month,
                most_active_day=most_active_day,
                most_active_month=most_active_month
            )

    
    def get_monthly_statistics(self, year: int, month: int) -> Dict[str, Union[int, List]]:
        """Получение статистики за конкретный месяц"""
        with self.get_session() as db:
            start_date = datetime(year, month, 1)
            if month == 12:
                end_date = datetime(year + 1, 1, 1)
            else:
                end_date = datetime(year, month + 1, 1)
            
            passwords = db.query(Password).all()
            payments = db.query(Payment).all()
            
            monthly_passwords = []
            monthly_payments = []
            daily_counts = {}
            
            for password in passwords:
                creation_date = self._parse_date(password.creation_date)
                if creation_date and start_date <= creation_date < end_date:
                    monthly_passwords.append(password)
                    day_key = creation_date.strftime('%Y-%m-%d')
                    daily_counts[day_key] = daily_counts.get(day_key, 0) + 1
            
            for payment in payments:
                creation_date = self._parse_date(payment.creation_date)
                if creation_date and start_date <= creation_date < end_date:
                    monthly_payments.append(payment)
                    day_key = creation_date.strftime('%Y-%m-%d')
                    daily_counts[day_key] = daily_counts.get(day_key, 0) + 1
            
            return {
                "passwords_added": len(monthly_passwords),
                "payments_added": len(monthly_payments),
                "total_added": len(monthly_passwords) + len(monthly_payments),
                "daily_breakdown": daily_counts,
                "most_active_day": max(daily_counts, key=daily_counts.get) if daily_counts else None
            }
    
    def get_comprehensive_report(self) -> Dict[str, Union[PasswordStatistics, GeneralStatistics]]:
        """Получение полного отчета со всей статистикой"""
        return {
            "password_statistics": self.get_password_statistics(),
            "general_statistics": self.get_general_statistics(),
        }

