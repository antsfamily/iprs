# -*- coding: utf-8 -*-


import os
import struct

fp = open('test.bin','wb')

# 按照上面的格式将数据写入文件中
# 这里如果string类型的话，在pack函数中就需要encode('utf-8')
name = b'lily'
age = [18, 20]
sex = b'female'
job = b'teacher'

# int类型占4个字节
fp.write(struct.pack('4s2i6s7s', name,age[0],age[1], sex, job))
fp.flush()
fp.close()

# 将文件中写入的数据按照格式读取出来
fd = open('test.bin','rb')
# 21 = 4 + 4 + 6 + 7
print(struct.unpack('4s2i6s7s',fd.read(25)))
fd.close()
