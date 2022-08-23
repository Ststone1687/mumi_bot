import os
import math
import random
import json
# n1(0), lv1(1), hp1(2), atk1(3), def1(4), spd1(5), dp1(6)
def start_buff(datas,buff,now,skill,txt):#開場 1
  number = skill[1]
  if(number == 100001):#召魂術 100001
    Ran = random.randint(1,4)
    if(Ran == 4):
      buff[now][now][3] = datas[now][3]
      skill[2] = 3
      txt += datas[now][0]+"發動了技能「召魂術」，提升了自身攻擊力100%，效果將持續三回合\n"
  
  elif(number == 100002):#在這裡！ 100002
    Ran = random.randint(1,2)
    if(Ran == 2 and datas[(now+1)%2][3]>datas[now][4]):
      buff[now][now][4] = datas[now][4]
      skill[2] = -1
      txt += datas[now][0]+"發動了技能「在這裡！」，提升了自身防禦力100%\n"

  elif(number == 100003):#調虎離山 100003
    Ran = random.randint(1,20)
    if(Ran==20):
      buff[now][now][2] = datas[now][2]*5
      skill[2] = -1
      txt += datas[now][0]+"發動了技能「調虎離山」，提升了自身血量500%\n"
  
  elif(number == 100004):#如虎添翼 100004
    buff[now][now][3] = int(datas[now][3]*0.1)
    buff[now][now][5] = int(datas[now][5]*0.15)
    skill[2] = -1
    txt += datas[now][0]+"發動了技能「如虎添翼」，提升了攻擊力10%及速度15%\n"

  elif(number == 100005):#狐假虎威 100005
    buff[now][now][2] = datas[(now*-1)+1][2]-datas[now][2]
    buff[now][now][3] = datas[(now*-1)+1][3]-datas[now][3]
    buff[now][now][4] = datas[(now*-1)+1][4]-datas[now][4]
    buff[now][now][5] = datas[(now*-1)+1][5]-datas[now][5]
    skill[2] = 3
    txt += datas[now][0]+"發動了技能「狐假虎威」，除了等級外，所有數值複製成對手數值了，維持三回合\n"

  elif(number == 100006):#虎頭蛇尾 100006
    buff[now][now][2] = datas[now][2]
    buff[now][now][3] = datas[now][3]
    buff[now][now][4] = datas[now][4]
    buff[now][now][5] = datas[now][5]
    skill[2] = random.randint(1,3)
    kkk = ""
    if(skill[2]==1):
      kkk = "一"
    elif(skill[2]==2):
      kkk = "二"
    else:
      kkk = "三"
    txt += datas[now][0]+"發動了技能「虎頭蛇尾」，除了等級外，提升了自身所有數值100%，維持"+kkk+"回合\n"
  
  return buff,skill,txt

def self_buff(datas,buff,now,skill,txt):#主動 2
  number = skill[1]
  if(number == 200001):#金字塔的秘密 200001
    if(datas[now][2]<50 and datas[now][5]>=100):
      Ran = random.randint(1,2)
      if(Ran == 2):
        buff[now][now][2] += 100
        buff[now][now][5] -= 50
        skill[2] = -1
        txt += datas[now][0]+"發動了技能「金字塔的秘密」，犧牲了50點速度轉換成了100點血量\n"
  
  return buff,skill,txt

def other_buff(datas,buff,now_atk,now,skill,txt,Dam,Ran,hit):#被動 3
  number = skill[1]
  if(number == 300001):#黑夜之王 300001
    if(hit == 0 and now_atk==now):
      r = random.randint(1,2)
      if(r==2):
        buff[now][(now+1)%2][5] -= int(datas[(now+1)%2][5]*0.5)
        skill[2] = 3
        txt += datas[now][0]+"發動了技能「黑夜之王」，降低了對手速度50%，效果將持續三回合\n"

  return buff,skill,txt

def damage(u1,u2,txt):
  #MLv:int,MATK:int,YDEF:int,MSPD:int,DP:int
  Ran = random.randint(50,150)
  Ran = Ran/100
  MLv,MATK,YDEF,MSPD,DP = u1[1],u1[3],u2[4],u1[5],u1[6]
  Dam = ((((2*MLv+10)/250)*(MATK/YDEF)*(Ran))*(MLv+MSPD+20)/4*DP)
  speed_past = random.randint(1,100)

  #txt += "現在數值：\n"
  #tostr = ["n","lv","hp","atk","def","sdp","dp"]
  #for i in range (7):
  #  txt += str(tostr[i])+":"+str(u1[i])+","
  #txt += "\n"
  #for i in range (7):
  #  txt += str(tostr[i])+":"+str(u2[i])+","
  #txt += "\n"

  if(speed_past<=int(math.log(u2[5])/math.log(u1[5])*10)):
    txt += u2[0]+"閃避了"+u1[0]+"的攻擊\n"
    return 0,1,0,txt
  elif(Ran>=1.25):
    txt += "暴擊！ "+u1[0]+"對"+u2[0]+"造成了"+str(int(Dam))+"點傷害\n"
    return int(Dam),Ran,1,txt
  else:
    txt += u1[0]+"對"+u2[0]+"造成了"+str(int(Dam))+"點傷害\n"
    return int(Dam),Ran,1,txt
  #(((2*MLv+10)/250)*(MATK/YDEF)*(Ran))*(MLv+MSPD+20)/4*DP

