from pathlib import Path
from loguru import logger

logger.add(sink = "test_log.txt")

if __name__ == "__main__":
		folder = Path("/home/cld100/applications/")

		for i in folder.iterdir():
			logger.info(i.name)
			logger.debug(i.is_dir())