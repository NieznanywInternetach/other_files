import timeit
from typing import Callable, Any, Union
from collections import defaultdict
from itertools import product

"""#========================================================================================
You can find here collection of algorithm tasks/games taken from several online repositories,
their solutions inside unit tests (done with test case class) and test case manager class
Surely they could be implemented better, or with usage of well-established library like 
unittest or pytest but it wasn't the point of this exercise

The basic principle is - define the unit case (and the function) and fill it up with test cases,
then put the unit test name as the first argument of TaskTest, adjust the rest of options 
if necessary and run() it 
#"""#=======================================================================================


class TaskUnitTest:
    test_count = 0

    def __init__(self, func: Callable, func_args: list[Any], assert_value: Any,
                 details: bool = False, performance_check: bool = False):
        TaskUnitTest.test_count += 1
        self.test_index = TaskUnitTest.test_count
        self.func = func
        self.func_args = func_args
        self.assert_value = assert_value
        self.details_flag = details
        self.performance_check_flag = performance_check

    def __str__(self):
        return f"{self.func.__name__ = },\n{self.func_args = },\n{self.assert_value = }"

    def run(self):
        result = self.func(*self.func_args)
        if self.details_flag:
            print(self)
        if not self.performance_check_flag:
            print(f"Test {self.test_index}: " + "Passed!" if result == self.assert_value else f"Failed wih {result = }")


class TaskTest:
    def __init__(self, func_test: Callable, details: bool = False, performance_check: bool = False,
                 sample_size: int = 10, iterations: int = 1000):
        self.test_function = func_test
        self.performance_check = performance_check
        self.details = details
        self.sample_size = sample_size
        self.iterations = iterations

    def run(self):
        if not self.performance_check:
            self.test_function(details=self.details)
        else:
            time_list = []
            for _ in range(self.sample_size):
                before = timeit.default_timer()
                for _ in range(self.iterations):
                    self.test_function(perf_check=self.performance_check)
                now = timeit.default_timer()
                time_list.append(now - before)
            print(f"All records are in seconds. Sample size: {self.sample_size}, Iterations each sample: {self.iterations}\n"
                  f"Function: {self.test_function.__name__}\n"
                  f"Total time:   {sum(time_list)}\n"
                  f"Min time:     {min(time_list)}\n"
                  f"Median time:  {sorted(time_list)[self.sample_size // 2]}\n"
                  f"Average time: {sum(time_list) / len(time_list)}\n"
                  f"Max time:     {max(time_list)}")


def find_all_primes(number: int) -> list[int]:
    from math import sqrt
    list_prime = []
    while number % 2 == 0:
        list_prime.append(2),
        number /= 2
    for i in range(3, int(sqrt(number)) + 1, 2):
        while number % i == 0:
            list_prime.append(i)
            number /= i
    if number > 2:
        list_prime.append(number)
    return list_prime

def binary_search(numbers: list[int], goal: int) -> bool:
    low = 0
    high = len(numbers)-1
    found = False
    while low <= high and not found:
        mid = (low + high)//2
        if numbers[mid] == goal:
            found = True
        else:
            if goal < numbers[mid]:
                high = mid-1
            else:
                low = mid+1
    return found

def binary_search_test(details=False):
    test1 = TaskUnitTest(binary_search, [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 10], True, details)
    test2 = TaskUnitTest(binary_search, [[1, 4, 9, 16, 25, 36, 49, 64, 81, 100], 42], False, details)
    test1.run()
    test2.run()

def factorial(num):
    result = 1
    if num < 2:
        return result
    for number in range(1, num+1):
        result *= number
    return result

def replace_vowels(txt, ch):
    # one liner
    #return ''.join([letter if letter not in 'aeoui' else ch for letter in txt])
    # multi liner
    new_text = list(txt)
    for index, letter in enumerate(new_text):
        if letter in 'aueio':
            new_text[index] = ch
    return "".join(new_text)

def count_vowels(word):
    return sum([word.count(vowel) for vowel in 'aeoui'])

def card_hide(card):
    # one liner
    # return ''.join('*' for digit in range(len(card)-4))+''.join(card[-4:])
    digit_count = len(card)
    return "".join([number if index > digit_count-5 else "*" for index, number in enumerate(card)])

def correct_signs(txt):
    tokens = txt.split()
    for index in range(1, len(tokens), 2):
        if tokens[index] == "<":
            if not (int(tokens[index-1]) < int(tokens[index+1])):
                return False
        else:
            if not (int(tokens[index-1]) > int(tokens[index+1])):
                return False
    return True

