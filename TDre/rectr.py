
#!/usr/bin/python
#! -*- encoding: utf-8 -*-
# openmvg使用示例
# usage : python tutorial_demo.py
 
import os
import subprocess
import sys
 
# openmvg编译bin目录(可cp -p到/usr/local/bin/)
OPENMVG_SFM_BIN = "/root/code/openMVG_Build/Linux-x86_64-RELEASE"
# pmvs编译bin目录(可cp -p到/usr/local/bin/)
PMVS_BIN = "/root/code/CMVS-PMVS/build/main"
# openmvg相机参数目录
CAMERA_SENSOR_WIDTH_DIRECTORY = "/root/code/openMVG/src/openMVG/exif/sensor_width_database"
 
 
# 0. 下载测试照片
os.chdir(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.abspath("./building")
#data_dir = os.path.abspath("./ImageDataset_SceauxCastle")
'''if not os.path.exists(data_dir):
  pImageDataCheckout = subprocess.Popen([ "git", "clone", "https://github.com/openMVG/ImageDataset_SceauxCastle.git" ])
  pImageDataCheckout.wait()'''
input_dir = os.path.join(data_dir, "images")
output_dir = data_dir
print ("Using input dir  : ", input_dir)
print ("      output_dir : ", output_dir)
matches_dir = os.path.join(output_dir, "matches")
camera_file_params = os.path.join(CAMERA_SENSOR_WIDTH_DIRECTORY, "sensor_width_camera_database.txt")    #相机参数
if not os.path.exists(matches_dir):
  os.mkdir(matches_dir)
 
# 1. 从图片数据集中生成场景描述文件sfm_data.json
print ("----------1. Intrinsics analysis----------")
pIntrisics = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_SfMInit_ImageListing"),  "-i", input_dir, "-o", matches_dir, "-d", camera_file_params, "-c", "3"] )
#*注：如果产出的sfm_data.json里intrinsics内容为空，通常是在图片没有exif信息导致获取不到相机焦距、ccd尺寸等参数，用带exif的原图即可。
pIntrisics.wait()
 
# 2. 计算图像特征
print ("----------2. Compute features----------")
pFeatures = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeFeatures"),  "-i", matches_dir+"/sfm_data.json", "-o", matches_dir, "-m", "SIFT", "-f" , "1"] )
pFeatures.wait()
 
# 3. 计算几何匹配
print ("----------3. Compute matches----------")
pMatches = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeMatches"),  "-i", matches_dir+"/sfm_data.json", "-o", matches_dir, "-f", "1", "-n", "ANNL2"] )
pMatches.wait()
 
# 4. 执行增量三维重建
reconstruction_dir = os.path.join(output_dir,"reconstruction_sequential")
print ("----------4. Do Incremental/Sequential reconstruction----------") #set manually the initial pair to avoid the prompt question
pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_IncrementalSfM"),  "-i", matches_dir+"/sfm_data.json", "-m", matches_dir, "-o", reconstruction_dir] )
pRecons.wait()
 
# 5. 计算场景结构颜色
print ("----------5. Colorize Structure----------")
pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeSfM_DataColor"),  "-i", reconstruction_dir+"/sfm_data.bin", "-o", os.path.join(reconstruction_dir,"colorized.ply")] )
pRecons.wait()
 
# 6. 测量稳健三角
print ("----------6. Structure from Known Poses (robust triangulation)----------")
pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeStructureFromKnownPoses"),  "-i", reconstruction_dir+"/sfm_data.bin", "-m", matches_dir, "-o", os.path.join(reconstruction_dir,"robust.ply")] )
pRecons.wait()
 
'''
# 使用全局SfM管道重建Reconstruction for the global SfM pipeline
# 3.1 全局sfm管道几何匹配
print ("----------3.1. Compute matches (for the global SfM Pipeline)----------")
pMatches = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeMatches"),  "-i", matches_dir+"/sfm_data.json", "-o", matches_dir, "-r", "0.8", "-g", "e"] )
pMatches.wait()
# 4.1 执行全局三维重建
reconstruction_dir = os.path.join(output_dir,"reconstruction_global")
print ("----------4.1. Do Global reconstruction----------")
pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_GlobalSfM"),  "-i", matches_dir+"/sfm_data.json", "-m", matches_dir, "-o", reconstruction_dir] )
pRecons.wait()
# 5.1 计算场景结构颜色
print ("----------5.1. Colorize Structure----------")
pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeSfM_DataColor"),  "-i", reconstruction_dir+"/sfm_data.bin", "-o", os.path.join(reconstruction_dir,"colorized.ply")] )
pRecons.wait()
# 6.1 测量稳健三角
print ("----------6.1. Structure from Known Poses (robust triangulation)----------")
pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeStructureFromKnownPoses"),  "-i", reconstruction_dir+"/sfm_data.bin", "-m", matches_dir, "-o", os.path.join(reconstruction_dir,"robust.ply")] )
pRecons.wait()
'''
 
# 7. 把openMVG生成的SfM_Data转为适用于PMVS输入格式的文件
print ("----------7. Export to PMVS/CMVS----------")
pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_openMVG2PMVS"),  "-i", reconstruction_dir+"/sfm_data.bin", "-o", reconstruction_dir] )
pRecons.wait()
#*注：执行后会在-o路径下生成一个PMVS目录，包含 models, txt, visualize 三个子目录：models为空；txt包含对应图像的txt文档，每个里面都是一个3x4的矩阵，大概是相机位姿；visualize包含11张图像，不确定是原图像还是校正过的图像
 
# 8. 使用PMVS重建稠密点云、表面、纹理
print ("----------8. pmvs2----------")
pRecons = subprocess.Popen( [os.path.join(PMVS_BIN, "pmvs2"),  reconstruction_dir+"/PMVS/", "pmvs_options.txt"] )  # 注：不要修改pmvs_options.txt文件名
pRecons.wait()
#*注：执行后会在./PMVS/models文件夹中生成一个pmvs_options.txt.ply点云文件，用meshlab打开即可看到重建出来的彩色稠密点云。
 

