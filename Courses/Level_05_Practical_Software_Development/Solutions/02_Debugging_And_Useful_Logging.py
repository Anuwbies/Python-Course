import logging
logger = logging.getLogger(__name__)

def total_amounts(amounts):
    total = 0
    for amount in amounts:
        total = total + amount
    logger.info("Processed %s records", len(amounts))
    return total

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")
    print(f"Total: {total_amounts([10, 20])}")
