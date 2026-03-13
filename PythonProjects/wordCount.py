from cmput274 import *
'''
CMPUT 274 - Introductory Numerical Mathematics and Computing
University of Alberta

A comprehensive utility module providing testing frameworks and functional data structures
for use in CMPUT 274 coursework.

DISCLAIMER: This module contains advanced programming concepts for educational purposes.
Students may ONLY use concepts that have been explicitly covered in class lectures.

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

def wordCounts(string):
  '''
  The wordCounts function takes in a single string paramter representing words and white space characters
  and takes the words only and counts the number of occurences of each word and returns a LList containing
  a pair of a word and its occurence for each of the words.

  string - A string
  Returns - A LList

  Examples:
  wordCounts("abc     def") -> LL(LL("abc",1), LL("def",1))
  wordCounts("   hello") -> LL(LL("hello", 1))
  '''
  def wordFinder(x, accum):
    '''
    The word_Finder function fits in the foldr function defined below by the variable: words. It takes two
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

  words = foldr(string, wordFinder, empty())
  words = filter(lambda e: not isEmpty(e), words)
  stringwords = foldr(words, lambda w, acc: cons(foldr(w, lambda chars, word: chars + word, ""), acc), empty())
  condition = lambda word,accumulator: accumulator if foldr(accumulator, lambda x, y: x == word or y, False) else cons(word, accumulator)
  reverse_order = foldl(stringwords, condition, empty())
  nonduplicate = foldl(reverse_order, lambda x,y: cons(x, y), empty())
  result = foldr(nonduplicate, lambda a,b: cons(LL(a, foldr(filter(lambda j: j == a, stringwords), lambda c,d: d+1, 0)), b) , empty())
  return result


def main():
  testExact("basic1", LL(LL("cook", 3), LL("the", 2), LL("not", 1)), wordCounts, "cook the cook not the cook")
  testExact("basic2", LL(LL("also", 1),
                         LL("don't.", 1),
                         LL("Also", 1),
                         LL("don't", 1)), wordCounts, "also don't.\n\nAlso   don't")
  testExact("basic3", LL(LL("abc",1), LL("def",1)), wordCounts, "abc     def")
  testExact("basic4", LL(LL("hello", 1)), wordCounts, "   hello")

  runTests()


if __name__ == "__main__":
  main()