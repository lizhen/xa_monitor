def binary_search(key, list):
    list.sort()
    n = len(list)
    middle = (n-1)//2
    if n < 1:
        return False
    else:
        if list[middle] == key:
            return middle
        elif list[middle] > key:
            return binary_search(key, list[0:middle])
        elif list[middle] < key:
            return binary_search(key, list[middle + 1:])


def half_search(ordered_list, key, left, right):
    while left <= right:
        mid = (left + right) // 2
        if key == ordered_list[mid]:
            return mid
        elif key > ordered_list[mid]:
            left = mid + 1
        else:
            right = mid - 1
    return None


def half_search1(ordered_list, key, left, right):
    if left > right:
        return None
    mid = (left + right) // 2
    if key == ordered_list[mid]:
        return mid
    elif key > ordered_list[mid]:
        return half_search1(ordered_list, key, mid + 1, right)
    else:
        return half_search1(ordered_list, key, left, mid - 1)


def takeSecond(elem):
    return elem[1]


if __name__ == '__main__':
    key = 12
    list = [12, 1, 12, 5, 9, 12, 3, 6, 12, 7, 25, 10, 12]
    # result = binary_search(key, list)
    # print('查找的元素：', key, '序号为：', result)

    list.sort()
    print(list)
    r1 = half_search1(list, 12, 0, len(list) - 1)
    print(r1)

    random = [(2, 2), (3, 4), (4, 1), (1, 3)]
    random.sort(key=takeSecond)
    print(random)

    buildings = [['p1',493309.41,4326710.521000001,20.894000000000002]
                ,['p2',493338.018,4326720.838,20.858]
                ,['p3',493316.55700000003,4326690.102,20.871]
                ,['p4',493345.532,4326699.101,20.866999999999997]
                ,['p5',493372.38,4326708.752,20.877]
                ,['p6',493324.13200000004,4326668.561000001,20.948]
                ,['p7',493352.969,4326678.268999999,20.945999999999998]
                ,['p8',493374.049,4326685.381,20.775]
                ,['p9',493331.50899999996,4326646.762,20.939]
                ,['p10',493360.32,4326656.435,20.925]
                ,['p11',493387.263,4326665.563999999,20.823]
                ,['p12',493338.314,4326627.329,21.061999999999998]
                ,['p13',493366.97799999994,4326637.757,21.026999999999997]
                ,['p14',493250.355,4326667.298,20.753]
                ,['p15',493268.451,4326673.754,20.857]
                ,['p16',493288.08200000005,4326680.103999999,20.779]
                ,['p17',493337.407,4326307.301,17.493]
                ,['p18',493351.82399999996,4326269.362,17.516]
                ,['p19',494063.559,4326330.512,17.788]
                ,['p20',494135.05100000004,4326330.597,17.764]
                ,['p21',494103.906,4326351.731000001,21.921]
                ,['p22',494172.18799999997,4326352.055,21.991]
                ,['p23',494319.968,4326786.089,22.386]
                ,['p24',494382.981,4326818.558999999,20.589000000000002]
                ,['p25',494562.169,4326833.078,22.276]]
    buildings.sort()
    print(buildings)


