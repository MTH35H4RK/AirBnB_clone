#!/usr/bin/python3

"""
This is a beautifully formatted code that passes pycodestyle checks.
"""


class PrettyMe:
    def __init__(self, value):
        self.value = value

    def display(self):
        print(f"Value: {self.value}")


def main():
    example_instance = PrettyMe("I am a pretty code!")
    example_instance.display()


if __name__ == "__main__":
    main()
