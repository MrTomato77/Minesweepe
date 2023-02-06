import random


def random_bom(rows: int, cols: int, bom_number: int) -> list:

    mine = []

    for row in range(rows):
        row_data = []
        for col in range(cols):
            position = random.randint(0, 1)
            if position == 1 and bom_number > 0:
                row_data.append(-1)
                bom_number -= 1
            else:
                row_data.append(0)
        mine.append(row_data)

    return mine


if __name__ == "__main__":
    mine = random_bom(5, 5, 5)
    for row in mine:
        print(row)