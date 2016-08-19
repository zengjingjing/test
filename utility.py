import os
import operator
def parse_ratio(dirname):
    ans = {}
    files = os.listdir(dirname)
    for filename in files :
        if filename == '.' or filename == '..' or filename == '.DS_Store':
            continue
        f = open(dirname + filename,'r')
        label = f.readline()
        if not ans.has_key(label):
            ans[label] = 1
        else:
            ans[label] = ans[label] + 1
    return ans


#get hand/print names(candicate = 1) from hdfs log
def parse_hdfs_log(dirname):
    lognames = os.listdir(dirname)
    hand_names = []
    print_names = []
    for logname in lognames:
        if logname == '.' or logname == '..' or logname == '.DS_Store':
            continue
        if logname.find('part') < 0:
            continue
        if not os.path.isfile(dirname + logname):
            continue
        log = open(dirname + logname)
        lines = log.readlines()
        for line in lines:
            if line.find('liujm') >= 0:
                continue
            if line.find('"is_handwriting":1') >= 0:
            #if line.find('"is_handwriting":1') >= 0 and line.find('"is_handwriting_candi":1') >= 0:
                left = line.find('[')
                right = line.find('@')
                hand_names.append(line[left+1:right])
            elif line.find('"is_handwriting":0') >= 0 and line.find('"is_handwriting_candi":1') >= 0:
                    left = line.find('[')
                    right = line.find('@')
                    print_names.append(line[left + 1:right])
    ans = []
    ans.append(hand_names)
    ans.append(print_names)
    return ans


#get hand images from labeled data
def get_hand(imgdir, classdir,savedir):
      #imgnames = os.listdir(imgdir)
      filenames = os.listdir(classdir)
      #print filenames
      for filename in filenames:
          if filename == '.' or filename == '..' or filename == '.DS_Store':
              continue
          if filename.find('box') < 0:
              continue
          f = open(classdir + filename,'r')
          label = f.readline()
          index = filename.find('box')
          imgname = imgdir + filename[0:index-1]
          savename = savedir + filename[0:index-1]
          #print label
          if label == '2' or label == '4':
              commandline = 'mv ' + imgname + ' ' + savename
             #print commandline
              os.system(commandline)

# parse the classifier log file
def parse_classifier_reason(logname):
    statistic = {}
    f = open(logname)
    lines = f.readlines()
    for line in lines:
        if not statistic.has_key(line):
            statistic[line] = 1
        else:
            statistic[line] = statistic[line] + 1
    statistic = sorted(statistic.items(), key=operator.itemgetter(1), reverse = True)
    return statistic


#delete some(not all) files from a dir
def delete_files_from_dir(dirname, count):
    filenames = os.listdir(dirname)
    #commandline =  'cd ' + dirname
    #os.system(commandline)
    for i in range(0, count - 1):
    #for filename in filenames:
        if filenames[i].find('png') < 0 and filenames[i].find('.jpg') < 0:
            continue
        commandline = 'rm ' + dirname + filenames[i]
        os.system(commandline)


# random select some images from a big set to from a small set and test
def random_select_for_subset(dirname, select_count):
    filenames = os.listdir(dirname)
    step = len(filenames) / select_count
    newfilenames = []
    for i in range(0, len(filenames), step):
        newfilenames.append(filenames[i])
    filenames = newfilenames
    subsetdir = dirname + 'subset/'
    subsetclassdir = subsetdir + 'class-result/'
    if not os.path.exists(subsetdir):
        os.mkdir(subsetdir)
    if not os.path.exists(subsetclassdir):
        os.mkdir(subsetclassdir)
    for filename in filenames:
        commandline = 'cp ' + dirname + filename + ' ' + subsetdir + filename
        os.system(commandline)
        commandline = 'cp ' + dirname + 'class-result/' + filename + '.box' + ' ' + subsetclassdir + filename + '.box'
        os.system(commandline)
