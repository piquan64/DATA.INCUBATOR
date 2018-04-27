#!/usr/bin/env Rscript

data.dir = "/rsgrps/laurameredith/data/LEO_iTag/water/plate1/Raw_Data/"

for (file in list.files(data.dir)) {
  print(file)
}