def hamming_distance(txt1, txt2):
    # one liner
    # return sum(x != y for (x, y) in zip(txt1, txt2))
    distance = 0
    for (char1, char2) in zip(txt1, txt2):
        if char1 != char2:
            distance += 1
    return distance

def hamming_distance_test(details=False, perf_check: bool = False):
    test1 = TaskUnitTest(hamming_distance, ["abcde", "bcdef"], 5, details, performance_check=perf_check)
    test2 = TaskUnitTest(hamming_distance, ["abcde", "abcde"], 0, details, performance_check=perf_check)
    test3 = TaskUnitTest(hamming_distance, ["strong", "strung" ], 1, details, performance_check=perf_check)

    test1.run()
    test2.run()
    test3.run()

def mine_grid(matrix: list[list[Union[int, str]]]):
    def update_surrounding_9(pos_y: int, pos_x: int):
        for mod_y in (-1, 0, 1):
            if pos_y == 0 and mod_y == -1 or pos_y == len_y and mod_y == 1:
                continue
            for mod_x in (-1, 0, 1):
                if pos_x == 0 and mod_x == -1 or pos_x == len_x and mod_x == 1:
                    continue
                if new_matrix[pos_y+mod_y][pos_x+mod_x] == "#":
                    continue
                elif new_matrix[pos_y+mod_y][pos_x+mod_x] == "-":
                    new_matrix[pos_y+mod_y][pos_x+mod_x] = 1
                else:
                    new_matrix[pos_y+mod_y][pos_x+mod_x] += 1

    new_matrix = matrix[:]
    len_y = len(matrix)-1
    len_x = len(matrix[0])-1

    for index_y, value_y in enumerate(matrix):
        for index_x, value_x in enumerate(matrix[index_y]):
            if value_x == "#":
                update_surrounding_9(index_y, index_x)
            elif value_x == "-":
                """both this line and two last from the subfunction above leads to the same result
                in terms of cells adjacent to a mine except this one fills the rest with zeros"""
                new_matrix[index_y][index_x] = 0


    return [[str(x) for x in y] for y in new_matrix]

def mine_grid_test(perf_check: bool = False):
    test1 = TaskUnitTest(mine_grid, [
                        [
                            ['-', '-', '-', '-', '-'],
                            ['-', '-', '-', '-', '-'],
                            ['-', '-', '#', '-', '-'],
                            ['-', '-', '-', '-', '-'],
                            ['-', '-', '-', '-', '-']
                        ]],[
                            ['0', '0', '0', '0', '0'],
                            ['0', '1', '1', '1', '0'],
                            ['0', '1', '#', '1', '0'],
                            ['0', '1', '1', '1', '0'],
                            ['0', '0', '0', '0', '0']
                        ], performance_check=perf_check)
    test2 = TaskUnitTest(mine_grid, [
                        [
                            ['-', '-', '-', '-', '#'],
                            ['-', '-', '-', '-', '-'],
                            ['-', '-', '#', '-', '-'],
                            ['-', '-', '-', '-', '-'],
                            ['#', '-', '-', '-', '-']
                        ]],[
                            ['0', '0', '0', '1', '#'],
                            ['0', '1', '1', '2', '1'],
                            ['0', '1', '#', '1', '0'],
                            ['1', '2', '1', '1', '0'],
                            ['#', '1', '0', '0', '0']
                        ], performance_check=perf_check)
    test3 = TaskUnitTest(mine_grid, [
                        [
                            ['-', '-', '-', '#', '#'],
                            ['-', '#', '-', '-', '-'],
                            ['-', '-', '#', '-', '-'],
                            ['-', '#', '#', '-', '-'],
                            ['-', '-', '-', '-', '-']
                        ]], [
                            ['1', '1', '2', '#', '#'],
                            ['1', '#', '3', '3', '2'],
                            ['2', '4', '#', '2', '0'],
                            ['1', '#', '#', '2', '0'],
                            ['1', '2', '2', '1', '0']
                        ], performance_check=perf_check)
    test1.run()
    test2.run()
    test3.run()

def how_many_digit(number):
    """calculated for all positive numbers"""
    exponent = len(str(number)) - 1
    digits = exponent * pow(10, exponent) + (1 - pow(10, exponent)) // 9
    rest_digits = (number - 10 ** exponent) * len(str(pow(10, exponent)))
    return digits + rest_digits

