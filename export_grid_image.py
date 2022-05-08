import os
import random
from PIL import Image, ImageOps
from glob import glob

def concat_images(image_paths, size, shape=None):
    # Open images and resize them
    width, height = size
    images = map(Image.open, image_paths)
    images = [ImageOps.fit(image, size, Image.ANTIALIAS) 
              for image in images]
    
    # Create canvas for the final image with total size
    shape = shape if shape else (1, len(images))
    image_size = (width * shape[1], height * shape[0])
    image = Image.new('RGB', image_size)
    
    # Paste images into final image
    for row in range(shape[0]):
        for col in range(shape[1]):
            offset = width * col, height * row
            idx = row * shape[1] + col
            image.paste(images[idx], offset)
    
    return image



print("Available folders are:")
folders=glob("data/*")
folder_list=[folder.split("/")[1] for folder in folders]
for folder in folder_list:
    print(folder)
    
time_stamp=input("Please type the timestamp folder name:")
row=int(input("# of Grid Rows:"))
col=int(input("# of Grid Cols:"))
start_scenario=int(input("Start Scenario:"))

folder = 'data/{}/images'.format(time_stamp)
# Get list of image paths
image_array=[]
image_num=start_scenario
while image_num<start_scenario+row*col:
    image_array.append(os.path.join(folder, str(image_num)+".png"))
    image_num+=1


# Create and save image grid
image = concat_images(image_array, (554, 436), (row, col))
save_location="data/"+time_stamp+"/grid{}_{}.jpg".format(str(row),str(col))
print("Image saved at: "+ save_location)
image.save(save_location, 'JPEG')