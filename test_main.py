import unittest

from main import Grammar
from main import BOOL_MODE, GRAMMAR_MODE


class MyTestCase(unittest.TestCase):
    def test_grammar_axiom_not_in_non_terminals(self):
        self.assertRaises(Exception, lambda: Grammar(
            {'E', 'T', 'F'},
            {'a', '(', ')', '+', '*'},
            {
                'E': ['F'],
                'F': ['(E)', 'Ta']
            },
            'Q'
        ))

    def test_grammar_content_independency(self):
        self.assertRaises(Exception, lambda: Grammar(
            {'E', 'T', 'F', 'Z'},
            {'a', '(', ')', '+', '*'},
            {
                'E': ['F'],
                'F': ['(E)', 'Ta'],
                'Y': ['E']
            },
            'E'
        ))

    def test_grammar_remove_useless_symbols_should_stay_the_same(self):
        original_grammar: Grammar = Grammar(
            {'S'},
            {'1', '0'},
            {
                'S': ['0', '1', '0S', '1S']
            },
            'S'
        )

        grammar_without_useless_symbols = original_grammar.remove_useless_symbols()

        self.assertEqual(original_grammar.non_terminals, grammar_without_useless_symbols.non_terminals)
        self.assertEqual(original_grammar.terminals, grammar_without_useless_symbols.terminals)
        self.assertEqual(original_grammar.axiom, grammar_without_useless_symbols.axiom)
        self.assertEqual(original_grammar.rules, grammar_without_useless_symbols.rules)

    def test_grammar_is_not_empty_when_its_not_empty(self):
        empty_grammar: Grammar = Grammar(
            {'A', 'B'},
            {'0', '1'},
            {
                'A': ['0'],
                'B': ['1']
            },
            'A'
        )

        self.assertTrue(empty_grammar.is_not_empty(ret_flag=BOOL_MODE))

    def test_grammar_is_not_empty_when_its_empty(self):
        empty_grammar: Grammar = Grammar(
            {'A'},
            {'0'},
            {},
            'A'
        )

        self.assertFalse(empty_grammar.is_not_empty(ret_flag=BOOL_MODE))


if __name__ == '__main__':
    unittest.main()
