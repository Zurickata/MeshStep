//#include "stdafx.h"
#include "DiffMatrix.h"
//#include "Services\Log.h"
#include "../Math\Matrix.h"


//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
CDiffMatrix::CDiffMatrix()
{
	m_H = m_W = 0;
	m_pMat = NULL;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
CDiffMatrix::~CDiffMatrix()
{
	Free();
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
void CDiffMatrix::Free()
{
	if( m_pMat )
	{
		// Free
		for( int j=0 ; j<m_W ; j++ )
			delete [] m_pMat[j];

		delete m_pMat;
		m_pMat = NULL;
	}

	// Mark as freed
	m_H = m_W = 0;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
void CDiffMatrix::LoadEmpty()
{
	for( int i=0 ; i<m_H ; i++ )
	for( int j=0 ; j<m_W ; j++ )
	{
		Elt(i,j).DelAll();
	}
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
void CDiffMatrix::DeleteNulls()
{
	for( int i=0 ; i<m_H ; i++ )
	for( int j=0 ; j<m_W ; j++ )
	{
		CLst<CProd> & L = Elt(i,j);
		for( void * Pos=L.HeadPos() ; Pos ;)
		{
			void * NextPos = Pos;
			L.Next(NextPos);

			const CProd & P = L.GetAt(Pos);
			if( fabs(P.m_Coef) < 1e-20 )
				L.DelAt(Pos);

			Pos = NextPos;
		}
	}
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CDiffMatrix::SetDims( int p_H, int p_W )
{
	// Ok ?
	if( p_H<0 || p_W<0 )
	{
		LOGERR("[CDiffMatrix::SetDims] : Invalid dims !");
		return false;
	}

	// Same dims ?
	if( p_H==m_H && p_W==m_W )
		return true;

	// Free previous
	Free();

	// If not empty, allocate something
	if( p_H && p_W )
	{
		// Alloc
		m_pMat = new CLst<CProd> * [p_W];
		for( int j=0 ; j<p_W ; j++ )
			m_pMat[j] = new CLst<CProd> [p_H];

		// Keep
		m_H = p_H;
		m_W = p_W;
	}

	return true;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
static CLst<CDiffMatrix::CProd> ERR_ELT;
CLst<CDiffMatrix::CProd> & CDiffMatrix::Elt( int p_I, int p_J )
{
#ifdef _DEBUG
	// Ok ?
	if( p_I>=m_H || p_I<0
	 || p_J>=m_W || p_J<0 )
	{
		LOGERR("[CDiffMatrix::Elt] : Accessing invalid element (i=%d,j=%d) !",p_I,p_J);
		ERR_ELT.AddTail( _PROD_(666.666,-1,-1) );
		return ERR_ELT;
	}
#endif

	return m_pMat[p_J][p_I];
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
const CLst<CDiffMatrix::CProd> & CDiffMatrix::Elt( int p_I, int p_J ) const
{
#ifdef _DEBUG
	// Ok ?
	if( p_I>=m_H || p_I<0
	 || p_J>=m_W || p_J<0 )
	{
		LOGERR("[CDiffMatrix::Elt] : Accessing invalid element (i=%d,j=%d) !",p_I,p_J);
		ERR_ELT.AddTail( _PROD_(666.666,-1,-1) );
		return ERR_ELT;
	}
#endif

	return m_pMat[p_J][p_I];
}


////////////////////////////////////////////////////////////////////////////////
//
// Operations
//
//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CDiffMatrix::TransposeTo( CDiffMatrix & p_Res ) const
{
	if( !p_Res.SetDims(Cols(),Rows()) )
	{
		LOGERR("[CDiffMatrix::TransposeTo] : Dimension error !");
		return false;
	}

	for( int i=0 ; i<Rows() ; i++ )
	for( int j=0 ; j<Cols() ; j++ )
	{
		p_Res.Elt(j,i) = Elt(i,j);
	}

	return true;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CDiffMatrix::Mult( const CMatrix & p_A, CDiffMatrix & p_Res ) const
{
	// Ok ?
	if( !Rows() || !Cols() || p_A.Rows()!=Cols() || !p_A.Cols() )
	{
		LOGERR("[CDiffMatrix::Mult] : Unable to multiplicate !");
		return false;
	}

	// Dim
	p_Res.SetDims( Rows(), p_A.Cols() );

	for( int i=0 ; i<p_Res.Rows() ; i++ )
	for( int j=0 ; j<p_Res.Cols() ; j++ )
	{
		p_Res.Elt(i,j).DelAll();

		for( int k=0 ; k<Cols() ; k++ )
		{
			// Compute product of element Elt(i,k) * p_A.Elt(k,j)
			for( void * iPos=Elt(i,k).HeadPos() ; iPos ; Elt(i,k).Next(iPos) )
			{
				CProd P = Elt(i,k).GetAt(iPos);
				P.Mult( p_A.Elt(k,j) );
				p_Res.AddToElt( i, j, P );
			}	
		}
	}

	return true;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CDiffMatrix::Mult( const CDiffMatrix & p_A, CDiffMatrix & p_Res ) const
{
	// Ok ?
	if( !Rows() || !Cols() || p_A.Rows()!=Cols() || !p_A.Cols() )
	{
		LOGERR("[CDiffMatrix::Mult] : Unable to multiplicate !");
		return false;
	}

	// Dim
	p_Res.SetDims( Rows(), p_A.Cols() );

	for( int i=0 ; i<p_Res.Rows() ; i++ )
	for( int j=0 ; j<p_Res.Cols() ; j++ )
	{
		p_Res.Elt(i,j).DelAll();

		for( int k=0 ; k<Cols() ; k++ )
		{
			// Compute product of element Elt(i,k) * p_A.Elt(k,j)
			const CLst<CProd> & L0 =     Elt(i,k);
			const CLst<CProd> & L1 = p_A.Elt(k,j);

			for( void * iPos0=L0.HeadPos() ; iPos0 ; L0.Next(iPos0) )
			for( void * iPos1=L1.HeadPos() ; iPos1 ; L1.Next(iPos1) )
			{
				CProd P = L0.GetAt(iPos0);
				P.Mult( L1.GetAt(iPos1) );
				p_Res.AddToElt( i, j, P );
			}
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
void CDiffMatrix::Log( CString p_Prefix/*=""*/ ) const
{
	if( !m_H )
	{
		LOGMSG("%s [.] = empty matrix",p_Prefix);
	}
	else
	{
		for( int j=0 ; j<m_W ; j++ )
		{
			LOGMSG("------ %s Col[%d] :",p_Prefix,j);

			for( int i=0 ; i<m_H ; i++ )
			{
				CString l_Row;
				l_Row.Format("%s [%.2d] = ",p_Prefix,i);
				CString l_Elt;

				for( void * iPos=Elt(i,j).HeadPos() ; iPos ;  )
				{
					l_Row += Elt(i,j).GetAt(iPos).ToString();
					Elt(i,j).Next(iPos);
					if( iPos )
						l_Row += " + ";
				}

				LOGMSG(l_Row);
			}

			LOGMSG("------ End col");
		}
	}

	LOGMSG();
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
CString CDiffMatrix::CProd::ToString() const
{
	CString Res;
	Res.Format( "%f*(", m_Coef );

	for( void * iPos=m_Prod.HeadPos() ; iPos ; m_Prod.Next(iPos) )
	{
		const CDiff & Diff = m_Prod.GetAt(iPos);
		CString Dif;
		Dif.Format("[dF%d/d%c]",Diff.m_Nod,Diff.m_Var==0 ? 'X' : Diff.m_Var==1 ? 'Y' : 'Z' );
		Res += Dif;
	}

	Res += ")";

	return Res;
}
