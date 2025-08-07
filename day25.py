from util import read_input
pk1,pk2 = [int(x) for x in read_input(25).splitlines()]
print(pk1)
print(pk2)

pk = 1
for loop_size in range(1, 100_000_000):
  pk = (pk * 7) % 20201227 # 7 is the subject number for the door
  if pk == pk1:
    loop_size_either = loop_size
    pk_other = pk2
    break
  if pk == pk2:
    loop_size_either = loop_size
    pk_other = pk1
    break

# compute the encryption key by using pk2 as subject number, and loop size 1
encryption_key = 1
for _ in range(loop_size_either):
  encryption_key = (encryption_key * pk_other) % 20201227
print(f"Encryption key: {encryption_key}")
assert encryption_key == 19924389, "First try!!"