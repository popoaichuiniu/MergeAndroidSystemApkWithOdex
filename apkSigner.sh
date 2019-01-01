#!/bin/sh
apkName=$1
echo $apkName
signedAPKName=${apkName%.*}"_signed.apk"
echo $signedAPKName
zlignAPKName=${signedAPKName%.*}"_zipalign.apk"
jarsigner -verbose -keystore ~/.android/debug.keystore -signedjar $signedAPKName  $apkName androiddebugkey -digestalg SHA1 -sigalg MD5withRSA -keypass android -storepass android
zipalign -f -v 4 $signedAPKName $zlignAPKName
zipalign -c -v 4 $zlignAPKName
rm $signedAPKName
