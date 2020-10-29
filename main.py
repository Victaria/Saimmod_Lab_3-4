from Executor import Executor


def main():
    print()
    pi1 = float(input('Enter pi1: '))
    pi2 = float(input('Enter pi2: '))
    print()

    executor = Executor(pi1, pi2)
    executor.run()


if __name__ == "__main__":
    main()
