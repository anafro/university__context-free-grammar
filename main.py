from __future__ import annotations

import pprint
from typing import Union

GRAMMAR_MODE = 0
BOOL_MODE = 1


class Grammar:
    def __init__(self, non_terminals: set, terminals: set, rules: dict, axiom: str):
        if axiom not in non_terminals:
            raise Exception("Axiom is not in the non-terminals.")
        if not set(rules.keys()).issubset(non_terminals):
            raise Exception("Grammar is not content-independent.")

        # нетерминалы
        self.non_terminals = non_terminals

        # терминалы (будем считать, что каждый терминал состоит только из одного символа)
        self.terminals = terminals

        # правила
        self.rules = rules

        # аксиома (начальный символ грамматики)
        self.axiom = axiom

    def remove_unreachable_symbols(self) -> Grammar:
        """ Возвращает грамматику без недостижимых символов (при этом нынешнюю грамматику не меняет) """
        # достижимые нетерминалы
        reachable_non_terminals = {self.axiom}

        # используется, чтобы не проходится по одним и тем же нетерминалам на каждой итерации
        reachable_non_terminals_original = reachable_non_terminals.copy()

        # достижимые терминалы
        reachable_terminals = set()

        while True:
            for rule_left_side in self.rules:

                # проходимся по правилам и проверяем,
                # есть ли левая сторона правила в достижимых нетерминалах
                if rule_left_side in reachable_non_terminals_original:
                    for rule in self.rules[rule_left_side]:

                        # проходимся по выводам правила и добавляем символы из этих выводов в достижимые
                        rule_output = rule
                        for char in rule_output:
                            if char in self.terminals:
                                reachable_terminals.add(char)
                            if char in self.non_terminals:
                                reachable_non_terminals_original.add(char)

            # убираем все достижимые нетерминалы,
            # которые уже проходили через верхний цикл (difference - разность множеств)
            reachable_non_terminals_original = reachable_non_terminals_original.difference(reachable_non_terminals)

            # проверяем, были ли найдены все достижимые нетерминалы
            if len(reachable_non_terminals_original) == 0:
                break

            # если нет, то добавляем достижимые нетерминалы,
            # которые были найденны на последней итерации (union - объединение множеств)
            else:
                reachable_non_terminals = reachable_non_terminals.union(reachable_non_terminals_original)

        # если достижимые нетерминалы совпадают с теми,
        # что были изначально определены в грамматике, то возвращаем новую, идентичную этой грамматику
        if self.non_terminals == reachable_non_terminals:
            return Grammar(self.non_terminals.copy(), self.terminals.copy(), self.rules.copy(), self.axiom)

        # в противном случае создаем новые правила вывода,
        # в которых будут все старые, кроме тех,
        # чья левая сторона не является достижимым нетерминалом
        else:
            new_rules = dict()
            for non_terminal in reachable_non_terminals:
                if non_terminal in self.rules:
                    new_rules[non_terminal] = self.rules[non_terminal].copy()

            # и возвращаем граматику с
            # достижимыми терминалами и нетерминалами,
            # и новыми правилами вывода
            return Grammar(reachable_non_terminals, reachable_terminals, new_rules, self.axiom)

    def print(self) -> None:
        """ Функция печати грамматики"""
        print("-" * 18)
        print('Non-terminals: ')
        non_terminals = ""

        for non_terminal in self.non_terminals:
            non_terminals += non_terminal + ' '

        print(non_terminals)
        print('\n')

        print('Terminals: ')
        terminals = ""

        for terminal in self.terminals:
            terminals += terminal + ' '

        print(terminals)
        print('\n')

        print('Rules of conclusion: ')

        for left_side in self.rules:
            rule = left_side + ' -> '
            for i in range(len(self.rules[left_side])):
                if i != len(self.rules[left_side]) - 1:
                    rule += self.rules[left_side][i] + " | "
                else:
                    rule += self.rules[left_side][i]

            print(rule)

        print('\n')

        print("Аксиома: " + self.axiom)
        print(18 * "-")

    def is_contain_nn(self, string: str, symbols: set) -> bool:
        for symbol in string:
            if symbol not in self.terminals and symbol not in symbols:
                return False
        return True

    def is_not_empty(self, ret_flag=GRAMMAR_MODE) -> Union[Grammar, bool]:
        # Два множества для "хороших" символов
        non_terminals: set = set()
        good_non_terminals: set = non_terminals.copy()

        while True:

            # идем по всем правилам
            for rule in self.rules:
                for i, rule_item in enumerate(self.rules[rule]):

                    # если правая часть содержит только хорошие символы и терминалы,
                    # то добавляем нетерминал к хорошим символам
                    if self.is_contain_nn(rule_item, non_terminals):
                        non_terminals.add(rule)
                        break

            # условие прерывания алгоритма:
            # если за проход мы не добавили никакого нового хорошего символа
            if non_terminals == good_non_terminals:
                break

            good_non_terminals = non_terminals.copy()

        # если вызвали функцию с параметром 1,
        # то она возвращает true (язык не пуст) либо false (язык пуст)
        if ret_flag == BOOL_MODE:
            return self.axiom in non_terminals

        # временный словарь правил
        rules_copy = self.rules.copy()
        for rule in self.rules:

            # если нетерминала нет в хороших символах,
            # то удаляем его из словаря
            if rule not in non_terminals:
                rules_copy.pop(rule)

            # иначе оставляет только те правила,
            # в правых частях которого содержатся
            # только хорошие символы и терминалы
            else:
                rule_buffer = []
                for i, rule_item in enumerate(self.rules[rule]):
                    if self.is_contain_nn(rule_item, non_terminals):
                        rule_buffer.append(rule_item)

                rules_copy[rule] = rule_buffer
        return Grammar(non_terminals, self.terminals, rules_copy, self.axiom)

    def remove_useless_symbols(self):
        """ Очень сложный алгоритм, спасибо, Алексей, Евгений """
        return self.is_not_empty().remove_unreachable_symbols()


if __name__ == '__main__':
    # G = Grammar({'E', 'T', 'F'},
    #             {'a', '(', ')', '+', '*'},
    #             {
    #                 'E': ['F'],
    #                 'F': ['(E)', 'Ta']
    #             },
    #             'E')

    # G.print()

    F = Grammar({'S'}, {'1', '0'}, {'S': ['0', '1', '0S', '1S']}, 'S')

    # E = Grammar({'S', 'A', 'B', 'C', 'D'}, {'1', '0', '2', '3'},
    #             {'A': ['B', 'A'], 'C': ['D', 'D2'], 'D': ['123', '1', '2', '3']}, 'S')

    H = Grammar({'A', 'B', 'S'}, {'a', 'b'}, {'S': ['aA'], 'A': ['AB'], 'B': ['b']}, 'S')

    F.print()
    pprint.pprint(vars(F))
    F = F.remove_useless_symbols()
    F.print()
    pprint.pprint(vars(F))
