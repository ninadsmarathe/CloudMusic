import itertools
import operator

num = ["the", "day", "is", "sunny", "the", "the", "the", "sunny", "is", "is"]
#num=["aaa","aa","a"]
final_ans=[]
k = 4
unique = set(num)
unique_list = []
for i in unique:
    unique_list.append(num.count(i))
dict_ = dict(zip(unique, unique_list))
x=sorted(dict_.items(), key=operator.itemgetter(1),reverse=True)

for key,group in itertools.groupby(x,operator.itemgetter(0)):
    final_ans.append(key)
if num.count(final_ans[0])==1:
    y=sorted(final_ans)
    print(y[:k])
else:
    print(final_ans[:k])