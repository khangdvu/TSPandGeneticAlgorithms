# tsp.py

#
# Helper functions for the Traveling Salesman Problem
#

import math
import random

# returns true if lst is a permutation of the ints 1 to len(lst), and false
# otherwise


def is_good_perm(lst):
    return sorted(lst) == list(range(1, len(lst) + 1))

# returns a list of pairs of coordinates, where the first pair is the location
# of the first city, the second pair is the location of second city, and so on


def load_city_locs(fname):
    f = open(fname)
    result = []
    for line in f:
        data = [int(s) for s in line.split(' ')]
        result.append(tuple(data[1:]))
    return result

# returns the distance between points (x1,y1) and (x2,y2)


def dist(x1, y1, x2, y2):
    dx = x1 - x2
    dy = y1 - y2
    return math.sqrt(dx*dx + dy*dy)

# c1 and c2 are integer names of cities, randing from 1 to len(city_locs)
# city_locs is a list of pairs of coordinates (e.g. from load_city_locs)


def city_dist(c1, c2, city_locs):
    return dist(city_locs[c1-1][0], city_locs[c1-1][1],
                city_locs[c2-1][0], city_locs[c2-1][1])



# city_perm is a list of 1 or more city names
# city_locs is a list of pairs of coordinates for every city


def total_dist(city_perm, city_locs):
    assert is_good_perm(city_perm), f'city_perm={city_perm}'
    n = len(city_perm)
    total = city_dist(city_perm[0], city_perm[n-1], city_locs)
    for i in range(1, n):
        total += city_dist(city_perm[i-1], city_perm[i], city_locs)
    return total


def str_lst(lst):
    return ', '.join(str(i) for i in lst)


def first_n(n, lst):
    result = str_lst(lst[:n])
    if len(lst) > n:
        result += ' ...'
    return result


def rand_perm(n):
    result = list(range(1, n+1))
    random.shuffle(result)
    return result


def rand_swap(lst):
    n = len(lst)
    i, j = random.randrange(n), random.randrange(n)
    lst[i], lst[j] = lst[j], lst[i]  # swap lst[i] and lst[j]


def my_crossover(s, t):
    assert is_good_perm(s)
    assert is_good_perm(t)
    assert len(s) == len(t)
    n = len(s)

    # choose a subset of t
    c = random.randrange(1, n-1)
    r = random.randrange(1, n-c)
    sub_lst = s[c:c+r]

    first_offspring = s[:]
    i = 0
    while i < r:
        j = 0
        while j < n:
            if first_offspring[j] in sub_lst:
                first_offspring[j] = sub_lst[i]
                i += 1
            j += 1

    sub_lst = t[c:c+r]
    second_offspring = s[:]
    i = 0
    while i < r:
        j = 0
        while j < n:
            if second_offspring[j] in sub_lst:
                second_offspring[j] = sub_lst[i]
                i += 1
            j += 1

    assert is_good_perm(first_offspring)
    assert is_good_perm(second_offspring)
    rand_swap(first_offspring)
    rand_swap(second_offspring)
    return first_offspring, second_offspring


# Ammar Al-Dallal
def tpxwr(s, t):
    assert is_good_perm(s)
    assert is_good_perm(t)
    assert len(s) == len(t)
    n = len(s)

    cp1 = random.randrange(1, n-2)
    cp2 = random.randrange(cp1+1, n-1)

    a = s[:cp1]
    b = s[cp1:cp2]
    c = s[cp2:n]

    d = t[:cp1]
    e = t[cp1:cp2]
    f = t[cp2:n]

    i = 0
    while i < len(e):
        if e[i] in a or e[i] in c:
            init = e[i]
            j = 0
            while j < len(d):
                if d[j] not in a and d[j] not in c and d[j] not in e:
                    e[i] = d[j]
                j += 1
            if e[i] == init:
                j = 0
                while j < len(f):
                    if f[j] not in a and f[j] not in c and f[j] not in e:
                        e[i] = f[j]
                    j += 1

        i += 1

    i = 0
    while i < len(b):
        if b[i] in d or b[i] in f:
            init = b[i]
            j = 0
            while j < len(a):
                if a[j] not in d and a[j] not in f and a[j] not in b:
                    b[i] = a[j]
                j += 1
            if b[i] == init:
                j = 0
                while j < len(c):
                    if c[j] not in d and c[j] not in f and c[j] not in b:
                        b[i] = c[j]
                    j += 1
        i += 1

    first_offspring = a + e + c
    second_offspring = d + b + f

    assert is_good_perm(first_offspring)
    assert is_good_perm(second_offspring)
    # random mutation, uncomment to use
    rand_swap(first_offspring)
    rand_swap(second_offspring)
    return first_offspring, second_offspring


