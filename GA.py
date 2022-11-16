# In[1]:


import numpy as np
import  random
import matplotlib.pyplot as plt
# get_ipython().run_line_magic('matplotlib', 'inline')


# # 1. 获取临接矩阵

# In[2]:
lis=[104.147618,103.985507,104.074238,103.963359]
lit=[30.635065,30.690991,30.612572,30.575972]
for z in range(1,2):
    for kz in range(5):
        def CacDistance(a,b):
            """
            计算两点之间的距离
            """
            a = np.array(a)
            b = np.array(b)
            c = a-b
            l=np.array([[9.6, 11.1]])
            c=c*l
            distance = np.sqrt(np.sum(c*c))
            return distance
        
        def CityDistance():
            """
          在locs中输入坐标
            """
            locs=[(lis[z],lit[z]),
                  (104.075782,30.660133),
                  (104.093631,30.664496),
                  (104.086102,30.652141),
                  (104.108255,30.649477),
                  (104.084984,30.671864),
                  (104.04816,30.664091),
                  (104.032957,30.680684),
                  (104.082411,30.67826),
                  (104.094005,30.689287),
                  (104.051343,30.691756),
                  (104.083052,30.694759),
                  (104.112585,30.653677),
                  (104.102693,30.667626)]
            n = len(locs)
            dis_mat = np.zeros([14,14])
            for i in range(n-1):
                for j in range(i+1,n):
                    dist = CacDistance(locs[i],locs[j])
                    dis_mat[i,j] = dist
        
            for i in range(n):
                dis_mat[:,i] = dis_mat[i,:]
        
            return dis_mat
        
        
        # # 2. 遗传算法
        
        # ## 2.1交叉
        
        # In[3]:
        
        
        def Cross(p1,p2):
            a = np.array(p1).copy()
            b = np.array(p2).copy()
        
            # 0~9之间随机生成两个整数,作为映射的起始点和结束点
            begin = random.randint(0,13)
            end = random.randint(0,13)
            # 使 begin 小于 end
            if begin > end:
                temp = begin
                begin = end
                end = temp
        
            #print begin,end
            # 建立映射关系
            cross_map = {}
            is_exist = False
            # 初步映射
            for i in range(begin,end+1):
                if a[i] not in cross_map.keys():
                    cross_map[a[i]] = []
                if b[i] not in cross_map.keys():
                    cross_map[b[i]] = []
        
                cross_map[a[i]].append(b[i])
                cross_map[b[i]].append(a[i])
        
        
            # 处理传递映射 如1:[6],6:[3,1]-->1:[6,3,1],6:[3,1]
            # 计算子串中元素出现的个数，个数为2，则该元素为传递的中间结点，如如1:[6],6:[3,1],‘6’出现的次数为2
            appear_times = {}
            for i in range(begin,end+1):
                if a[i] not in appear_times.keys():
                    appear_times[a[i]] = 0
                if b[i] not in appear_times.keys():
                    appear_times[b[i]] = 0
        
                appear_times[a[i]] += 1
                appear_times[b[i]] += 1
        
                if a[i] == b[i]:
                    appear_times[a[i]] -= 1
        
        
            for k,v in appear_times.items():
                if v == 2:
                    values = cross_map[k]
                    for key in values:
                        cross_map[key].extend(values)
                        cross_map[key].append(k)
                        cross_map[key].remove(key)
                        cross_map[key] = list(set(cross_map[key]))
        
        
            # 使用映射关系交叉
            # 先映射选中的子串
            temp = a[begin:end+1].copy()
            a[begin:end+1] = b[begin:end+1]
            b[begin:end+1] = temp
        
            # 根据映射规则映射剩下的子串
            seg_a = a[begin:end+1]
            seg_b = b[begin:end+1]
        
            remain = list(range(begin))
            remain.extend(range(end+1,len(a)))
        
            for i in remain:
                keys = cross_map.keys()
                if a[i] in keys:
                    for fi in cross_map[a[i]]:
                        if fi not in seg_a:
                            a[i] = fi
                            break
        
                if b[i] in keys:
                    for fi in cross_map[b[i]]:
                        if fi not in seg_b:
                            b[i] = fi
                            break
        
            return a,b            
        
        
        # ## 2.2 变异
        
        # In[4]:
        
        
        def Variation(s):
            c = range(14)
            index1,index2 = random.sample(c,2)
            temp = s[index1]
            s[index1] = s[index2]
            s[index2] = temp
            return s
        
        
        # ## 2.3 计算适应度
        
        # In[5]:
        
        
        def cost(s):
            dis = CityDistance()
            n = len(s)
            cost = 0
            for i in range(n):
                if i==13:
                    cost += dis[s[i],s[0]]
                else:
                    cost += dis[s[i],s[i+1]]
            return -cost
        
        
        # ## 2.4 构建遗传算法
        
        # In[6]:
        
        
        # 获取列表的第三个元素
        def TakeThird(elem):
            """
            按适应度从大到小，排序时作为sort的key参数
            """
            return elem[2]
        
        def CacAdap(population):
            # adap n*4,n为行数，每行包括：个体下标,适应度,选择概率,累积概率
            #population 见程序末尾
            # 计算每一个个体的适应度,选择概率
            adap = []
            psum = 0
            # 计算适应度
            i = 0
            for p in population:
                icost = np.exp(cost(p))
                psum += icost
                # 添加个体下标
                adap.append([i])
                # 添加适应度
                adap[i].append(icost)
                i += 1
            # 计算选择概率
            for p in adap:
                # 添加选择概率和累积概率，这里累积概率暂时等于选择概率，后面会重新计算赋值
                p.append(p[1]/psum)
                p.append(p[2])
        
            # 根据适应度从大到小排序
            adap.sort(key=TakeThird,reverse=True)
            #print adap
            # 计算累计概率
            n = len(adap)
            for i in range(1,n):
                p = adap[i][3] + adap[i-1][3]
                adap[i][3] = p
            
            return adap
        
        def Chose(adap):
            """
            轮盘选择操作
            """
            chose = []
            # 选择次数
            epochs = 28 #max(len(adap)/2,20)
            #while(len(set(chose)) <2):
            #print 'chosing...length %d'%len(set(chose))
            n = len(adap)
            for a in range(epochs):
                p = random.random()#生成一个随机的小数
                if adap[0][3] >= p:
                    chose.append(adap[0][0])
                else:
                    for i in range(1,n):
                        if adap[i][3] >= p and adap[i-1][3] < p:
                            chose.append(adap[i][0])
                            break
        
            chose = list((chose))
            return chose
        
        def Cross_Variation(chose,population):
            """
            交叉变异操作
            """
            # 交叉率
            p_c = 0.7
            # 变异率
            p_m = 0.3
            # 交叉变异操作
            chose_num = len(chose)
            sample_times = chose_num//2
            for i in range(sample_times):
                index1,index2 = random.sample(chose,2)
                #print index1,index2
                # 参与交叉的父结点
                parent1 = population[index1]
                parent2 = population[index2]
                # 这两个父结点已经交叉，后面就不要参与了，就像这两个人以及结婚，按规矩不能在与其他人结婚了，故从采样样本中移除
                chose.remove(index1)
                chose.remove(index2)
                
                p = random.random()
                if p_c >= p:
                    child1,child2 = Cross(parent1,parent2)
                    #print child1,child2
                    p1 = random.random()
                    p2 = random.random()
                    if p_m > p1:
                        child1 = Variation(child1)
                    if p_m > p2:
                        child2 = Variation(child2)
                    population.append(list(child1))
                    population.append(list(child2))
            return population
        
        
        # In[7]:
        
        
        def GA(population):
            """
            一次遗传过程
            """
            
            adap = CacAdap(population)
        
            # 选择操作
            chose = Chose(adap)
            # 交叉变异
            population = Cross_Variation(chose,population)
                
        
            return population
        
        
        # ## 2.5 循环调用遗传算法，直到达到终止条件
        
        # In[8]:
        
        
        def find_min(population):
            loss = []
            # 遗传次数
            epochs = 101
            i = 0
            while i < epochs:
                adap = []
                # 计算适应度
                for p in population:
                    icost = cost(p)
                    adap.append(icost)
                
                # 使用遗传算法更新种群
                population = GA(population)
                
                min_cost = max(adap)
                if i%10 == 0:
                    print('epoch %d: loss=%.3f 万米'%(i,-min_cost))
                loss.append([i,-min_cost])
                i += 1
                if i == epochs:
                    # 输出最优解
                    p_len = len(population)
                    for index in range(p_len):
                        if adap[index] == min_cost:
                            print('最优路径:')
                            print(population[index])
                            print('公里数:')
                            print('%.3f 万米'%(-min_cost))
                            break
            # 打印损失函数变换
            loss = np.array(loss)
            plt.plot(loss[:,0],loss[:,1])
            plt.title('GA')
            a=str(z)
            c=str(kz)
            plt.show()
            plt.savefig(a+'-'+c+'.jpg')
            print(a+'-'+c+'完成')
            
        
        
        # In[9]:
        
        
        # 初始化
        s1 = [1,2,5,7,3,8,9,10,11,12,13,4,6,0]
        s2 = [13, 3, 1, 4, 12, 2, 5, 8, 6, 0, 7, 10, 11, 9]
        s3 = [13, 12, 4, 3, 2, 5, 8, 1, 6, 0, 7, 10, 11, 9]
        s4 = [13, 12, 0, 4, 3, 2, 8, 5, 1, 6, 7, 10, 11, 9]
        population = [s1,s2,s3,s4]
        # 调用
        find_min(population)
        
        
        # In[ ]:
        print('对应关系：（0:f,1:a,2:b,3:2,4:3,5:5,6:6,7:7,8:8,9:9,10:10,11:11,12:12,13:13）')


