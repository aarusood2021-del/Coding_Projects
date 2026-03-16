from cmput274 import *
'''
CMPUT 274
University of Alberta

A comprehensive utility module providing testing frameworks and functional data structures
for use in CMPUT 274 coursework.

===============================================================================
TESTING FRAMEWORK
===============================================================================

The module provides three types of test case functions for verifying code correctness:

1. testExact(name, expected, fn, *args)
   - Tests functions that should return exact values (integers, strings, lists, etc.)
   - Compares actual vs expected using exact equality (==)
   - Best for non-float comparisons

2. testWithin(name, expected, error_margin, fn, *args)
   - Tests functions that return floating-point values
   - Verifies result falls within [expected - error_margin, expected + error_margin]
   - Essential for dealing with floating-point precision issues

3. testPrint(name, expected_output, fn, *args)
   - Tests functions that print to stdout rather than returning values
   - Captures printed output and compares to expected string
   - Useful for testing display/printing functions

4. runTests()
   - Executes all registered test cases and displays results
   - Call this after defining all your test cases

Example Usage:
    def add(a, b):
        return a + b
    
    testExact("addition_test", 5, add, 2, 3)     # Registers test
    runTests()                                    # Runs and shows results

===============================================================================
LINKED LIST ABSTRACT DATA TYPE (ADT)
===============================================================================

The module implements a functional linked list ADT called "LList". This data structure
follows strict functional programming principles - once created, lists cannot be
modified, only used to create new lists.

LList Definition:
    An LList is either:
    - empty (represents an empty list)
    - cons(element, LList) (represents a non-empty list with first element 'element'
                            and remaining elements as another LList)

Textual Representation:
    (a1, a2, a3, ..., an) represents cons(a1, cons(a2, ...cons(an, empty())))

Core Operations:
    - empty() -> LList
        Creates an empty LList
        
    - cons(element, llist) -> LList
        Creates a new LList by prepending element to existing llist
        
    - first(llist) -> element
        Returns the first element of a non-empty LList
        
    - rest(llist) -> LList
        Returns a new LList containing all elements except the first
        
    - isEmpty(llist) -> bool
        Returns True if the LList is empty, False otherwise
        
    - second(llist), third(llist), fourth(llist), fifth(llist)
        Convenience functions to access deeper elements
        
    - LL(*args) -> LList
        Convenience constructor: LL(1, 2, 3) creates (1, 2, 3)

Higher-Order Functions:
    - foldr(llist, fn, base) -> value
        Right-associative fold/reduce over the list
        Example: foldr(LL(1,2,3), lambda x, y: x + y, 0) -> 6
        
    - foldl(llist, fn, acc) -> value
        Left-associative fold/reduce over the list
        
    - map(f, llist) -> LList
        Applies function f to each element, returns new LList
        Example: map(lambda x: x*2, LL(1,2,3)) -> (2,4,6)
        
    - filter(f, llist) -> LList
        Returns new LList containing only elements where f(element) is True
        Example: filter(lambda x: x%2==0, LL(1,2,3,4)) -> (2,4)
        
    - buildList(f, n) -> LList
        Creates LList by applying f to numbers 0 through n-1
        Example: buildList(lambda x: x**2, 4) -> (0,1,4,9)

Implementation Notes:
    - The LList implementation uses trampolining for recursion optimization
    - All list operations are non-destructive (functional style)
    - The ADT can only be manipulated through these provided functions
    - Direct manipulation of internal representation invalidates the ADT

===============================================================================
AUTHOR: CMPUT 274 Course Staff
DATE: Fall 2024
'''

def strToTokenList(s):
  '''
  strToTokenList takes a string that represents a valid fimpl program
                 and returns the sequential LList of tokens that
                 appear in that program.

  s       - str
  returns - LList of str

  Examples:
    strToTokenList("mul add -3 5 sub 1 -4 ")
        -> LL("mul", "add", "-3", "5", "sub", "1", "-4")
    strToTokenList("add      -2\n\n   \t4")
        -> LL("add", "-2", "4")
  '''
  def stringwordFinder(x, accum):
    '''
    The stringwordFinder function fits in the foldr function defined below by the variable: words. It takes two
    parameters: x, which is supplied by string and accum, which stores the value of x to an empty
    LList.

    x - A defined word
    accum - A constructed LList
    Returns - accum
    '''
    if x == ' ' or x == '\t' or x == '\n':
      if isEmpty(accum) or isEmpty(first(accum)):
        return accum
      return cons(empty(), accum)
    else:
      if isEmpty(accum):
        return cons(LL(x), accum)
      return cons(cons(x, first(accum)), rest(accum))

  words = filter(lambda e: not isEmpty(e), foldr(s, stringwordFinder, empty()))
  stringwords = foldr(words, lambda w, acc: cons(foldr(w, lambda chars, word: chars + word, ""), acc), empty())
  return stringwords

