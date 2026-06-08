from utils.logger import get_logger


# =====================================================
# TO BE REMOVED, JUST FOR TESTING IF LOGGER IS WORKING
# =====================================================

def main():
    logger = get_logger()

    logger.info("Server check started")
    logger.warning("Slow service detected")
    logger.error("Service down")


if __name__ == "__main__":
    main()