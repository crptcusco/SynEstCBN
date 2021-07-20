import re  # analysis of regular expressions
import operator  # unary operator management
import sys  # allows to use functions for interaction with the system

from string import ascii_lowercase, ascii_uppercase  # import the list of uppercase and lowercase letters
from itertools import product  # generate combinations of numbers
from collections import namedtuple  # structures like trees


class SignalModel(object):
    def __init__(self, rdda_entrada, rdda_salida, l_variaveis_saida, name_variable, acoplament_function):
        self.rdda_entrada = rdda_entrada
        self.rdda_salida = rdda_salida
        self.l_variaveis_saida = l_variaveis_saida
        self.name_variable = name_variable
        self.acoplament_function = acoplament_function
        self.true_table = self.process_true_table()

    def show(self):
        print("Network Input : " + str(self.rdda_entrada) + "\n"
              + "Network Output : " + str(self.rdda_salida) + "\n"
              + "Variables : " + str(self.l_variaveis_saida) + "\n"
              + "Name Variable : " + str(self.name_variable) + "\n"
              + "Acoplament Function : " + str(self.acoplament_function) + "\n"
              + "Trusth Table: " + str(self.true_table))

    def process_true_table(self):
        r_true_table = {}
        print("Generating the True Table")
        # First we must understand the coupling signal
        # we will use regular expressions to recognize the boolean formula

        # TOKENIZATION
        # Regular expression matching optional whitespace followed by a token
        # (if group 1 matches) or an error (if group 2 matches).
        TOKEN_RE = re.compile(r'\s*(?:([A-Za-z01()~∧∨→↔])|(\S))')

        # Special token indicating the end of the input string.
        TOKEN_END = '<end of input>'

        def tokenize(s):
            """Generate tokens from the string s, followed by TOKEN_END."""
            for match in TOKEN_RE.finditer(s):
                token, error = match.groups()
                if token:
                    yield token
                else:
                    raise SyntaxError("Unexpected character {!r}".format(error))
            yield TOKEN_END

        # PARSING
        Constant = namedtuple('Constant', 'value')
        Variable = namedtuple('Variable', 'name')
        UnaryOp = namedtuple('UnaryOp', 'op operand')
        BinaryOp = namedtuple('BinaryOp', 'left op right')

        # Tokens representing Boolean constants (0=False, 1=True).
        CONSTANTS = '01'

        # Tokens representing variables.
        VARIABLES = set(ascii_lowercase) | set(ascii_uppercase)

        # Map from unary operator to function implementing it.
        UNARY_OPERATORS = {
            '~': operator.not_,
        }

        # Map from binary operator to function implementing it.
        BINARY_OPERATORS = {
            '∧': operator.and_,
            '∨': operator.or_,
            '→': lambda a, b: not a or b,
            '↔': operator.eq,
        }

        def parse(s):
            """Parse s as a Boolean expression and return the parse tree."""
            tokens = tokenize(s)  # Stream of tokens.
            token = next(tokens)  # The current token.

            def error(expected):
                # Current token failed to match, so raise syntax error.
                raise SyntaxError("Expected {} but found {!r}"
                                  .format(expected, token))

            def match(valid_tokens):
                # If the current token is found in valid_tokens, consume it
                # and return True. Otherwise, return False.
                nonlocal token
                if token in valid_tokens:
                    token = next(tokens)
                    return True
                else:
                    return False

            def term():
                # Parse a <Term> starting at the current token.
                t = token
                if match(VARIABLES):
                    return Variable(name=t)
                elif match(CONSTANTS):
                    return Constant(value=(t == '1'))
                elif match('('):
                    tree = disjunction()
                    if match(')'):
                        return tree
                    else:
                        error("')'")
                else:
                    error("term")

            def unary_expr():
                # Parse a <UnaryExpr> starting at the current token.
                t = token
                if match('~'):
                    operand = unary_expr()
                    return UnaryOp(op=UNARY_OPERATORS[t], operand=operand)
                else:
                    return term()

            def binary_expr(parse_left, valid_operators, parse_right):
                # Parse a binary expression starting at the current token.
                # Call parse_left to parse the left operand; the operator must
                # be found in valid_operators; call parse_right to parse the
                # right operand.
                left = parse_left()
                t = token
                if match(valid_operators):
                    right = parse_right()
                    return BinaryOp(left=left, op=BINARY_OPERATORS[t], right=right)
                else:
                    return left

            def implication():
                # Parse an <Implication> starting at the current token.
                return binary_expr(unary_expr, '→↔', implication)

            def conjunction():
                # Parse a <Conjunction> starting at the current token.
                return binary_expr(implication, '∧', conjunction)

            def disjunction():
                # Parse a <Disjunction> starting at the current token.
                return binary_expr(conjunction, '∨', disjunction)

            tree = disjunction()
            if token != TOKEN_END:
                error("end of input")
            return tree

        def evaluate(tree, env):
            """Evaluate the expression in the parse tree in the context of an
            environment mapping variable names to their values.
            """
            if isinstance(tree, Constant):
                return tree.value
            elif isinstance(tree, Variable):
                return env[tree.name]
            elif isinstance(tree, UnaryOp):
                return tree.op(evaluate(tree.operand, env))
            elif isinstance(tree, BinaryOp):
                return tree.op(evaluate(tree.left, env), evaluate(tree.right, env))
            else:
                raise TypeError("Expected tree, found {!r}".format(type(tree)))

        # we have to create a dictionary for each variable in the output set
        l_abecedario = list(ascii_uppercase)

        dict_aux_var_saida = {}
        cont_aux_abecedario = 0
        for variable_saida in self.l_variaveis_saida:
            dict_aux_var_saida[str(variable_saida)] = l_abecedario[cont_aux_abecedario]
            cont_aux_abecedario = cont_aux_abecedario + 1

        # generate combinations of the output signal
        l_permutaciones = []
        for v_permutacion in product([True, False], repeat=len(self.l_variaveis_saida)):
            l_permutaciones.append(v_permutacion)

        # process each of the permutations we simply have to evaluate and solve
        for c_permutacion in l_permutaciones:
            aux_dictionary = dict(zip(dict_aux_var_saida.values(), c_permutacion))
            aux_acoplament_function = self.acoplament_function
            for aux_elemento in dict_aux_var_saida.keys():
                aux_acoplament_function = aux_acoplament_function.replace(str(aux_elemento),
                                                                          str(dict_aux_var_saida[aux_elemento]))
            print(aux_acoplament_function)
            print(dict_aux_var_saida)
            print(aux_dictionary)

            # Creating the key of the truth table
            aux_llave = ''
            for v_literal in c_permutacion:
                if (v_literal == True):
                    aux_llave = aux_llave + "1"
                else:
                    aux_llave = aux_llave + "0"
            if evaluate(parse(aux_acoplament_function), aux_dictionary):
                r_true_table[aux_llave] = "1"
            else:
                r_true_table[aux_llave] = "0"

        # print the tru table
        # print(r_true_table)
        # sys.exit()

        return r_true_table
