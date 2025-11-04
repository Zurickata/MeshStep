//#include "stdafx.h"
#include "Vector.h"
//#include "Matrix.h"
//#include <Services\Log.h>



//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
CVector::CVector()
{
//	LOGMSG("CVector::CVector");
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
CVector::CVector( const CVector & p_V )
{
//	LOGMSG("CVector::CVector( const CVector & p_V )");

	//this->CVector::CVector(); // parent default constructor called

	*this = p_V;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
CVector::CVector( int p_H )
{
//	LOGMSG("CVector::CVector(int p_H=%d )",p_H);

	//this->CVector::CVector(); // parent default constructor called

	SetDim(p_H);
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
CVector::CVector( int p_H, double p_0, .../*,1,2,3..*/ )
{
//	LOGMSG("CVector::CVector( int p_H=%d, double p_0, .../*,1,2,3..*/ )",p_H);

	//this->CVector::CVector(); // parent default constructor called

	// Init matrix
	if( !CMatrix::SetDims(p_H,1) )
	{
		LOGERR("[CVector::CVector] : Could not set dims (%d) !",p_H);
		return;
	}

	Elt(0) = p_0;

	va_list l_List;
	va_start( l_List, p_0 );

	for( int i=1 ; i<p_H ; i++ )
	{
		Elt(i) = va_arg( l_List, double );
	}

	va_end( l_List );
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
CVector::~CVector()
{
//	LOGMSG("CVector::~CVector");
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CVector::SetDims( int p_H/*ROWS*/, int p_W/*COLS*/ )
{
//	LOGMSG("CVector::SetDims(H=%d,W=%d)",p_H,p_W);

	if( p_W > 1 )
		LOGERR("[CVector::SetDims] : Width=%d ignored ==> W=1 !",p_W);
	
	return CMatrix::SetDims( p_H, 1 );
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CVector::SetDim( int p_H )
{
//	LOGMSG("CVector::SetDim(H=%d)",p_H);

	return CMatrix::SetDims( p_H, 1 );
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
double & CVector::Elt( int p_I )
{
	return CMatrix::Elt( p_I, 0 );
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
const double & CVector::Elt( int p_I ) const
{
	return CMatrix::Elt( p_I, 0 );
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CVector::SubVectorTo( int p_FirstRow, int p_LastRow, CVector & p_To )
{
	// Ok ?
	if( p_FirstRow>p_LastRow
	 || p_FirstRow<0
	 || p_LastRow>=m_H )
	{
		LOGERR("[CVector::SubVectorTo] : Invalid range !");
		return false;
	}

	// Fill new matrix
	p_To.SetDim( p_LastRow-p_FirstRow+1 );
	for( int i=0 ; i<p_To.Rows() ; i++ )
	{
		p_To.Elt(i) = Elt( p_FirstRow+i );
	}

	return true;
}


////////////////////////////////////////////////////////////////////////////////
//
// Operations
//
//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CVector::ScalProd( const CVector & p_B, double & p_Prod ) const
{
	// Ok ?
	if( Rows() != p_B.Rows() )
	{
		LOGERR("[CVector::ProdScal] : Prod impossible (%d <> %d) !",Rows(),p_B.Rows());
		return false;
	}

	p_Prod = 0;
	for( int i=0 ; i<Rows() ; i++ )
		p_Prod += Elt(i) * p_B.Elt(i);

	return true;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CVector::ExtrProd( const CVector & p_B, CMatrix & p_Prod ) const
{
	// Ok ?
	if( !p_Prod.SetDims(Rows(),p_B.Rows()) )
	{
		LOGERR("[CVector::ProdExtr] : Prod impossible !");
		return false;
	}

	for( int i=0 ; i<p_Prod.Rows() ; i++ )
	for( int j=0 ; j<p_Prod.Cols() ; j++ )
		p_Prod.Elt(i,j) = Elt(i) * p_B.Elt(j);

	return true;
}
	
//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CVector::CrossProd( const CVector & p_B, CVector & p_AxB ) const
{
	// R3 vectors only
	if( Rows()!=3 || p_B.Rows()!=3 )
	{
		LOGERR("[CVector::CrossProd] : Prod impossible !");
		return false;
	}

	p_AxB.SetDim(3);
	p_AxB.Elt(0) = Elt(1)*p_B.Elt(2) - Elt(2)*p_B.Elt(1);
	p_AxB.Elt(1) = Elt(2)*p_B.Elt(0) - Elt(0)*p_B.Elt(2);
	p_AxB.Elt(2) = Elt(0)*p_B.Elt(1) - Elt(1)*p_B.Elt(0);

	return true;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
double CVector::Norm2()
{
	if( !m_H )
	{
		LOGERR("[CVector::Norm2] : EMPTY vector : norm2 = 0!");
		return 0;
	}

	double Norm2 = 0;
	for( int i=0 ; i<m_H ; i++ )
		Norm2 += Elt(i)*Elt(i);

	return Norm2;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CVector::Normalize()
{
	// Vector well defined ?
	if( !m_H )
	{
		LOGERR("[CVector::Normalize] : Could not normalize EMPTY vector !");
		return false;
	}

	double Norm2 = 0;
	for( int i=0 ; i<m_H ; i++ )
		Norm2 += Elt(i)*Elt(i);

	double Norm = sqrt(Norm2);
	if( fabs(Norm) < TOLERANCE )
	{
		LOGERR("[CVector::Normalize] : Could not normalize NULL vector !");
		return false;
	}

	for(int i=0 ; i<m_H ; i++ )
		Elt(i) /= Norm;

	return true;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
double CVector::Dist( const CVector & p_B ) const
{
	if( Rows() != p_B.Rows() )
	{
		LOGERR("[CVector::Dist] : Vectors do not have same dimension !");
		return false;
	}

	double Res2 = 0;

	for( int i=0 ; i<Rows() ; i++ )
	{
		double Delta = Elt(i) - p_B.Elt(i);
		Res2 += Delta*Delta;
	}

	return sqrt(Res2);
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CVector::MassCenter( const CContainer1<CVector> & pPts, CVector & pG )
{
	int lPtsCount = pPts.Width();

	// Check points
	if( !lPtsCount )
	{
		LOGERR("[CVector::MassCenter] : No points in set !");
		return false;
	}

	// Set dim
	int lDim = pPts[0].Rows();
	if( !pG.SetDim(lDim) )
	{
		LOGERR("[CVector::MassCenter] : Could not set dim !");
		return false;
	}

	// Sum up
	pG.LoadValue( 0 );
	for( int iP=0 ; iP<lPtsCount ; iP++ )
	{
		const CVector & lP = pPts[iP];

		if( lP.Rows() != lDim )
		{
			LOGERR("[CVector::MassCenter] : Dim error !");
			return false;
		}

		for( int i=0 ; i<lDim ; i++ )
			pG.Elt(i) += lP.Elt(i);
	}

	// Normalize
	for( int i=0 ; i<lDim ; i++ )
		pG.Elt(i) /= lPtsCount;

	return true;
}
