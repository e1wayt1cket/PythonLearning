def classify1(score):
    if 85 <= score <= 100:
        return 'A'
    elif 75 <= score < 85:
        return 'B'
    elif 65 <= score < 75:
        return 'C'
    elif 60 <= score < 65:
        return 'D'
    elif 0 <= score < 60:
        return 'F'
    else:
        return 0
score=0
score=int(input('plz type your score:'))
level=classify1(score)
print(level)
