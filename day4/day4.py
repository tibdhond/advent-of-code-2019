def main():
    i = "177777"
    count = 0
    while int(i) <= 683082:
        if i[5] == "9":
            j = 4
            while i[j] == "9":
                j -= 1
            i = "%s%s%s" % (i[:j], str(int(i[j]) + 1), "".join([str(int(i[j]) + 1) for _ in range(5-j)]))
            if int(i) > 683082:
                break
        else:
            i = i[:-1] + str(int(i[-1]) + 1)
        j = 0
        while j < 5:
            same = 1
            while j <= 4 and i[j] == i[j+1]:
                same += 1
                j += 1
            if same == 2:
                count += 1
                print(i)
                break
            j += 1
    print(count)


if __name__ == '__main__':
    main()