def isIdentifier(s):
  '''
  isIdentifier returns True if the given string is a valid fimpl
               identifier, False otherwise.

  s       - str
  returns - bool

  Examples:
    isIdentifier("foo") -> True
    isIdentifier("Foo") -> False
    isIdentifier("add") -> False
    isIdentifier("xDIM") -> True
  '''
  
  LList = foldr(s, lambda a,b: cons(a,b), empty())
  if 65 <= ord(first(LList)) <= 90:
    return False
  elif s == 'add' or s == 'sub' or s == 'mul' or s == 'div':
    return False
  else:
    boolIdentifier = map(lambda a: True if (97 <= ord(a) <= 122 or 65 <= ord(a) <= 90) else False, s)
    identifier = foldr(boolIdentifier, lambda x, y: False if x == False else y, True)
    return identifier

'''
An ExprTree is one of:
 - LL("ident", str)
 - LL("intLit", int)
 - LL("binOp", Operator, ExprTree, ExprTree)

An Operator is one of:
 - "add"
 - "mul"
 - "div"
 - "sub"
'''

def tokensToExprTree(tokens):
  '''
  tokensToExprTree parses the first complete expression in the LList of tokens
                   into an ExprTree and returns a pair of the form
                   LL(ExprTree, LList) where the first item is the ExprTree
                   that represents the given expression, and the second item
                   is the parameter tokens but without any of the tokens that
                   were used to construct this expression

  tokens  - A LList of str
  returns - A LL(ExprTree, LList of Str)

  Examples:
    tokensToExprTree(LL("add", "-2", "4"))
      -> (('binOp',
           'add',
           ('intLit', -2),
           ('intLit', 4)),
         ())
    tokensToExprTree(LL("x", "5", "add", "3", "y"))
      -> (("ident", "x"),
          ("5", "add", "3", "y"))
    tokensToExprTree(LL("add", "x", "add", "5", "3", "mul", "10", "2"))
      -> (('binOp', 
           'add',
            ('ident', 'x'),
            ('binOp', 'add',
              ('intLit', 5),
              ('intLit', 3)
            )
          )
          ("mul", "10", "2")
         )
  '''
  binaryOperator = LL("add", "mul", "div", "sub")

  def strToInt(tokens):
    '''
    strToInt takes in one parameter: tokens, which is guaranteed to be a string and returns an 
    integer associated with that value.

    tokens - a string
    returns - an integer

    Examples:
    strToInt("100001") -> 100001
    strToInt("60854") -> 60854
    strToInt("10001000") -> 10001000
    '''
    if tokens == "":
        return 0
    if tokens[0] == "-":
        return -1 * strToInt(tokens[1:])  
    if len(tokens) == 1:
        return ord(tokens[0]) - ord("0")
    last = ord(tokens[-1]) - ord("0")
    return last + 10 * strToInt(tokens[0:-1])

  def isIntegerStr(tokens):
    '''
    The function isIntegerStr takes in one parameter: tokens and returns True if tokens is a 
    valid integer otherwise False.

    tokens - a string
    returns - a boolean value

    Examples:
    isIntegerStr("-456") -> True
    isIntegerStr("--456") -> False
    '''
    if tokens == "":
        return False
    if tokens[0] == "-" and len(tokens) > 1:
        tokens = tokens[1:]
    return foldr(tokens, lambda ch, acc: ('0' <= ch <= '9') and acc, True)

  def consume(tokens):
    """
    The consume function return the remaining tokens after consuming exactly one
    complete prefix expression starting at the first token.

    tokens - a LList
    returns - a new LList

    Examples:
    consume(LL("add", "x", "add", "5", "3", "mul", "10", "2")) -> ("mul", "10", "2")
    consume(LL("add", "-2", "4")) -> ()
    """
    if isEmpty(tokens):
        return empty()
    tok = first(tokens)
    if foldr(binaryOperator, lambda op, acc: (op == tok) or acc, False):
        rem1 = rest(tokens)
        rem2 = consume(rem1)
        rem3 = consume(rem2)
        return rem3
    if isIntegerStr(tok):  
        return rest(tokens)
    if isIdentifier(tok):
        return rest(tokens)
    return rest(tokens)

  def treeFunction(tokens):
    '''
    The treeFunction takes in one parameter: tokens and parses exactly one complete prefix 
    expression from the front of the given token list and return both the expression tree 
    for that expression, and the remaining tokens after that expression.

    tokens - a LList
    returns - a new LList

    Examples:
    tokens = LL("5") 
    treeFunction(tokens) -> cons( ('intLit', 5), cons(empty(), empty()))
    tokens = LL("x", "10")
    treeFunction(tokens) -> cons( ('ident', "x"), cons(LL("10"), empty()))
    ''' 
    def formFunction(tokens):
      '''
      The function formFunction takes in a single parameter tokens and parses the simplest possible 
      expression starting at the beginning of the token list. This function attempts to classify the 
      first token as either an integer literal, an identifier, or the beginning of a binary operator expression

      tokens - a LList
      returns - a new constructed LList

      Examples:
      tokens = LL("-13", "mul", "2", "3")
      formFunction(tokens) -> ('intLit', -13)
      tokens = LL("foo", "10")
      formFunction(tokens) -> ('ident', "foo")
      '''
      if isEmpty(tokens):
        return empty()
      isNumber = foldr(first(tokens), lambda a,b: cons(a,b), empty())
      mapisNumber = map(lambda a: True if 0 <= ord(a)-ord('0') <= 9 else False, (lambda isNumber: rest(isNumber) if len(isNumber) >= 2 else isNumber)(isNumber))
      ifNumber = foldr(mapisNumber, lambda x, y: x == False or y, True)
      if (first(isNumber) == '-' or 0 <= ord(first(isNumber))-ord('0') <= 9) and ifNumber == True:
        form = cons('intLit', cons(strToInt(first(tokens)), empty()))
        return form
      if isIdentifier(first(tokens)) == True:
        form = cons('ident', cons(first(tokens), empty()))
        return form
      else:
        return treeFunction(tokens)
    if isEmpty(tokens):
      return empty()
    if foldr(binaryOperator, lambda x, y: x == first(tokens) or y, False):
      op = first(tokens)
      leftTree = formFunction(rest(tokens))
      rem_after_left = consume(rest(tokens))
      rightTree = formFunction(rem_after_left)
      treeForm = cons('binOp',
                  cons(op,
                  cons(leftTree,
                  cons(rightTree,
                      empty()))))
      return treeForm
    else:
      treeForm = cons(formFunction(tokens), cons(rest(tokens), empty()))
      return treeForm
  return (lambda tokens: treeFunction(tokens) if not foldr(binaryOperator, lambda x, y: x == first(tokens) or y, False) else cons(treeFunction(tokens), cons(consume(tokens), empty())))(tokens)