def how_many_digit_test(perf_check: bool = False):
    test1 = TaskUnitTest(how_many_digit, [1], 0, performance_check=perf_check)
    test2 = TaskUnitTest(how_many_digit, [10], 9, performance_check=perf_check)
    test3 = TaskUnitTest(how_many_digit, [13], 15, performance_check=perf_check)
    test4 = TaskUnitTest(how_many_digit, [100], 189, performance_check=perf_check)
    test5 = TaskUnitTest(how_many_digit, [2020], 6969, performance_check=perf_check)
    test6 = TaskUnitTest(how_many_digit, [103496754], 820359675, performance_check=perf_check)
    test7 = TaskUnitTest(how_many_digit, [3248979384], 31378682729, performance_check=perf_check)
    test8 = TaskUnitTest(how_many_digit, [122398758003456], 1724870258940729, performance_check=perf_check)
    test9 = TaskUnitTest(how_many_digit, [58473029386609125789], 1158349476621071404669, performance_check=perf_check)

    test1.run()
    test2.run()
    test3.run()
    test4.run()
    test5.run()
    test6.run()
    test7.run()
    test8.run()
    test9.run()

class Employee:
    def __init__(self, full_name: str, **kwargs):
        splitted_full_name = full_name.split()
        self.name = splitted_full_name[0]
        self.surname = splitted_full_name[1]
        for k, v in kwargs.items():
            setattr(self, k, v)

def employee_test():
    test_count = 0
    def run(instance: Employee, attribute: str, asserted_value: Any):
        nonlocal test_count
        test_count += 1
        result = instance.__getattribute__(attribute)
        print(f"Test {test_count}: " + "Passed!" if result == asserted_value else f"Failed wih {result = }")


    john = Employee('John Doe')
    mary = Employee('Mary Major', salary=120000)
    richard = Employee('Richard Roe', salary=110000, height=178)
    giancarlo = Employee('Giancarlo Rossi', salary=115000, height=182, nationality='Italian')
    peng = Employee('Peng Zhu', salary=500000, height=185, nationality='Chinese',
                    subordinates=[i.surname for i in (john, mary, richard, giancarlo)])

    run(john, "surname", 'Doe')
    run(mary, "salary", 120000)
    run(richard, "height", 178)
    run(giancarlo,"nationality", 'Italian')
    run(peng, "subordinates", ['Doe', 'Major', 'Roe', 'Rossi'])

def can_see_the_stage(seats: list[list[int]]) -> bool:
    max_row = len(seats)-1
    for index_row, row in enumerate(seats):
        if index_row != max_row:
            for index_seat, seat in enumerate(row):
                if seats[index_row+1][index_seat] <= seat:
                    return False
    return True

def can_see_the_stage_test(perf_check: bool = False):
    test1 = TaskUnitTest(can_see_the_stage, [
                        [   [1, 2, 3],
                            [4, 5, 6],
                            [7, 8, 9]]], True, performance_check=perf_check)
    test2 = TaskUnitTest(can_see_the_stage, [
                        [   [1, 2, 2],
                            [1, 2, 3],
                            [4, 4, 4]]], False, performance_check=perf_check)
    test3 = TaskUnitTest(can_see_the_stage, [
                        [   [1, 1, 2],
                            [5, 2, 3],
                            [4, 4, 4]]], False, performance_check=perf_check)
    test4 = TaskUnitTest(can_see_the_stage, [
                        [   [1, 1, 2],
                            [5, 2, 3],
                            [6, 4, 4]]], True, performance_check=perf_check)
    test5 = TaskUnitTest(can_see_the_stage, [
                        [   [0, 0, 0],
                            [1, 1, 1],
                            [2, 2, 2]]], True, performance_check=perf_check)
    test6 = TaskUnitTest(can_see_the_stage, [
                        [   [2, 0, 0],
                            [1, 1, 1],
                            [2, 2, 2]]], False, performance_check=perf_check)
    test7 = TaskUnitTest(can_see_the_stage, [
                        [   [1, 0, 0],
                            [1, 1, 1],
                            [2, 2, 2]]], False, performance_check=perf_check)
    test8 = TaskUnitTest(can_see_the_stage, [
                        [   [1, 2, 3, 2, 1, 1],
                            [2, 4, 4, 3, 2, 2],
                            [5, 5, 5, 5, 4, 4],
                            [6, 6, 7, 6, 5, 5]]], True, performance_check=perf_check)
    test9 = TaskUnitTest(can_see_the_stage, [
                        [   [1, 2, 3, 2, 1, 1],
                            [2, 4, 4, 3, 2, 2],
                            [5, 5, 5, 10, 4, 4],
                            [6, 6, 7, 6, 5, 5]]], False, performance_check=perf_check)

    test1.run()
    test2.run()
    test3.run()
    test4.run()
    test5.run()
    test6.run()
    test7.run()
    test8.run()
    test9.run()

