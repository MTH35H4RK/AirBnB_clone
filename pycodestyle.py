#!/usr/bin/python3

"""
This module demonstrates beautifully formatted code that passes pycodestyle checks.
"""

class prettyMe:
    def __init__(self, value):
        self.value = value

    def display(self):
        print(f"Value: {self.value}")

def main():
    example_instance = prettyMe("I am a pretty code!")
    example_instance.display()

if __name__ == "__main__":
    main()