def test():
    city_locs = load_city_locs('cities1000.txt')
    n = len(city_locs)

    s = [422, 997, 468, 735, 679, 413, 759, 910, 168, 699, 116, 583, 685, 936, 352, 76, 511, 36, 886, 571, 806, 336, 984, 747, 392, 621, 33, 335, 971, 1, 810, 862, 341, 384, 567, 680, 658, 427, 976, 400, 800, 
521, 496, 786, 34, 510, 493, 432, 749, 280, 909, 850, 531, 456, 742, 732, 230, 579, 315, 533, 932, 554, 858, 24, 966, 424, 179, 869, 653, 276, 193, 640, 578, 598, 915, 473, 610, 37, 782, 466, 73, 402, 
404, 279, 486, 445, 600, 125, 839, 791, 133, 625, 807, 907, 677, 113, 974, 329, 240, 796, 697, 870, 15, 560, 233, 343, 84, 91, 728, 644, 403, 844, 987, 672, 147, 561, 741, 958, 667, 676, 188, 184, 247, 166, 542, 221, 963, 487, 442, 726, 339, 393, 60, 752, 161, 965, 311, 623, 71, 873, 564, 622, 428, 159, 943, 360, 326, 940, 838, 216, 541, 479, 458, 143, 208, 372, 628, 223, 14, 992, 92, 863, 661, 492, 872, 211, 608, 668, 304, 528, 572, 613, 11, 606, 431, 618, 285, 526, 802, 555, 899, 214, 1000, 425, 164, 708, 209, 617, 562, 925, 946, 308, 769, 633, 535, 435, 684, 344, 692, 448, 845, 126, 52, 979, 95, 563, 768, 773, 328, 703, 998, 477, 38, 257, 436, 327, 513, 97, 860, 516, 631, 666, 897, 235, 865, 690, 830, 635, 995, 203, 199, 314, 642, 255, 794, 139, 310, 30, 410, 238, 357, 548, 596, 853, 447, 887, 803, 811, 210, 891, 945, 56, 47, 268, 390, 947, 657, 504, 991, 686, 261, 499, 89, 420, 739, 189, 259, 366, 382, 256, 20, 177, 154, 2, 911, 264, 930, 706, 558, 22, 141, 82, 134, 112, 978, 306, 294, 
408, 103, 718, 968, 349, 469, 74, 376, 252, 122, 321, 174, 867, 237, 441, 585, 942, 716, 43, 924, 835, 565, 290, 68, 847, 231, 200, 251, 766, 289, 110, 320, 183, 525, 483, 118, 59, 407, 101, 509, 63, 552, 453, 144, 745, 438, 721, 365, 283, 396, 307, 248, 281, 379, 956, 500, 599, 720, 841, 452, 815, 883, 876, 906, 922, 682, 662, 389, 927, 8, 900, 530, 455, 460, 855, 687, 277, 701, 569, 149, 318, 866, 105, 367, 175, 373, 472, 381, 158, 595, 664, 964, 470, 505, 912, 536, 812, 488, 795, 655, 592, 478, 57, 391, 584, 476, 40, 954, 121, 347, 777, 274, 229, 198, 297, 481, 288, 848, 346, 226, 901, 66, 42, 380, 688, 232, 854, 981, 722, 549, 129, 581, 464, 683, 781, 903, 824, 840, 351, 330, 611, 498, 77, 295, 933, 135, 603, 557, 816, 846, 254, 729, 506, 419, 918, 545, 582, 262, 727, 79, 446, 591, 953, 825, 789, 620, 480, 388, 48, 86, 490, 670, 108, 250, 645, 753, 497, 501, 934, 538, 502, 225, 180, 148, 632, 345, 649, 130, 758, 926, 417, 80, 849, 18, 25, 856, 748, 570, 969, 117, 299, 733, 333, 717, 443, 875, 278, 377, 228, 263, 801, 322, 109, 935, 6, 412, 484, 5, 426, 83, 178, 270, 704, 597, 313, 630, 750, 302, 904, 170, 523, 920, 629, 804, 694, 546, 905, 652, 64, 181, 454, 702, 197, 123, 162, 944, 
751, 370, 157, 519, 282, 503, 641, 589, 399, 69, 128, 957, 551, 45, 124, 153, 300, 843, 960, 580, 776, 395, 819, 977, 517, 192, 13, 894, 982, 284, 959, 474, 609, 489, 709, 785, 914, 711, 16, 287, 429, 
616, 371, 317, 654, 674, 7, 212, 457, 41, 705, 12, 881, 467, 319, 418, 763, 761, 859, 136, 93, 387, 394, 423, 673, 973, 213, 265, 615, 355, 292, 414, 772, 102, 671, 892, 291, 770, 155, 737, 767, 337, 698, 411, 809, 515, 495, 269, 222, 485, 573, 736, 994, 952, 602, 814, 440, 898, 94, 340, 348, 601, 532, 50, 828, 10, 939, 104, 605, 543, 524, 961, 693, 190, 756, 359, 797, 32, 465, 21, 151, 937, 651, 98, 588, 529, 774, 461, 681, 358, 893, 173, 851, 659, 817, 266, 451, 107, 194, 740, 783, 187, 689, 614, 182, 574, 880, 507, 713, 832, 364, 790, 246, 878, 972, 890, 324, 138, 647, 738, 619, 607, 120, 834, 421, 65, 439, 715, 463, 723, 171, 985, 312, 955, 325, 669, 612, 895, 826, 23, 744, 26, 636, 142, 386, 986, 234, 586, 342, 75, 90, 202, 449, 593, 820, 176, 361, 316, 354, 990, 665, 471, 813, 566, 140, 
544, 241, 437, 917, 576, 31, 244, 921, 273, 119, 224, 78, 114, 999, 730, 163, 434, 406, 207, 303, 868, 590, 227, 253, 696, 559, 430, 842, 28, 9, 639, 236, 491, 301, 204, 258, 760, 520, 99, 627, 675, 195, 743, 871, 792, 731, 55, 821, 375, 494, 296, 996, 35, 827, 712, 53, 577, 989, 217, 67, 929, 788, 332, 115, 338, 831, 185, 746, 913, 398, 762, 54, 967, 700, 215, 553, 96, 450, 167, 72, 923, 508, 587, 
272, 293, 864, 568, 719, 950, 916, 949, 267, 242, 518, 787, 145, 537, 695, 433, 656, 286, 779, 350, 514, 397, 793, 51, 482, 818, 829, 206, 874, 4, 707, 385, 643, 710, 409, 156, 896, 919, 889, 764, 857, 575, 988, 755, 931, 27, 861, 775, 808, 305, 624, 951, 975, 62, 44, 534, 137, 298, 784, 239, 714, 475, 823, 754, 205, 970, 879, 111, 663, 444, 556, 725, 637, 29, 196, 70, 88, 271, 822, 100, 334, 191, 980, 547, 512, 650, 852, 634, 165, 152, 539, 249, 691, 374, 243, 938, 771, 522, 928, 309, 837, 368, 17, 638, 331, 604, 218, 798, 356, 885, 648, 323, 459, 363, 983, 260, 993, 902, 888, 646, 594, 415, 219, 19, 172, 805, 186, 416, 46, 550, 106, 275, 724, 353, 150, 201, 169, 378, 941, 908, 132, 405, 61, 877, 39, 49, 660, 765, 146, 882, 734, 757, 948, 799, 836, 362, 678, 245, 58, 833, 778, 962, 369, 462, 
160, 127, 626, 87, 527, 220, 401, 780, 3, 383, 540, 884, 85, 81, 131]
    assert is_good_perm(s)
    print(total_dist(s, city_locs))

