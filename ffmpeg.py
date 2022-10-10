import subprocess
import time

if __name__ == '__main__':
    path = r'D:\ffmpeg\bin\info.txt'
    """
    name
    url_01
    url_02
    """
    with open(path, 'r', encoding="UTF-8") as f:
        links = f.readlines()

    i, j, cur_name = 0, 0, ''

    while i < len(links):
        s = links[i].strip('\n')
        if s and s[:4] != 'http':
            j, cur_name = 0, s
        elif s:
            if j > 0:
                p = subprocess.Popen('D:\\ffmpeg\\bin\\ffmpeg -i %s -c copy -bsf:a aac_adtstoasc %s_%02d.mp4' %
                                     (links[i+j].strip('\n'), cur_name, j), shell=True)
            else:
                p = subprocess.Popen('D:\\ffmpeg\\bin\\ffmpeg -i %s -c copy -bsf:a aac_adtstoasc %s.mp4' %
                                     (links[i].strip('\n'), cur_name), shell=True)
            return_code = p.wait()
            print(cur_name + '_%02d' % j)
            j += 1
            time.sleep(60)
        i += 1
