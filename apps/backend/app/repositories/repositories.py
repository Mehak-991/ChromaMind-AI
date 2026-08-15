from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.models import User, UserSession, PredictionHistory, UserSettings
from uuid import UUID


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def create(self, user: User) -> User:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user


class SessionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_session(self, session: UserSession) -> UserSession:
        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)
        return session

    async def get_session(self, token: str) -> UserSession | None:
        result = await self.db.execute(
            select(UserSession).where(UserSession.refresh_token == token)
        )
        return result.scalars().first()

    async def delete_session(self, token: str) -> None:
        session = await self.get_session(token)
        if session:
            await self.db.delete(session)
            await self.db.commit()


class PredictionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, record: PredictionHistory) -> PredictionHistory:
        self.db.add(record)
        await self.db.commit()
        await self.db.refresh(record)
        return record

    async def get_by_id(self, prediction_id: UUID) -> PredictionHistory | None:
        result = await self.db.execute(
            select(PredictionHistory).where(PredictionHistory.id == prediction_id)
        )
        return result.scalars().first()

    async def get_history(
        self, user_id: UUID, page=1, limit=10
    ) -> list[PredictionHistory]:
        offset = (page - 1) * limit
        result = await self.db.execute(
            select(PredictionHistory)
            .where(PredictionHistory.user_id == user_id)
            .order_by(PredictionHistory.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def delete(self, prediction_id: UUID) -> None:
        record = await self.get_by_id(prediction_id)
        if record:
            await self.db.delete(record)
            await self.db.commit()


class SettingsRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_user_id(self, user_id: UUID) -> UserSettings | None:
        result = await self.db.execute(
            select(UserSettings).where(UserSettings.user_id == user_id)
        )
        return result.scalars().first()

    async def update(self, settings_obj: UserSettings) -> UserSettings:
        self.db.add(settings_obj)
        await self.db.commit()
        await self.db.refresh(settings_obj)
        return settings_obj
