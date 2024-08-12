from datetime import datetime

from cryptography.fernet import Fernet
from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.secret import Secret
from schemas.secret import SecretCreate, SecretOut, SecretDecryptOut, SecretKeyOut

# генерация ключа
key = Fernet.generate_key()
cipher_suite = Fernet(key)


async def generate_secret(secret: SecretCreate, user_id: int, db: AsyncSession) -> SecretKeyOut:
    """
    Генерирует новый секрет и сохраняет его в базе данных.

    :param secret: объект с данными о новом секрете (типа SecretCreate)
    :param user_id: идентификатор пользователя (типа int)
    :param db: экземпляр сессии базы данных (типа AsyncSession)
    :return: ключ секрета (типа SecretKeyOut)
    """
    secret_content = cipher_suite.encrypt(secret.secret_content)
    passphrase = cipher_suite.encrypt(secret.passphrase)
    created_at = datetime.utcnow()
    db_secret = Secret(secret_content=secret_content, lifetime=secret.lifetime, passphrase=passphrase, user_id=user_id,
                       created_at=created_at)
    db.add(db_secret)
    await db.commit()
    return SecretKeyOut(passphrase=passphrase)


async def get_secret(secret_key: bytes, user_id: int, db: AsyncSession) -> SecretDecryptOut:
    """
    Получает секрет по зашифрованному ключу и удаляет его из базы данных.

    :param secret_key: зашифрованный ключ секрета (типа bytes)
    :param user_id: идентификатор пользователя (типа int)
    :param db: экземпляр сессии базы данных (типа AsyncSession)
    :return: расшифрованный секрет (типа SecretDecryptOut)
    """
    query = await db.execute(select(Secret).where((Secret.passphrase == secret_key) & (Secret.user_id == user_id)))
    db_secret = query.scalars().first()
    if db_secret is None:
        raise HTTPException(status_code=404, detail='Секрет не найден')

    encrypted_secret = db_secret.secret_content
    decrypted_secret = cipher_suite.decrypt(encrypted_secret)
    await db.delete(db_secret)
    await db.commit()
    return SecretDecryptOut(secret_content=decrypted_secret)


async def get_secrets(user_id: int, db: AsyncSession) -> [SecretOut]:
    """
    Получает список всех секретов.

    :param user_id: идентификатор пользователя (типа int)
    :param db: экземпляр сессии базы данных (типа AsyncSession)
    :return: список секретов (типа Sequence[SecretOut])
    """
    query = await db.execute(select(Secret).where(Secret.user_id == user_id))
    return query.scalars().all()
