"""
Assignment 2 Fit2004 SEM1 2021
author: Bernadine Nzavake
Last edited 16/04/2021
"""


def best_schedule(weekly_income: list, competitions: list) -> int:
    """
    implement the maximum made by a user either participating on a event or not in a week
    :param weekly_income: list of daily income
    :param competitions: list of special event
    :return: maximum income made
    :complexity: O(NlogN) N the total size of weekly_income and competitions
    space complexity O(N) from the memo list
    """
    for j in range(len(weekly_income)):
        competitions.append((j, j, weekly_income[j]))
    # sort the list in non-decreasing order based on the second item of the tuple
    competitions.sort(key=lambda x: x[1])
    # initite the base
    memo = [0] * (len(competitions) + 1)
    pre_e = competitions[0][1]
    pre_s = competitions[0][0]
    memo[1] = competitions[0][2]
    smallest_e, index = 0, 1
    # base = 0 no earning, no working
    # memo[i] = profit made at the special event in specific time, and always include the winning at the time
    # to get value at memo[i] ether memo[i-1], memo[i-2] or the last smallest ending point + winning
    for i in range(2, len(competitions)+1):
        cur_s = competitions[i-1][0]
        cur_e = competitions[i-1][1]
        win = competitions[i-1][2]
        if pre_e < cur_s:
            memo[i] = memo[i-1]+win
        elif pre_e == cur_s:
            if memo[i - 1] != memo[i - 2] and cur_e == cur_s:
                memo[i] = max(win, memo[i - 1])
            elif memo[i - 1] == memo[i - 2] and cur_e != pre_s:
                memo[i] = memo[i] = max(memo[i-1], memo[i-2]+win)
            elif memo[i-1] != memo[i-2]:
                memo[i] = max(memo[i-1], memo[i-2]+win)
            else:
                memo[i] = max(memo[i-1], memo[i-3]+win)
        elif pre_e > cur_s:
            if cur_s > smallest_e:
                memo[i] = memo[index] + win
                smallest_e = cur_e
                index = i
            elif cur_s == 0:
                memo[i] = win
            elif cur_s == smallest_e:
                memo[i] = max(memo[index], memo[index-1]+win)
                smallest_e = cur_e
                index = i
        pre_e = cur_e
        pre_s = cur_s
    return memo[len(memo)-1]


def best_itinerary(profit: list, quarantine_time: list, home: int) -> int:
    """
    calculate the best profit from day 1 to day d start from home, while traveling from city to
    city or staying in the same city.
    :param profit: list nd earning in day d in city c
    :param quarantine_time: number of day to quarantine in city c
    :param home: starting city
    :return: maximize earning
    :complexity: O(nd) n is the number of city and d the number of days,
    space complexity: nd is the number of city and d the number of days, from the memo list
    """
    memo = [None] * (len(profit) + 1)
    for t in range(len(memo)):
        memo[t] = [0] * len(profit[0])
    d = 0
    c = home
    # memo[i][j] = profit made at j from home
    # base = 0 memo[i][j]; i =n, j = d
    while d < len(profit) and c < len(profit[0]):
        # city at o
        if c == 0:
            l = c + 1
            qdl = quarantine_time[l]
            temp_dl = d + qdl + 1
            if l < len(profit[0]) and temp_dl < len(profit):
                # from c to c+1
                if profit[temp_dl][l] > profit[d][c]:
                    memo[temp_dl][l] += profit[temp_dl][l]
                    c = l
                    d = temp_dl
                # same city
                else:
                    memo[d][c] += profit[d][c]
            # no possible travel
            else:
                memo[d][c] += profit[d][c]
        # inner city
        elif len(profit[0]) - 1 > c > 0:
            l = c + 1
            qdl = quarantine_time[l]
            temp_dl = d + qdl + 1
            r = c - 1
            qdr = quarantine_time[r]
            temp_dr = d + qdr + 1
            if l < len(profit[0]) and r >= 0 and temp_dr < len(profit) and temp_dl < len(profit):
                # from c to c+1
                if profit[temp_dl][l] > profit[temp_dr][r] > profit[d][c]:
                    memo[temp_dl][l] += profit[temp_dl][l]
                    c = l
                    d = temp_dl
                elif profit[temp_dr][r] > profit[temp_dl][l] > profit[d][c]:
                    memo[temp_dr][r] += profit[temp_dr][r]
                    c = r
                    d = temp_dr
                else:
                    memo[d][c] += profit[d][c]
                # no possible travel
            else:
                memo[d][c] += profit[d][c]
        # city at n-1
        elif c == len(profit[0]) - 1:
            r = c - 1
            qdr = quarantine_time[r]
            temp_dr = d + qdr + 1
            if r >= 0 and temp_dr < len(profit):
                # from c to c-1
                if profit[temp_dr][r] > profit[d][c]:
                    memo[temp_dr][r] += profit[temp_dr][r]
                    c = r
                    d = temp_dr
                    memo[d][c] += profit[d][c]
            # no possible travel
            else:
                memo[d][c] += profit[d][c]
        d += 1
    # retrieve the maximum profit
    for k in range(len(memo) - 1, -1, -1):
        memo[d][c] += max(memo[k])
    return memo[d][c]
