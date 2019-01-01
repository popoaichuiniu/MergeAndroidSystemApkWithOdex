import  subprocess
import os
def execuateCmd(cmd):
	status,output=subprocess.getstatusoutput(cmd);
	return status,output

def convertOdexTodex(odexFile):
	if(odexFile.endswith(".odex")):
		odexFileName=odexFile.replace(".odex","")
		cmdOdexToSmali="java -jar baksmali-2.1.3.jar  -x "+odexFile+" -d framework"+" -o "+odexFileName
		status, output=execuateCmd(cmdOdexToSmali)
		if(status!=0):
			print(odexFile+" cmdOdexToSmali error "+output)
		else:
			cmdSmaliToDex="java -jar smali-2.1.3.jar "+odexFileName+" -o "+odexFileName+".dex"
			status, output = execuateCmd(cmdSmaliToDex)
			if(status!=0):
				print(odexFile+" cmdSmaliToDex error "+ output)
			else:
				print("success")
				rmDir="rm -r "+odexFileName
				status, output=execuateCmd(rmDir)
				if(status!=0):
					print("rm dir error "+output)

def getApk():
	for file in os.listdir("."):
		if (file.endswith(".apk")):
			fileName=file.replace(".apk","")
			unzipComd="unzip -o "+file+" -d "+fileName
			status, output=execuateCmd(unzipComd)
			if(status!=0):
				print(file+" unziperror "+output)
			else:
				apkdir=fileName
				flagHasdex=False
				for item in os.listdir(apkdir):
					if(item.endswith(".dex")):
						flagHasdex=True
						break
				if(not flagHasdex):
					if(os.path.exists(fileName+".dex")):
						copyDexToApkDirCmd="cp "+fileName+".dex "+fileName+"/classes.dex"
						status, output=execuateCmd(copyDexToApkDirCmd)
						if(status!=0):
							print(file + " copyDexToApkDirCmd error " + output)
						else:
							flagHasdex = True
				if(flagHasdex):
					str_all_item = ""
					for item in os.listdir(apkdir):
						str_all_item = str_all_item + " "+item
					zipApkCmd = "cd "+fileName+" && zip "  + fileName + "1.apk" + str_all_item
					status, output = execuateCmd(zipApkCmd)
					if (status != 0):
						print(file + " zipApkCmd error " + output)
					else:
						apkSignerCmd = "./apkSigner.sh " + fileName+"/"+fileName + "1.apk"
						status, output = execuateCmd(apkSignerCmd)
						if (status != 0):
							print("apkSignerCmd error " + output)
						else:
							print(file + "success"+output)








# for file in os.listdir("."):
# 	if(file.endswith(".odex")):
# 		convertOdexTodex(file)


getApk()