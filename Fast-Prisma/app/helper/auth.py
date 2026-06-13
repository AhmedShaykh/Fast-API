from app.config.db import db;

async def blacklist_token(token: str) -> None:

    exists = await db.blacklistedtoken.find_unique(
        where={"token": token}
    );

    if not exists:

        await db.blacklistedtoken.create(
            data={"token": token}
        );

async def is_blacklisted(token: str) -> bool:

    result = await db.blacklistedtoken.find_unique(
        where={"token": token}
    );

    return result is not None;