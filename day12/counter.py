# i = 0
# end = 277068010964808
# limit = 10
# length = 2
# inc = 10
# while i < end:
#     while i < limit:
#         i += 1
#     print(i)
#
#     next_limit = limit + inc
#     limit = next_limit if next_limit < end else end
#     if len(str(limit)) > length:
#         length += 1
#         inc *= 10

i = 0
while i < 10000000:
    i += 1

print(i)
