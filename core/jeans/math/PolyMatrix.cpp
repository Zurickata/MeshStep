//#include "stdafx.h"
#include "PolyMatrix.h"
#include "Matrix.h"



//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
CPolyMatrix::CPolyMatrix()
{
	m_H = m_W = 0;
	m_pMat = NULL;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
CPolyMatrix::~CPolyMatrix()
{
	Free();
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
void CPolyMatrix::Free()
{
	if( m_pMat )			
	{
		// Free
		for( int i=0 ; i<m_H ; i++ )
			delete [] m_pMat[i];

		delete [] m_pMat;
		m_pMat = NULL;
	}

	// Mark as freed
	m_H = m_W = 0;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CPolyMatrix::SetDims( int p_H, int p_W )
{
	// Ok ?
	if( p_H<=0 || p_W<=0 )
	{
		LOGERR("[CPolyMatrix::SetDims] : Invalid dims !");
		return false;
	}

	// Same dims ?
	if( p_H==m_H && p_W==m_W )
		return true;

	// Free previous
	Free();

	// Alloc
	m_pMat = new CPolynom * [p_H];
	for( int i=0 ; i<p_H ; i++ )
		m_pMat[i] = new CPolynom [p_W];

	// Keep
	m_H = p_H;
	m_W = p_W;

	return true;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
static CPolynom ERR_ELT;
CPolynom & CPolyMatrix::Elt( int p_I, int p_J )
{
	// Ok ?
	if( p_I>=m_H || p_I<0
	 || p_J>=m_W || p_J<0 )
	{
		LOGERR("[CPolyMatrix::Elt] : Accessing invalid element (i=%d,j=%d) !",p_I,p_J);
		return ERR_ELT;
	}

	return m_pMat[p_I][p_J];
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
CPolynom CPolyMatrix::Elt( int p_I, int p_J ) const
{
	// Ok ?
	if( p_I>=m_H || p_I<0
	 || p_J>=m_W || p_J<0 )
	{
		LOGERR("[CPolyMatrix::Elt] : Accessing invalid element (i=%d,j=%d) !",p_I,p_J);
		return ERR_ELT;
	}

	return m_pMat[p_I][p_J];
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CPolyMatrix::SubMatrixTo( int p_FirstRow, int p_LastRow, int p_FirstCol, int p_LastCol, CPolyMatrix & p_To )
{
	// Ok ?
	if( p_FirstRow>p_LastRow
	 || p_FirstCol>p_LastCol
	 || p_FirstRow<0
	 || p_FirstCol<0
	 || p_LastRow>=m_H
	 || p_LastCol>=m_W )
	{
		LOGERR("[CPolyMatrix::SubMatrixTo] : Invalid range !");
		return false;
	}

	// Fill new matrix
	p_To.SetDims( p_LastRow-p_FirstRow+1, p_LastCol-p_FirstCol+1 );
	for( int i=0 ; i<p_To.Rows() ; i++ )
	for( int j=0 ; j<p_To.Cols() ; j++ )
	{
		p_To.Elt(i,j) = Elt( p_FirstRow+i, p_FirstCol+j );
	}

	return true;
}

////////////////////////////////////////////////////////////////////////////////
//
// Operations
//
//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CPolyMatrix::Mult( const CMatrix & p_A, CPolyMatrix & p_Res )
{
	// Ok ?
	if( !Rows() || !Cols() || p_A.Rows()!=Cols() || !p_A.Cols() )
	{
		LOGERR("[CPolyMatrix::Mult] : Unable to multiplicate !");
		return false;
	}

	// Dim
	p_Res.SetDims( Rows(), p_A.Cols() );

	for( int i=0 ; i<p_Res.Rows() ; i++ )
	for( int j=0 ; j<p_Res.Cols() ; j++ )
	{
		for( int k=0 ; k<Cols() ; k++ )
			p_Res.Elt(i,j) = p_Res.Elt(i,j) + Elt(i,k) * p_A.Elt(k,j);
	}

	return true;
}
	
//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CPolyMatrix::Mult( const CPolyMatrix & p_A, CPolyMatrix & p_Res )
{
	// Ok ?
	if( !Rows() || !Cols() || p_A.Rows()!=Cols() || !p_A.Cols() )
	{
		LOGERR("[CPolyMatrix::Mult] : Unable to multiplicate !");
		return false;
	}

	// Dim
	p_Res.SetDims( Rows(), p_A.Cols() );

	for( int i=0 ; i<p_Res.Rows() ; i++ )
	for( int j=0 ; j<p_Res.Cols() ; j++ )
	{
		for( int k=0 ; k<Cols() ; k++ )
			p_Res.Elt(i,j) = p_Res.Elt(i,j) + Elt(i,k) * p_A.Elt(k,j);
	}

	return true;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CPolyMatrix::TransposeTo( CPolyMatrix & p_Res )
{
	if( !p_Res.SetDims(Cols(),Rows()) )
	{
		LOGERR("[CPolyMatrix::TransposeTo] : Dimension error !");
		return false;
	}

	for( int i=0 ; i<Rows() ; i++ )
	for( int j=0 ; j<Cols() ; j++ )
	{
		p_Res.Elt(j,i) = Elt(i,j);
	}

	return true;
}



////////////////////////////////////////////////////////////////////////////////
//
// Evaluation
//
//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
void CPolyMatrix::EvalTo( double X, double Y, CMatrix & p_To ) const
{
	if( p_To.SetDims(Rows(),Cols()) )
	{
		for( int i=0 ; i<Rows() ; i++ )
		for( int j=0 ; j<Cols() ; j++ )
			p_To.Elt(i,j) = Elt(i,j).EvalAt(X,Y);
	}
}
//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
void CPolyMatrix::EvalTo( double X, double Y, double Z, CMatrix & p_To ) const
{
	if( p_To.SetDims(Rows(),Cols()) )
	{
		for( int i=0 ; i<Rows() ; i++ )
		for( int j=0 ; j<Cols() ; j++ )
			p_To.Elt(i,j) = Elt(i,j).EvalAt(X,Y,Z);
	}
}


////////////////////////////////////////////////////////////////////////////////
//
// Integration
//
//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CPolyMatrix::IntegralTo( int p_MaxDegX, int p_MaxDegY, int p_MaxDegZ, double * p_pSums, CMatrix & p_Res )
{
	if( !p_Res.SetDims(m_H,m_W) )
	{
		LOGERR("[CPolyMatrix::IntegralTo] : Unable to set dims for integration !");
		return false;
	}

	// Compute integration matrix
	for( int i=0 ; i<m_H ; i++ )
	for( int j=0 ; j<m_W ; j++ )
	{
		double SumPol;
		if( !Elt(i,j).IntegralTo(p_MaxDegX,p_MaxDegY,p_MaxDegZ,p_pSums,SumPol))
		{
            //string bug = Elt(i,j).ToString();
			LOGERR("[CPolyMatrix::IntegralTo] : Could not compute integral for element (%d,%d)=%s !",i,j,Elt(i,j).ToString().c_str());
			return false;
		}
		else
		{
			p_Res.Elt(i,j) = SumPol;
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
void CPolyMatrix::Log( string p_Prefix/*=""*/ )
{
	/*if( !m_H )
	{
		LOGMSG("%s [.] = empty matrix",p_Prefix.c_str());
	}
	else
	{
		for( int i=0 ; i<m_H ; i++ )
		{
			string l_Row;
			l_Row.Format("%s [%.2d] = [\t",p_Prefix,i);
			for( int j=0 ; j<m_W ; j++ )
			{
				l_Row += "\t\t" + Elt(i,j).ToString();
			}
			l_Row += "\t\t]";
			LOGMSG(l_Row.c_str());
		}
	}

	LOGMSG("\n");*/
}


////////////////////////////////////////////////////////////////////////////////
//
// Co-Facteurs
//
//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
CLst<int> CPolyMatrix::m_LocalRows;
CLst<int> CPolyMatrix::m_LocalCols;

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
CPolynom CPolyMatrix::CF_Det( bool p_EmptyMat/*=false*/ )
{
	// Ok ?
	if( !m_H || m_H!=m_W )
	{
		LOGERR("[CMatrix::CF_Det] : Unable to compute determinant !");
		return 0;
	}

	// Init local cols and rows
	InitLocalRowsCols();

	return CF_RecDet(p_EmptyMat);
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
int CPolyMatrix::MaxZeroLocalRow()
{
	int l_MaxZeroCount = -1;
	int l_LocalRow = 0;
	int l_BestRow;

	for( void * i_RowPos=m_LocalRows.HeadPos() ; i_RowPos ; m_LocalRows.Next(i_RowPos) )
	{
		int l_GlobalRow = m_LocalRows.GetAt(i_RowPos);
		int l_ZeroCount = 0;

		for( void * i_ColPos=m_LocalCols.HeadPos() ; i_ColPos ; m_LocalCols.Next(i_ColPos) )
		{
			int l_GlobalCol = m_LocalCols.GetAt(i_ColPos);

			if( Elt(l_GlobalRow,l_GlobalCol).IsZero() )
				l_ZeroCount++;
		}

		if( l_ZeroCount > l_MaxZeroCount )
		{
			l_MaxZeroCount = l_ZeroCount;
			l_BestRow = l_LocalRow;
		}

		l_LocalRow++;
	}

	return l_BestRow;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
CPolynom CPolyMatrix::CF_RecDet( bool p_EmptyMat/*=false*/ )
{
	// 0x0 ?
	if( LocalCols() == 0 )
	{
		return 1;
	}
	// 1x1 ?
	else if( LocalCols() == 1 )
	{
		return Elt(m_LocalRows.GetHead(),m_LocalCols.GetHead());
	}
	// 2x2 ?
	else if( LocalCols() == 2 )
	{
		CPolynom l_00 = Elt(m_LocalRows.GetHead(),m_LocalCols.GetHead());
		CPolynom l_11 = Elt(m_LocalRows.GetTail(),m_LocalCols.GetTail());
		CPolynom l_01 = Elt(m_LocalRows.GetHead(),m_LocalCols.GetTail());
		CPolynom l_10 = Elt(m_LocalRows.GetTail(),m_LocalCols.GetHead());

		return l_00*l_11 - l_01*l_10;
	}

	//--- Decrease dim and recurse

	// Remove first local row
	int l_LocalI;
	if( p_EmptyMat )
		l_LocalI = MaxZeroLocalRow();
	else
		l_LocalI = 0;

	int l_GlobalRow = RemoveLocalRow(l_LocalI);

	// Develop along first row
	CPolynom l_Det = 0;
	for( int i_LocalJ=0 ; i_LocalJ<LocalCols() ; i_LocalJ++ )
	{
		// Remove local col
		int l_GlobalCol = RemoveLocalCol(i_LocalJ);

		// Compute sub det only if element non null
		CPolynom l_Elt = Elt(l_GlobalRow,l_GlobalCol);
		if( !l_Elt.IsZero() )
			l_Det = l_Det + ((l_LocalI+i_LocalJ)%2 ? -1 : +1) * l_Elt * CF_RecDet(p_EmptyMat);

		// Add global col for further computing
		AddGlobalCol( l_GlobalCol );
	}

	// Add global row further computing
	AddGlobalRow( l_GlobalRow );

	return l_Det;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
void CPolyMatrix::InitLocalRowsCols()
{
	m_LocalRows.DelAll();
	m_LocalCols.DelAll();
	for( int i=0 ; i<m_H ; i++ )
	{
		m_LocalRows.AddTail(i);
		m_LocalCols.AddTail(i);
	}
}
int CPolyMatrix::RemoveLocalRow( int p_LocalI )
{
	if( p_LocalI<0 || p_LocalI>=m_LocalRows.Count() )
	{
		LOGERR("[CPolyMatrix::RemoveLocalRow] : Could not remove %d !",p_LocalI);
		return -1;
	}
	void * l_Pos = m_LocalRows.FindIdx(p_LocalI);
	int l_GlobalRow = m_LocalRows.GetAt( l_Pos );
	m_LocalRows.DelAt( l_Pos );
	return l_GlobalRow;
}
int CPolyMatrix::RemoveLocalCol( int p_LocalJ )
{
	if( p_LocalJ<0 || p_LocalJ>=m_LocalCols.Count() )
	{
		LOGERR("[CPolyMatrix::RemoveLocalCol] : Could not remove %d !",p_LocalJ);
		return -1;
	}
	void * l_Pos = m_LocalCols.FindIdx(p_LocalJ);
	int l_GlobalCol = m_LocalCols.GetAt( l_Pos );
	m_LocalCols.DelAt( l_Pos );
	return l_GlobalCol;
}
void CPolyMatrix::AddGlobalRow( int p_GlobalI )
{
	void * i_Pos = m_LocalRows.HeadPos();
	while( i_Pos && m_LocalRows.GetAt(i_Pos)<p_GlobalI )
		m_LocalRows.Next(i_Pos);
	if( i_Pos )
		m_LocalRows.AddBefore( i_Pos, p_GlobalI );
	else
		m_LocalRows.AddTail(p_GlobalI);
}
void CPolyMatrix::AddGlobalCol( int p_GlobalJ )
{
	void * i_Pos = m_LocalCols.HeadPos();
	while( i_Pos && m_LocalCols.GetAt(i_Pos)<p_GlobalJ )
		m_LocalCols.Next(i_Pos);
	if( i_Pos )
		m_LocalCols.AddBefore( i_Pos, p_GlobalJ );
	else
		m_LocalCols.AddTail(p_GlobalJ);
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CPolyMatrix::CF_InverseTo( CPolyMatrix & p_Cof, CPolynom & p_Det )
{
	// Ok ?
	if( !Rows() || Rows()!=Cols() )
	{
		LOGERR("[CPolyMatrix::CF_InverseTo] : Unable to inverse !");
		return false;
	}

	// Inversible ?
	p_Det = CF_Det();
	if( p_Det.IsZero() )
	{
		LOGERR("[CPolyMatrix::CF_InverseTo] : Matrix not inversible !");
		return false;
	}

	// Dims
	p_Cof.SetDims(Rows(),Cols());

	// Fill with transpose(co-factors)
	for( int i=0 ; i<Rows() ; i++ )
	for( int j=0 ; j<Cols() ; j++ )
	{
		// Remove
		RemoveLocalRow(i);
		RemoveLocalCol(j);

		// Compute co-factor and transpose
		p_Cof.Elt(j,i) = ((i+j)%2 ? -1 : +1) * CF_RecDet();

		// Add
		AddGlobalRow(i);
		AddGlobalCol(j);
	}

	return true;
}

