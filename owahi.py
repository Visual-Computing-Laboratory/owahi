#!/usr/bin/env python3
import sys
import getopt
import cv2 as cv
import numpy as np
import psutil
from datetime import datetime

class bcolors:
		HEADER = '\033[95m'
		OKBLUE = '\033[94m'
		OKCYAN = '\033[96m'
		OKGREEN = '\033[92m'
		WARNING = '\033[93m'
		FAIL = '\033[91m'
		ENDC = '\033[0m'
		BOLD = '\033[1m'
		UNDERLINE = '\033[4m'


def IsCudaOpenCV():
	if cv.cuda.getCudaEnabledDeviceCount() > 0:
		return(cv.__version__ + " dikompilasi mendukung CUDA.")
	else:
		return(cv.__version__)

def PrintTimestamp(dt):
	return("{day:02d}/{month:02d}/{year:d} {hour:02d}:{minute:02d}:{second:02d}.{micro:06d} {tz}".format(day=dt.day,month=dt.month,year=dt.year,hour=dt.hour,minute=dt.minute,second=dt.second,micro=dt.microsecond,tz=dt.astimezone().tzname())) 

#	str(dt.day) + "/" + str(dt.month) + "/" + str(dt.year) + " " + str(dt.hour) + ":" + str(dt.minute) + ":" + str(dt.second) + "." + str(dt.microsecond) + " " + dt.astimezone().tzname()) 

def PrintErrorMsg():
	print(f"{bcolors.BOLD}NAMA{bcolors.ENDC}")
	print(f"\t{bcolors.BOLD}owahi.py{bcolors.ENDC} -- aplikasi konversi resolusi dan frame-rate gambar bergerak\n")
	print(f"{bcolors.BOLD}PENGGUNAAN{bcolors.ENDC}")
	print(f"\towahi.py <{bcolors.BOLD}file-masukan{bcolors.ENDC}> <{bcolors.BOLD}file-keluaran{bcolors.ENDC}> <{bcolors.BOLD}resolusi{bcolors.ENDC}> <{bcolors.BOLD}frame-rate{bcolors.ENDC}>\n")
	print(f"{bcolors.BOLD}DESKRIPSI{bcolors.ENDC}")
	print(f"\t<{bcolors.BOLD}file-masukan{bcolors.ENDC}> nama file (lengkap dengan path) moving images yang akan")
	print(f"\t dilakukan konversi.")
	print(f"\t<{bcolors.BOLD}file-keluaran{bcolors.ENDC}> nama file (lengkap dengan path) moving images hasil")
	print(f"\t konversi. Video container format akan disesuaikan dengan extention file")
	print(f"\t yang digunakan (.avi, .mp4, atau .ogg). Perhatian: jika nama file yang")
	print(f"\t digunakan sudah ada, akan ditimpa tanpa peringatan.")
	print(f"\t<{bcolors.BOLD}resolusi{bcolors.ENDC}> kode resolusi standar videoIn untuk moving images keluaran:")
	print(f"\t - {bcolors.BOLD}240p{bcolors.ENDC} untuk videoIn   426 x  420")
	print(f"\t - {bcolors.BOLD}360p{bcolors.ENDC} untuk videoIn   640 x  360")
	print(f"\t - {bcolors.BOLD}480p{bcolors.ENDC} untuk videoIn   854 x  480")
	print(f"\t - {bcolors.BOLD}720p{bcolors.ENDC} untuk videoIn  1280 x  720")
	print(f"\t - {bcolors.BOLD}1080p{bcolors.ENDC} untuk videoIn 1920 x 1080")
	print(f"\t - {bcolors.BOLD}1440p{bcolors.ENDC} untuk videoIn 2560 x 1440")
	print(f"\t - {bcolors.BOLD}2160p{bcolors.ENDC} untuk videoIn 3840 x 2160")
	print(f"\t<{bcolors.BOLD}frame-rate{bcolors.ENDC}> angka integer frame per-second hasil konverter moving images keluaran.")
	print(f"\t Jika fps keluaran lebih kecil dari aslinya, maka akan ada pengurangan")
	print(f"\t frame sesuai dengan yang dibutuhkan. Jika fps keluaran lebih besar dari")
	print(f"\t aslinya, maka ada frame-frame yang ditambahkan pada hasil keluaran.")
	print()
	sys.exit(1)

