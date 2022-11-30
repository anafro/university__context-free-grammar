class Grammar:
    def __init__(self, N: set, T: set, P: dict, S: str):
        if S not in N:
            raise Exception("Axiom is not in Non-terminals")
        if not set(P.keys()).issubset(N):
            raise Exception("Grammar is not content-independent")
        #Все ли терминалы из правил в множестве...
        self.N = N  # нетерминалы
        self.T = T  # терминалы (будем считать, что каждый терминал состоит только из одного символа)
        self.P = P  # правила
        self.S = S  # аксиома (начальный символ грамматики)
 
    def remove_unreachable_symbols(self):
        """ Возвращает грамматику без недостижимых символов (при этом нынешнюю грамматику не меняет) """
        V_nonterminals = set([self.S])  # достижимые нетерминалы
        V_nonterminals_temp = V_nonterminals.copy()
        # используется, чтобы не проходится по одним и тем же нетерминалам на каждой итерации
 
        V_terminals = set()  # достижимые терминалы
 
        while True:
            for rule_left_side in self.P:
                # проходимся по правилам и проверяем,
                # есть ли левая сторона правила в достижимых нетерминалах
                if rule_left_side in V_nonterminals_temp:
                    for rule in self.P[rule_left_side]:
                        # проходимся по выводам правила и добавляем символы из этих выводов в достижимые
                        rule_output = rule
                        for char in rule_output:
                            if char in self.T:
                                V_terminals.add(char)
                            if char in self.N:
                                V_nonterminals_temp.add(char)
 
            V_nonterminals_temp = V_nonterminals_temp.difference(V_nonterminals)
            # убираем все достижимые нетерминалы,
            # которые уже проходили через верхний цикл (difference - разность множеств)
            if len(V_nonterminals_temp) == 0:  # проверяем, были ли найдены все достижимые нетерминалы
                break
            else:
                V_nonterminals = V_nonterminals.union(V_nonterminals_temp)
                # если нет, то добавляем достижимые нетерминалы,
                # которые были найденны на последней итерации (union - объединение множеств)
 
        if self.N == V_nonterminals:
            # если достижимые нетерминалы совпадают с теми,
            # что были изначально определены в грамматике, то возвращаем новую, идентичную этой грамматику
            return Grammar(self.N.copy(), self.T.copy(), self.P.copy(), self.S)
        else:
            # в противном случае создаем новые правила вывода, в которых будут все старые, кроме тех, чья левая сторона не является достижимым нетерминалом
            new_rules = dict()
            for nonterminal in V_nonterminals:
                if nonterminal in self.P:
                    new_rules[nonterminal] = self.P[nonterminal].copy()
            return Grammar(V_nonterminals, V_terminals, new_rules,
                           self.S)  # и возвращаем граматику с достижимыми терминалами и нетерминалами, и новыми правилами вывода
 
    def print(self):
        """ Функция печати грамматики"""
        print(18 * "-")
        print('Нетерминалы: ')
        nonterminals = ""
        for nonterminal in self.N:
            nonterminals += nonterminal + ' '
        print(nonterminals)
        print('\n')
 
        print('Терминалы: ')
        terminals = ""
        for terminal in self.T:
            terminals += terminal + ' '
        print(terminals)
        print('\n')
 
        print('Правила вывода:')
        for left_side in self.P:
            rule = ""
            rule = left_side + ' -> '
            for i in range(len(self.P[left_side])):
                if i != len(self.P[left_side]) - 1:
                    rule += self.P[left_side][i] + " | "
                else:
                    rule += self.P[left_side][i]
            print(rule)
        print('\n')
 
        print("Аксиома: " + self.S)
        print(18 * "-")
 
    def is_contain_nn(self, string, symbols):
        for symbol in string:
            if symbol not in self.T and symbol not in symbols:
                return False
        return True
 
    def is_not_empty(self, retFlag=0):
        N = set()
        NTemp = N.copy() #Два множества для "хороших" символов
        while True:
            for rule in self.P: #идем по всем правилам
                for i, elem in enumerate(self.P[rule]):
                    if self.is_contain_nn(elem, N): #если правая часть содержит только хорошие символы и терминалы, то добавляем нетерминал к хорошим символам
                        N.add(rule)
                        break
            if N == NTemp:
                break #условие прерывания алгоритма: если за проход мы не добавили никакого нового хорошего символа, то цикл прерывается
            NTemp = N.copy()
        if (retFlag==1): #если вызвали функцию с параметром 1, то она возвращает true (язык не пуст) либо false (язык пуст)
            return self.S in N
        tempP = self.P.copy() #временный словарь правил
        for rule in self.P:
            if rule not in N:
                tempP.pop(rule) #если нетерминала нет в хороших символах то удаляем его из словаря
            else:               #иначе оставляет только те правила, в правых частях которого содержатся только хорошие символы и терминалы
                tempRule = []
                for i, elem in enumerate(self.P[rule]):
                    if self.is_contain_nn(elem, N):
                        tempRule.append(elem)
                tempP[rule] = tempRule
        return Grammar(N,self.T,tempP,self.S)
 
    def remove_useless_symbols(self):
        """ Очень сложный алгоритм, спасибо, Алексей, Евгений """
            return self.is_not_empty().remove_unreachable_symbols()
 
 
if __name__ == '__main__':
    G = Grammar({'E', 'T', 'F'},
                {'a', '(', ')', '+', '*'},
                {
                 'E': ['F'],
                 'F': ['(E)', 'Ta']
                },
                'E')
 
    F = Grammar({'S'}, {'1', '0'}, {'S': ['0', '1', '0S', '1S']}, 'S')
 
    E = Grammar({'S','A', 'B', 'C', 'D'}, {'1', '0', '2', '3'},
                {'A': ['B', 'A'], 'C': ['D', 'D2'], 'D': ['123', '1', '2', '3']}, 'S')
 
    H = Grammar({'A', 'B', 'S'}, {'a', 'b'}, {'S': ['aA'], 'A': ['AB'], 'B': ['b']}, 'S')
 
    E.print()
    E=E.remove_useless_symbols()
    E.print()
