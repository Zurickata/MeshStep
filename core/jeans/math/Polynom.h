#ifndef __CPolynom__
#define __CPolynom__

#include <string>

using namespace std;

class CVector;


//------------------------------------------------------------------------------
// POLYNOMS
//------------------------------------------------------------------------------
class CPolynom
{
public:
	
	// Construction / destruction
	CPolynom();
	CPolynom( int p_DegX, int p_DegY, int p_DegZ, double p_Coef );
	CPolynom( const CPolynom & p_Poly );
	CPolynom( double p_Monom0 );
	virtual ~CPolynom();

	// Set
	void SetDegs( int p_DegX, int p_DegY, int p_DegZ );
	double & Monom( int p_DegX, int p_DegY, int p_DegZ );
	const double & Monom( int p_DegX, int p_DegY, int p_DegZ ) const;

	// Operators
	CPolynom operator*( double p_Scal ) const;
	CPolynom operator/( double p_Scal ) const;
	friend CPolynom operator*( double p_Scal, const CPolynom & p_Poly ) { return p_Poly*p_Scal; }
	friend CPolynom operator+( double p_Scal, const CPolynom & p_Poly ) { return p_Poly+p_Scal; }
	friend CPolynom operator-( double p_Scal, const CPolynom & p_Poly ) { return p_Poly*(-1)+p_Scal; }
	friend CPolynom operator-( const CPolynom & p_Poly ) { return p_Poly*(-1); }
	CPolynom operator*( const CPolynom & p_Poly ) const;
	CPolynom operator+( double p_Scal ) const;
	CPolynom operator-( double p_Scal ) const;
	CPolynom operator+( const CPolynom & p_Poly ) const;
	CPolynom operator-( const CPolynom & p_Poly ) const;
//	CPolynom & operator+=( const CPolynom & p_Poly );
	CPolynom & operator=( const CPolynom & p_Poly );
	CPolynom & operator=( double p_Monom0 );
	CPolynom PolPow( int Pow ) const;

	// Evaluation
	double EvalAt( double X, double Y ) const;
	double EvalAt( double X, double Y, double Z ) const;
	double EvalAt( const CVector & pPt3D ) const;
	bool IsZero( double tol=TOLERANCE ) const;

	// Composition
	CPolynom Compose( const CPolynom & PolX, const CPolynom & PolY, const CPolynom & PolZ ) const;
	CPolynom Compose( const CPolynom & PolX, const CPolynom & PolY ) const;

	// Derivation
	CPolynom DerX();
	CPolynom DerY();
	CPolynom DerZ();

	// Integration
	bool IntegralTo( int p_MaxDegX, int p_MaxDegY, int p_MaxDegZ, double * p_pSums, double & p_Res ) const;

	// Monoms
	static const CPolynom XYZ;
	static const CPolynom XY;
	static const CPolynom XZ;
	static const CPolynom YZ;
	static const CPolynom X;
	static const CPolynom Y;
	static const CPolynom Z;

	// Debug
	string ToString() const;
	void Log( string p_Prefix="" ) const;

	// What is zero and what is not ....
	static const double TOLERANCE;


protected:

	void Free();
	
	int m_DegX;
	int m_DegY;
	int m_DegZ;

	int m_Monoms;

	double * m_pCoefs;
};



//------------------------------------------------------------------------------
#define _XYZ_ (CPolynom::XYZ)
#define _XY_  (CPolynom::XY)
#define _XZ_  (CPolynom::XZ)
#define _YZ_  (CPolynom::YZ)
#define _X_   (CPolynom::X)
#define _Y_   (CPolynom::Y)
#define _Z_   (CPolynom::Z)
//------------------------------------------------------------------------------



#endif //__CPolynom__
