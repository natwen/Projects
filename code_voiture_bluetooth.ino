#include <Servo.h>
#iclude <HCSR04.h>n
#include <SoftwareSerial.h>

SoftwareSerial serialBT(2,13); //(TxBT,RxBT) //création d'une deuxième voie série
bool mesure = false; //booléen qui va nous permettre de rentrer dans la boucle de prises de mesures ou non


#define enable_droit 5
#define direction_droit_A 3
#define direction_droit_B 4

#define enable_gauche 9 //PWM
#define direction_gauche_A 8
#define direction_gauche_B 7

char droite ='d';
char gauche ='g';
String avant="avant";
String arriere="arriere";

int receiver = 12;
int trigger = 11;
int pin_servo = 10;

HCSR04 sr04 = HCSR04(receiver,trigger);

Servo servo;
int pos_milieu=90;
int pos_droite=0;
int pos_gauche=180;
int pos[3] = {180,90,0};
long a = 0;
long distance[3] ={1,1,1};
int maxi;
int priorite=0;


void setup() {
   Serial.begin(9600);
   serialBT.begin(9600); //paramétrage de la deuxième voie série
   pinMode(enable_droit,OUTPUT);
   pinMode(direction_droit_A,OUTPUT);
   pinMode(direction_droit_B,OUTPUT);
   pinMode(enable_gauche,OUTPUT);
   pinMode(direction_gauche_A,OUTPUT);
   pinMode(direction_gauche_B,OUTPUT);
   servo.attach(pin_servo);
   delay(1000);
}

void loop() {
  //capteur position centrale

    {
        String messageRecu=""; //création d'une variable chaine de caractères
        while(serialBT.available()) //la fonction available renvoie de le nombre de caractères à lire donc tant qu'on a des caractères à lire on continue
        {
          delay(3);
          char c = serialBT.read();
          messageRecu += c; //on concatène 1 à 1 les caractères de la chaine reçu depuis le portable à la variable messageRecu
        }
        if (messageRecu.length() >0)
        {
            Serial.println(messageRecu);
                if (messageRecu == "marche")
                {  
                    mesure = true;
                    serialBT.println("Roule Ginette !");
                }
                else if (messageRecu == "arret")
                {    
                  arret();
                  mesure = false;
                  serialBT.println("Au dodo Ginette");
                }
           }
    }

  if(mesure) {  
  servo.write(pos[1]);
  delay(500);
  a=sr04.dist();
  
  delay(125);
  if(a>20){
    avancer(125);
    serialBT.println("avance"); //remplacement des Serial.println par serialBT pour envoyer sur la bonne voie série ie le module bluetooth/téléphone
  }
  else{
    arret();
    //prise des distances
    for(int i = 0; i<3 ; i++){
      servo.write(pos[i]);
      delay(500);
      distance[i]=sr04.dist();
      delay(500);
     }

      if(distance[priorite]>=15){
        tourner(direction_priorite(priorite));
        //serialBT.println((String)direction_priorite(priorite));
        priorite=non_priorite(priorite);
        
        delay(125);
      }else if(distance[non_priorite(priorite)]>=15){
        tourner(direction_priorite(non_priorite(priorite)));
        //serialBT.println((String)direction_priorite(non_priorite(priorite)));
        delay(125);
      }else{
      demitour();
      serialBT.println("demitour");
     }
     
     
    serialBT.print("Gauche ");
    serialBT.println((String)distance[0]);
    serialBT.print("Droite ");
    serialBT.println((String)distance[1]);
    serialBT.print("Centre ");
    serialBT.println((String)distance[2]); 
  
  }
  }
  }

void demitour(){
  reculer();
  delay(1200);
  tourner(droite);
  delay(350);
}
void tourner(char d){
  if(d==droite){
      digitalWrite(enable_droit,HIGH);
      sens_rotation(droite,arriere);
  
      digitalWrite(enable_gauche,HIGH);
      sens_rotation(gauche,avant);
  
  }else if(d==gauche){
      digitalWrite(enable_droit,HIGH);
      sens_rotation(droite,avant);
  
      digitalWrite(enable_gauche,HIGH);
      sens_rotation(gauche,arriere);
  }
}
void avancer(int puissance){
  digitalWrite(enable_droit,puissance); //plutôt analogWrite
  sens_rotation(droite,avant);
  
  digitalWrite(enable_gauche,puissance); //idem
  sens_rotation(gauche,avant);

}
void reculer(){
  digitalWrite(enable_droit,HIGH);
  sens_rotation(droite,arriere);
  
  digitalWrite(enable_gauche,HIGH);
  sens_rotation(gauche,arriere);

}
void arret(){
  digitalWrite(enable_droit,LOW);
  digitalWrite(enable_gauche,LOW);
}
void sens_rotation(char pos,String direc){
  if(pos=='r' or pos =='d'){//right ou droite
    if(direc=="avant"){
      digitalWrite(direction_droit_A,LOW);
      digitalWrite(direction_droit_B,HIGH);
    }else{
      digitalWrite(direction_droit_A,HIGH);
      digitalWrite(direction_droit_B,LOW);
    }
  }else if(pos=='l' or pos=='g'){//left ou gauche
    if(direc=="avant"){
      digitalWrite(direction_gauche_A,LOW);
      digitalWrite(direction_gauche_B,HIGH);
    }else{
      digitalWrite(direction_gauche_A,HIGH);
      digitalWrite(direction_gauche_B,LOW);
    }
  }
}
void mouvement(int vitesse_droite, String sens_droite, int vitesse_gauche, String sens_gauche){
  digitalWrite(enable_droit, vitesse_droite);
  digitalWrite(enable_gauche, vitesse_gauche);
  sens_rotation(droite,sens_droite);
  sens_rotation(gauche, sens_gauche);
  
}
char direction_priorite(int prio){
  if(prio == 0){
    return(gauche);
  }else{
    return(droite);

  }
}
int non_priorite(int prio){
  if(prio==0){
    return(2);
  }else{
    return(0);
  }
}
