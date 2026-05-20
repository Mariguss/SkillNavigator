from app.core.container import Container
from app.models.user import User
from app.core.security import get_password_hash

def main():
    container = Container()
    user_repo = container.user_repository()
    
    with user_repo.session_factory() as session:
        # Проверяем, нет ли уже такого админа
        admin_exists = session.query(User).filter_by(login="admin").first()
        if admin_exists:
            print("Админ уже существует!")
            return

        admin = User(
            login="admin",
            email="admin@navigator.ru",
            password_hash=get_password_hash("super_secure_password"),
            is_superuser=True
        )
        session.add(admin)
        session.commit()
        print("Суперпользователь успешно создан!")

if __name__ == "__main__":
    main()