def count_now_fight(datas,buff,now_fight):
  for j in range(7):
    now_fight[0][j] = datas[0][j] + buff[0][0][j] + buff[1][0][j]
    now_fight[1][j] = datas[1][j] + buff[0][1][j] + buff[1][1][j]
  return now_fight

def fight(n1:str,lv1:int,hp1:int,atk1:int,def1:int,spd1:int,n2:str,lv2:int,hp2:int,atk2:int,def2:int,spd2:int,dp1:float,dp2:float,arm1:int,arm2:int,skt1:int,skn1:int,skt2:int,skn2:int):
  if(arm1 != 0):
    hp1,atk1,def1,spd1 = arms(hp1,atk1,def1,spd1,arm1)
  if(arm2 != 0):
    hp2,atk2,def2,spd2 = arms(hp2,atk2,def2,spd2,arm2)
  datas = [[n1,lv1,hp1,atk1,def1,spd1,dp1],[n2,lv2,hp2,atk2,def2,spd2,dp2]]
  buff  = [[["",0,0,0,0,0,0],["",0,0,0,0,0,0]],[["",0,0,0,0,0,0],["",0,0,0,0,0,0]]]
  now_fight  = [["",0,0,0,0,0,0],["",0,0,0,0,0,0]]
  h1,h2 = hp1,hp2
  skill=[[skt1,skn1,0],[skt2,skn2,0]]
  #skill type,skill number,skill statue
  txt = ""
  list = {}
  now = 0
  if(skill[0][0]==1):
    now_fight = count_now_fight(datas,buff,now_fight)
    buff,skill[0],txt = start_buff(now_fight,buff,0,skill[0],txt)
    datas[0][2] += buff[0][0][2]
    datas[1][2] += buff[0][1][2]
    buff[0][0][2],buff[0][1][2] = 0,0
  if(skill[1][0]==1):
    now_fight = count_now_fight(datas,buff,now_fight)
    buff,skill[1],txt = start_buff(now_fight,buff,1,skill[1],txt)
    datas[0][2] += buff[1][0][2]
    datas[1][2] += buff[1][1][2]
    buff[1][0][2],buff[1][1][2] = 0,0
  while(datas[0][2]>0 and datas[1][2]>0):
    if(skill[0][2]==0):
      buff[0] = [["",0,0,0,0,0,0],["",0,0,0,0,0,0]]
    if(skill[1][2]==0):
      buff[1] = [["",0,0,0,0,0,0],["",0,0,0,0,0,0]]
    if(skill[0][2]>0):
      skill[0][2] -= 1
    if(skill[1][2]>0):
      skill[1][2] -= 1
    S1 = random.randint(1,3)*(datas[0][5]+buff[0][0][5]+buff[1][0][5])
    S2 = random.randint(1,3)*(datas[0][5]+buff[0][1][5]+buff[1][1][5])
    if(S1>=S2):#s1先攻
      now = 0
    else:#s2先攻
      now = 1
    for i in range(2):
      now = (now+i)%2
      if(skill[now][0]==2):
        now_fight = count_now_fight(datas,buff,now_fight)
        buff,skill[now],txt = self_buff(now_fight,buff,now,skill[now],txt)
        datas[0][2] += buff[now][0][2]
        datas[1][2] += buff[now][1][2]
        buff[now][0][2],buff[now][1][2] = 0,0
      now_fight = count_now_fight(datas,buff,now_fight)
      Dam,Ran,hit,txt = damage(now_fight[now],now_fight[(now+1)%2],txt)
      datas[(now+1)%2][2] -= Dam
      if(datas[(now+1)%2][2]<0):
        break
      if(skill[now][0]==3):
        now_fight = count_now_fight(datas,buff,now_fight)
        buff,skill[now],txt = other_buff(now_fight,buff, now,now,skill[now],txt,Dam,Ran,hit)
        datas[0][2] += buff[now][0][2]
        datas[1][2] += buff[now][1][2]
      if(skill[(now+1)%2][0]==3):
        now_fight = count_now_fight(datas,buff,now_fight)
        buff,skill[(now+1)%2],txt = other_buff(now_fight,buff, now,(now+1)%2,skill[(now+1)%2],txt,Dam,Ran,hit)
        datas[0][2] += buff[(now+1)%2][0][2]
        datas[1][2] += buff[(now+1)%2][1][2]
        buff[(now+1)%2][0][2],buff[(now+1)%2][1][2] = 0,0
  if(datas[0][2]<=0):
    txt += str(datas[1][0])+"獲勝！\n"
    return txt,0,0,h1-datas[0][2],h2-datas[1][2]
  else:
    txt += str(datas[0][0])+"獲勝！\n"
    return txt,0,1,h1-datas[0][2],h2-datas[1][2]

def arms(HP:int,ATK:int,DEF:int,SPD:int,number:int):
  with open("arms.json","r",encoding="utf-8")as f:
    data = json.load(f)
  L = data[str(number)]
  if("." in str(L[1])):
    HP *= L[1]
  else:
    HP += L[1]
  if("." in str(L[2])):
    ATK *= L[2]
  else:
    ATK += L[2]
  if("." in str(L[3])):
    DEF *= L[3]
  else:
    DEF += L[3]
  if("." in str(L[4])):
    SPD *= L[4]
  else:
    SPD += L[4]
  return int(HP),int(ATK),int(DEF),int(SPD)