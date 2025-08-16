from life import Board

if __name__ == "__main__":
    board = Board(6, 6)

    # Test 1: dead cells stay dead
    init = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
    board.state = init
    next_state = board.next_state()
    if next_state == init:
        print("TEST 1 PASSED")
    else:
        print("TEST 1 FAILED")
        print(f"{init=}")
        print(f"{next_state=}")

    # Test 2: alive cells die from overcrowd with corners alive
    init = [
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 1]
    ]
    final = [
        [1, 0, 0, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [1, 0, 0, 1]
    ]
    board.state = init
    next_state = board.next_state()
    if next_state == final:
        print("TEST 2 PASSED")
    else:
        print("TEST 2 FAILED")
        print(f"{init=}")
        print(f"{next_state=}")

    # Test 3: single alive cell  and cell with 1 neighbour dies
    init = [
        [0, 0, 0, 1],
        [0, 0, 0, 0],
        [1, 1, 0, 0],
        [0, 0, 0, 0]
    ]
    final = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
    board.state = init
    next_state = board.next_state()
    if next_state == final:
        print("TEST 3 PASSED")
    else:
        print("TEST 3 FAILED")
        print(f"{init=}")
        print(f"{next_state=}")

    # Test 4: alive cell with 2 neighbours stay alive and dead cell with 3 becomes alive
    init = [
        [0, 0, 1, 0],
        [0, 1, 0, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
    final = [
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
    board.state = init
    next_state = board.next_state()
    if next_state == final:
        print("TEST 4 PASSED")
    else:
        print("TEST 4 FAILED")
        print(f"{init=}")
        print(f"{next_state=}")

    # Test 5: alive cell with 4 neighbours die
    init = [
        [0, 0, 1, 0],
        [0, 1, 1, 1],
        [0, 0, 1, 0],
        [0, 0, 0, 0]
    ]
    final = [
        [0, 1, 1, 1],
        [0, 1, 0, 1],
        [0, 1, 1, 1],
        [0, 0, 0, 0]
    ]
    board.state = init
    next_state = board.next_state()
    if next_state == final:
        print("TEST 5 PASSED")
    else:
        print("TEST 5 FAILED")
        print(f"{init=}")
        print(f"{next_state=}")