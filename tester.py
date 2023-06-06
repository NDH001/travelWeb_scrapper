import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s:%(name)s:%(message)s")

file_handler = logging.FileHandler("logging/scrapper.log")
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)


logger.addHandler(file_handler)

x = [1, 2]

for i in range(10):
    try:
        print(x[i])
    except:
        logger.exception(f"logger test{i}")
    else:
        print("LIAMNESSOn")
