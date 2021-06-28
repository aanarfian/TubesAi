import csv
import image_extraction as ie

for i in range(16):
    pathfile = "mateng/" +str(i+1)+ ".jpg"
    gblur = ie.process_image(pathfile)
    energy = ie.get_energy(gblur)
    entropy = ie.get_entropy(gblur)
    intensity, st_deviation = ie.get_intensity_and_st_deviation(gblur)
    smoothness = ie.get_smoothnes(st_deviation)

    with open('data_training2.csv', mode='a', newline="") as data_training:
        data_write = csv.writer(data_training, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_write.writerow([energy, entropy, st_deviation, intensity, smoothness, 'matang'])