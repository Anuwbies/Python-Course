import logging
import os
import signal
from threading import Event
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from storage import process_one

logger = logging.getLogger(__name__)

def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    engine = create_engine(os.environ["DATABASE_URL"], pool_pre_ping=True, pool_timeout=2,
                           connect_args={"connect_timeout":2,"options":"-c statement_timeout=2000"})
    stop = Event()
    def request_stop(signum, frame):
        stop.set()
    signal.signal(signal.SIGINT, request_stop)
    signal.signal(signal.SIGTERM, request_stop)
    try:
        while not stop.is_set():
            try:
                performed = process_one(engine)
            except OperationalError:
                logger.exception("Worker database operation failed")
                stop.wait(1)
            else:
                stop.wait(0.2 if performed else 0.5)
    finally:
        engine.dispose()

if __name__ == "__main__":
    main()
