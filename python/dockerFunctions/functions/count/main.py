def main():
    inWord = 0
    wordCount = 0

    for char in slice:
        if char.isalpha():
            if not inWord:
                inWord = 1
                wordCount += 1
        else:
            if inWord:
                inWord = 0
    return {"wordNum": wordCount}

