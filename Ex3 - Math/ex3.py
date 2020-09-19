# FILE : ex3.py
# WRITER : Ron Shuvy, ronshuvy, 206330193
# EXERCISE : intro2cs1 2019, ex3


def input_list():
    """ Ask for a list of numbers from the user and calculates their sum
    :return: a list of numbers with its sum
    :rtype: list
    """
    num_list = []  # input numbers
    sum_of_list = 0
    user_input = input()
    while user_input != "":
        num_list.append(int(user_input))
        sum_of_list += int(user_input)
        user_input = input()  # asks for next number from user
    num_list.append(sum_of_list)
    return num_list


def inner_product(vec_1, vec_2):
    """ Calculates the inner product of 2 given vectors
    :param vec_1: first vector
    :param vec_2: second vector
    :return: the inner product result
    :rtype: float
    """
    if len(vec_1) != len(vec_2):
        return None
    ip_result = 0
    for i in range(len(vec_1)):
        ip_result += (vec_1[i] * vec_2[i])
    return ip_result


def sequence_monotonicity(sequence):
    """ Determines the sequence's property of monotonicity
    :param sequence: a list of numbers considered as sequence
    :return: boolean list ordered by properties :
    increasing, strictly increasing, decreasing and strictly decreasing
    :rtype: list
    """
    monotonicity_list = [True, True, True, True]
    if not sequence:
        return monotonicity_list
    for i in range(len(sequence)-1):
        if sequence[i] == sequence[i+1]:
            monotonicity_list[1], monotonicity_list[3] = False, False
        elif sequence[i] > sequence[i+1]:
            monotonicity_list[0], monotonicity_list[1] = False, False
        elif sequence[i] < sequence[i+1]:
            monotonicity_list[2], monotonicity_list[3] = False, False
    return monotonicity_list


def monotonicity_inverse(def_bool):
    """ Gets list of monotonicity's properties of a sequence
    :param def_bool: properties of monotonicity
    :return: example of such sequence
    :rtype: list
    """
    increasing = [1, 1, 2, 3]
    strictly_increasing = [1, 2, 3, 4]
    decreasing = [3, 3, 2, 1]
    strictly_decreasing = [4, 3, 2, 1]
    monotonous = [1, 1, 1, 1]
    not_monotonous = [1, 2, 1, 2]
    if def_bool == sequence_monotonicity(increasing):
        return increasing
    elif def_bool == sequence_monotonicity(strictly_increasing):
        return strictly_increasing
    elif def_bool == sequence_monotonicity(decreasing):
        return decreasing
    elif def_bool == sequence_monotonicity(strictly_decreasing):
        return strictly_decreasing
    elif def_bool == sequence_monotonicity(monotonous):
        return monotonous
    elif def_bool == sequence_monotonicity(not_monotonous):
        return not_monotonous
    else:
        return None


def primes_for_asafi(n):
    """ Returns the first n prime numbers
    :param n: number of first primes
    :return: primes list
    :rtype: list
    """
    primes_list = [2]
    primes_counter = 1
    num = 3  # The number we test each time
    while primes_counter != n:
        is_prime = True
        for i in range(2, num):  # Worst case : sqrt(n) iterations
            if i * i > num:  # Checks up to sqrt of num
                break
            if num % i == 0:
                is_prime = False
                break
        if is_prime:  # if we found prime number
            primes_list.append(num)
            primes_counter += 1
        num += 1
    return primes_list


def sum_of_vectors(vec_lst):
    """ Return the sum of all given vectors
    :param vec_lst: list of vectors
    :return: the vector of sum
    :rtype: list
    """
    if not vec_lst:
        return None
    vec_sum = vec_lst[0][:]
    for i in range(1, len(vec_lst)):
        for j in range(len(vec_lst[i])):  # j is a coordinate
            vec_sum[j] = vec_lst[i][j] + vec_sum[j]
    return vec_sum


def num_of_orthogonal(vectors):
    """ Finds pairs of vectors which are orthogonal to each other
    :param vectors: list of vectors
    :return: number of orthogonal pairs
    :rtype: int
    """
    num_of_pairs = 0
    for i in range(len(vectors)-1):
        # Checks each vector with its consecutive vectors in the list
        for j in range(i+1, len(vectors)):
            # The vectors which follows after the i-th vector
            if inner_product(vectors[i], vectors[j]) == 0:
                # If true - we found an orthogonal pair!
                num_of_pairs += 1
    return num_of_pairs
