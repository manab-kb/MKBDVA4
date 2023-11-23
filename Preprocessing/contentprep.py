import os
import re

f =  open("/Users/manabkb/Desktop/pytch-releases/pytch-tutorials/index.yaml", "r")
content = f.readlines()
f.close()

tutdir = "/Users/manabkb/Desktop/pytch-releases/pytch-tutorials"
embeddingfile = "/Users/manabkb/Desktop/Manab Biswas/Pytch - Summer Internship/Model/Dataset/Extras/Simplified-Dataset/Embeddings/gpt-embeddings.json"

completesubtutcontent = []

for entry in os.listdir(tutdir):
    if entry != "site-layer":
        path = tutdir + "/" + entry

        if os.path.isdir(path):
            for subentry in os.listdir(path):
                subpath = path + "/" + subentry

                if os.path.isfile(subpath):
                    if subpath.__contains__("tutorial.md"):
                        f = open(subpath, "r")
                        tutcontent = f.read()
                        f.close()

                        tempcontent = tutcontent.split("#")
                        subtutcontent = [x for x in tempcontent if x != '']
                        
                        for subtut in subtutcontent:
                            if str(subtut).__contains__("{{< commit "):
                                while str(subtut).__contains__("{{< commit"):
                                    commitstartindex = re.search("{{< commit ", subtut).end()
                                    replacestartindex = re.search("{{< commit ", subtut).start()

                                    commitendindex = re.search(" >}}", subtut).start()
                                    replaceendindex = re.search(" >}}", subtut).end()

                                    commitname = subtut[commitstartindex:commitendindex]
                                    
                                    for index in range(0,len(content)):
                                        if content[index].startswith("- name: "):
                                            if entry.casefold() in content[index].casefold():
                                                tipname = content[index+1]
                                                tip = tipname.split(":")[1].strip()

                                                os.chdir("/Users/manabkb/Desktop/pytch-releases/pytch-tutorials")
                                                os.system("git checkout {0}".format(tip))
                                                os.chdir(entry)
                                                os.system("git log --follow {0} > temp.txt".format("code.py"))

                                                tf = open("temp.txt", "r")
                                                tcontent = tf.readlines()
                                                tf.close()

                                                for itemindex in range(0, len(tcontent)):
                                                    if commitname in tcontent[itemindex]:
                                                        commithash = tcontent[itemindex-4]
                                                        commithash = commithash[7:]
                                                        break

                                                os.system("git checkout {0}".format(commithash))
                                                rf = open("code.py")
                                                codecontent = rf.read()
                                                rf.close()

                                                os.system("git checkout releases")
                                                os.remove("temp.txt")
                                                break
                                    
                                    newcontent = subtut[:replacestartindex] + codecontent + subtut[replaceendindex:]
                                    subtut = newcontent
                                completesubtutcontent.append(newcontent)
                            else:
                                completesubtutcontent.append(str(subtut))

outputfile = open("/Users/manabkb/Desktop/Manab Biswas/Pytch - Summer Internship/Model/Dataset/Extras/Simplified-Dataset/Embeddings/embeddings-list.txt", "w")
outputfile.write(str(completesubtutcontent))
outputfile.close()