def main(argv):
	if len(sys.argv) != 5:
		PrintErrorMsg()
	ResInd = ['240p','360p','480p','720p','1080p','1440p','2160p']
	FileExtentionList = ['avi', 'mp4', 'ogg']

	FileMasukan = sys.argv[1]
	FileKeluaran = sys.argv[2]
	ResolusiO = sys.argv[3]
	FrameRateO = sys.argv[4]

	if ResolusiO not in ResInd:
		PrintErrorMsg()
	if not FrameRateO.isdigit():
		PrintErrorMsg()
	FileNameKeluaran = FileKeluaran.split('/')
	FileNameKeluaran = FileNameKeluaran[(len(FileNameKeluaran)-1)]
	ExtentionFile = FileNameKeluaran.split('.')
	if ExtentionFile[(len(ExtentionFile)-1)] not in FileExtentionList:
		PrintErrorMsg()

	videoIn = cv.VideoCapture(FileMasukan)
	(major_ver, minor_ver, subminor_ver) = (cv.__version__).split('.')
	if int(major_ver)  < 3:
		FrameRateI = videoIn.get(cv.cv.CV_CAP_PROP_FPS)
		ResolusiI = str(int(videoIn.get(cv.cv.CV_CAP_PROP_FRAME_WIDTH))) + " x " + str(int(videoIn.get(cv.cv.CV_CAP_PROP_FRAME_HEIGHT)))
	else:
		FrameRateI = videoIn.get(cv.CAP_PROP_FPS)
		ResolusiI = str(int(videoIn.get(cv.CAP_PROP_FRAME_WIDTH))) + " x " + str(int(videoIn.get(cv.CAP_PROP_FRAME_HEIGHT)))
	if not videoIn.isOpened():
		print(f"{bcolors.BOLD}TERJADI KESALAHAN{bcolors.ENDC}: file masukan " + FileMasukan + " tidak dapat dibuka\n")
		sys.exit(2)

	print("Versi OpenCV      : " + IsCudaOpenCV())
	print("Logical CPU       : " + str(psutil.cpu_count()) + " vCPU")
	print("Nama File Masukan : {}".format(FileMasukan))
	print("    Resolusi      : {}".format(ResolusiI))
	print("    Frame Rate    : {} fps".format(int(FrameRateI)))
	print("Nama File Keluaran: {}".format(FileKeluaran))
	print("    Resolusi      : {}".format(ResolusiO))
	print("    Frame Rate    : {} fps".format(FrameRateO))
	
	StartTime = datetime.now()
	print("Proses dimulai : " + PrintTimestamp(StartTime))
	print()

	fourcc = cv.VideoWriter_fourcc('M', 'J', 'P', 'G')
	out = cv.VideoWriter(FileKeluaran,fourcc,int(FrameRateO), (1280,720))
	i = 0
	while True:
		ret, frame = videoIn.read()
		print("frame ke-{}".format(i),end="\r")
		i+=1
		if ret == True:
			b = cv.resize(frame,(1280,720),fx=0,fy=0, interpolation = cv.INTER_CUBIC)
			out.write(b)
		else:
			break
	videoIn.release()
	out.release()

	EndTime = datetime.now()
	print()
	print("\nProses selesai : " + PrintTimestamp(EndTime))
	print()

print(f"\n{bcolors.WARNING}{bcolors.BOLD}Visual Computing Laboratory{bcolors.ENDC}")
print(f"{bcolors.FAIL}{bcolors.BOLD}{bcolors.UNDERLINE}Universitas Narotama - Surabaya{bcolors.ENDC}\n")
if __name__ == "__main__":
	main(sys.argv[1:])