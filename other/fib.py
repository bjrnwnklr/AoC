
class Fibonacci:
    def __init__(self) -> None:
        self.numbers = dict()

    def fib_n(self, n: int) -> int:
        """Generates the nth Fibonacci number. Uses memoization.

        Args:
            n (int): The nth number of the Fibonacci series to generate.

        Returns:
            int: The nth number of the Fibonacci series.
        """
        if n in self.numbers:
            return self.numbers[n]
        else:
            if n == 0:
                result = 0
            elif n == 1:
                result = 1
            elif n == 2:
                result = 1
            else:
                result = self.fib_n(n-1) + self.fib_n(n-2)

            self.numbers[n] = result
            return result


if __name__ == '__main__':

    fib = Fibonacci()
    print(fib.fib_n(1))
    print(fib.fib_n(2))
    print(fib.fib_n(10))
    print(fib.fib_n(100))
    print(fib.fib_n(50))
    print(fib.fib_n(49))
