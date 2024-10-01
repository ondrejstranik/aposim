import tifffile as tf
import numpy as np
import matplotlib.pyplot as plt
import os
import datetime as DT

base_dir = r"E:\Walter_2024\Recordings\img_Gratings_2024-08-08_14-09-05_ex300us"
base_dir = r"E:\Walter_2024\Recordings\img_Gratings_2024-08-08_14-19-32_ex1500us"
base_dir = r"E:\Walter_2024\Recordings\img_Gratings_2024-08-15_10-29-32_ex1500us"
# folder_name = 'img_both_2023-04-24_16-31-50'
# folder_name = 'img_both_2023-05-16_11-33-35'
folder_name = base_dir+r'\raw'
save_folder = base_dir+r'\SIM5'
# ###############################################################################
# ft1 = np.fft.fftshift(np.fft.fft2(image1))
# ft2 = np.fft.fftshift(np.fft.fft2(image2))
# ft3 = np.fft.fftshift(np.fft.fft2(image3))
# I0 = (ft1 + ft2 + ft3)/3.0

def I0_Ip(image1,image2,image3,I0_filename,Ip_filename):
    # wide field
    I0 = (image1/3.0 + image2/3.0+ image3/3.0)
    # ift_I0 = np.fft.ifft2(np.fft.ifftshift(I0))
    plt.title('I0_averaged')
    plt.imshow(I0, cmap='gray')
    plt.show()
    # store the image I0
    Amp=1
    # tf.imwrite(I0_filename,np.uint8(I0*Amp/257))
    tf.imwrite(I0_filename,np.uint16(I0*Amp))
    print('MaximumI0: ', np.max(I0))

    # homodyne detection
    phase1=0             
    phase2=1/3
    phase3=2/3
    weight1=1
    weight2=1
    weight3=1
    Ip_h = np.abs(weight1*image1*np.exp(2j*np.pi*phase1) + weight2*image2*np.exp(2j*np.pi*phase2) + weight3*image3*np.exp(2j*np.pi*phase3))
    # print(np.exp(2j*np.pi*phase1))
    # print(np.exp(2j*np.pi*phase2))
    # print(np.exp(2j*np.pi*phase3))
    plt.title('Ip_homodyne')
    Amp_p=10
    #plt.imshow(Ip_h*Amp_p, cmap='gray')
    #plt.show()
    # plt.clim(4, 10)
    
    tf.imwrite(Ip_filename,np.uint16(Ip_h*Amp_p))
    print('MaximumIp_h: ', np.max(Ip_h))
    print('MinimumIp_h: ', np.min(Ip_h))
    # tf.imwrite(Ip_filename,np.uint8(Ip_h*Amp_p/257))

##########################################################################################################
if not os.path.exists(save_folder):
    os.makedirs(save_folder)
# Load the three input images
# image1 = tf.imread(folder_name+'\posi_0.0.tif')
image1 = tf.imread(folder_name+'\posi0.0.tif')
image2 = tf.imread(folder_name+'\posi16.666666666666668.tif')
image3 = tf.imread(folder_name+'\posi33.333333333333336.tif')

# I0_filename = os.path.join(save_folder, folder_name+'I0_sample_0.tif')
I0_filename = save_folder+r'\I0_averaged.tif'
Ip_filename = save_folder+r'\Ip_homodyne.tif'
original_name = save_folder+r'\original.tif'

plt.title('original image')
plt.imshow(image1, cmap='gray')
plt.show()
tf.imwrite(original_name,np.uint16(image1))
# tf.imwrite(original_name,np.uint8(image1/257))

I0_Ip(image1,image2,image3,I0_filename,Ip_filename)







