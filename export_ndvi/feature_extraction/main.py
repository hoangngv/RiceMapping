from utilize import *
import glob
import os

s2 = '..\\s2'

list_s2 = glob.glob(s2 + "\\*.tif")

train_notrice_index = "..\\index\\train-nonrice.csv"
train_rice_index = "..\\index\\train-rice.csv"
test_notrice_index = "..\\index\\test-nonrice.csv"
test_rice_index = "..\\index\\test-rice.csv"

dir_csv = '..\\csv_data\\'

s2_nonrice = ExtractTiffFromPoint(list_s2, train_notrice_index, dir_csv + "s2_train-nonrice.csv")
s2_rice = ExtractTiffFromPoint(list_s2, train_rice_index, dir_csv + "s2_train-rice.csv")
test_s2_nonrice = ExtractTiffFromPoint(list_s2, test_notrice_index, dir_csv + "s2_testNonRice.csv")
test_s2_rice = ExtractTiffFromPoint(list_s2, test_rice_index, dir_csv + "s2_testRice.csv")


