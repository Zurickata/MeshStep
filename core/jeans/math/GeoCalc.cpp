#include "stdafx.h"
#include <float.h>
#include "GeoCalc.h"
#include "Vector.h"




//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CGeoCalc::PlaneCut( const CVector & pP1, const CVector & pP2, CVector & pDir, CVector & pRoot )
{
	// Check dims
	if( pP1.Rows()!=4 || pP2.Rows()!=4 )
	{
		LOGERR("[CGeoCalc::PlaneCut] : Invalid plane equations : dims !");
		return false;
	}

	// Check norms
	static CVector N1( 3, 0.0,0.0,0.0 );
	N1.X() = pP1.A();
	N1.Y() = pP1.B();
	N1.Z() = pP1.C();

	static CVector N2( 3, 0.0,0.0,0.0 );
	N2.X() = pP2.A();
	N2.Y() = pP2.B();
	N2.Z() = pP2.C();

	double NormN1 = sqrt(N1.Norm2());
	double NormN2 = sqrt(N2.Norm2());
	if( NormN1<DBL_EPSILON || NormN2<DBL_EPSILON )
	{
		LOGERR("[CGeoCalc::PlaneCut] : Invalid plane equations : norms !");
		return false;
	}

	// Compute intersection direction
	N1.CrossProd( N2, pDir );

	// Check planes non parallel
	if( sqrt(pDir.Norm2()) < DBL_EPSILON )
	{
		// No error
		return false;
	}

	// Project origin onto P1
	static CVector O1;
	N1.Mult( -pP1.D()/(NormN1*NormN1), O1 );

	// Compute 2nd projection direction
	static CVector N4;
	pDir.CrossProd( N1, N4 );

	// Project O1 onto P2
	double N2scalN4;
	N2.ScalProd( N4, N2scalN4 );
	double K = -(pP2.A()*O1.X()+pP2.B()*O1.Y()+pP2.C()*O1.Z()+pP2.D()) / N2scalN4;

	// Set root 
	pRoot.SetDim( 3 );
	pRoot.X() = O1.X() + K*N4.X();
	pRoot.Y() = O1.Y() + K*N4.Y();
	pRoot.Z() = O1.Z() + K*N4.Z();

	// Normalize dir
	pDir.Normalize();

	return true;
}

