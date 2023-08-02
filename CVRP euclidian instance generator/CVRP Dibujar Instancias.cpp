#include <string>
#include <iostream>
#include "miniwin.h"
#include <sstream>
#include <fstream>
#include <stdlib.h>
#include <time.h>
#include <list>
#include <cmath>
#include "Nodo.h"

using namespace miniwin;
using namespace std;

list <Nodo*> nodos;
int counter = 1;
bool origen;

int pantalla[100][100] = {};

void blanco(int x, int y){
    if(counter == 1){
        color(ROJO);
        origen = true;
    } else {
        color(BLANCO);
        origen = false;
    }
	for(int i=0;i<5;i++){
		for(int j=0;j<5;j++){
			punto(x+i,y+j);
		}
	}
	pantalla[x/5][y/5] = 1;
	nodos.push_back(new Nodo(origen, counter, x/5, y/5));
	counter++;
}

//dibujar en la cuadricula
void dibujar_mouse(int x, int y){
	x=x-(x%5);
	y=y-(y%5);
	if(pantalla[x/5][y/5] != 1){
       blanco(x,y);
	}

}

void printInstance(){
    cout<<"numNodos = "<<counter-2<<endl<<endl;
    cout<<"costoNodos = [";
    for(list<Nodo*>::iterator it = nodos.begin(); it != nodos.end(); it++){
        int demand = (*it)->getDemand();
        if(it != nodos.begin()){
            cout<<", ";
        }
        cout<<demand;
    }
    cout<<"]"<<endl<<endl;
    cout<<"costoAristas = [";
    for(list<Nodo*>::iterator i = nodos.begin(); i != nodos.end(); i++){
        if(i != nodos.begin()){
            cout<<", "<<endl<<'\t'<<'\t';
        }
        cout<<"[";
        for(list<Nodo*>::iterator j = nodos.begin(); j!= nodos.end(); j++){
            if(j != nodos.begin()){
                cout<<", ";
            }
            float ix = (*i)->getX();
            float iy = (*i)->getY();
            float jx = (*j)->getX();
            float jy = (*j)->getY();
            float cost = sqrt(pow(ix-jx,2)+pow(iy-jy,2));
            cout<<cost;
        }
        cout<<"]";
    }
    cout<<"]"<<endl<<endl;
}


int main()
{
    srand(time(NULL));
	//imprime la pantalla en blanco
   vredimensiona(500,500);

   int x, y;
   int t=tecla();

   //ciclo while que mantiene el codigo corriendo mientras no se presione espacio
   while(t!=ESPACIO){
   	//seccion para detectar al raton y sus coordenadas
   	if(raton_dentro()==true){
   		if(raton_boton_izq()==true){
   			x=(int)raton_x();
   			y=(int)raton_y();
   			dibujar_mouse(x,y);
		   }

	   }
	refresca();
	t=tecla();
   }
    printInstance();


   vcierra();
    return 0;
}
