import iprs

filename = './E2_82217_STD_F327.tiff'

A = iprs.imread(filename)

iprs.imshow(A, cmap='gray')

