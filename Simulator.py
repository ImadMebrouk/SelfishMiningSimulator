from random import random
from math import exp
import numpy as np
from tkinter import *

# simulation de selfish mining 

# inputs :
#    q (alpha) (relative hashrate) 
#    gamma (fraction de mineur honetes qui construise sur un block d'un mineur malhonnete )
#    n nombre de cycles 

#output : 
        #  Time spent 
        #  nb of difficulty adjustement 
        # % of orphan blocks
        #  profitabilty ratio 

#AJUSTEMENT DIFFICULTE : TimeSpent for 2016 blocks/ 2016 *600

# fraction of hash power owned by selfish miner
alpha = ""#float(input("Enter Alpha: "))

# fraction of honest miners that build on selfish miner block in a tie.

gamma = "" #float(input("Enter Gamma: "))

#def ajustement(nbBlocks):
#    delta = nbBlocks*600*2016

def TimeSpent(NbSmBlocks, NbHmBlocks, q, delta): 
    # TIME SPENT: for hm : exp(p/to)  avec p = 1-q (ici q = alpha ) et To = 600 sec 
    #             for sm : exp(q/To)
    # 1ere phase : no*To * difficulté
    # no = 2016 
    # difficulte delta = Temps mis / Temps theorique (no*To)  no = nombre de cycle 
    #Temps d'ajout d'un bloc (10 minutes)
    To = 600.0;
    #p(Honest) et q(Selfish) avec q > 0.5
    p = (1-q)
    #Lambda
    lbda = ((To*delta)/p)
  
    HTime = lbda
    HTime = HTime * NbHmBlocks

    #delta en fonction de l'ajustement de difficulté
    STime = ((To*delta)/q)
    STime = STime* NbSmBlocks

    #Sno= somme des blocs honnetes et des blocs selfish
    TimeSpent = (HTime + STime) #/(60*60*24)

    return TimeSpent

def AdjustDifficulty(total_block,cycleTime,delta):
    #ajustement tous les 2016 blocks
        if(total_block !=0 and (total_block)%2016 == 0): #Ajustement de difficulté

          #  if(delta == 1):
           #   delta = cycleTime/(600*2016)
           
              #premier ajustement de difficulté

           # else: 
            newdelta = cycleTime/(600*2016)
            delta = delta/newdelta
                
                #ajustement de la difficulté : difficulté = difficulté/delta
            print("Temps moyen de minage d'un block avant l'ajustement de difficulté : "+ str((cycleTime/(60))/2016))
            cycleTime=0

            print("Nombre de blocks tous les 2016 itérations : " + str(total_block) )

            print("ajustement de difficulté :" + str(delta))

        return (delta,cycleTime)

