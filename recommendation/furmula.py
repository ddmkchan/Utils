#!/usr/bin/python
#coding=utf-8

#from recommend import users
from math import sqrt

users = {"Angelica": {"Blues Traveler": 4.75, "Broken Bells": 4.5, "Norah Jones": 5, "Phoenix": 4.25, "Slightly Stoopid": 4},
    "Throne": {"Blues Traveler": 4, "Broken Bells": 3, "Norah Jones": 5, "Phoenix": 2, "Slightly Stoopid": 1}
    }


def pearson(rating1, rating2):
    sum_xy = 0
    sum_x = 0
    sum_y = 0
    sum_x2 = 0
    sum_y2 = 0
    n = 0
    for key in rating1:
        if key in rating2:
            n += 1
            x = rating1[key]
            y = rating2[key]
            sum_xy += x * y
            sum_x += x
            sum_y += y
            sum_x2 += x**2
            sum_y2 += y**2
        # now compute denominator
    denominator = sqrt(sum_x2 - (sum_x**2) / n) * sqrt(sum_y2 -(sum_y**2) / n)
    if denominator == 0:
        return 0
    else:
        return (sum_xy - (sum_x * sum_y) / n) / denominator

def cosine_similarity(rating1, rating2):
    sum_xy = 0
    sum_x2 = 0
    sum_y2 = 0
    for key in rating1:
        if key in rating2:
            x = rating1[key]
            y = rating2[key]
            sum_xy += x * y
            sum_x2 += x**2
            sum_y2 += y**2
    return sum_xy / (sqrt(sum_x2) * sqrt(sum_y2))

if __name__ == "__main__":
    print pearson(users['Angelica'], users['Throne'])
    print cossim(users['Angelica'], users['Throne'])