# Each generation, pairs of permutations from the top 50% of the population
# are "bred" to create the next generation.


def crossover_search(fname, max_iter, pop_size):
    city_locs = load_city_locs(fname)
    n = len(city_locs)
    curr_gen = [rand_perm(n) for i in range(pop_size)]
    curr_gen = [(total_dist(p, city_locs), p) for p in curr_gen]
    curr_gen.sort()
    assert len(curr_gen) == pop_size

    print(
        f'crossover_search("{fname}", max_iter={max_iter}, pop_size={pop_size}) ...')
    for i in range(max_iter):
        # copy the top 50% of the population to the next generation, and for the rest randomly
        # cross-breed pairs

        top_half = [p[1] for p in curr_gen[:int(n/2)]]
        next_gen = top_half[:]
        while len(next_gen) < pop_size:
            s = random.choice(top_half)
            t = random.choice(top_half)
            first, second = tpxwr(s, t)
            next_gen.append(first)
            next_gen.append(second)

        next_gen = next_gen[:pop_size]

        # create the next generation of (score, permutations) pairs
        assert len(next_gen) == pop_size
        curr_gen = [(total_dist(p, city_locs), p) for p in next_gen]
        curr_gen.sort()
        if i % 50 == 0:
            print(f'Iter {i} being simulated...')

    print()
    print(
        f'After {max_iter} generations of {pop_size} permutations, the best is:')
    print(f'score = {curr_gen[0][0]}')
    print(curr_gen[0][1])
    assert is_good_perm(curr_gen[0][1])


