from ..models.blacklist_token import BlacklistedToken;
from sqlalchemy.orm import Session;

def blacklist_token(db: Session, token: str):

    exists = (
        db.query(BlacklistedToken)
        .filter(BlacklistedToken.token == token)
        .first()
    );

    if not exists:

        db.add(BlacklistedToken(token=token));

        db.commit();

def is_blacklisted(db: Session, token: str) -> bool:

    return (
        db.query(BlacklistedToken)
        .filter(BlacklistedToken.token == token)
        .first()
    );