__author__ = "Bernadine Nzavake"
from typing import TypeVar
T = TypeVar("T")


class SequenceDatabase:
    def __init__(self):
        self.trie = TrieQ1()

    def addSequence(self, s: str) -> None:
        """
        add a new sequence of DNA into a trie
        :param s: string of char within [A,B,C,D]
        complexity: O(len(s))
        """
        self.trie.insert(s, s)

    def query(self, q: str) -> T:
        """
        look for the sequence with with prefix q that has highest frequency and/or the lexicographically
        least
        :param q: string of char within [A,B,C,D] or empty string
        :return: a string with prefix q that has highest frequency and/or the lexicographically
        least, None if there is q in the trie
        complexity: O(N) where N is the len(q)
        """
        unique_list = self.trie.search(q)
        return_data = ""
        if unique_list is not None:
            pre_freq = unique_list[0][1]
            return_data = unique_list[0][0]
            i = 1
            while i < len(unique_list):
                if pre_freq < unique_list[i][1]:
                    return_data = unique_list[i][0]
                    pre_freq = unique_list[i][1]
                elif pre_freq == unique_list[i][1]:
                    if return_data > unique_list[i][0]:
                        return_data = unique_list[i][0]
                i += 1
        else:
            return_data = None
        return return_data


class OrfFinder:
    def __init__(self, genome: str) -> None:
        """
        initialise the suffix trie of the genome
        :param genome: string of char within [A,B,C,D]
        complexity: O(N^2) where N is the length of genome
        """
        self.genome = genome
        self.suf_trie = TrieQ2()
        for i in range(len(genome)):
            self.suf_trie.insert_in_order(genome[i:], i)
            self.suf_trie.insert_reverse(genome[i:], i)

    def find(self, start: str, end: str) -> list:
        """
        Find substring starting with start and ending with end
        :param start: string of char [A,B,C,D]
        :param end: string of char [A,B,C,D]
        :return: list of all substring
        complexity: O(len(start) + O(len(end)+ U) where U is the length of the substring
        """
        index_lists = self.suf_trie.search(start)
        index_liste = self.suf_trie.search(end)
        # add to each index of the len of the end
        for i in range(len(index_liste)):
            index_liste[i] += len(end)
        i = 0
        j = 0
        output = []
        while i < len(index_lists):
            s = index_lists[i]
            while j < len(index_liste):
                e = index_liste[j]
                # check whether there is a valid substring
                if e-s >= len(start)+len(end):
                    # u = (s, e)
                    output.append(self.genome[s:e])
                j += 1
            i += 1
        return output


class TrieQ1:
    def __init__(self):
        self.root = Node(5)

    def insert(self, _str_: str, data= None) -> bool:
        """
        insert a string into a trie
        :param _str_: string of char within [A,B,C,D]
        :return: true if new word insert, false other wise
        complexity: O(N) where N is the length of _str_
        """
        current = self.root
        i = 0
        new_word = False
        return self.insert_aux(_str_, current, data, i, new_word)

    def insert_aux(self, _str_: str, current: T, data, i: int, new_word: bool) -> bool:
        if i == len(_str_):
            index = 0
            if current.link[index] is not None:
                current = current.link[index]
                new_word = False
            else:
                current.link[index] = Node(5, data)
                current = current.link[index]
                current.uni_freq += 1
                new_word = True
            current.frequency += 1
            return new_word
        else:
            index = ord(_str_[i]) - 65 + 1
            if current.link[index] is not None:
                current = current.link[index]
            else:
                current.link[index] = Node(5, data)
                current = current.link[index]
            ans = self.insert_aux(_str_, current,data, i+1, new_word)
            # add 1 to frequency and unique frequency count if a new word is added
            # other wise add only one to the frequency count
            if ans:
                current.frequency += 1
                current.uni_freq += 1
                current.uni_data.append((data, current.frequency))
            else:
                current.frequency += 1
            return ans

    def search(self, instance: str):
        current = self.root
        i = 0
        return self.search_aux(instance, current, i)

    def search_aux(self, instance, current, i):
        if i == len(instance):
            return current.uni_data
        else:
            index = ord(instance[i]) - 65 + 1
            if current.link[index] is not None:
                current = current.link[index]
            else:
                return None
            ans = self.search_aux(instance, current, i + 1)
            return ans


class TrieQ2:
    def __init__(self):
        self.root = Node(5)

    def insert_in_order(self, _str_: str, pos):
        """
        insert a string into a trie in order
        :param _str_: string of char within [A,B,C,D]
        :param pos: position from which it is been added from
        :return: the last node
        complexity: O(N) where N is the length of _str_
        """
        current = self.root
        i = 0
        return self.insert_aux_in_order(_str_, current, i, pos)

    def insert_reverse(self, _str_: str, pos):
        """
        insert a string into a trie in reverse order
        :param _str_: string of char within [A,B,C,D]
        :param pos: position from which it is been added from
        :return: the last node
        complexity: O(N) where N is the length of _str_
        """
        current = self.root
        i = len(_str_) - 1
        return self.insert_aux_reverse(_str_, current, i, pos)

    def insert_aux_reverse(self, _str_, current, i, pos):
        if i == 0:
            index = 0
            if current.link[index] is not None:
                current = current.link[index]
            else:
                current.link[index] = Node(5)
                current = current.link[index]
            return current
        else:
            index = ord(_str_[i]) - 65 + 1
            if current.link[index] is not None:
                current = current.link[index]
            else:
                current.link[index] = Node(5)
                current = current.link[index]
            ans = self.insert_aux_reverse(_str_, current, i - 1, pos)
            # add the position in it node
            current.index_list.append(pos)
            return ans

    def insert_aux_in_order(self, _str_, current, i, pos):
        if i == len(_str_):
            index = 0
            if current.link[index] is not None:
                current = current.link[index]
            else:
                current.link[index] = Node(5)
                current = current.link[index]
            return current
        else:
            index = ord(_str_[i]) - 65 + 1
            if current.link[index] is not None:
                current = current.link[index]
            else:
                current.link[index] = Node(5)
                current = current.link[index]
            ans = self.insert_aux_in_order(_str_, current, i + 1, pos)
            # add the position in it node
            current.index_list.append(pos)
            return ans

    def search(self, instance: str):
        current = self.root
        i = 0
        return self.search_aux(instance, current, i)

    def search_aux(self, instance, current, i):
        if i == len(instance):
            return current.index_list
        else:
            index = ord(instance[i]) - 65 + 1
            if current.link[index] is not None:
                current = current.link[index]
            else:
                return None
            ans = self.search_aux(instance, current, i + 1)
            return ans


class Node:
    def __init__(self, size=27, data=None):
        self.link = [None] * size
        self.frequency = 0
        self.index_list = []
        self.uni_freq = 0
        self.uni_data = []
        self.data = data

    def __str__(self):
        print(self.link)