def runsimulation(iter, alpha, gamma):
    #initialisation de la blockchain 
    delta = 1; 
    hmblocks = 0
    hmorphans = 0
    hmchain = 0
    smblocks = 0
    smorphans = 0
    smchain = 0
    TotalTime = 0
    CycleTime =0

    for _ in range(1, iter):
        # Invariants
        # La chaine de selfish mining est toujours plus longue ou égale à celle de honest mining    
        assert smchain >= hmchain
        # SM will never risk more than one block to a tie
        assert smchain != hmchain or smchain < 2
             
        if (random() < alpha):
            # SM found a block
            if smchain > 0 and smchain == hmchain:
                # SM publishes its chain to resolve tie.
                smchain = smchain + 1
                smblocks += smchain
                hmorphans += hmchain

                total_block =hmblocks+smblocks
               
                TotalTime += TimeSpent(smchain,0,alpha,delta)
                CycleTime += TimeSpent(smchain,0,alpha,delta)

                tupl = AdjustDifficulty(total_block,CycleTime,delta)
                delta = tupl[0]
                CycleTime = tupl[1]

                hmchain = 0
                smchain = 0
            else:
                # SM mines selfishly
                assert (smchain == 0 and hmchain == 0) or smchain > hmchain
                smchain = smchain + 1
        else:
            #Honest Minertrouve un block
            if smchain == 0:
                # HM publishes and SM builds on top
                assert hmchain == 0
                hmchain = hmchain + 1
                hmblocks += hmchain
                smorphans += smchain

                total_block =hmblocks+smblocks
               
                TotalTime += TimeSpent(0,hmchain,alpha,delta)
                CycleTime += TimeSpent(0,hmchain,alpha,delta)
            
                tupl = AdjustDifficulty(total_block,CycleTime,delta)
                delta = tupl[0]
                CycleTime = tupl[1]

                hmchain = 0
                smchain = 0

            elif (smchain == hmchain and random() < gamma):
                # In case of a tie, a fraction of HM may build on SM's chain
                # and this gets the longest published chain
                assert hmchain == 1
                smblocks += smchain
                hmorphans += hmchain

                hmblocks = hmblocks + 1

                total_block =hmblocks+smblocks

                TotalTime += TimeSpent(smchain,1,alpha,delta)
                CycleTime += TimeSpent(smchain,1,alpha,delta)
            
                tupl = AdjustDifficulty(total_block,CycleTime,delta)
                delta = tupl[0]
                CycleTime = tupl[1]

                hmchain = 0
                smchain = 0
                
            else:
                # HM builds on its own chain.
                hmchain = hmchain + 1
                if smchain == hmchain + 1:
                    # If SMs chain is longer by exactly 1,
                    # SM will publish his longer chain.
                    smblocks += smchain
                    hmorphans += hmchain

                    total_block =hmblocks+smblocks
                    
                    TotalTime += TimeSpent(smchain,0,alpha,delta)
                    CycleTime += TimeSpent(smchain,0,alpha,delta)

                    tupl = AdjustDifficulty(total_block,CycleTime,delta)
                    delta = tupl[0]
                    CycleTime = tupl[1]

                    hmchain = 0
                    smchain = 0

                if hmchain > smchain:
                    # if HM has longer chain, SM switches to it.
                    hmblocks += hmchain
                    smorphans += smchain

                    total_block =hmblocks+smblocks
                 
                    TotalTime += TimeSpent(0,hmchain,alpha,delta)
                    CycleTime += TimeSpent(0,hmchain,alpha,delta)    

                    tupl = AdjustDifficulty(total_block,CycleTime,delta)
                    delta = tupl[0]
                    CycleTime = tupl[1]

                    hmchain = 0
                    smchain = 0


    print("Resultat de la Simulation : \n")
    print("Variables : \n    Iterations: %d, \n    Alpha: %f, \n    gamma: %f" % (iter, alpha, gamma))
    print("\n")
    print("Temps Total : " + str(TotalTime/(60*60*24)) + " jours");
    print("Temps moyen de minage d'un block : " + str((TotalTime/(60))/total_block) + " minutes");
    nbdifficult = int((total_block /2016))
    print("Nombre d'ajustement de difficulté : "+  str(nbdifficult) )
    print("\n")
    print("Nombre de blocks sur la blockchain officielle : " + str(total_block));
    print("Selfish Minings: %d blocks, \n Honest Mining: %d blocks, \n ratio: %f" % (smblocks, hmblocks,smblocks / float(smblocks + hmblocks)))

    print("Ratio rentabilité du mineur malhonete: " + str(float(smblocks/total_block)))
    print("\n")
    print("Blocks Orphelins : \n  Selfish: %d, \n  Honest: %d, \n  ratio d'orphelins:  %f; SM: %f, HM: %f"
            % (smorphans, hmorphans,
               (smorphans + hmorphans) / float(smblocks + hmblocks + smorphans + hmorphans),
               smorphans / float(smblocks + smorphans),
               hmorphans / float(hmblocks + hmorphans)))
    print("   Blocks encore contestés : SM %d, HM %d"
            % (smchain, hmchain))
    print("-----------   \n")

#cycle = int(input("enter Cycle number"))
#runsimulation(cycle)

class Interface(Frame):
       
    def __init__(self, fenetre, **kwargs):
        Frame.__init__(self, fenetre, width=1000, height=2000, **kwargs)
        self.pack(fill=BOTH)
        
        menubar = Menu(fenetre)

        menu1 = Menu(menubar, tearoff=0)
        menu1.add_command(label="Voir la Documentation", command=ShowDocumentation)
         
        menu1.add_separator()
        menu1.add_command(label="Quitter", command=self.quit)
        menubar.add_cascade(label="Aide", menu=menu1)
        fenetre.config(menu= menubar)
           
        
        self.message = Label(self, text=" Bienvenue sur le simulateur de Selfish Mining \n")
        self.message.grid(row=1,column=1)

        
        self.alphalabel = Label(self, text="Alpha")
        self.alphalabel.grid(row=2,column=1)

        self.alpha = Spinbox(self, from_=0, to=50)
        self.alpha.grid(row=2,column=2)
        
        self.gammalabel = Label(self, text="Gamma")
        self.gammalabel.grid(row=3,column=1)

        self.gamma = Spinbox(self, from_=0, to=100)
        self.gamma.grid(row=3,column=2)

        self.iterationlabel = Label(self, text="Nombre d'itérations")
        self.iterationlabel.grid(row=4,column=1)

        self.iteration = Spinbox(self, from_=0, to=10000)
        self.iteration.grid(row=4,column=2)
        
        self.bouton_quitter = Button(self, text="Quit", command=self.quit)
        self.bouton_quitter.grid(row=5,column=2)
        
        self.bouton_cliquer = Button(self, text="Launch",command=Launch)
        self.bouton_cliquer.grid(row=5,column=1)

def Launch():
        alpha = float(interface.alpha.get())/100.0
        gamma = float(interface.gamma.get())/100.0
        runsimulation(int(interface.iteration.get()), alpha, gamma)

       
def ShowDocumentation():
     messagebox.showinfo("Documentation", "Bonjour ! Bienvenue sur la doc du simulateur de Selfish Mining \n Appuyez sur Entrer pour lancer le simulateur")


fenetre = Tk()
fenetre.title("Selfish Mining")
interface = Interface(fenetre)


interface.mainloop()
interface.destroy()
