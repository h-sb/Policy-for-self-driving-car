import os
import pdb
import copy
import math
import numpy as np

#correct
if os.path.exists("output.txt"):
  os.remove("output.txt")


f2=open("output.txt","a+")
def main():

    mdpinit()


class MDP():
    def actions(self, state):
        if state in mdpinit.end_pos_car:
            return 0
        else:
            return
class mdpinit:

    def ReadInput(self):
        self.start_pos_car=[]
        self.end_pos_car=[]
        self.obs_pos=[]
        grids_list=[]

        with open("input2.txt","r") as f1:
            line=f1.readline()
            line=line.rstrip()
            self.s=int(line)
            #print "s=",self.s#size of grid

            line=f1.readline()
            line=line.rstrip()
            n=int(line)
            ##print "n=",n#no of cars

            line=f1.readline()
            line=line.rstrip()
            ob=int(line)
            #print "ob=",ob#no of obstacles

            cnt=0
            while(cnt!=ob):
                line=next(f1)
                line=line.rstrip()
                x,y=line.split(",")
                temp=[int(x),int(y)]
                self.obs_pos.append(temp)

                cnt+=1

            #print self.obs_pos

            cnt=0
            while(cnt!=n):
                line=next(f1)
                line=line.rstrip()
                x,y=line.split(",")
                temp=[int(x),int(y)]
                self.start_pos_car.append(temp)

                cnt+=1

            #print self.start_pos_car

            cnt=0
            while(cnt!=n):
                line=next(f1)
                line=line.rstrip()
                x,y=line.split(",")
                temp=[int(x),int(y)]
                self.end_pos_car.append(temp)

                cnt+=1

            #print self.end_pos_car

            i=0
            while i<n:
                grids_list.append(self.displayGrid(i))
                i=i+1
            car=1
            # for car_grid in grids_list:
            #     #print " car:",car
            #     # #print car_grid
            #     for row in car_grid:
            #         #print(row)
            #     car=car+1
            # #print "gl",grids_list
            i=1
            policy={}
            car=0
            U_all=[]
            policy_all=[]
            for car_grid in grids_list:
                #print self.end_pos_car[car]
                U=self.valueIteration(car_grid,i,self.end_pos_car[car],self.obs_pos)
                #print U
                U_all.append(U)
                policy=self.determine_policy(U)
                #print policy

                policy_all.append(policy)


                i=i+1
                car=car+1

            self.simulation(policy_all,grids_list)

            # #print "FIRST POLICY:",policy_all[0]
            # self.simulation(self.end_pos_car)

    def simulation(self,policy_all,grids_list):
        result=[]

        cost_list=[]
        car_cost={}
        for i in range(len(grids_list)):
            cost_list=[]

            for j in range(10):
                cost=0


                pos=tuple(self.start_pos_car[i])
                #print "start_pos:",pos
                np.random.seed(j)
                swerve = np.float64(np.random.random_sample(1000000))
                k=0
                #print "end_pos:",self.end_pos_car[i]
                if pos==tuple(self.end_pos_car[i]):
                    cost=100
                while pos != tuple(self.end_pos_car[i]):
                    move = policy_all[i][pos[0],pos[1]]
                    #print "Default move:",move, swerve[k]
                    if swerve[k] > 0.7:
                        if swerve[k] > 0.8:
                            if swerve[k] > 0.9:
                                move = self.turn_left(self.turn_left(move))
                            else:
                                move = self.turn_left(move)
                        else:
                            #print "right"
                            move = self.turn_right(move)

                    k=k+1

                    if self.validate_move(pos,move):
                        pos=pos[0]+move[0],pos[1]+move[1]
                        cost=cost+grids_list[i][pos[1]][pos[0]]
                    else:
                        cost=cost+grids_list[i][pos[1]][pos[0]]
                    #print "move made:",pos

                #print "cost at end of j",j,cost
                cost_list.append(cost)
            avg_c=sum(cost_list)/10.0
            avg_cost=math.floor(avg_c)
            car_cost[i]=avg_cost
        print "costs:",car_cost
        for key,val in car_cost.iteritems():
            f2.write(str(int(val)))
            f2.write('\n')

    def validate_move(self,pos,move):
        if 0<= pos[0]+move[0]<self.s:
            if 0<= pos[1]+move[1]<self.s:
                return True
            else:
                return False
        else:
            return False


    def turn_left(self,move):

        if move==(0,-1):
            return (1,0)
        elif move==(1,0):
            return (0,1)
        elif move==(0,1):
            return (-1,0)
        elif move==(-1,0):
            return (0,-1)
        else:
            return 'wrong'


    def turn_right(self,move):
        #check_valid
        if move==(0,-1):
            return (-1,0)
        elif move==(-1,0):
            return (0,1)
        elif move==(0,1):
            return (1,0)
        elif move==(1,0):
            return (0,-1)
        else:
            return 'wrong'




    def displayGrid(self,i):
        grids = [[-1.0] * self.s for _ in range(self.s)]
        # for i <n:for diff cars
        grids[self.end_pos_car[i][1]][self.end_pos_car[i][0]]=grids[self.end_pos_car[i][1]][self.end_pos_car[i][0]]+100.0

        for i,j in self.obs_pos:
            grids[j][i]=grids[j][i]-100.0


        # #print ("grids[pos][row]=",grids[self.end_pos_car[0][0]][self.end_pos_car[0][1]])
        # for row in grids:
        #
        #     # if (row[0]==self.end_pos_car[0][1]):#for 1 car only. if multiple cars add loop
        #     #     pos=self.end_pos_car[0][0]
        #
        #
        #     #print(row)
        return grids

    def valueIteration(self, car_grid,i,end_pos_car,obs_pos):
        coord=[]
        gamma=0.9
        epsilon=0.1

        self.car_grid=car_grid#check issue!!
        for i in range(self.s):
            for j in range (self.s):
                co=j,i
                coord.append(co)
        #print "---------CORD___",coord

        U1=dict([(s, 0) for s in coord])
        end_pos=end_pos_car[0],end_pos_car[1]
        U1[end_pos]=99
        #print "UTILITIES:",U1
        c=0

        while True:

            U = copy.deepcopy(U1)
            delta = 0.0
            for self.x in coord:
                if self.x==end_pos:

                    continue
                # for ob in obs_pos:
                #     if self.x==ob:
                #         print "a"
                #         continue


                ar=[0,0,0,0]
                # #print "x:",car_grid[x[0]][x[1]]
                actions=self.valid_actions(self.x)

                # #print "actions:",self.x,actions
                i=0
                for a in actions:

                    # #print "now serving:",i
                    if a==1:

                        ar[i]=U[self.x]

                    else:

                        res=self.calc_arg(i,U)
                        #print "res:",res
                        ar[i]=res

                    i=i+1
                max_val=self.calc_max(ar)

                U1[self.x]=car_grid[self.x[1]][self.x[0]]+(gamma*max_val)
                # no=math.fabs(U1[self.x]-U[self.x])
                # #print "no.:",no
                delta = max(delta,math.fabs(U1[self.x]-U[self.x]))
                # #print "-----s:",self.x,ar,U1[self.x]

            if delta < epsilon * (1 - gamma) / gamma:

                # #print U1
                return U


                # #print "-----s:",self.x,ar,U1[self.x]
            c=c+1


    def calc_max(self,ar):
        n=ar[0]*0.7+ar[1]*0.1+ar[2]*0.1+ar[3]*0.1
        e=ar[0]*0.1+ar[1]*0.7+ar[2]*0.1+ar[3]*0.1
        w=ar[0]*0.1+ar[1]*0.1+ar[2]*0.7+ar[3]*0.1
        s=ar[0]*0.1+ar[1]*0.1+ar[2]*0.1+ar[3]*0.7
        #print "news:",n,e,w,s
        return max(n,e,w,s)

    def valid_actions(self,x):
        actions=[0,0,0,0]
        if (x[1]-1<0):#north
            actions[0]=1
        if (x[0]+1>=self.s):#east
            actions[1]=1
        if (x[0]-1<0):#west
            actions[2]=1
        if (x[1]+1>=self.s):#south
            actions[3]=1
        return actions

    def calc_arg(self,index,U1):

        if index==0:
            val=U1[self.x[0],self.x[1]-1]
        elif index==1:
            # #print ("coord:",self.x[]+1,self.x[1])
            val=U1[self.x[0]+1,self.x[1]]
        elif index==2:
            val=U1[self.x[0]-1,self.x[1]]
        elif index==3:
            val=U1[self.x[0],self.x[1]+1]
        else:
            val="wrong"
        #print ("val:",val)
        return val

#chang here too

    def determine_policy(self,U):
        policy={}

        for key in U:
            options={}
            directn={}
            chosen=[]
            directn['0,-1']=key[0],key[1]-1#n
            directn['1,0']=key[0]+1,key[1]#e
            directn['-1,0']=key[0]-1,key[1]#w
            directn['0,1']=key[0],key[1]+1#s


            # j=0
            for i in directn.keys():
                if directn[i] in U.keys():
                    options[i]=U[directn[i]]
                else:
                    # #print "key:",key
                    options[i]=U[key]
                # j=j+1


            mv=max(options.itervalues())
            #print mv
            for k,val in options.items():
                if mv==val:
                    chosen.append(k)
            if len(chosen)>1:
                if '0,-1' in chosen:
                    ch='0,-1'
                elif '0,1' in chosen:
                    ch='0,1'
                elif '1,0' in chosen:
                    ch='1,0'
                else:
                    ch='-1,0'
            else:
                ch=chosen[0]
            choice=ch.split(",")
            i=int(choice[0])
            j=int(choice[1])
            policy[key]=i,j

        return policy


    def __init__(self):

        self.ReadInput()




main()
f2.close()
