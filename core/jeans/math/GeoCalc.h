#ifndef __CGeoCalc__
#define __CGeoCalc__



class CVector;



class CGeoCalc
{
public:

	//------------------------------------------------------------------------------
	// Computes plane intersection : pP1( A1, B1, C1, D1 ) / P1: A1x + B1y + C1z + D1 = 0
	// pDir and pRoot are 3D vectors direction and point on the solution axis
	// norm(pDir) = 1
	// return false if no intersection found or incorrect plane specification
	//------------------------------------------------------------------------------
	static bool PlaneCut( const CVector & pP1, const CVector & pP2, CVector & pDir, CVector & pRoot );




};


#endif //__CGeoCalc__
