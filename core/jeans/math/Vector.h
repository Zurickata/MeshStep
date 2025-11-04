#ifndef __CVector__
#define __CVector__



#include <math.h>
#include "Matrix.h"



class CVector : public CMatrix
{
public:

	// Construction / destruction
	CVector();
	CVector( const CVector & p_V );
	CVector( int p_H );
	CVector( int p_H, double p_0, .../*,1,2,3..*/ );
	virtual ~CVector();

	// Sizing
	bool SetDims( int p_H/*ROWS*/, int p_W/*COLS*/ );
	bool SetDim( int p_H );

	// Access
	double & Elt( int p_I );
	const double & Elt( int p_I ) const;
	bool SubVectorTo( int p_FirstRow, int p_LastRow, CVector & p_To );

	// For 3D vectors
	double & X() { return Elt(0); }
	double & Y() { return Elt(1); }
	double & Z() { return Elt(2); }
	const double & X() const { return Elt(0); }
	const double & Y() const { return Elt(1); }
	const double & Z() const { return Elt(2); }

	// For 3D planes
	double & A() { return Elt(0); }
	double & B() { return Elt(1); }
	double & C() { return Elt(2); }
	double & D() { return Elt(3); }
	const double & A() const { return Elt(0); }
	const double & B() const { return Elt(1); }
	const double & C() const { return Elt(2); }
	const double & D() const { return Elt(3); }

	// Operations
	bool ScalProd( const CVector & p_B, double & p_Prod ) const;
	bool ExtrProd( const CVector & p_B, CMatrix & p_Prod ) const;
	bool CrossProd( const CVector & p_B, CVector & p_AxB ) const;
	double Norm2();
	bool Normalize();
	double Dist( const CVector & p_B ) const;

	// Static operators
	static bool MassCenter( const CContainer1<CVector> & pPts, CVector & pG );
};



#endif //__CVector__
