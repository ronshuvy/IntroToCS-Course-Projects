import itertools


class Node:
    def __init__(self, data, positive_child=None, negative_child=None):
        self.data = data
        self.positive_child = positive_child
        self.negative_child = negative_child


class Record:
    def __init__(self, illness, symptoms):
        self.illness = illness
        self.symptoms = symptoms


def parse_data(filepath):
    """
    Parsing data from a given file and build Record objects
    :param filepath: filepath
    :return: list of records
    """
    with open(filepath) as data_file:
        records = []
        for line in data_file:
            words = line.strip().split()
            records.append(Record(words[0], words[1:]))
        return records


class Diagnoser:
    def __init__(self, root):
        self.root = root

    def diagnose(self, symptoms):
        """
        Diagnoses an illness
        :param symptoms: list of strings
        :return: an illness (string)
        """
        return self.diagnose_helper(self.root, symptoms)

    def diagnose_helper(self, node, symptoms):
        """
        Diagnoses an illness based on a given symptoms by using decision tree
        :param node: current vertex in the tree
        :param symptoms: list of string
        :return: an illness (string)
        """
        # If current node is a leaf
        if not node.positive_child and not node.negative_child:
            return node.data

        # current node has a question
        if node.data in symptoms:
            return self.diagnose_helper(node.positive_child, symptoms)
        return self.diagnose_helper(node.negative_child, symptoms)

    def calculate_success_rate(self, records):
        """
        Calculates success rate of the given decision tree based on its
         diagnose in compares to the correct illness
        :param records: list of (illness, symptoms)
        :return: float between 0-1
        """
        success_diagnoses = 0
        for record in records:
            if self.diagnose(record.symptoms) == record.illness:
                success_diagnoses += 1
        try:
            return success_diagnoses / len(records)
        except ZeroDivisionError:
            return 0

    def all_illnesses(self):
        """
        Returns all illnesses in the tree's leaves by incidence sorting
        (max to min)
        :return: list of illnesses (strings)
        """
        illnesses_dict = self.gather_all_illnesses(self.root, dict())

        # Sorting the dictionary by illnesses incidence
        illnesses_sorted = {
            k: v for k, v in sorted(illnesses_dict.items(),
                                    key=lambda item: item[1], reverse=True)}

        return list(illnesses_sorted.keys())

    def gather_all_illnesses(self, node, ills_dict):
        """
        Returns all illnesses in the tree's leaves with the number of
        its instances
        :param node: current vertex in the tree
        :param ills_dict: contains keys and values - (illness : counter)
        :return: dictionary of illnesses and (strings)
        """

        # Check if current node is a leaf
        if not node.negative_child and not node.positive_child:
            if not node.data:
                return
            if node.data in ills_dict.keys():
                ills_dict[node.data] += 1
            else:
                ills_dict[node.data] = 1
            return ills_dict

        self.gather_all_illnesses(node.positive_child, ills_dict)
        self.gather_all_illnesses(node.negative_child, ills_dict)

        return ills_dict

    def paths_to_illness(self, illness):
        """
        Returns list of all paths to a given illness
        :param illness: string
        :return: list of all paths to the given illness
        :rtype: list of lists
        """
        return self.path_to_illness_helper(illness, self.root, [], [])

    def path_to_illness_helper(self, illness, node, paths, curr_path):
        """
        Returns list of all paths to a given illness
        :param illness: string
        :param node: current vertex in the tree
        :param paths: list of all different paths that was found
        :param curr_path: list of booleans - current path in the tree
        :return: list of lists
        """
        # Checks if current node is a leaf
        if not node.positive_child and not node.negative_child:
            if node.data == illness:
                paths.append(curr_path)
            return paths

        p1 = curr_path + [True]  # symptoms appears (positive answer)
        self.path_to_illness_helper(illness, node.positive_child, paths, p1)
        p2 = curr_path + [False]  # symptoms doesn't appear (negative answer)
        self.path_to_illness_helper(illness, node.negative_child, paths, p2)
        return paths


def build_tree(records, symptoms):
    """
    Builds decision tree according to a given symptoms
    :param records: list of records (illness, list of symptoms)
    :param symptoms: list of strings
    :return: Node (tree's root)
    """
    return build_tree_helper(records, symptoms, 0, [])


def build_tree_helper(records, symptoms, ind, path):
    """
    Builds decision tree according to a given symptoms
    :param records: list of records (illness, list of symptoms)
    :param symptoms: list of strings
    :param ind: index of current symptoms in symptoms list
    :param path: list of booleans - represents the current path in the tree
    :return: Node (tree's root)
    """

    if ind == len(symptoms):
        illness = choose_illness_from_symptoms(records, symptoms, path)
        return Node(illness)

    node_data = symptoms[ind]
    ind += 1
    pos_path = path + [True]  # build positive child subtree
    neg_path = path + [False]  # build negative child subtree
    return Node(node_data,
                build_tree_helper(records, symptoms, ind, pos_path),
                build_tree_helper(records, symptoms, ind, neg_path))


def choose_illness_from_symptoms(records, symptoms, bool_path):
    """
    Chooses the most common illness from the illnesses in a given tree
    :param records: list of records (illness, list of symptoms)
    :param symptoms: list of strings
    :param bool_path: list of booleans - represents a given path in the tree
    :return: illness (string)
    """
    poss_illnesses = dict()

    for record in records:
        is_match = True

        for i, symptom in enumerate(symptoms):
            if (symptom in record.symptoms) != bool_path[i]:
                is_match = False
                break

        if is_match:
            if record.illness in poss_illnesses.keys():
                poss_illnesses[record.illness] += 1
            else:
                poss_illnesses[record.illness] = 1

    if not poss_illnesses:
        return None

    return max(poss_illnesses.items(), key=lambda x: x[1])[0]


def optimal_tree(records, symptoms, depth):
    """
    Returns the tree with the highest success rating
    :param records: list of records (illness, list of symptoms)
    :param symptoms: list of symptoms
    :param depth: size of each sub-symptoms
    :return: Node (tree's root)
    """

    trees_and_rates = dict()
    for comb in itertools.combinations(symptoms, depth):
        # each combination is a sub-list of symptoms list
        curr_tree = build_tree(records, comb)
        diagnoser = Diagnoser(curr_tree)
        success_rate = diagnoser.calculate_success_rate(records)
        trees_and_rates[curr_tree] = success_rate

    if not trees_and_rates:  # if depth is 0
        return Node(None)

    return max(trees_and_rates.items(), key=lambda x: x[1])[0]