def lookup(key, pairs):
  '''
  lookup returns the value associated with the given key in the
         LList of pairs. May assume the key exists in the LList
         of pairs

  key     - X
  pairs   - LList of LL(X, Y)
  returns - Y

  Examples:
    lookup("x", LL(LL("x", 5), LL("y", 10))) -> 5
    lookup("y", LL(LL("x", 5), LL("y", 10))) -> 10
  '''
  return foldr(pairs, lambda a,b: second(a) if key == first(a) else b, empty())

def evalExpr(eTree, defns):
  '''
  evalExpr returns the result of evaluating the given ExprTree eTree given
           the provided identifier definitions in the LList of pairs defns

  eTree   - an ExprTree
  defns   - a LList of LL(str, int)
  returns - int

  Examples:
    evalExpr(first(tokensToExprTree(strToTokenList("mul add -3 5 sub 1 -4 "))),
            LL()) -> 10

    evalExpr(first(tokensToExprTree(strToTokenList("add x 3"))),
            LL(LL("x", 2))) -> 5

    evalExpr(first(tokensToExprTree(strToTokenList("add x 3"))),
            LL(LL("x", -25))) -> -22
  '''
  if eTree == empty():
    leftSide = empty()
    return leftSide
  if first(eTree) == 'ident':
    leftSide = lookup(second(eTree), defns)
    return leftSide
  if first(eTree) == 'intLit':
    leftSide = second(eTree)
    return leftSide
  if first(eTree) == 'binOp':
    if second(eTree) == 'add':
        return evalExpr(third(eTree), defns) + evalExpr(first(rest(rest(rest((eTree))))), defns)
    elif second(eTree) == 'mul':
        return evalExpr(third(eTree), defns) * evalExpr(first(rest(rest(rest((eTree))))), defns)
    elif second(eTree) == 'div':
        return evalExpr(third(eTree), defns) // evalExpr(first(rest(rest(rest((eTree))))), defns)
    else:
        return evalExpr(third(eTree), defns) - evalExpr(first(rest(rest(rest((eTree))))), defns)

