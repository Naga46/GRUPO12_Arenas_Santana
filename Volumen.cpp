#include <iostream>

using namespace std;

class Box {
	public:
		double length; 
		double breadth;
		double height;
};

int main() {
	Box Box1;
	Box Box2;
	double volume = 0.0;


//box1 specification
Box1.height = 5.0;
Box1.length = 5.0;
Box1.breadth = 5.0;

//box 2 specification

Box2.height = 2.0;
Box2.length = 2.0;
Box2.breadth = 2.0;

//Volume of box 1 
volume = Box1.height * Box1.length * Box1.breadth;
cout << "Volume of Box1 : " << volume << endl;

//volume of Box 2 

volume = Box2.height * Box2.length * Box2.breadth;
cout << "Volume of Box2 : " << volume <<endl;
return 0;
}
