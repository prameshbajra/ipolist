from src.listing.main import lambda_handler


def init_test():
    lambda_handler(None, None)


if __name__ == '__main__':
    print("STARTING TESTS ... \n ")
    init_test()
    print("\nTEST RAN ... \n")