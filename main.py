from src.hello import Hello


def handler(event, context):
    print(Hello().message())
    return True

if __name__ == '__main__':
    handler('', '')