#this task is meh
def grey_scale(image: list[list[list[int]]]):
    new_image = []
    for height_index, height in enumerate(image):
        new_image.append([])
        for width in height:
            new_grey_pixel = sum(width) // len(width)
            new_grey_pixel = 0 if new_grey_pixel < 0 else 255 if new_grey_pixel > 255 else new_grey_pixel
            new_image[height_index].append([new_grey_pixel for _ in width])
    return new_image

def grey_scale_test(perf_check: bool = False):
    test1 = TaskUnitTest(grey_scale, [[
                    [[0,0,0], [0,0,157]],
                    [[1,100,0], [0,10,0]]
                ]], [
                     [[0, 0, 0], [52, 52, 52]],
                     [[33, 33, 33], [3, 3, 3]]], performance_check=perf_check)

    test2 = TaskUnitTest(grey_scale, [[
                    [[0,0,0], [0,0,157], [100,229,4]],
                    [[1,100,0], [0,10,0], [0,168,0]],
                    [[0,125,0], [15,0,9], [0,139,0]],
                    [[0,125,0], [0,0,9], [0,200,0]]
                ]], [[[0,0,0], [52,52,52], [111,111,111]],
                    [[33,33,33], [3,3,3], [56,56,56]],
                    [[41,41,41], [8,8,8], [46,46,46]],
                    [[41,41,41], [3,3,3], [66,66,66]]], performance_check=perf_check)

    test3 = TaskUnitTest(grey_scale, [[
                    [[0,0,255], [0,0,0], [0,0,157], [100,229,4]],
                    [[100,0,3], [1,100,0], [0,10,0], [0,168,0]],
                    [[16,30,0], [0,125,0], [15,0,9], [0,139,0]],
                    [[200,2,0], [0,125,0], [0,0,9], [0,200,0]]
                ]], [
                    [[85,85,85], [0,0,0], [52,52,52], [111,111,111]],
                    [[34,34,34], [34,34,34], [3,3,3], [56,56,56]],
                    [[15,15,15], [42,42,42], [8,8,8], [46,46,46]],
                    [[67,67,67], [42,42,42], [3,3,3], [67,67,67]]], performance_check=perf_check)

    test4 = TaskUnitTest(grey_scale, [[
                    [[0,-1,-120], [300,0,157]],
                    [[1,100,0], [256,10,0]]
                ]], [
                    [[0,0,0], [137,137,137]],
                    [[33,33,33], [88,88,88]]], performance_check=perf_check)
    test1.run()
    test2.run()
    test4.run()

def will_hit(func: str, pos: tuple):
    a, rest  = func.split("x")
    sign, b = rest.split()
    a, b = int(a), int(b)
    if sign == "+":
        return True if pos[1] == a*pos[0] + b else False
    else:
        return True if pos[1] == a*pos[0] - b else False

def will_hit_test(perf_check: bool = False):
    test1 = TaskUnitTest(will_hit, ["2x - 5", (0, 0)], False, performance_check=perf_check)
    test2 = TaskUnitTest(will_hit, ["-4x + 6", (1, 2)], True, performance_check=perf_check)
    test3 = TaskUnitTest(will_hit, ["-4x + 6", (2, 2)], False, performance_check=perf_check)
    test4 = TaskUnitTest(will_hit, ["3x - 8", (4, 4)], True, performance_check=perf_check)
    test5 = TaskUnitTest(will_hit, ["2x + 6", (3, 2)], False, performance_check=perf_check)
    test6 = TaskUnitTest(will_hit, ["-3x + 15", (5, 0)], True, performance_check=perf_check)

    test1.run()
    test2.run()
    test3.run()
    test4.run()
    test5.run()
    test6.run()

def longest_substring(number: str):
    """returns 00 if found none
        fun fact - 100 000 iteration per second for strings of len == 30"""
    result = "00"
    cache = []
    last_odd = False
    last_even = False
    for digit in number:
        if int(digit) % 2:
            if last_odd:
                cache_str = "".join(cache)
                if len(cache_str) > len(result):
                    result = cache_str
                cache.clear()
            cache.append(digit)
            last_even = False
            last_odd = True
        else:
            if last_even:
                cache_str = "".join(cache)
                if len(cache_str) > len(result):
                    result = cache_str
                cache.clear()
            cache.append(digit)
            last_even = True
            last_odd = False
    cache_str = "".join(cache)
    if len(cache_str) > len(result):
        result = cache_str
    return result