def main():
  testExact("tList1", LL("mul", "add", "-3", "5", "sub", "1", "-4"),
            strToTokenList, "mul add -3 5 sub 1 -4 ")
  testExact("tList2", LL("add", "-2", "4"),
            strToTokenList, "add      -2\n\n   \t4")

  testExact("isID1", True, isIdentifier, "foo")
  testExact("isID2", False, isIdentifier, "Foo")
  testExact("isID3", False, isIdentifier, "add")
  testExact("isID4", True, isIdentifier, "xDIM")

  testExact("exprTree1", 
            LL(LL('binOp',
                  'add',
                  LL('intLit', -2),
                  LL('intLit', 4)),
              LL()), 
            tokensToExprTree, 
            LL("add", "-2", "4"))

  testExact("exprTree2",
            LL(LL('binOp',
                  'add',
                  LL('ident', 'x'),
                  LL('binOp', 'add',
                     LL('intLit', 5),
                     LL('intLit', 3))),
                LL("mul", "10", "2")),
            tokensToExprTree,
            LL("add", "x", "add", "5", "3", "mul", "10", "2"))

  testExact("lookup1", 5, lookup, "x", LL(LL("a", 3), LL("x", 5)))

  
  fimplProg1 = "mul add -3 5 sub 1 -4 "
  genTree = lambda prog: first(tokensToExprTree(strToTokenList(prog)))
  testExact("eval1", 10, evalExpr,
            genTree(fimplProg1), empty())
  fimplProg2 = "add x 3"
  defns1 = LL(LL("x", 2))
  testExact("eval2", 5, evalExpr, 
            genTree(fimplProg2), defns1)

  defns2 = LL(LL("x", -25))
  testExact("eval2", -22, evalExpr, 
            genTree(fimplProg2), defns2)

  testExact("strToTokenList_basic",
      LL("mul", "add", "-3", "5", "sub", "1", "-4"),
      strToTokenList,
      "mul add -3 5 sub 1 -4 "
  )

  testExact("strToTokenList_mixed_whitespace",
      LL("add", "-2", "4"),
      strToTokenList,
      "   add   -2\n\n \t4"
  )

  testExact("strToTokenList_only_whitespace",
      empty(),
      strToTokenList,
      "   \n\t   "
  )

  testExact("strToTokenList_single_token_newline",
      LL("x"),
      strToTokenList,
      "x\n"
  )

  testExact("isIdentifier_simple_valid", True,  isIdentifier, "foo")
  testExact("isIdentifier_leading_upper", False, isIdentifier, "Foo")
  testExact("isIdentifier_keyword_add",   False, isIdentifier, "add")
  testExact("isIdentifier_mixed_case",    True,  isIdentifier, "xDIM")
  testExact("isIdentifier_contains_digit", False, isIdentifier, "a1")
  testExact("isIdentifier_contains_underscore", False, isIdentifier, "a_b")
  testExact("isIdentifier_keyword_prefix1", True,  isIdentifier, "addx")
  testExact("isIdentifier_keyword_prefix2", True,  isIdentifier, "divv")

  testExact("tokensToExprTree_int_literal",
      LL(LL("intLit", 0), empty()),
      tokensToExprTree,
      LL("0")
  )

  testExact("tokensToExprTree_negative_int",
      LL(LL("intLit", -12345), empty()),
      tokensToExprTree,
      LL("-12345")
  )

  testExact("tokensToExprTree_ident_with_remainder",
      LL(LL("ident", "x"), LL("5")),
      tokensToExprTree,
      LL("x", "5")
  )

  testExact("tokensToExprTree_simple_add",
      LL(
          LL("binOp", "add",
              LL("intLit", -2),
              LL("intLit", 4)
          ),
          empty()
      ),
      tokensToExprTree,
      LL("add", "-2", "4")
  )

  testExact("tokensToExprTree_nested_add_with_remainder",
      LL(
          LL("binOp", "add",
              LL("ident", "x"),
              LL("binOp", "add",
                  LL("intLit", 5),
                  LL("intLit", 3)
              )
          ),
          LL("mul", "10", "2")
      ),
      tokensToExprTree,
      LL("add", "x", "add", "5", "3", "mul", "10", "2")
  )

  testExact("tokensToExprTree_deep_left_operand",
      LL(
          LL("binOp", "add",
              LL("binOp", "add",
                  LL("intLit", 1),
                  LL("intLit", 2)
              ),
              LL("intLit", 3)
          ),
          LL("4")
      ),
      tokensToExprTree,
      LL("add", "add", "1", "2", "3", "4")
  )

  testExact("tokensToExprTree_big_example_full",
      LL(
          LL("binOp", "mul",
              LL("binOp", "add",
                  LL("intLit", -3),
                  LL("intLit", 5)
              ),
              LL("binOp", "sub",
                  LL("intLit", 1),
                  LL("ident", "foo")
              )
          ),
          empty()
      ),
      tokensToExprTree,
      LL("mul", "add", "-3", "5", "sub", "1", "foo")
  )

  env = LL(LL("x", 5), LL("y", 7), LL("z", -3))

  testExact("lookup_first",  5, lookup, "x", env)
  testExact("lookup_middle", 7, lookup, "y", env)
  testExact("lookup_last",  -3, lookup, "z", env)

  env_dup = LL(LL("x", 1), LL("x", 999), LL("y", 50))
  testExact("lookup_duplicate_uses_first", 1, lookup, "x", env_dup)

  expr_spec_mul_add_sub = LL("binOp", "mul",
      LL("binOp", "add",
          LL("intLit", -3),
          LL("intLit", 5)
      ),
      LL("binOp", "sub",
          LL("intLit", 1),
          LL("intLit", -4)
      )
  )

  testExact("evalExpr_spec_mul_add_sub",
      10,
      evalExpr,
      expr_spec_mul_add_sub,
      empty()
  )

  expr_add_x_3 = LL("binOp", "add",
      LL("ident", "x"),
      LL("intLit", 3)
  )

  testExact("evalExpr_add_x_3_x_2",
      5,
      evalExpr,
      expr_add_x_3,
      LL(LL("x", 2))
  )

  testExact("evalExpr_add_x_3_x_minus25",
      -22,
      evalExpr,
      expr_add_x_3,
      LL(LL("x", -25))
  )

  expr_mixed = LL("binOp", "add",
      LL("binOp", "mul",
          LL("intLit", 2),
          LL("ident", "x")
      ),
      LL("binOp", "sub",
          LL("ident", "y"),
          LL("intLit", 3)
      )
  )

  testExact("evalExpr_mixed_ops_and_idents",
      6,
      evalExpr,
      expr_mixed,
      LL(LL("x", 5), LL("y", -1))
  )

  expr_10_20 = LL("binOp", "add",
      LL("intLit", 10),
      LL("intLit", 20)
  )
  env_noise = LL(LL("x", 999), LL("y", -999))

  testExact("evalExpr_ignores_unused_env",
      30,
      evalExpr,
      expr_10_20,
      env_noise
  )

  expr_add_x_0 = LL("binOp", "add",
      LL("ident", "x"),
      LL("intLit", 0)
  )
  env_dup2 = LL(LL("x", 1), LL("x", 999))

  testExact("evalExpr_duplicate_bindings_first_wins",
      1,
      evalExpr,
      expr_add_x_0,
      env_dup2
  )

  expr_negdiv = LL("binOp", "div",
      LL("intLit", -7),
      LL("intLit", 2)
  )

  testExact("evalExpr_negative_division",
      -4,
      evalExpr,
      expr_negdiv,
      empty()
  )

  expr_deep = LL("binOp", "mul",
      LL("binOp", "add",
          LL("binOp", "add",
              LL("intLit", 1),
              LL("intLit", 2)
          ),
          LL("intLit", 3)
      ),
      LL("binOp", "sub",
          LL("intLit", 10),
          LL("binOp", "div",
              LL("intLit", 9),
              LL("intLit", 2)
          )
      )
  )

  testExact("evalExpr_deep_nested_expression",
      36,
      evalExpr,
      expr_deep,
      empty()
  )

  expr_nested_ident = LL("binOp", "mul",
      LL("binOp", "add",
          LL("ident", "x"),
          LL("intLit", 5)
      ),
      LL("binOp", "sub",
          LL("intLit", 10),
          LL("ident", "x")
      )
  )

  testExact("evalExpr_nested_ident_use",
      54,
      evalExpr,
      expr_nested_ident,
      LL(LL("x", 4))
  )

  runTests()

if __name__ == "__main__":
  main()
