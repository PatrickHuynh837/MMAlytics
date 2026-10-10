from fastapi import APIRouter
from sqlalchemy import text
from server.database import engine


router = APIRouter(
    prefix="/fights",
    tags=["fights"]
)


@router.get("/")
def get_fights():
    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT *
                FROM fights
            """)
        )

        fights = [dict(row._mapping) for row in result]

    return fights