def longest_substring_test(perf_check: bool = False):
    test1 = TaskUnitTest(longest_substring, ["844929328912985315632725682153"], "56327256", performance_check=perf_check)
    test2 = TaskUnitTest(longest_substring,["769697538272129475593767931733"], "27212947", performance_check=perf_check)
    test3 = TaskUnitTest(longest_substring, ["937948289456111258444958189244"], "894561", performance_check=perf_check)
    test4 = TaskUnitTest(longest_substring, ["736237766362158694825822899262"], "636", performance_check=perf_check)
    test5 = TaskUnitTest(longest_substring, ["369715978955362655737322836233"], "369", performance_check=perf_check)
    test6 = TaskUnitTest(longest_substring, ["345724969853525333273796592356"], "496985", performance_check=perf_check)
    test7 = TaskUnitTest(longest_substring, ["548915548581127334254139969136"], "8581", performance_check=perf_check)
    test8 = TaskUnitTest(longest_substring, ["417922164857852157775176959188"], "78521", performance_check=perf_check)
    test9 = TaskUnitTest(longest_substring, ["251346385699223913113161144327"], "638569", performance_check=perf_check)
    test10 = TaskUnitTest(longest_substring, ["483563951878576456268539849244"], "18785", performance_check=perf_check)
    test11 = TaskUnitTest(longest_substring, ["853667717122615664748443484823"], "474", performance_check=perf_check)
    test12 = TaskUnitTest(longest_substring, ["398785511683322662883368457392"], "98785", performance_check=perf_check)
    test13 = TaskUnitTest(longest_substring, ["368293545763611759335443678239"], "76361", performance_check=perf_check)
    test14 = TaskUnitTest(longest_substring, ["775195358448494712934755311372"], "4947", performance_check=perf_check)
    test15 = TaskUnitTest(longest_substring, ["646113733929969155976523363762"], "76523", performance_check=perf_check)
    test16 = TaskUnitTest(longest_substring, ["575337321726324966478369152265"], "478369", performance_check=perf_check)
    test17 = TaskUnitTest(longest_substring, ["754388489999793138912431545258"], "545258", performance_check=perf_check)
    test18 = TaskUnitTest(longest_substring, ["198644286258141856918653955964"], "2581418569", performance_check=perf_check)
    test19 = TaskUnitTest(longest_substring, ["643349187319779695864213682274"], "349", performance_check=perf_check)
    test20 = TaskUnitTest(longest_substring, ["919331281193713636178478295857"], "36361", performance_check=perf_check)

    test1.run()
    test2.run()
    test3.run()
    test4.run()
    test5.run()
    test6.run()
    test7.run()
    test8.run()
    test9.run()
    test10.run()
    test11.run()
    test12.run()
    test13.run()
    test14.run()
    test15.run()
    test16.run()
    test17.run()
    test18.run()
    test19.run()
    test20.run()

def compress(numbers: list[str]):
    """
    cache = defaultdict(lambda: 0)
    for num in numbers:
        cache[num] += 1
    return "".join([f"{k}{v}" if v > 1 else f"{k}" for k, v in cache.items()])
    #"""
    previous_char = ""
    char_index = -1
    char_list = []
    for char in numbers:
        if previous_char != char:
            char_list.append([char, 1]) # [char, number] == {key: value} but with repetition
            previous_char = char
            char_index += 1
            continue
        char_list[char_index][1] += 1
    return "".join(f"{k}{v}" if v > 1 else f"{k}" for (k, v) in char_list)

