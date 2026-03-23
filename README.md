# Pytest Experiment

This project will teach you how to write unit tests in Python using a module called Pytest

pytest is preferred over Python's builtin unittest due to simplicity, and less boilerplate

For any file that you want to test you need to create a file test_filename.py ( this test_ prefix is what pytest looks for )
This test file must have functions called test_function_name() with assert statements

What is a unit test?
Why should you write it?

Importance of unit testing : 
There are various types of tests : integration test, system test, end-to-end test
Unit test is the smallest type of test, which typically tests a very small component of code
Ensures you get the expected result from the code

Test-Driven-Development
Writing the tests first asserting expected output, and then writing the code to pass the tests