def tournament_selection_search(fname, max_iter, pop_size):
    city_locs = load_city_locs(fname)
    n = len(city_locs)
    curr_gen = [rand_perm(n) for i in range(pop_size)]
    curr_gen = [(total_dist(p, city_locs), p) for p in curr_gen]
    curr_gen.sort()
    curr_gen = curr_gen[:pop_size]
    assert len(curr_gen) == pop_size

    print(
        f'tournament_selection_search("{fname}", max_iter={max_iter}, pop_size={pop_size}) ...')
    for i in range(max_iter):
        if i % 10 == 0:
            print(f'Iter {i} being simulated...')
        # binary tournament selection from top 67% to populate new generation to find parents
        # parents are then cross-bred
        # best of current gen is retained, the rest of the population will be offsprings

        top_two_third = [p for p in curr_gen[:int(n*2/3)]]
        next_gen = []
        next_gen.append(curr_gen[0][1])
        for j in range(int(pop_size/2)):
            s1 = random.choice(top_two_third)
            s2 = random.choice(top_two_third)
            if s1[0] < s2[0]:
                s = s1[1]
            else:
                s = s2[1]
            
            t1 = random.choice(top_two_third)
            t2 = random.choice(top_two_third)
            if t1[0] < t2[0]:
                t = t1[1]
            else:
                t = t2[1]
            first, second = my_crossover(s,t)
            next_gen.append(first)
            next_gen.append(second)            

        next_gen = next_gen[:pop_size]
        #
        #  create the next generation of (score, permutations) pairs
        assert len(next_gen) == pop_size
        curr_gen = [(total_dist(p, city_locs), p) for p in next_gen]
        curr_gen.sort()


    print()
    print(
        f'After {max_iter} generations of {pop_size} permutations, the best is:')
    print(f'score = {curr_gen[0][0]}')
    print(curr_gen[0][1])
    assert is_good_perm(curr_gen[0][1])



# Tournament selection search but the best permutation on record is added to the random first population
def initialized_tournament_selection_search(best_permutation, fname, max_iter, pop_size):
    city_locs = load_city_locs(fname)
    n = len(city_locs)
    curr_gen = [rand_perm(n) for i in range(pop_size)]
    curr_gen = [(total_dist(p, city_locs), p) for p in curr_gen]
    curr_gen.append((total_dist(best_permutation, city_locs), best_permutation))
    curr_gen.sort()
    curr_gen = curr_gen[:pop_size]
    assert len(curr_gen) == pop_size

    print(
        f'tournament_selection_search("{fname}", max_iter={max_iter}, pop_size={pop_size}) ...')
    for i in range(max_iter):
        if i % 10 == 0:
            print(f'Iter {i} being simulated...')
        # binary tournament selection from top 67% to populate new generation to find parents
        # parents are then cross-bred
        # best of current gen is retained, the rest of the population will be offsprings

        top_two_third = [p for p in curr_gen[:int(n*2/3)]]
        next_gen = []
        next_gen.append(curr_gen[0][1])
        for j in range(int(pop_size/2)):
            s1 = random.choice(top_two_third)
            s2 = random.choice(top_two_third)
            if s1[0] < s2[0]:
                s = s1[1]
            else:
                s = s2[1]
            
            t1 = random.choice(top_two_third)
            t2 = random.choice(top_two_third)
            if t1[0] < t2[0]:
                t = t1[1]
            else:
                t = t2[1]
            first, second = my_crossover(s,t)
            next_gen.append(first)
            next_gen.append(second)            

        next_gen = next_gen[:pop_size]
        #
        #  create the next generation of (score, permutations) pairs
        assert len(next_gen) == pop_size
        curr_gen = [(total_dist(p, city_locs), p) for p in next_gen]
        curr_gen.sort()


    print()
    print(
        f'After {max_iter} generations of {pop_size} permutations, the best is:')
    print(f'score = {curr_gen[0][0]}')
    print(curr_gen[0][1])
    assert is_good_perm(curr_gen[0][1])
    return curr_gen[0][1]