def compress_test(perf_check: bool = False, details: bool = False):
    test1 = TaskUnitTest(compress, [["a", "a", "b", "b", "c", "c", "c"]], "a2b2c3", performance_check=perf_check, details=details)
    test2 = TaskUnitTest(compress, [["a"]], "a", performance_check=perf_check, details=details)
    test3 = TaskUnitTest(compress, [["a", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b"]], "ab12", performance_check=perf_check, details=details)
    test4 = TaskUnitTest(compress, [["a", "a", "a", "b", "b", "a", "a"]], "a3b2a2", performance_check=perf_check, details=details)
    test1.run()
    test2.run()
    test3.run()
    test4.run()

def is_economical(number):
    primes_list = find_all_primes(number)
    number_len = len(str(number))
    primes_len = 0
    primes_count = defaultdict(lambda: 0)
    for num in primes_list:
        primes_count[num] += 1
    for k, v in primes_count.items():
        primes_len += len(str(int(k)))
        if v > 1:
            primes_len += len(str(v))
    if primes_len == number_len:
        return "Equidigital"
    elif primes_len < number_len:
        return "Frugal"
    else:
        return "Wasteful"

def is_economical_test(perf_check: bool = False, details: bool = False):
    test1 = TaskUnitTest(is_economical, [14], "Equidigital", performance_check=perf_check, details=details)
    test2 = TaskUnitTest(is_economical, [125], "Frugal", performance_check=perf_check, details=details)
    test3 = TaskUnitTest(is_economical, [1024], "Frugal", performance_check=perf_check, details=details)
    test4 = TaskUnitTest(is_economical, [30], "Wasteful", performance_check=perf_check, details=details)
    test5 = TaskUnitTest(is_economical, [81], "Equidigital", performance_check=perf_check, details=details)
    test6 = TaskUnitTest(is_economical, [243], "Frugal", performance_check=perf_check, details=details)
    test7 = TaskUnitTest(is_economical, [5], "Equidigital", performance_check=perf_check, details=details)
    test8 = TaskUnitTest(is_economical, [6], "Wasteful", performance_check=perf_check, details=details)
    test9 = TaskUnitTest(is_economical, [1267], "Equidigital", performance_check=perf_check, details=details)
    test10 = TaskUnitTest(is_economical, [1701], "Frugal", performance_check=perf_check, details=details)
    test11 = TaskUnitTest(is_economical, [1267], "Equidigital", performance_check=perf_check, details=details)
    test12 = TaskUnitTest(is_economical, [12871], "Equidigital", performance_check=perf_check, details=details)
    test13 = TaskUnitTest(is_economical, [88632], "Wasteful", performance_check=perf_check, details=details)

    test1.run()
    test2.run()
    test3.run()
    test4.run()
    test5.run()
    test6.run()
    test7.run()
    test8.run()
    test9.run()
    test10.run()
    test11.run()
    test12.run()
    test13.run()

def who_goes_free(prisoners: int, step: int):
    if prisoners == 1:
        return 1
    return ((who_goes_free(prisoners - 1, step) + step - 1) % prisoners) + 1

def who_goes_free_test(perf_check: bool = False, details: bool = False):
    test0 = TaskUnitTest(who_goes_free, [47, 5], 4, performance_check=perf_check, details=details)
    test0.run()
    test1 = TaskUnitTest(who_goes_free, [9, 2], 3, performance_check=perf_check, details=details)
    test2 = TaskUnitTest(who_goes_free, [9, 3], 1, performance_check=perf_check, details=details)
    test3 = TaskUnitTest(who_goes_free, [7, 2], 7, performance_check=perf_check, details=details)
    test4 = TaskUnitTest(who_goes_free, [7, 3], 4, performance_check=perf_check, details=details)
    test5 = TaskUnitTest(who_goes_free, [15, 4], 13, performance_check=perf_check, details=details)
    test6 = TaskUnitTest(who_goes_free, [14, 3], 2, performance_check=perf_check, details=details)
    test7 = TaskUnitTest(who_goes_free, [53, 7], 22, performance_check=perf_check, details=details)
    test8 = TaskUnitTest(who_goes_free, [543, 21], 456, performance_check=perf_check, details=details)
    test9 = TaskUnitTest(who_goes_free, [673, 13], 304, performance_check=perf_check, details=details)

    test1.run()
    test2.run()
    test3.run()
    test4.run()
    test5.run()
    test6.run()
    test7.run()
    test8.run()
    test9.run()


def mandragora(health_data: list[int]):
    all_actions = product('be', repeat=len(health_data))
    highest_exp = 0
    for actions in all_actions:
        exp = 0
        health_player = 1
        for health_mandragora, action in zip(sorted(health_data), actions):
            if action == 'e':
                health_player += 1
            else:
                exp += health_player * health_mandragora
        if exp > highest_exp:
            highest_exp = exp
    return highest_exp

def mandragora_test(perf_check: bool = False, details: bool = False):
    test1 = TaskUnitTest(mandragora, [[3, 2, 2]], 10, performance_check=perf_check, details=details)
    test1.run()


if __name__ == "__main__":
    TaskTest(mandragora_test, details=False, performance_check=True, sample_size=10, iterations=1000).run()
    pass