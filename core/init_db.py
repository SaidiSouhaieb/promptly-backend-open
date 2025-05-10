from app.db.session import Base, engine
from app.db.models import user
from core.logging import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


def init_db():
    logger.info("Initializing database...")
    Base.metadata.create_all(bind=engine)
