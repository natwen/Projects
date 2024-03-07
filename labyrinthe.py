import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import random as rd
import time

e=50
m=4*e+1
n=(m//4)+1


def creer_labyrinthe():
  #L=[]
  M=np.zeros((m,m)) #Ici M est la matrice labyrinthe saint-graal
  N=np.zeros((n,n)) #P représente les noeuds du labyrinthe en contact direct avec un mur exterieur. Pour l'instant, seuls les murs touchent les murs.
  for k in range(m):
    M[0,k]=2
    M[m-1,k]=2
    M[k,0]=2
    M[k,m-1]=2
  for k in range(n):
    N[k,0]=1
    N[k,n-1]=1
    N[0,k]=1
    N[n-1,k]=1
  for i in range(1,n-1):
    for j in range(1,n-1):
      a,b=i,j
      while N[a,b]!=1:
        if N[a+1,b]==2 and N[a-1,b]==2 and N[a,b+1]==2 and N[a,b-1]==2:
          if a==i and b==j:
            break
          a,b=i,j
        M[4*a,4*b]=2
        N[a,b]=2
        #L.append(np.copy(M))
        r=rd.randint(0,3)
        if r==0 and N[a-1,b]!=2:
          for k in range(1,4):
            M[4*a-k,4*b]=2     #Vers le haut
          a-=1
        if r==1 and N[a+1,b]!=2:
          for k in range(1,4):
            M[4*a+k,4*b]=2      #Vers le bas
          a+=1
        if r==2 and N[a,b+1]!=2:
          for k in range(1,4):
            M[4*a,4*b+k]=2      #Vers la droite
          b+=1
        if r==3 and N[a,b-1]!=2:
          for k in range(1,4):
            M[4*a,4*b-k]=2      #Vers la gauche
          b-=1
      for c in range(1,n-1):
        for d in range(1,n-1):
          if N[c,d]==2:
            N[c,d]=1


  return M


M=creer_labyrinthe()


f=m-3
g=2       #Les coordonnées initiales, en bas à gauche

def puraupif():
  L=[]
  compteur=0
  ligne,colonne=f,g
  M[ligne,colonne]=3
  L.append(np.copy(M))
  while compteur<50000:
    if ligne==2 and colonne==m-3:
      print("Réussi!")
      return L
    r=rd.randint(0,3)
    if r==0 and M[ligne-2,colonne]==0:
      for k in range(1,5):
        M[ligne,colonne]=0
        ligne-=1
        M[ligne,colonne]=3
        L.append(np.copy(M))      #vers le haut
      compteur+=1
    if r==1 and M[ligne+2,colonne]==0:
      for k in range(1,5):
        M[ligne,colonne]=0
        ligne+=1
        M[ligne,colonne]=3
        L.append(np.copy(M))      #vers le bas
      compteur+=1
    if r==2 and M[ligne,colonne+2]==0:
      for k in range(1,5):
        M[ligne,colonne]=0
        colonne+=1
        M[ligne,colonne]=3
        L.append(np.copy(M))      #vers la droite
      compteur+=1
    if r==3 and M[ligne,colonne-2]==0:
      for k in range(1,5):
        M[ligne,colonne]=0
        colonne-=1
        M[ligne,colonne]=3
        L.append(np.copy(M))      #vers la gauche
      compteur+=1

  return L


def aupif_slide():
  L=[]
  compteur=0
  ligne,colonne=f,g
  M[ligne,colonne]=3
  L.append(np.copy(M))
  while compteur<50000:
    if ligne==2 and colonne==m-3:
      print("Réussi !")
      return L
    r=rd.randint(0,3)
    if r==0:
      while M[ligne-2,colonne]==0:
        M[ligne,colonne]=0
        ligne-=1
        M[ligne,colonne]=3
        L.append(np.copy(M))      #vers le haut
        compteur+=1
    if r==1:
      while M[ligne+2,colonne]==0:
        M[ligne,colonne]=0
        ligne+=1
        M[ligne,colonne]=3
        L.append(np.copy(M))      #vers le bas
        compteur+=1
    if r==2:
      while M[ligne,colonne+2]==0:
        M[ligne,colonne]=0
        colonne+=1
        M[ligne,colonne]=3
        L.append(np.copy(M))      #vers la droite
        compteur+=1
    if r==3:
      while M[ligne,colonne-2]==0:
        M[ligne,colonne]=0
        colonne-=1
        M[ligne,colonne]=3
        L.append(np.copy(M))      #vers la gauche
        compteur+=1
  return L

def aupif_debile():
  L=[]
  compteur=0
  ligne,colonne=f,g
  M[ligne,colonne]=3
  L.append(np.copy(M))
  while (ligne!=2 or colonne!=m-3) and compteur<50000:
    compteur+=1
    r=rd.randint(0,3)
    if r==0:
      while M[ligne-2,colonne]==0 or M[ligne+1,colonne+2]==1 or M[ligne-1,colonne-2]==1: #s'arrete lorsqu'elle est à un carrefour.
        M[ligne,colonne]=0
        ligne-=1
        M[ligne,colonne]=3
        L.append(np.copy(M))      #vers le haut
    if r==1:
      while M[ligne+2,colonne]==0 or M[ligne-1,colonne+2]==1 or M[ligne+1,colonne-2]==1:
        M[ligne,colonne]=0
        ligne+=1
        M[ligne,colonne]=3
        L.append(np.copy(M))      #vers le bas
    if r==2:
      while M[ligne,colonne+2]==0 or M[ligne+2,colonne-1]==1 or M[ligne-2,colonne-1]==1:
        M[ligne,colonne]=0
        colonne+=1
        M[ligne,colonne]=3
        L.append(np.copy(M))      #vers la droite
    if r==3:
      while M[ligne,colonne-2]==0 or M[ligne+2,colonne+1]==1 or M[ligne-2,colonne+1]==1:
        M[ligne,colonne]=0
        colonne-=1
        M[ligne,colonne]=3
        L.append(np.copy(M))      #vers la gauche
  return L


def aupif():
  L=[]
  direction=0
  compteur=0
  ligne,colonne=f,g
  M[ligne,colonne]=3
  L.append(np.copy(M))
  while compteur<50000:
    r=rd.randint(0,3)
    if ligne==2 and colonne==m-3:
      print("Réussi!")
      return L
    if r==0 and M[ligne-2,colonne]==0 and direction!=1:
      for k in range(1,5):
        M[ligne,colonne]=0
        ligne-=1
        M[ligne,colonne]=3
        L.append(np.copy(M))      #vers le haut
      compteur+=1
      if M[ligne-2,colonne]==2 and M[ligne,colonne+2]==2 and M[ligne,colonne-2]==2:
        direction=4
      else:
        direction=0
    if r==1 and M[ligne+2,colonne]==0 and direction!=0:
      for k in range(1,5):
        M[ligne,colonne]=0
        ligne+=1
        M[ligne,colonne]=3
        L.append(np.copy(M))      #vers le bas
      compteur+=1
      if M[ligne+2,colonne]==2 and M[ligne,colonne+2]==2 and M[ligne,colonne-2]==2:
        direction=4
      else:
        direction=1
    if r==2 and M[ligne,colonne+2]==0 and direction!=3:
      for k in range(1,5):
        M[ligne,colonne]=0
        colonne+=1
        M[ligne,colonne]=3
        L.append(np.copy(M))      #vers la droite
      compteur+=1
      if M[ligne+2,colonne]==2 and M[ligne-2,colonne]==2 and M[ligne,colonne+2]==2:
        direction=4
      else:
        direction=2
    if r==3 and M[ligne,colonne-2]==0 and direction!=2:
      for k in range(1,5):
        M[ligne,colonne]=0
        colonne-=1
        M[ligne,colonne]=3
        L.append(np.copy(M))      #vers la gauche
      compteur+=1
      if M[ligne+2,colonne]==2 and M[ligne-2,colonne]==2 and M[ligne,colonne-2]==2:
        direction=4
      else:
        direction=3
  return L



def compter_chemins_dispos(P,A,B):
  S=0
  if M[A-2,B]==0:
    if P[((A-2)//4)-1,(B-2)//4]!=1:
      S+=1
  if M[A+2,B]==0:
    if P[((A-2)//4)+1,(B-2)//4]!=1:
      S+=1
  if M[A,B-2]==0:
    if P[(A-2)//4,((B-2)//4)-1]!=1:
      S+=1
  if M[A,B+2]==0:
    if P[(A-2)//4,((B-2)//4)+1]!=1:
      S+=1
  return S

def aupif_cartographe():
  L=[]
  P=np.zeros((e,e),int)
  direction=0
  compteur=0
  ligne,colonne=f,g
  M[ligne,colonne]=3
  L.append(np.copy(M))
  while (ligne!=2 or colonne!=m-3) and compteur<50000:
    compteur+=1
    if ligne==2 and colonne==m-3:
      print("Réussi !")
      return L
    if P[(ligne-2)//4,(colonne-2)//4]==0:
      P[(ligne-2)//4,(colonne-2)//4]=compter_chemins_dispos(P,ligne,colonne)


    if P[(ligne-2)//4,(colonne-2)//4]==1:
      while P[(ligne-2)//4,(colonne-2)//4]==1:
        #P[(ligne-2)//4,(colonne-2)//4]=-1
        r=rd.randint(0,3)
        if r==0 and M[ligne-2,colonne]==0:
          if P[((ligne-2)//4)-1,(colonne-2)//4]!=1:
            for k in range(1,5):
              M[ligne,colonne]=0
              ligne-=1
              M[ligne,colonne]=3
              L.append(np.copy(M))      #vers le haut
        if r==1 and M[ligne+2,colonne]==0:
          if P[((ligne-2)//4)+1,(colonne-2)//4]!=1:
            for k in range(1,5):
              M[ligne,colonne]=0
              ligne+=1
              M[ligne,colonne]=3
              L.append(np.copy(M))      #vers le bas
        if r==2 and M[ligne,colonne+2]==0:
          if P[((ligne-2)//4),((colonne-2)//4)+1]!=1:
            for k in range(1,5):
              M[ligne,colonne]=0
              colonne+=1
              M[ligne,colonne]=3
              L.append(np.copy(M))      #vers la droite
        if r==3 and M[ligne,colonne-2]==0:
          if P[((ligne-2)//4),((colonne-2)//4)-1]!=1:
            for k in range(1,5):
              M[ligne,colonne]=0
              colonne-=1
              M[ligne,colonne]=3
              L.append(np.copy(M))      #vers la gauche
        P[(ligne-2)//4,(colonne-2)//4]=compter_chemins_dispos(P,ligne,colonne)




    r=rd.randint(0,3)
    if r==0 and M[ligne-2,colonne]==0 and direction!=1:
      if P[((ligne-2)//4)-1,(colonne-2)//4]!=1:
        for k in range(1,5):
          M[ligne,colonne]=0
          ligne-=1
          M[ligne,colonne]=3
          L.append(np.copy(M))      #vers le haut
        if M[ligne-2,colonne]==2 and M[ligne,colonne+2]==2 and M[ligne,colonne-2]==2:
          direction=4
        else:
          direction=0
    if r==1 and M[ligne+2,colonne]==0 and direction!=0:
      if P[((ligne-2)//4)+1,(colonne-2)//4]!=1:
        for k in range(1,5):
          M[ligne,colonne]=0
          ligne+=1
          M[ligne,colonne]=3
          L.append(np.copy(M))      #vers le bas
        if M[ligne+2,colonne]==2 and M[ligne,colonne+2]==2 and M[ligne,colonne-2]==2:
          direction=4
        else:
          direction=1
    if r==2 and M[ligne,colonne+2]==0 and direction!=3:
      if P[((ligne-2)//4),((colonne-2)//4)+1]!=1:
        for k in range(1,5):
          M[ligne,colonne]=0
          colonne+=1
          M[ligne,colonne]=3
          L.append(np.copy(M))      #vers la droite
        if M[ligne+2,colonne]==2 and M[ligne-2,colonne]==2 and M[ligne,colonne+2]==2:
          direction=4
        else:
          direction=2
    if r==3 and M[ligne,colonne-2]==0 and direction!=2:
      if P[((ligne-2)//4),((colonne-2)//4)-1]!=1:
        for k in range(1,5):
          M[ligne,colonne]=0
          colonne-=1
          M[ligne,colonne]=3
          L.append(np.copy(M))      #vers la
        if M[ligne+2,colonne]==2 and M[ligne-2,colonne]==2 and M[ligne,colonne-2]==2:
          direction=4
        else:
          direction=3
  return L


def droitier():
  L=[]
  direction=0
  compteur=0
  ligne,colonne=f,g
  L.append(np.copy(M))
  while (ligne!=2 or colonne!=m-3) and compteur<50000:
    compteur+=1
    if direction==0:                #il vient du bas (dirigé donc vers le haut)
      if M[ligne,colonne+2]==0:
        for k in range(1,5):
          M[ligne,colonne]=0
          colonne+=1
          M[ligne,colonne]=3
          L.append(np.copy(M))      #vers la droite
        direction=2
      elif M[ligne-2,colonne]==0:
        for k in range(1,5):
          M[ligne,colonne]=0
          ligne-=1
          M[ligne,colonne]=3
          L.append(np.copy(M))      #vers le haut
        direction=0
      elif M[ligne,colonne-2]==0:
        for k in range(1,5):
          M[ligne,colonne]=0
          colonne-=1
          M[ligne,colonne]=3
          L.append(np.copy(M))      #vers la gauche
        direction=3
      else:
        for k in range(1,5):
          M[ligne,colonne]=0
          ligne+=1
          M[ligne,colonne]=3
          L.append(np.copy(M))      #vers le bas
        direction=1


    if direction==2:                #il vient de la gauche (dirigé donc vers la droite)
      if M[ligne+2,colonne]==0:
        for k in range(1,5):
          M[ligne,colonne]=0
          ligne+=1
          M[ligne,colonne]=3
          L.append(np.copy(M))      #vers le bas
        direction=1
      elif M[ligne,colonne+2]==0:
        for k in range(1,5):
          M[ligne,colonne]=0
          colonne+=1
          M[ligne,colonne]=3
          L.append(np.copy(M))      #vers la droite
        direction=2
      elif M[ligne-2,colonne]==0:
        for k in range(1,5):
          M[ligne,colonne]=0
          ligne-=1
          M[ligne,colonne]=3
          L.append(np.copy(M))      #vers le haut
        direction=0
      elif M[ligne,colonne-2]==0:
        for k in range(1,5):
          M[ligne,colonne]=0
          colonne-=1
          M[ligne,colonne]=3
          L.append(np.copy(M))      #vers la gauche
        direction=3


    if direction==1:                #il vient du haut (dirigé donc vers le bas)
      if M[ligne,colonne-2]==0:
        for k in range(1,5):
          M[ligne,colonne]=0
          colonne-=1
          M[ligne,colonne]=3
          L.append(np.copy(M))      #vers la gauche
        direction=3
      elif M[ligne+2,colonne]==0:
        for k in range(1,5):
          M[ligne,colonne]=0
          ligne+=1
          M[ligne,colonne]=3
          L.append(np.copy(M))      #vers le bas
        direction=1
      elif M[ligne,colonne+2]==0:
        for k in range(1,5):
          M[ligne,colonne]=0
          colonne+=1
          M[ligne,colonne]=3
          L.append(np.copy(M))      #vers la droite
        direction=2
      elif M[ligne-2,colonne]==0:
        for k in range(1,5):
          M[ligne,colonne]=0
          ligne-=1
          M[ligne,colonne]=3
          L.append(np.copy(M))      #vers le haut
        direction=0


    if direction==3:                #il vient de la droite (dirigé donc vers le gauche)
      if M[ligne-2,colonne]==0:
        for k in range(1,5):
          M[ligne,colonne]=0
          ligne-=1
          M[ligne,colonne]=3
          L.append(np.copy(M))      #vers le haut
        direction=0
      elif M[ligne,colonne-2]==0:
        for k in range(1,5):
          M[ligne,colonne]=0
          colonne-=1
          M[ligne,colonne]=3
          L.append(np.copy(M))      #vers la gauche
        direction=3
      elif M[ligne+2,colonne]==0:
        for k in range(1,5):
          M[ligne,colonne]=0
          ligne+=1
          M[ligne,colonne]=3
          L.append(np.copy(M))      #vers le bas
        direction=1
      elif M[ligne,colonne+2]==0:
        for k in range(1,5):
          M[ligne,colonne]=0
          colonne+=1
          M[ligne,colonne]=3
          L.append(np.copy(M))      #vers la droite
        direction=2




  return L






def aupif_cartographe_eff():
  L=[]
  P=np.zeros((e,e),int)
  direction=0
  compteur=0
  ldispo=[]
  ligne,colonne=f,g
  M[ligne,colonne]=3
  L.append(np.copy(M))
  while compteur<50000:
    compteur+=1
    if P[(ligne-2)//4,(colonne-2)//4]==0:
      P[(ligne-2)//4,(colonne-2)//4]=compter_chemins_dispos(P,ligne,colonne)


    if P[(ligne-2)//4,(colonne-2)//4]==1:
      while P[(ligne-2)//4,(colonne-2)//4]==1 and (ligne!=2 or colonne!=m-3):

        ldispo=[(M[ligne-2,colonne]==0),(M[ligne+2,colonne]==0),(M[ligne,colonne+2]==0),(M[ligne,colonne-2]==0)]
        p=0


        if ldispo[0]:
          if P[((ligne-2)//4)-1,(colonne-2)//4]==1:
            ldispo[0]=False
        if ldispo[1]:
          if P[((ligne-2)//4)+1,(colonne-2)//4]==1:
            ldispo[1]=False
        if ldispo[2]:
          if P[((ligne-2)//4),((colonne-2)//4)+1]==1:
            ldispo[2]=False
        if ldispo[3]:
          if P[((ligne-2)//4),((colonne-2)//4)-1]==1:
            ldispo[3]=False

        for k in range(len(ldispo)):
          if ldispo[k]:
            p=k

        if p==0:
          for k in range(1,5):
            M[ligne,colonne]=0
            ligne-=1
            M[ligne,colonne]=3
            L.append(np.copy(M))      #vers le haut
        if p==1:
          for k in range(1,5):
            M[ligne,colonne]=0
            ligne+=1
            M[ligne,colonne]=3
            L.append(np.copy(M))      #vers le bas
        if p==2:
          for k in range(1,5):
            M[ligne,colonne]=0
            colonne+=1
            M[ligne,colonne]=3
            L.append(np.copy(M))      #vers la droite
        if p==3:
          for k in range(1,5):
            M[ligne,colonne]=0
            colonne-=1
            M[ligne,colonne]=3
            L.append(np.copy(M))      #vers la gauche
        P[(ligne-2)//4,(colonne-2)//4]=compter_chemins_dispos(P,ligne,colonne)

    if ligne==2 and colonne==m-3:
      print("Réussi !")
      return L

    ldispo=[(M[ligne-2,colonne]==0 and direction!=1),(M[ligne+2,colonne]==0 and direction!=0),(M[ligne,colonne+2]==0 and direction!=3),(M[ligne,colonne-2]==0 and direction!=2)]

    if ldispo[0]:
      if P[((ligne-2)//4)-1,(colonne-2)//4]==1:
        ldispo[0]=False
    if ldispo[1]:
      if P[((ligne-2)//4)+1,(colonne-2)//4]==1:
        ldispo[1]=False
    if ldispo[2]:
      if P[((ligne-2)//4),((colonne-2)//4)+1]==1:
        ldispo[2]=False
    if ldispo[3]:
      if P[((ligne-2)//4),((colonne-2)//4)-1]==1:
        ldispo[3]=False

    machin=0
    for k in ldispo:
      if k:
        machin+=1
    r=rd.randint(0,machin-1)

    S=-1
    p=0
    for k in range(len(ldispo)):
      if ldispo[k]:
        S+=1
      if S==r:
        p=k
        break



    if p==0:
      for k in range(1,5):
        M[ligne,colonne]=0
        ligne-=1
        M[ligne,colonne]=3
        L.append(np.copy(M))      #vers le haut
      if M[ligne-2,colonne]==2 and M[ligne,colonne+2]==2 and M[ligne,colonne-2]==2:
        direction=4
      else:
        direction=0
    if p==1:
      for k in range(1,5):
        M[ligne,colonne]=0
        ligne+=1
        M[ligne,colonne]=3
        L.append(np.copy(M))      #vers le bas
      if M[ligne+2,colonne]==2 and M[ligne,colonne+2]==2 and M[ligne,colonne-2]==2:
        direction=4
      else:
        direction=1
    if p==2:
      for k in range(1,5):
        M[ligne,colonne]=0
        colonne+=1
        M[ligne,colonne]=3
        L.append(np.copy(M))      #vers la droite
      if M[ligne+2,colonne]==2 and M[ligne-2,colonne]==2 and M[ligne,colonne+2]==2:
        direction=4
      else:
        direction=2
    if p==3:
      for k in range(1,5):
        M[ligne,colonne]=0
        colonne-=1
        M[ligne,colonne]=3
        L.append(np.copy(M))      #vers la
      if M[ligne+2,colonne]==2 and M[ligne-2,colonne]==2 and M[ligne,colonne-2]==2:
        direction=4
      else:
        direction=3

  return L







def aupif_cart_eff_curieux():
  L=[]
  P=np.zeros((e,e),int)
  direction=0
  compteur=0
  ldispo=[]
  ligne,colonne=f,g
  M[ligne,colonne]=3
  L.append(np.copy(M))
  while compteur<50000:
    compteur+=1
    if P[(ligne-2)//4,(colonne-2)//4]==0:
      P[(ligne-2)//4,(colonne-2)//4]=compter_chemins_dispos(P,ligne,colonne)


    if P[(ligne-2)//4,(colonne-2)//4]==1:
      while P[(ligne-2)//4,(colonne-2)//4]==1 and (ligne!=2 or colonne!=m-3):

        ldispo=[(M[ligne-2,colonne]==0),(M[ligne+2,colonne]==0),(M[ligne,colonne+2]==0),(M[ligne,colonne-2]==0)]
        p=0


        if ldispo[0]:
          if P[((ligne-2)//4)-1,(colonne-2)//4]==1:
            ldispo[0]=False
        if ldispo[1]:
          if P[((ligne-2)//4)+1,(colonne-2)//4]==1:
            ldispo[1]=False
        if ldispo[2]:
          if P[((ligne-2)//4),((colonne-2)//4)+1]==1:
            ldispo[2]=False
        if ldispo[3]:
          if P[((ligne-2)//4),((colonne-2)//4)-1]==1:
            ldispo[3]=False

        for k in range(len(ldispo)):
          if ldispo[k]:
            p=k

        if p==0:
          for k in range(1,5):
            M[ligne,colonne]=0
            ligne-=1
            M[ligne,colonne]=3
            L.append(np.copy(M))      #vers le haut
        if p==1:
          for k in range(1,5):
            M[ligne,colonne]=0
            ligne+=1
            M[ligne,colonne]=3
            L.append(np.copy(M))      #vers le bas
        if p==2:
          for k in range(1,5):
            M[ligne,colonne]=0
            colonne+=1
            M[ligne,colonne]=3
            L.append(np.copy(M))      #vers la droite
        if p==3:
          for k in range(1,5):
            M[ligne,colonne]=0
            colonne-=1
            M[ligne,colonne]=3
            L.append(np.copy(M))      #vers la gauche
        P[(ligne-2)//4,(colonne-2)//4]=compter_chemins_dispos(P,ligne,colonne)

    if ligne==2 and colonne==m-3:
      print("Réussi !")
      print(compteur)
      return L

    ldispo=[(M[ligne-2,colonne]==0 and direction!=1),(M[ligne+2,colonne]==0 and direction!=0),(M[ligne,colonne+2]==0 and direction!=3),(M[ligne,colonne-2]==0 and direction!=2)]

    nombre_zeros=0
    if ldispo[0]:
      if P[((ligne-2)//4)-1,(colonne-2)//4]==1:
        ldispo[0]=False
      elif P[((ligne-2)//4)-1,(colonne-2)//4]==0:
        nombre_zeros+=1
    if ldispo[1]:
      if P[((ligne-2)//4)+1,(colonne-2)//4]==1:
        ldispo[1]=False
      elif P[((ligne-2)//4)+1,(colonne-2)//4]==0:
        nombre_zeros+=1
    if ldispo[2]:
      if P[((ligne-2)//4),((colonne-2)//4)+1]==1:
        ldispo[2]=False
      elif P[((ligne-2)//4),((colonne-2)//4)+1]==0:
        nombre_zeros+=1
    if ldispo[3]:
      if P[((ligne-2)//4),((colonne-2)//4)-1]==1:
        ldispo[3]=False
      elif P[((ligne-2)//4),((colonne-2)//4)-1]==0:
        nombre_zeros+=1




    machin=0
    for k in ldispo:
      if k:
        machin+=1

    S=-1
    p=0
    if nombre_zeros>0:
      r=rd.randint(0,nombre_zeros-1)
      if ldispo[0]:
        if P[((ligne-2)//4)-1,(colonne-2)//4]==0:
          S+=1
          if S==r:
            p=0
      if ldispo[1]:
        if P[((ligne-2)//4)+1,(colonne-2)//4]==0:
          S+=1
          if S==r:
            p=1
      if ldispo[2]:
        if P[((ligne-2)//4),((colonne-2)//4)+1]==0:
          S+=1
          if S==r:
            p=2
      if ldispo[3]:
        if P[((ligne-2)//4),((colonne-2)//4)-1]==0:
          S+=1
          if S==r:
            p=3
    else:
      r=rd.randint(0,machin-1)
      for k in range(len(ldispo)):
        if ldispo[k]:
          S+=1
        if S==r:
          p=k
          break


    if p==0:
      for k in range(1,5):
        M[ligne,colonne]=0
        ligne-=1
        M[ligne,colonne]=3
        L.append(np.copy(M))      #vers le haut
      if M[ligne-2,colonne]==2 and M[ligne,colonne+2]==2 and M[ligne,colonne-2]==2:
        direction=4
      else:
        direction=0
    if p==1:
      for k in range(1,5):
        M[ligne,colonne]=0
        ligne+=1
        M[ligne,colonne]=3
        L.append(np.copy(M))      #vers le bas
      if M[ligne+2,colonne]==2 and M[ligne,colonne+2]==2 and M[ligne,colonne-2]==2:
        direction=4
      else:
        direction=1
    if p==2:
      for k in range(1,5):
        M[ligne,colonne]=0
        colonne+=1
        M[ligne,colonne]=3
        L.append(np.copy(M))      #vers la droite
      if M[ligne+2,colonne]==2 and M[ligne-2,colonne]==2 and M[ligne,colonne+2]==2:
        direction=4
      else:
        direction=2
    if p==3:
      for k in range(1,5):
        M[ligne,colonne]=0
        colonne-=1
        M[ligne,colonne]=3
        L.append(np.copy(M))      #vers la
      if M[ligne+2,colonne]==2 and M[ligne-2,colonne]==2 and M[ligne,colonne-2]==2:
        direction=4
      else:
        direction=3

  return L





start_time=time.time()
liste_matrice=aupif_cart_eff_curieux()
print (time.time()-start_time, " secondes")
print(len(liste_matrice))





def generateur_matrices(Frame=0):
        return liste_matrice[Frame]

plt.style.use('seaborn-pastel')
def maj(Frame):
    mat.set_data(generateur_matrices(Frame))
    return


fig, ax = plt.subplots()
mat = ax.matshow(generateur_matrices())
anim = ani.FuncAnimation(fig, maj, interval=10, frames=len(liste_matrice))
plt.show()
