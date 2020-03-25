def parseInt(string):
    try:
        return int(string)
    except ValueError:
        return 0
