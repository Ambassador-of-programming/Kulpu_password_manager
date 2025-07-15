# from config.database.crud import DatabaseManager, PasswordCRUD
# from config.database.base import Base, engine
# from config.database.crud import StatistikManager

# # Пример использования
# if __name__ == "__main__":
    
#     # Создаем менеджер базы данных
#     db_manager = DatabaseManager()
    
#     # Добавляем запись с явным указанием типов
#     new_password = db_manager.add_password_record(
#         title="Тестовый сайт",
#         login="test_user",
#         password="1",
#         url_site="https://test.com",
#         email="user@test.com",
#         notes="Важный аккаунт",
#         key_words=["работа", "важно"]  # List[str]
#     )
    
#     print(f"Создана запись с ID: {new_password.id}")
    
#     # Получаем запись по ID
#     password_data = db_manager.get_password_by_id(password_id=new_password.id)
#     print(f"Данные пароля: {password_data}")
    
# #     # Читаем определенные поля
#     records = db_manager.read_password_records("id", "title", "login")
#     print(f"Записи: {records}")
    
#     # Обновляем запись с явным указанием параметров
#     updated = db_manager.update_password(
#         password_id=new_password.id, 
#         notes="Обновленные заметки"
#     )
#     print(f"Запись обновлена: {updated.notes if updated else 'Не найдена'}")
    
#     # # Удаляем запись
#     # deleted = db_manager.delete_password_by_id(password_id=new_password.id)
#     # print(f"Запись удалена: {deleted}")
    
#     # Основная статистика
    # stats = StatistikManager()
    # password_stats = stats.get_comprehensive_report()
    # print(f"Статистика паролей: {password_stats}")
