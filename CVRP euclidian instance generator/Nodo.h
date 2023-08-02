#ifndef NODO_H_INCLUDED
#define NODO_H_INCLUDED

class Nodo{
public:
    Nodo(bool orig, int num, int x, int y);
    int getX(){return coordx;};
    int getY(){return coordy;};
    bool getOrigen(){return origen;};
    int getNum(){return number;};
    int getDemand(){return demand;};
private:
    int number;
    int coordx;
    int coordy;
    bool origen;
    int demand;
};

Nodo::Nodo(bool orig, int num, int x, int y){
    number = num;
    coordx = x;
    coordy = y;
    origen = orig;
    if(origen == true){
        demand = 0;
    } else {
        demand = (rand()%5)+1;
    }

}


#endif // NODO_H_INCLUDED
