from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from config.database.base import Base, engine


# Модель для таблицы passwords
class Password(Base):
    __tablename__ = "passwords"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=True)
    password = Column(String, nullable=True)
    login = Column(String, nullable=True)
    url_site = Column(String, nullable=True)
    email = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    key_words = Column(String, nullable=True)
    creation_date = Column(String, nullable=True)  # Можно изменить на DateTime
    change_date = Column(String, nullable=True)    # Можно изменить на DateTime
    
    def __repr__(self):
        return f"<Password(id={self.id}, title='{self.title}')>"
    
    def to_dict(self):
        """Преобразует объект в словарь, исключая None значения"""
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if value is not None:
                result[column.name] = value
        return result

# Модель для таблицы payments
class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=True)
    password = Column(String, nullable=True)
    login = Column(String, nullable=True)
    url_site = Column(String, nullable=True)
    email = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    key_words = Column(String, nullable=True)
    creation_date = Column(String, nullable=True)  # Можно изменить на DateTime
    change_date = Column(String, nullable=True)    # Можно изменить на DateTime
    
    def __repr__(self):
        return f"<Payment(id={self.id}, title='{self.title}')>"
    
    def to_dict(self):
        """Преобразует объект в словарь, исключая None значения"""
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if value is not None:
                result[column.name] = value
        return result

class PasswordWithDateTime(Base):
    __tablename__ = "crypto_wallets"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=True)
    seed_phrase = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    key_words = Column(String, nullable=True)
    creation_date = Column(DateTime, default=datetime.utcnow, nullable=True)
    change_date = Column(DateTime, onupdate=datetime.utcnow, nullable=True)
    
    def __repr__(self):
        return f"<Password(id={self.id}, title='{self.title}')>"
    
    def to_dict(self):
        """Преобразует объект в словарь, исключая None значения"""
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if value is not None:
                if isinstance(value, datetime):
                    result[column.name] = value.isoformat()
                else:
                    result[column.name] = value
        return result

