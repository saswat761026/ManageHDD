import os
import shutil


class Copy:
    def __init__(self, base_src_dir, base_des_dir):
        self.abs_src_dir = base_src_dir
        self.abs_des_dir = base_des_dir

    def copyfile(self, pattern, src, des):
        src_path = os.path.join(self.abs_src_dir, src)
        files_present = os.listdir(src_path)
        
        files_to_move = []
        for item in files_present:
            if pattern in item:
                files_to_move.append(item)
        
        des_path = os.path.join(self.abs_des_dir, des)

        print(f"Total number of files to move{len(files_to_move)}\n")

        for item in files_to_move:
            if shutil.move(os.path.join(src_path, item), os.path.join(des_path, item)):
                print(f"Successfully moved {item}\n")
            else:
                print(f"Failed to move {item}\n")    
        print(f"Completly moved the pattern: {pattern}")
            
#cp = Copy("/home/avish", "/home/avish")
#cp.copyfile('x', 'Documents', 'Downloads')






