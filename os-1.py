import os
import shutil


num = 0

def main():
    if num == 0 :
        items = os.listdir()
        ad = (".")



        x = ""
        li = []
        for j in items:
            x = os.path.splitext(j)[1] 
            if x != "":
                li.append(x)
                se = set(li)
                li = list(se)

            
        for i in li :
            x = os.path.join(ad,i)
            os.makedirs(x,exist_ok=True)




            for q in items:
                a = os.path.splitext(q)[0]

                for y in items:
                    b = os.path.splitext(y)[1]

                    if a == b :
                        try:
                            shutil.move(y,q)
                        except:
                            continue

main()
main()
num = 1



    
with open("duc.txt","w",encoding="utf8") as report:

    report.write("                     Report\n")
    report.write("-----------------------------------------\n")

    for item in os.listdir("."):
        if os.path.isdir(item):
            total_size = 0

            for file in os.listdir(item):
                file_path = os.path.join(item,file)
                total_size += os.path.getsize(file_path)
                report.write(f"{file_path}: {os.path.getsize(file_path)/1024} kb\n")
                report.write(f"{file_path}: {os.path.getsize(file_path)/1024/1024} mb\n\n")
           
            report.write(f"total({item}): {total_size / 1024}kb\n ")
            report.write(f"total({item}): {total_size / 1024/1024}mb\n")
            report.write(f"**************************************************\n")

