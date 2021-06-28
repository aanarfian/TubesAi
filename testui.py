import csv
import image_extraction as im
import naive_bayes as nb

def process_image(file):
    # Extract Feature dulu gan
    gblur = im.process_image(file)
    energy = im.get_energy(gblur)
    entropy = im.get_entropy(gblur)
    intensity, st_deviation = im.get_intensity_and_st_deviation(gblur)
    smoothness = im.get_smoothnes(st_deviation)

    # Load data training
    filename = 'data_training2.csv'
    dataset = nb.load_csv(filename)

    # convert string ke float
    for i in range(len(dataset[0])-1):
        nb.str_column_to_float(dataset, i)

    # Convert class ke int
    lookup = nb.str_column_to_int(dataset, len(dataset[0])-1)
    # fit model
    model = nb.summarize_by_class(dataset)
    # define a new record
    row = [energy, entropy, st_deviation, intensity, smoothness]

    # # predict the label
    label = nb.predict(model, row)
    # print('- Data=%s\n- Predicted: %s\n- Probabilities: %s' % (row, label[0], label[1]))
    return(row, label[0], label[1], lookup)


# for i in range(13) :
#     pathfile = "mentah/" +str(i+1)+ ".jpg"
#     # pathfile = "mateng/" +str(i+1)+ ".jpg"
#     # load image dan convert grayscale
#     img = cv2.imread(pathfile, 0)
#     # menghaluskan gambar dengan blur
#     gblur = cv2.GaussianBlur(img, (5, 5), 0)


#     m,n = gblur.shape
#     cA, (cH, cV, cD) = dwt2(gblur,'db1')
#     # a - LL, h - LH, v - HL, d - HH as in matlab
#     cHsq = [[elem * elem for elem in inner] for inner in cH]
#     cVsq = [[elem * elem for elem in inner] for inner in cV]
#     cDsq = [[elem * elem for elem in inner] for inner in cD]
#     Energy = (np.sum(cHsq) + np.sum(cVsq) + np.sum(cDsq))/(m*n)
#     print ("energy =", Energy)

#     # print ("energy =", energy)

#     # entropi
#     glcm = np.squeeze(greycomatrix(gblur, distances=[1], 
#                                 angles=[0], symmetric=True, 
#                                 normed=True))
#     entropy = -np.sum(glcm*np.log2(glcm + (glcm==0)))
#     print("entropi", entropy)

#     # deviasi & mean
#     mean, std = cv2.meanStdDev(gblur)
#     print("rerata kontras", std[0][0])
#     print("intensitas", mean[0][0])

#     # smoothness
#     R = 1 - 1/(1+std[0][0]**2)
#     print("smoothness", R)

    
#     with open('data_training1.csv', mode='a', newline="") as data_training:
#         data_write = csv.writer(data_training, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#         data_write.writerow([Energy, entropy, std[0][0], mean[0][0], R, 'mentah'])

        
# # window
# # cv2.imshow("shapes", gblur)
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()