if __name__ == '__main__':
   # test()
#    tournament_selection_search('cities1000.txt', max_iter=100, pop_size=50)
    best_permutation = [422, 997, 468, 43, 679, 666, 759, 755, 440, 945, 80, 583, 91, 222, 152, 76, 511, 36, 490, 571, 806, 336, 484, 49, 392, 209, 33, 252, 251, 381, 810, 862, 341, 175, 723, 903, 658, 497, 26, 400, 118, 521, 496, 786, 34, 510, 493, 432, 749, 280, 770, 790, 386, 456, 203, 732, 230, 303, 315, 555, 445, 554, 539, 570, 857, 127, 266, 67, 653, 276, 63, 131, 417, 931, 109, 680, 275, 868, 181, 966, 466, 332, 402, 75, 279, 581, 696, 600, 920, 519, 791, 133, 201, 907, 677, 565, 840, 329, 462, 796, 983, 304, 20, 560, 233, 238, 638, 486, 458, 50, 509, 844, 987, 672, 147, 561, 741, 958, 160, 231, 188, 886, 247, 166, 492, 550, 963, 97, 196, 338, 339, 537, 60, 782, 356, 591, 419, 750, 454, 250, 564, 622, 531, 831, 548, 685, 326, 482, 838, 547, 541, 444, 94, 702, 208, 459, 204, 223, 839, 619, 908, 259, 661, 330, 
72, 211, 608, 879, 108, 712, 572, 859, 11, 606, 431, 524, 243, 370, 802, 834, 793, 396, 959, 425, 214, 882, 62, 617, 241, 387, 946, 954, 769, 314, 293, 435, 277, 684, 344, 35, 448, 845, 308, 113, 227, 
491, 563, 768, 773, 328, 703, 95, 477, 416, 257, 874, 730, 513, 535, 860, 220, 973, 413, 897, 464, 901, 577, 830, 957, 148, 382, 15, 633, 650, 613, 794, 65, 8, 778, 140, 584, 637, 774, 596, 853, 447, 887, 528, 811, 367, 891, 260, 56, 47, 873, 375, 799, 452, 114, 780, 686, 261, 499, 487, 420, 739, 752, 115, 351, 343, 354, 256, 889, 103, 23, 371, 911, 264, 244, 320, 558, 22, 141, 82, 134, 157, 940, 904, 294, 360, 644, 718, 183, 777, 682, 286, 875, 116, 122, 321, 174, 867, 237, 441, 585, 942, 716, 609, 538, 835, 449, 335, 423, 68, 847, 518, 102, 138, 766, 936, 586, 968, 525, 483, 800, 681, 909, 262, 943, 69, 803, 578, 144, 31, 964, 630, 996, 215, 632, 307, 248, 575, 379, 956, 500, 772, 5, 747, 815, 883, 979, 906, 695, 469, 41, 820, 927, 310, 900, 530, 455, 460, 569, 693, 965, 701, 952, 149, 253, 
697, 105, 225, 364, 373, 472, 428, 368, 595, 664, 993, 470, 706, 912, 536, 812, 488, 795, 655, 130, 478, 729, 391, 40, 12, 761, 284, 121, 202, 634, 274, 229, 239, 297, 481, 288, 848, 346, 221, 865, 66, 246, 380, 688, 232, 854, 135, 722, 549, 129, 692, 235, 977, 985, 824, 567, 507, 640, 451, 77, 299, 771, 670, 876, 579, 816, 846, 825, 57, 318, 207, 918, 545, 599, 298, 727, 79, 74, 899, 953, 523, 789, 512, 480, 674, 984, 399, 132, 362, 947, 365, 390, 753, 955, 501, 44, 843, 475, 597, 180, 989, 271, 662, 14, 592, 758, 711, 453, 347, 849, 18, 378, 856, 476, 24, 969, 117, 193, 333, 717, 342, 189, 278, 377, 228, 851, 324, 807, 322, 71, 935, 628, 301, 48, 841, 393, 994, 178, 270, 939, 258, 635, 268, 479, 269, 168, 170, 254, 311, 282, 804, 694, 546, 905, 974, 64, 37, 915, 645, 809, 611, 473, 944, 861, 319, 656, 38, 629, 503, 376, 687, 86, 594, 721, 668, 551, 45, 124, 742, 300, 139, 58, 580, 641, 290, 819, 636, 517, 683, 13, 894, 982, 981, 366, 474, 403, 735, 709, 785, 914, 926, 16, 287, 429, 159, 143, 317, 663, 198, 7, 212, 457, 345, 334, 176, 881, 504, 814, 526, 418, 885, 919, 652, 136, 93, 934, 427, 394, 395, 745, 631, 213, 265, 654, 355, 648, 414, 410, 421, 671, 892, 291, 1, 155, 737, 111, 337, 698, 411, 898, 515, 495, 302, 832, 485, 573, 736, 83, 506, 602, 938, 978, 467, 226, 340, 89, 601, 728, 603, 81, 582, 704, 104, 2, 543, 961, 618, 589, 872, 756, 359, 797, 106, 556, 21, 151, 88, 651, 
852, 588, 776, 489, 461, 59, 358, 893, 327, 801, 988, 817, 765, 498, 323, 194, 740, 783, 187, 689, 614, 182, 85, 880, 864, 713, 657, 384, 930, 850, 388, 878, 972, 890, 625, 101, 292, 738, 446, 529, 910, 120, 533, 164, 925, 757, 156, 463, 438, 171, 781, 185, 17, 325, 669, 767, 895, 826, 154, 784, 976, 192, 837, 627, 986, 675, 990, 443, 404, 90, 281, 593, 389, 748, 352, 316, 933, 255, 665, 471, 813, 505, 922, 544, 924, 562, 917, 576, 568, 921, 273, 119, 566, 621, 42, 999, 437, 163, 975, 406, 691, 557, 610, 751, 123, 855, 932, 559, 430, 842, 28, 9, 639, 51, 998, 412, 534, 888, 760, 520, 99, 605, 714, 385, 743, 871, 792, 733, 836, 821, 55, 995, 296, 128, 408, 827, 552, 53, 690, 494, 217, 357, 929, 788, 191, 184, 726, 616, 744, 746, 913, 361, 762, 54, 967, 450, 283, 553, 150, 700, 167, 96, 923, 508, 587, 272, 348, 532, 673, 719, 950, 916, 949, 372, 818, 731, 787, 145, 624, 1000, 433, 112, 676, 779, 350, 514, 397, 992, 236, 306, 242, 829, 206, 436, 4, 707, 863, 643, 710, 78, 409, 542, 896, 173, 398, 715, 764, 199, 659, 527, 407, 27, 590, 775, 374, 305, 426, 951, 434, 705, 52, 6, 137, 720, 263, 146, 289, 502, 823, 754, 205, 970, 313, 200, 598, 612, 465, 623, 869, 29, 442, 70, 937, 822, 100, 195, 73, 980, 667, 620, 642, 98, 349, 165, 234, 858, 249, 125, 808, 285, 32, 153, 522, 928, 312, 142, 158, 646, 331, 604, 218, 798, 161, 763, 647, 107, 84, 363, 725, 699, 197, 902, 177, 971, 126, 415, 219, 19, 172, 805, 186, 649, 46, 267, 724, 162, 10, 190, 353, 309, 169, 25, 941, 92, 607, 405, 61, 877, 39, 866, 660, 179, 224, 708, 734, 439, 948, 870, 615, 210, 678, 245, 960, 833, 30, 962, 369, 240, 216, 424, 626, 87, 110, 516, 401, 991, 3, 383, 540, 884, 574, 828, 295]
    for i in range(100):
        best_permutation = initialized_tournament_selection_search(best_permutation, 'cities1000.txt', max_iter=100, pop_size=50)