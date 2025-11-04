//#include "stdafx.h"
#include "Polynom.h"
//#include <Services/Log.h>
#include <float.h>
#include <math.h>
#include "Vector.h"



//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
static inline int MAX( int A, int B ) { return A > B ? A : B ; }

// What is zero and what is not ....
const double CPolynom::TOLERANCE = 1e-15;

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
const CPolynom CPolynom::XYZ( 1, 1, 1, 1 );
const CPolynom CPolynom::XY ( 1, 1, 0, 1 );
const CPolynom CPolynom::XZ ( 1, 0, 1, 1 );
const CPolynom CPolynom::YZ ( 0, 1, 1, 1 );
const CPolynom CPolynom::X  ( 1, 0, 0, 1 );
const CPolynom CPolynom::Y  ( 0, 1, 0, 1 );
const CPolynom CPolynom::Z  ( 0, 0, 1, 1 );

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
CPolynom::CPolynom()
{
	// Init polynom
	m_pCoefs = NULL;

	// Default polynom is P(x,y,z) = 0
	SetDegs(0,0,0);
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
CPolynom::CPolynom( int p_DegX, int p_DegY, int p_DegZ, double p_Coef )
{
	// Init polynom
	m_pCoefs = NULL;
	SetDegs( p_DegX, p_DegY, p_DegZ );
	Monom( p_DegX, p_DegY, p_DegZ) = p_Coef;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
CPolynom::CPolynom( const CPolynom & p_Poly )
{
	// Init polynom
	m_pCoefs = NULL;
	*this = p_Poly;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
CPolynom::CPolynom( double p_Monom0 )
{
	// Init polynom
	m_pCoefs = NULL;
	*this = p_Monom0;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
CPolynom::~CPolynom()
{
	Free();
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
void CPolynom::Free()
{
	if( m_pCoefs )
	{
		delete[] m_pCoefs;
		m_pCoefs = NULL;
		m_Monoms = 0;
	}
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
void CPolynom::SetDegs( int p_DegX, int p_DegY, int p_DegZ )
{
	if( p_DegX<0 || p_DegY<0 || p_DegZ<0 )
	{
		LOGERR("[CPolynom::SetDeg] : Trying to set negative deg !");
		p_DegX = p_DegY = p_DegZ = 0;
	}

	Free();

	// Init polynom
	m_DegX = p_DegX;
	m_DegY = p_DegY;
	m_DegZ = p_DegZ;

	m_Monoms = (m_DegX+1)*(m_DegY+1)*(m_DegZ+1);
	m_pCoefs = new double [ m_Monoms ];

	// Reset polynom
	for( int i=0 ; i<m_Monoms ; i++ )
	{
		m_pCoefs[i] = 0;
	}
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
double & CPolynom::Monom( int p_DegX, int p_DegY, int p_DegZ )
{
	static double beast = 666.666;
	if( p_DegX<0      || p_DegY<0      || p_DegZ<0
	 || p_DegX>m_DegX || p_DegY>m_DegY || p_DegZ>m_DegZ )
	{
		LOGERR("[CPolynom::Monom] : Degree overflow ! My degs=(%d,%d,%d)",m_DegX,m_DegY,m_DegZ);
		return beast;
	}

	// Get monom
	return m_pCoefs[ p_DegX + (m_DegX+1)*(p_DegY+(m_DegY+1)*p_DegZ) ];
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
const double & CPolynom::Monom( int p_DegX, int p_DegY, int p_DegZ ) const
{
	return ((CPolynom*)this)->Monom(p_DegX,p_DegY,p_DegZ);
}


////////////////////////////////////////////////////////////////////////////////
//
// Operators
//
//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
CPolynom CPolynom::operator*( double p_Scal ) const
{
	CPolynom l_Res;
	
	l_Res.SetDegs( m_DegX, m_DegY, m_DegZ );

	for( int i=0 ; i<m_Monoms ; i++ )
	{
		l_Res.m_pCoefs[i] = p_Scal * m_pCoefs[i];
	}

	return l_Res;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
CPolynom CPolynom::operator/( double p_Scal ) const
{
	CPolynom l_Res;

	// Division by 0 ?
	if( fabs(p_Scal) < TOLERANCE )
	{
		LOGERR("[CPolynom::operator/] : Division by 0 !");
		return l_Res;
	}
	
	l_Res.SetDegs( m_DegX, m_DegY, m_DegZ );

	for( int i=0 ; i<m_Monoms ; i++ )
	{
		l_Res.m_pCoefs[i] = m_pCoefs[i] / p_Scal;
	}

	return l_Res;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
CPolynom CPolynom::operator*( const CPolynom & p_Poly ) const
{
	CPolynom l_Res;
	
	l_Res.SetDegs( m_DegX+p_Poly.m_DegX, m_DegY+p_Poly.m_DegY, m_DegZ+p_Poly.m_DegZ );

	for( int x1=0 ; x1<=m_DegX ; x1++ )
	for( int y1=0 ; y1<=m_DegY ; y1++ )
	for( int z1=0 ; z1<=m_DegZ ; z1++ )
	{
		for( int x2=0 ; x2<=p_Poly.m_DegX ; x2++ )
		for( int y2=0 ; y2<=p_Poly.m_DegY ; y2++ )
		for( int z2=0 ; z2<=p_Poly.m_DegZ ; z2++ )
		{
			l_Res.Monom(x1+x2,y1+y2,z1+z2) += Monom(x1,y1,z1)*p_Poly.Monom(x2,y2,z2);
		}
	}

	return l_Res;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
CPolynom CPolynom::operator+( double p_Scal ) const
{
	CPolynom l_Res;

	l_Res = *this;
	l_Res.m_pCoefs[0] += p_Scal;

	return l_Res;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
CPolynom CPolynom::operator-( double p_Scal ) const
{
	CPolynom l_Res;

	l_Res = *this;
	l_Res.m_pCoefs[0] -= p_Scal;

	return l_Res;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
CPolynom CPolynom::operator+( const CPolynom & p_Poly ) const
{
	CPolynom l_Res;

	l_Res.SetDegs( MAX(m_DegX,p_Poly.m_DegX), MAX(m_DegY,p_Poly.m_DegY), MAX(m_DegZ,p_Poly.m_DegZ) );
		
	for( int x=0 ; x<l_Res.m_DegX+1 ; x++ )
	for( int y=0 ; y<l_Res.m_DegY+1 ; y++ )
	for( int z=0 ; z<l_Res.m_DegZ+1 ; z++ )
	{
		if( x<m_DegX+1 && y<m_DegY+1 && z<m_DegZ+1 )
			l_Res.Monom(x,y,z) += Monom(x,y,z);

		if( x<p_Poly.m_DegX+1 && y<p_Poly.m_DegY+1 && z<p_Poly.m_DegZ+1 )
			l_Res.Monom(x,y,z) += p_Poly.Monom(x,y,z);
	}

	return l_Res;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
CPolynom CPolynom::operator-( const CPolynom & p_Poly ) const
{
	CPolynom l_Res;

	l_Res.SetDegs( MAX(m_DegX,p_Poly.m_DegX), MAX(m_DegY,p_Poly.m_DegY), MAX(m_DegZ,p_Poly.m_DegZ) );

	for( int x=0 ; x<l_Res.m_DegX+1 ; x++ )
	for( int y=0 ; y<l_Res.m_DegY+1 ; y++ )
	for( int z=0 ; z<l_Res.m_DegZ+1 ; z++ )
	{
		if( x<m_DegX+1 && y<m_DegY+1 && z<m_DegZ+1 )
			l_Res.Monom(x,y,z) += Monom(x,y,z);

		if( x<p_Poly.m_DegX+1 && y<p_Poly.m_DegY+1 && z<p_Poly.m_DegZ+1 )
			l_Res.Monom(x,y,z) -= p_Poly.Monom(x,y,z);
	}

	return l_Res;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
//CPolynom & CPolynom::operator+=( const CPolynom & p_Poly )
//{
//	*this = *this + p_Poly;
//	return *this;
//}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
CPolynom & CPolynom::operator=( const CPolynom & p_Poly )
{
	SetDegs( p_Poly.m_DegX, p_Poly.m_DegY, p_Poly.m_DegZ );

	for( int i=0 ; i<m_Monoms ; i++ )
	{
		m_pCoefs[i] = p_Poly.m_pCoefs[i];
	}

	return *this;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
CPolynom & CPolynom::operator=( double p_Monom0 )
{
	SetDegs( 0, 0, 0 );
	m_pCoefs[0] = p_Monom0;
	return *this;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
static const CPolynom One = 1;
CPolynom CPolynom::PolPow( int Pow ) const
{
	if( Pow )
		return (*this) * PolPow(Pow-1);
	else
		return One;
}


////////////////////////////////////////////////////////////////////////////////
//
// Evaluation
//
//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
// pow( double x, double y ) as defined in <math.h> is much slower for integer powers
static double IntPow( double X, int N )
{
	double lRes = 1;
	while( N )
	{
		lRes *= X;
		N--;
	}

	return lRes;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
double CPolynom::EvalAt( double X, double Y ) const
{
	double Res = 0;

	for( int x=0 ; x<m_DegX+1 ; x++ )
	for( int y=0 ; y<m_DegY+1 ; y++ )
	{
		Res += Monom(x,y,0) * IntPow(X,x) * IntPow(Y,y);
	}

	return Res;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
double CPolynom::EvalAt( double X, double Y, double Z ) const
{
	double Res = 0;

	for( int x=0 ; x<m_DegX+1 ; x++ )
	for( int y=0 ; y<m_DegY+1 ; y++ )
	for( int z=0 ; z<m_DegZ+1 ; z++ )
	{
		Res += Monom(x,y,z) * IntPow(X,x) * IntPow(Y,y) * IntPow(Z,z);
	}

	return Res;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
double CPolynom::EvalAt( const CVector & pPt3D ) const
{
	// Are we in 3D ?
	if( pPt3D.Rows()!=3 || pPt3D.Cols()!=1 )
	{
		LOGERR("[CPolynom::EvalAt] : CVector is not a 3D vector !");
		return -666e+66;
	}

	return EvalAt( pPt3D.Elt(0), pPt3D.Elt(1), pPt3D.Elt(2) );
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CPolynom::IsZero( double tol/*=TOLERANCE*/ ) const
{
	for( int x=0 ; x<m_DegX+1 ; x++ )
	for( int y=0 ; y<m_DegY+1 ; y++ )
	for( int z=0 ; z<m_DegZ+1 ; z++ )
	{
		if( fabs(Monom(x,y,z)) >= tol )
			return false;
	}

	return true;
}


////////////////////////////////////////////////////////////////////////////////
//
// Composition
//
//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
CPolynom CPolynom::Compose( const CPolynom & PolX, const CPolynom & PolY, const CPolynom & PolZ ) const
{
	CPolynom Res;

	// Sum for all monoms
	for( int x=0 ; x<m_DegX+1 ; x++ )
	for( int y=0 ; y<m_DegY+1 ; y++ )
	for( int z=0 ; z<m_DegZ+1 ; z++ )
	{
		// If monom non null
		double Coef = Monom(x,y,z);

		if( fabs(Coef) > TOLERANCE )
		{
			Res = Res + Coef * PolX.PolPow(x) * PolY.PolPow(y) * PolZ.PolPow(z);
		}
	}

	return Res;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
CPolynom CPolynom::Compose( const CPolynom & PolX, const CPolynom & PolY ) const
{
	CPolynom Res;

	// Sum for all monoms
	for( int x=0 ; x<m_DegX+1 ; x++ )
	for( int y=0 ; y<m_DegY+1 ; y++ )
	{
		// If monom non null
		double Coef = Monom(x,y,0);

		if( fabs(Coef) > TOLERANCE )
		{
			Res = Res + Coef * PolX.PolPow(x) * PolY.PolPow(y);
		}
	}

	return Res;
}


////////////////////////////////////////////////////////////////////////////////
//
// Derivation
//
//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
CPolynom CPolynom::DerX()
{
	int x,y,z;

	// Adjust degs
	int MaxDX = 0;
	int MaxDY = 0;
	int MaxDZ = 0;
	for( x=1 ; x<m_DegX+1 ; x++ )
	for( y=0 ; y<m_DegY+1 ; y++ )
	for( z=0 ; z<m_DegZ+1 ; z++ )
	{
		if( fabs(Monom(x,y,z)) > TOLERANCE )
		{
			MaxDX = x;
			MaxDY = y>MaxDY ? y : MaxDY ;
			MaxDZ = z>MaxDZ ? z : MaxDZ ;
		}
	}

	// Check if X dependent
	if( !MaxDX )
		return 0;

	// Result
	CPolynom Res;
	Res.SetDegs( MaxDX-1, MaxDY, MaxDZ );

	// Init degs
	for( x=0 ; x<MaxDX   ; x++ )
	for( y=0 ; y<MaxDY+1 ; y++ )
	for( z=0 ; z<MaxDZ+1 ; z++ )
	{
		Res.Monom(x,y,z) = (x+1) * Monom(x+1,y,z);
	}

	return Res;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
CPolynom CPolynom::DerY()
{
	int x,y,z;

	// Adjust degs
	int MaxDX = 0;
	int MaxDY = 0;
	int MaxDZ = 0;
	for( x=0 ; x<m_DegX+1 ; x++ )
	for( y=1 ; y<m_DegY+1 ; y++ )
	for( z=0 ; z<m_DegZ+1 ; z++ )
	{
		if( fabs(Monom(x,y,z)) > TOLERANCE )
		{
			MaxDX = x;
			MaxDY = y>MaxDY ? y : MaxDY ;
			MaxDZ = z>MaxDZ ? z : MaxDZ ;
		}
	}

	// Check if Y dependent
	if( !MaxDY )
		return 0;

	// Result
	CPolynom Res;
	Res.SetDegs( MaxDX, MaxDY-1, MaxDZ );

	// Init degs
	for( x=0 ; x<MaxDX+1 ; x++ )
	for( y=0 ; y<MaxDY   ; y++ )
	for( z=0 ; z<MaxDZ+1 ; z++ )
	{
		Res.Monom(x,y,z) = (y+1) * Monom(x,y+1,z);
	}

	return Res;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
CPolynom CPolynom::DerZ()
{
	int x,y,z;

	// Adjust degs
	int MaxDX = 0;
	int MaxDY = 0;
	int MaxDZ = 0;
	for( x=0 ; x<m_DegX+1 ; x++ )
	for( y=0 ; y<m_DegY+1 ; y++ )
	for( z=1 ; z<m_DegZ+1 ; z++ )
	{
		if( fabs(Monom(x,y,z)) > TOLERANCE )
		{
			MaxDX = x;
			MaxDY = y>MaxDY ? y : MaxDY ;
			MaxDZ = z>MaxDZ ? z : MaxDZ ;
		}
	}

	// Check if Z dependent
	if( !MaxDZ )
		return 0;

	// Result
	CPolynom Res;
	Res.SetDegs( MaxDX, MaxDY, MaxDZ-1 );

	// Init degs
	for( x=0 ; x<MaxDX+1 ; x++ )
	for( y=0 ; y<MaxDY+1 ; y++ )
	for( z=0 ; z<MaxDZ   ; z++ )
	{
		Res.Monom(x,y,z) = (z+1) * Monom(x,y,z+1);
	}

	return Res;
}


////////////////////////////////////////////////////////////////////////////////
//
// Integration
//
//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CPolynom::IntegralTo( int p_MaxDegX, int p_MaxDegY, int p_MaxDegZ, double * p_pSums, double & p_Res ) const
{
	// Check available info
	if( m_DegX>p_MaxDegX || m_DegY>p_MaxDegY || m_DegZ>p_MaxDegZ )
	{
		LOGERR("[CPolynom::IntegralTo] : Integration info not available for all my monoms ! My degs=(%d,%d,%d)",m_DegX,m_DegY,m_DegZ);		
		return false;
	}

	// Integration of all monoms
	p_Res = 0;
	for( int x=0 ; x<m_DegX+1 ; x++ )
	for( int y=0 ; y<m_DegY+1 ; y++ )
	for( int z=0 ; z<m_DegZ+1 ; z++ )
	{
		// If monom non null
		double Coef = Monom(x,y,z);

		if( fabs(Coef) > TOLERANCE )
		{
			p_Res = p_Res + Coef * p_pSums[ x + (p_MaxDegX+1)*(y + (p_MaxDegY+1)*z) ];
		}
	}

	return true;
}


////////////////////////////////////////////////////////////////////////////////
//
// Debug
//
//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
string CPolynom::ToString() const
{
	string Pol = "";

	for( int x=m_DegX ; x>=0 ; x-- )
	for( int y=m_DegY ; y>=0 ; y-- )
	for( int z=m_DegZ ; z>=0 ; z-- )
	{
		double CoefXYZ = Monom(x,y,z);

		if( CoefXYZ )
		{
			string MonomX;
			if( x )
			{
				if( x == 1)
					MonomX = "X";
				else{
					char word[256];
					sprintf( word, "X%d",x);
					//MonomX.assign( word );
                    MonomX = word;
				}
			}

			string MonomY;
			if( y )
			{
				if( y == 1)
					MonomY = "Y";
				else{
					char word[256];
					sprintf(word, "Y%d",y);
					//MonomX.assign( word );
                    MonomX = word;
				}
			}

			string MonomZ;
			if( z )
			{
				if( z == 1)
					MonomZ = "Z";
				else{
					char word[256];
					sprintf(word, "Z%d",z);
					//MonomX.assign( word );
                    MonomX = word;
				}
			}

			//if( Pol.GetLength() )
			if( Pol.size() )
				Pol += "+";

			string MonomXYZ;
			char word[512];
			sprintf(word, "(%lf)%s%s%s",CoefXYZ,
					MonomX.c_str(),
					MonomY.c_str(),
					MonomZ.c_str());
			//MonomX.assign( word );
            MonomX = word;
			Pol += MonomXYZ;
		}
	}

	//if( !Pol.size() )
    if (Pol=="") {
        Pol = "(0)";
    }
		
	return Pol;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
void CPolynom::Log( string p_Prefix/*=""*/ ) const
{
	LOGMSG("%s : (DX=%d,DY=%d,DZ=%d) = %s",p_Prefix.c_str(),m_DegX,
			m_DegY,m_DegZ,ToString().c_str());
}

