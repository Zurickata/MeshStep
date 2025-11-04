#include "stdafx.h"
#include "SparseMatrix.h"
#include <Math/Matrix.h>
#include <Math/Vector.h>
#include <Services/Log.h>
#include <Array/Array2.h>
#include <GraphTools/GraphTools.h>
#include <fcntl.h>
#include <io.h>
#include <float.h>



//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
// What is zero and what is not ....
const double CSparseMatrix::TOLERANCE = 1e-15;

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
CSparseMatrix::CSparseMatrix()
{
	m_H = m_W = 0;
	m_pRows = m_pCols = NULL;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
CSparseMatrix::~CSparseMatrix()
{
	Free();
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
void CSparseMatrix::Free()
{
	// Free cells from rows
	for( int i=0 ; i<m_H ; i++ )
	{
		for( void * Pos=m_pRows[i].HeadPos() ; Pos ; m_pRows[i].Next(Pos) )
			delete m_pRows[i].GetAt(Pos);
	}

	// Delete lists
	delete [] m_pRows;
	delete [] m_pCols;

	// Mark as freed
	m_H = m_W = 0;
	m_pRows = m_pCols = NULL;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CSparseMatrix::SetDims( int p_H/*ROWS*/, int p_W/*COLS*/ )
{
	// Ok ?
	if( p_H<=0 || p_W<=0 )
	{
		LOGERR("[CSparseMatrix::SetDims] : Invalid dims !");
		return false;
	}

	// Same dims ?
	if( p_H==m_H && p_W==m_W )
		return true;

	// Free previous
	Free();

	// Alloc
	m_pRows = new CLst<CCell*> [p_H];
	m_pCols = new CLst<CCell*> [p_W];

	// Keep
	m_H = p_H;
	m_W = p_W;

	return true;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
double CSparseMatrix::Elt( int p_I, int p_J ) const
{
	// Ok ?
	if( p_I>=m_H || p_I<0
	 || p_J>=m_W || p_J<0 )
	{
		LOGERR("[CSparseMatrix::Elt] : Accessing invalid element (i=%d,j=%d) !",p_I,p_J);
		return 0;
	}

	// Look for cell in the smallest list
	void * l_pUnused;
	const CCell * l_pCell;
	if( m_pRows[p_I].Count() < m_pCols[p_J].Count() )
		l_pCell = FindCellInRow( p_I, p_J, l_pUnused );
	else
		l_pCell = FindCellInCol( p_I, p_J, l_pUnused );

	// If found, access value, if not, null cell
	return l_pCell ? l_pCell->m_Val : 0 ;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
CSparseMatrix::CCell * CSparseMatrix::PtrElt( int p_I/*ROW*/, int p_J/*COL*/ )
{
	// Ok ?
	if( p_I>=m_H || p_I<0
	 || p_J>=m_W || p_J<0 )
	{
		LOGERR("[CSparseMatrix::PtrElt] : Accessing invalid element (i=%d,j=%d) !",p_I,p_J);
		return NULL;
	}

	// Look for cell in the smallest list
	CLst<CCell*> & RowI = m_pRows[p_I];
	CLst<CCell*> & ColJ = m_pCols[p_J];

	void * l_pNextCellInRow;
	void * l_pNextCellInCol;
	if( RowI.Count() < ColJ.Count() )
	{
		// Find in row
		CCell * l_pCell = FindCellInRow( p_I, p_J, l_pNextCellInRow );

		// Found ?
		if( l_pCell )
			return l_pCell;

		// Find in col
		FindCellInCol( p_I, p_J, l_pNextCellInCol );
	}
	else
	{
		// Find in col
		CCell * l_pCell = FindCellInCol( p_I, p_J, l_pNextCellInCol );

		// Found ?
		if( l_pCell )
			return l_pCell;

		// Find in row
		FindCellInRow( p_I, p_J, l_pNextCellInRow );
	}

	// Allocate new cell
	CCell * l_pNewCell = new CCell(p_I,p_J);

	// Insert cell in rows
	if( l_pNextCellInRow )
		l_pNewCell->m_RowPos = RowI.AddBefore( l_pNextCellInRow, l_pNewCell );
	else
		l_pNewCell->m_RowPos = RowI.AddTail( l_pNewCell );

	// Insert cell in cols
	if( l_pNextCellInCol )
		l_pNewCell->m_ColPos = ColJ.AddBefore( l_pNextCellInCol, l_pNewCell );
	else
		l_pNewCell->m_ColPos = ColJ.AddTail( l_pNewCell );

	return l_pNewCell;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
void CSparseMatrix::LoadEmpty()
{
	int i,j;

	// Free cells from rows
	for( i=0 ; i<m_H ; i++ )
	{
		for( void * Pos=m_pRows[i].HeadPos() ; Pos ; m_pRows[i].Next(Pos) )
			delete m_pRows[i].GetAt(Pos);
	}

	// Empty rows
	for( i=0 ; i<Rows() ; i++ )
		m_pRows[i].DelAll();

	// Empty cols
	for( j=0 ; j<Cols() ; j++ )
		m_pCols[j].DelAll();
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CSparseMatrix::FromMatrix( const CMatrix & p_From, double tol/*=TOLERANCE*/ )
{
	// Ok ?
	if( !SetDims(p_From.Rows(),p_From.Cols()) )
	{
		LOGERR("[CSparseMatrix::FromMatrix] : Unable to set dims !");
		return false;
	}

	LoadEmpty();

	for( int i=0 ; i<Rows() ; i++ )
	for( int j=0 ; j<Cols() ; j++ )
	{
		double Fij = p_From.Elt(i,j);
		if( fabs(Fij) > tol )
		{
			// New cell
			CCell * l_pMij = new CCell(i,j);
			l_pMij->m_Val = Fij;

			// Add to col
			l_pMij->m_ColPos = m_pCols[j].AddTail(l_pMij);

			// Add to row
			l_pMij->m_RowPos = m_pRows[i].AddTail(l_pMij);
		}
	}

	return true;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CSparseMatrix::ToMatrix( CMatrix & p_To ) const
{
	// Ok ?
	if( !p_To.SetDims(Rows(),Cols()) )
	{
		LOGERR("[CSparseMatrix::ToMatrix] : Unable to set dims !");
		return false;
	}

	p_To.LoadValue(0);

	// Set values from rows
	for( int i=0 ; i<Rows() ; i++ )
	{
		for( void * Pos=m_pRows[i].HeadPos() ; Pos ; m_pRows[i].Next(Pos) )
		{
			const CCell * l_pMij = m_pRows[i].GetAt(Pos);
			p_To.Elt(i,l_pMij->m_J) = l_pMij->m_Val;
		}
	}

	return true;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CSparseMatrix::ColToVector( int p_J, CVector & p_To, int p_MatFirstRow/*=0*/ )
{
#ifdef _DEBUG
	// Ok ?
	if( p_J<0 || p_J>=Cols() || p_MatFirstRow<0 || p_MatFirstRow>=Rows() )
	{
		LOGERR("[CSparseMatrix::ColToVector] : Invalid col or row index !");
		return false;
	}
#endif

	p_To.SetDim( Rows()-p_MatFirstRow );
	p_To.LoadValue( 0 );

	const CLst<CCell*> & ColJ = m_pCols[p_J];
	for( void * PosI=ColJ.TailPos() ; PosI ; ColJ.Prev(PosI) )
	{
		const CCell * l_pKij = ColJ.GetAt(PosI);
		int I = l_pKij->m_I - p_MatFirstRow;

		if( I < 0 )
			break;

		p_To.Elt(I) = l_pKij->m_Val;
	}

	return true;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CSparseMatrix::Mult( const CVector & p_A, CVector & p_Res ) const
{
	// Ok ?
	if( !Rows() || !Cols() || Cols()!=p_A.Rows() )
	{
		LOGERR("[CSparseMatrix::Mult] : Unable to multiplicate !");
		return false;
	}

	// Dim result
	p_Res.SetDim( m_H );

	// Calc
	for( int i=0 ; i<m_H ; i++ )
	{
		p_Res.Elt(i) = 0;

		const CLst<CCell*> & RowI = m_pRows[i];
		for( void * Pos=RowI.HeadPos() ; Pos ; RowI.Next(Pos) )
		{
			const CCell * l_pKij = RowI.GetAt(Pos);
			p_Res.Elt(i) += l_pKij->m_Val * p_A.Elt( l_pKij->m_J );
		}
	}

	return true;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CSparseMatrix::CompleteMult( const CVector & p_A, CVector & p_Res ) const
{
	//--------------------------------------------------------------------------
	// Use with symetric matrices where only the lower triangular mat is stored 
	//--------------------------------------------------------------------------

	// Ok ?
	if( !Rows() || !Cols() || Cols()!=p_A.Rows() )
	{
		LOGERR("[CSparseMatrix::CompleteMult] : Unable to multiplicate !");
		return false;
	}

	// Dim result
	p_Res.SetDim( m_H );

	// Calc
	for( int i=0 ; i<m_H ; i++ )
	{
		p_Res.Elt(i) = 0;

		// Start multiplication using incomplete row cells
		const CLst<CCell*> & RowI = m_pRows[i];
		for( void * Pos=RowI.HeadPos() ; Pos ; RowI.Next(Pos) )
		{
			const CCell * l_pKij = RowI.GetAt(Pos);
			p_Res.Elt(i) += l_pKij->m_Val * p_A.Elt( l_pKij->m_J );
		}

		// Complete row using col data
		const CLst<CCell*> & ColI = m_pCols[i];
		for( Pos=ColI.HeadPos() ; Pos ; ColI.Next(Pos) )
		{
			const CCell * l_pKki = ColI.GetAt(Pos);
			int k = l_pKki->m_I;

			// Skip diagonal term already taken into account in row
			if( k == i )
				continue;

			p_Res.Elt(i) += l_pKki->m_Val * p_A.Elt( k );
		}
	}

	return true;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
void CSparseMatrix::RemoveCell( CCell * p_pCell )
{
	// Clear from lists
	m_pRows[p_pCell->m_I].DelAt( p_pCell->m_RowPos );
	m_pCols[p_pCell->m_J].DelAt( p_pCell->m_ColPos );

	// Delete cell
	delete p_pCell;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
void CSparseMatrix::RemoveCellKeepDiagonal( CCell * p_pCell )
{
	// Cell coords
	int I = p_pCell->m_I;
	int J = p_pCell->m_J;

	// If removing diagonal element, replace value by 1 and keep cell
	if( I == J )
	{
		p_pCell->m_Val = 1;
	}
	else
	{
		// If removing other element, simply clear from lists
		m_pRows[I].DelAt( p_pCell->m_RowPos );
		m_pCols[J].DelAt( p_pCell->m_ColPos );

		// Delete cell
		delete p_pCell;
	}
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
CSparseMatrix & CSparseMatrix::operator=( const CSparseMatrix & p_In )
{
	if( SetDims(p_In.Rows(),p_In.Cols()) )
	{
		// Empty initial matrix
		LoadEmpty();

		// Copy elements from rows
		for( int i=0 ; i<m_H ; i++ )
		{
			const CLst<CCell*> & lRowI = p_In.m_pRows[i];

			for( void * iPosJ=lRowI.HeadPos() ; iPosJ ; lRowI.Next(iPosJ) )
			{
				// Source cell
				const CCell * lpCellIJ = lRowI.GetAt(iPosJ);

				// Destination cell
				CCell * lpNewCell = PtrElt( i, lpCellIJ->m_J );
				
				// Copy val and ref count
				lpNewCell->m_Val      = lpCellIJ->m_Val;
				lpNewCell->m_RefCount = lpCellIJ->m_RefCount;
			}
		}
	}
	else
	{
		LOGERR("[CSparseMatrix::operator=] : Unable to copy matrix !");
	}

	return *this;
}


////////////////////////////////////////////////////////////////////////////////
//
// File operations
//
//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CSparseMatrix::SaveBin( const CString & pFname )
{
	// Open file for writing
	FILE * l_File = fopen( pFname , "w" );
	if( !l_File )
	{
		LOGERR("[CSparseMatrix::SaveBin] : Could not create file <%s> !",pFname);
		return false;
	}

	// Switch to binary
	_setmode( _fileno(l_File) , _O_BINARY );

	// Write header for sparse matrix and dims
	if( fwrite("SPMAT",sizeof(char),5,l_File)!=5
	 || fwrite(&m_H,sizeof(int),1,l_File)!=1
	 || fwrite(&m_W,sizeof(int),1,l_File)!=1 )
	{
		LOGERR("[CSparseMatrix::SaveBin] : Could not write header !");
		return false;
	}

	// Write mat elements from rows
	int n;
	for( int i=0 ; i<m_H ; i++ )
	{
		const CLst<CCell*> & lRow = m_pRows[i];
		n = lRow.Count();

		// Write number of elements in row
		if( fwrite(&n,sizeof(int),1,l_File)!=1 )
		{
			LOGERR("[CSparseMatrix::SaveBin] : Could not write row #%d !",i);
			return false;
		}

		// Write all elements in row
		for( void * j=lRow.HeadPos() ; j ; lRow.Next(j) )
		{
			const CCell * lpCell = lRow.GetAt(j);

			if( fwrite(&lpCell->m_J,sizeof(int),1,l_File)!=1
			 || fwrite(&lpCell->m_Val,sizeof(double),1,l_File)!=1 )
			{
				LOGERR("[CSparseMatrix::SaveBin] : Could not write element (%d,%d) !",i,lpCell->m_J);
				return false;
			}
		}
	}

	// Fini
	fclose(l_File);
	return true;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CSparseMatrix::LoadBin( const CString & pFname )
{
	// Open file for writing
	FILE * l_File = fopen( pFname , "r" );
	if( !l_File )
	{
		LOGERR("[CSparseMatrix::LoadBin] : Could not open file <%s> !",pFname);
		return false;
	}

	// Switch to binary
	_setmode( _fileno(l_File) , _O_BINARY );

	// Read header for sparse matrix and dims
	char lHeader[6];
	lHeader[5] = 0;
	int lW, lH;
	if( fread(lHeader,sizeof(char),5,l_File)!=5
	 || strcmp(lHeader,"SPMAT")
	 || fread(&lH,sizeof(int),1,l_File)!=1
	 || fread(&lW,sizeof(int),1,l_File)!=1
	 || !SetDims(lH,lW) )
	{
		LOGERR("[CSparseMatrix::LoadBin] : Could not init matrix !");
		return false;
	}

	// Read mat elements from rows
	int lN;
	int lJ;
	double lV;
	for( int i=0 ; i<m_H ; i++ )
	{
		// Read number of elements in row
		if( fread(&lN,sizeof(int),1,l_File)!=1 )
		{
			LOGERR("[CSparseMatrix::LoadBin] : Could not read row #%d !",i);
			return false;
		}

		// Read all elements in row
		for( int v=0 ; v<lN ; v++ )
		{
			if( fread(&lJ,sizeof(int),1,l_File)!=1
			 || fread(&lV,sizeof(double),1,l_File)!=1 )
			{
				LOGERR("[CSparseMatrix::LoadBin] : Could not read element #%d in row #%d !",v,i);
				return false;
			}

			// Create element
			PtrElt(i,lJ)->m_Val = lV;
		}
	}

	// Fini
	fclose(l_File);
	return true;
}


////////////////////////////////////////////////////////////////////////////////
//
// Cholesky
//
//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CSparseMatrix::LLt_ify( CSparseMatrix & p_L, int p_FirstRowCol/*=0*/ ) const
{
	//----------------------------------------------------------------
	// HYPOTHESIS:
	//
	//  - L is empty (constructor or p_L.LoadEmpty() before)
	//
	//  - K (*this) contains at least the lower part of the
	//      symmetric matrix, diagonal included
	//
	//----------------------------------------------------------------

	// Square ?
	if( Rows() != Cols() )
	{
		LOGERR("[CSparseMatrix::LLt_ify] : Matrix not square !");
		return false;
	}

	// First row-col ok ?
	if( p_FirstRowCol<0 || p_FirstRowCol>=Rows() )
	{
		LOGERR("[CSparseMatrix::LLt_ify] : First row-col out of matrix range !");
		return false;
	}

	// Ok ?
	if( !p_L.SetDims(Cols()-p_FirstRowCol,Cols()-p_FirstRowCol) )
	{
		LOGERR("[CSparseMatrix::LLt_ify] : Dim error !");
		return false;
	}

	// Temporary structure
#pragma message("################################# verifier si pas d'allocations inutiles")
	CVector V;
	V.SetDim(p_L.Cols());
	V.LoadValue(0);

	// Log
	int LogCount = 0;
	bool LogNow;
	int LogLength = p_L.Cols() / 100; // Log 100 times

	void * PosI;
	void * PosJ;

	// Fill-in all cols
	for( int J0=0 ; J0<p_L.Cols() ; J0++ )
	{
		      CLst<CCell*> & LRowJ0 = p_L.m_pRows[J0];
			  CLst<CCell*> & LColJ0 = p_L.m_pCols[J0];
		const CLst<CCell*> & KColJ0 = m_pCols[J0+p_FirstRowCol];

		//----------------------
		// Fill V with K values
		//----------------------

		// Keep also track of non null K elements in row strictly below J0
		CLst<int> LColJ0_NN;

		// Fill V, for I>=J0
		for( PosI=KColJ0.TailPos() ; PosI ; KColJ0.Prev(PosI) )
		{
			const CCell * l_pCell = KColJ0.GetAt(PosI);
			int I = l_pCell->m_I - p_FirstRowCol;

			V.Elt(I) = l_pCell->m_Val;

			if( I == J0 )
				break;

			LColJ0_NN.AddHead(I);
		}

		//----------------------------------------
		// Add to V scal products Lj0k*Ljk, k>=J0
		//----------------------------------------

		for( PosJ=LRowJ0.HeadPos() ; PosJ ; LRowJ0.Next(PosJ) )
		{
			const CCell * l_pLj0j = LRowJ0.GetAt(PosJ);
			double Lj0j = l_pLj0j->m_Val;

			const CLst<CCell*> & LColJ = p_L.m_pCols[l_pLj0j->m_J];
			PosI = l_pLj0j->m_ColPos;

			while( PosI )
			{
				const CCell * l_pLij = LColJ.GetAt(PosI);

				V.Elt(l_pLij->m_I) -= Lj0j*l_pLij->m_Val;

				LColJ.Next(PosI);
			}
		}

		//----------------------------------
		// Check LLt-ibility and comp Lj0j0
		//----------------------------------

		double & Lj0j0 = V.Elt(J0);

		if( Lj0j0 <= 0 )
		{
			LOGERR("[CSparseMatrix::LLt_ify] : Unable to LLt-ify !");
			return false;
		}

		Lj0j0 = sqrt(Lj0j0);

		//--------------------------
		// { i, NN(Lij0) and i>j0 }
		//--------------------------

		// Merge with all non null L rows
		for( PosJ=LRowJ0.HeadPos() ; PosJ ; LRowJ0.Next(PosJ) )
		{
			int J = LRowJ0.GetAt(PosJ)->m_J;

			CLst<int> LColJ_NN;
			p_L.NonNullRows( J, J0, LColJ_NN );

			MergeLists( LColJ_NN, LColJ0_NN );
		}

		//---------------
		// Create col J0
		//---------------

		for( PosI=LColJ0_NN.TailPos() ; PosI ; LColJ0_NN.Prev(PosI) )
		{
			int I = LColJ0_NN.GetAt(PosI);

			// New cell
			CCell * l_pLij0 = new CCell(I,J0);
			l_pLij0->m_Val = V.Elt(I) / Lj0j0;

			// Add cell to col
			l_pLij0->m_ColPos = LColJ0.AddHead(l_pLij0);

			// Add cell to row
			l_pLij0->m_RowPos = p_L.m_pRows[I].AddTail(l_pLij0);

			// Clean V
			V.Elt(I) = 0;
		}

		// Create cell for Lj0j0
		CCell * l_pLj0j0 = new CCell(J0,J0);
		l_pLj0j0->m_Val = Lj0j0;

		// Add cell to col
		l_pLj0j0->m_ColPos = LColJ0.AddHead(l_pLj0j0);

		// Add cell to row
		l_pLj0j0->m_RowPos = LRowJ0.AddTail(l_pLj0j0);

		// Clean V
		Lj0j0 = 0;

		// Log progression
		LogNow = LogCount == LogLength;
		if( LogNow )
		{
			LOGMSG("[CSparseMatrix::LLt_ify] : Created cols up to %d / %d",J0,p_L.Cols()-1);
			LogCount = 0;
		}

		LogCount++;
	}

	// Final log
	if( !LogNow )
		LOGMSG("[CSparseMatrix::LLt_ify] : Created cols up to %d / %d",p_L.Cols()-1,p_L.Cols()-1);

	LOGMSG("[CSparseMatrix::LLt_ify] : Done !");

	return true;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
#pragma message(">>>>> voir si possibilite de repercuter la nouvelle structure de K sur L (elimination de cellules)")
bool CSparseMatrix::LLt_Update( CSparseMatrix & p_L, int p_SubmatFirstRowCol/*=0*/, int p_UpdateFromGlobalCol/*=0*/ ) const
{
//------------------------------------------------------------
CGraphTools::StartPerfMeter();
//------------------------------------------------------------

	//----------------------------------------------------------------
	// HYPOTHESIS:
	//
	//  - L contains previous version of factorisation
	//
	//  - K (*this) contains at least the lower part of the
	//      symmetric matrix, diagonal included
	//
	//----------------------------------------------------------------

#ifdef _DEBUG
	// First row-col ok ?
	if( p_SubmatFirstRowCol<0 || p_SubmatFirstRowCol>=Rows() )
	{
		LOGERR("[CSparseMatrix::LLt_Update] : Submatrix first row-col out of matrix range !");
		return false;
	}

	// Square and fair ?
	if( Rows()!=Cols()
	 || p_L.Rows()!=p_L.Cols()
	 || Rows()-p_SubmatFirstRowCol!=p_L.Rows() )
	{
		LOGERR("[CSparseMatrix::LLt_Update] : Dimensions mismatch !");
		return false;
	}
#endif

	// Temporary structure
	CVector V;
	V.SetDim(p_L.Cols());
	V.LoadValue(0);

	// List iterators
	void * PosI;
	void * PosJ;

	// First col for update
	int l_StartJ0 = 0;

	// If partially updating matrix, move first col
	if( p_UpdateFromGlobalCol > p_SubmatFirstRowCol )
		l_StartJ0 = p_UpdateFromGlobalCol - p_SubmatFirstRowCol;

	// Fill-in all cols
	for( int J0=l_StartJ0 ; J0<p_L.Cols() ; J0++ )
	{
			  CLst<CCell*> & LRowJ0 = p_L.m_pRows[J0];
			  CLst<CCell*> & LColJ0 = p_L.m_pCols[J0];
		const CLst<CCell*> & KColJ0 = m_pCols[J0+p_SubmatFirstRowCol];

		//----------------------
		// Fill V with K values
		//----------------------

		// Fill V, for I>=J0
		for( PosI=KColJ0.TailPos() ; PosI ; KColJ0.Prev(PosI) )
		{
			const CCell * l_pCell = KColJ0.GetAt(PosI);
			int I = l_pCell->m_I - p_SubmatFirstRowCol;

			V.Elt(I) = l_pCell->m_Val;

			if( I == J0 )
				break;
		}

		//----------------------------------------
		// Add to V scal products Lj0k*Ljk, k>=J0
		//----------------------------------------

		for( PosJ=LRowJ0.HeadPos() ; PosJ ; LRowJ0.Next(PosJ) )
		{
			const CCell * l_pLj0j = LRowJ0.GetAt(PosJ);

			// Stop before col J0
			if( l_pLj0j->m_J == J0 )
				break;

			double Lj0j = l_pLj0j->m_Val;

			const CLst<CCell*> & LColJ = p_L.m_pCols[l_pLj0j->m_J];
			PosI = l_pLj0j->m_ColPos;

			while( PosI )
			{
				const CCell * l_pLij = LColJ.GetAt(PosI);

				V.Elt(l_pLij->m_I) -= Lj0j*l_pLij->m_Val;

				LColJ.Next(PosI);
			}
		}

		//----------------------------------
		// Check LLt-ibility and comp Lj0j0
		//----------------------------------

		double & Lj0j0 = V.Elt(J0);

		if( Lj0j0 <= 0 )
		{
			LOGERR("[CSparseMatrix::LLt_Update] : Unable to LLt-ify !");
			return false;
		}

		Lj0j0 = sqrt(Lj0j0);

		//---------------
		// Create col J0
		//---------------

		// Lj0j0
		PosI = LColJ0.HeadPos();
		LColJ0.GetAt(PosI)->m_Val = Lj0j0;
		LColJ0.Next(PosI);

		// Lij0
		while( PosI )
		{
			CCell * l_pLij0 = LColJ0.GetAt(PosI);
			int I = l_pLij0->m_I;

			l_pLij0->m_Val = V.Elt(I) / Lj0j0;

			// Clean V
			V.Elt(I) = 0;

			LColJ0.Next(PosI);
		}

		// Clean last element in V
		Lj0j0 = 0;
	}

//------------------------------------------------------------
CGraphTools::LogPerfMeter("CSparseMatrix::LLt_Update");
//------------------------------------------------------------

	return true;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CSparseMatrix::LLt_Solve( const CSparseMatrix & p_L, CVector & p_X, const CVector & p_Y, int p_YFirstRow/*=0*/ )
{
#ifdef _DEBUG
	// L matrix ok ?
	if( !p_L.Rows() || p_L.Rows()!=p_L.Cols() )
	{
		LOGERR("[CSparseMatrix::LLt_Solve] : Empty or not square L matrix !");
		return false;
	}

	// Y vector ok ?
	if( p_L.Rows() != p_Y.Rows()-p_YFirstRow )
	{
		LOGERR("[CSparseMatrix::LLt_Solve] : Dimensions mismatch !");
		return false;
	}
#endif

	int I, J;

	// Z <== Z / LZ=Y
	CVector Z;
	Z.SetDim( p_Y.Rows()-p_YFirstRow );
	for( I=0 ; I<Z.Rows() ; I++ )
	{
		Z.Elt(I) = p_Y.Elt(p_YFirstRow+I);

		const CLst<CCell*> & LRowI = p_L.m_pRows[I];
		void * PosJ = LRowI.TailPos();

		double Lii = LRowI.GetAt(PosJ)->m_Val;
		LRowI.Prev(PosJ);

#ifdef _DEBUG
		// Check invertibility
		if( Lii == 0 )
		{
			LOGERR("[CSparseMatrix::LLt_Solve] : Unable to solve !");
			return false;
		}
#endif
		for( ; PosJ ; LRowI.Prev(PosJ) )
		{
			const CCell * l_pLij = LRowI.GetAt(PosJ);
			Z.Elt(I) -= l_pLij->m_Val*Z.Elt(l_pLij->m_J);
		}

		Z.Elt(I) /= Lii;
	}

	// X <== X / LtX=Z
	p_X.SetDim( Z.Rows() );
	for( J=Z.Rows()-1 ; J>=0 ; J-- )
	{
		p_X.Elt(J) = Z.Elt(J);

		const CLst<CCell*> & LColJ = p_L.m_pCols[J];
		void * PosI = LColJ.HeadPos();

		double Lii = LColJ.GetAt(PosI)->m_Val;
		LColJ.Next(PosI);

		for( ; PosI ; LColJ.Next(PosI) )
		{
			const CCell * l_pLij = LColJ.GetAt(PosI);
			p_X.Elt(J) -= l_pLij->m_Val*p_X.Elt(l_pLij->m_I);
		}

		p_X.Elt(J) /= Lii;
	}

	return true;
}


////////////////////////////////////////////////////////////////////////////////
//
// Gaussian elimination
//
//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
//bool CSparseMatrix::SubsInAllRowsFor( int p_Var, CVector & p_F )
//{
//	// Check if matrix and vector are ok ?
//	if( !Rows() || Rows()!=Cols() || Rows()!=p_F.Rows() )
//	{
//		LOGERR("[CSparseMatrix::SubsInAllRowsFor] : Wrong dims !");
//		return false;
//	}
//
//	// Check if variable ok
//	if( p_Var<0 || p_Var>=Rows() )
//	{
//		LOGERR("[CSparseMatrix::SubsInAllRowsFor] : Wrong variable !");
//		return false;
//	}
//
//	// Divisor
//	double lPivot = Elt( p_Var, p_Var );
//	if( fabs(lPivot) < DBL_EPSILON )
//	{
//		LOGERR("[CSparseMatrix::SubsInAllRowsFor] : Could not substitute for variable %d ! Null coef.",p_Var);
//		return false;
//	}
//
//	CLst<CCell*> & lRowJ0 = m_pRows[p_Var];
//	CLst<CCell*> & lColJ0 = m_pCols[p_Var];
//
//	for( void * iPosI=lColJ0.HeadPos() ; iPosI ; ) //lColJ0.Next(iPosI) )
//	{
//		// Read I 
//		int I = lColJ0.GetAt(iPosI)->m_I;
//
//		// If variable row, skip
//		if( I == p_Var )
//		{
//			lColJ0.Next(iPosI);
//			continue;
//		}
//
//		for( void * iPosJ=lRowJ0.HeadPos() ; iPosJ ; lRowJ0.Next(iPosJ) )
//		{
//			// Read J
//			int J = lRowJ0.GetAt(iPosJ)->m_J;
//
//			// If variable row, skip
//			if( J == p_Var )
//				continue;
//
//
//
//	//		// Change vector
//	//		// Change vector
//	//		// Change vector
//
//
//
//
//			// Read M_IJ0 and M_J0J
//			double M_IJ0 = Elt(I,p_Var);
//			double M_J0J = Elt(p_Var,J);
//
//			// Access cell
//			CCell * lpMIJ = PtrElt(I,J);
//			lpMIJ->m_Val -= M_IJ0*M_J0J/lPivot;
//
//
//		}
//
//		// Remove cell from mat
//		CCell * lpCellIJ0 = lColJ0.GetAt(iPosI);
//		lColJ0.Next(iPosI);
//
//		m_pRows[I].DelAt( lpCellIJ0->m_RowPos );
//		lColJ0.DelAt( lpCellIJ0->m_ColPos );
//
//		// Delete cell
//		delete lpCellIJ0;
//	}
//
//
//
//	// Empty row J0
//	for( void * iPosJ=lRowJ0.HeadPos() ; iPosJ ; lRowJ0.Next(iPosJ) )
//	{
//		CCell * lpCellJ0J = lRowJ0.GetAt(iPosJ);
//
//		// Remove from col
//		m_pCols[lpCellJ0J->m_J].DelAt( lpCellJ0J->m_ColPos );
//
//		// Destroy cell
//		delete lpCellJ0J;
//	}
//	
//	// Remove all pointers
//	lRowJ0.DelAll();
//
//
//
//
//	return true;
//}


////////////////////////////////////////////////////////////////////////////////
//
// Protected
//
//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
void CSparseMatrix::NonNullRows( int p_InJ, int p_BelowI, CLst<int> & p_Is ) const
{
	for( void * Pos=m_pCols[p_InJ].TailPos() ; Pos ; m_pCols[p_InJ].Prev(Pos) )
	{
		int i = m_pCols[p_InJ].GetAt(Pos)->m_I;

		if( i <= p_BelowI )
			return;

		p_Is.AddHead(i);
	}
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
void CSparseMatrix::MergeLists( const CLst<int> & p_As, CLst<int> & p_Bs )
{
	// As empty
	if( !p_As.Count() )
	{
		return;
	}

	// Bs empty
	if( !p_Bs.Count() )
	{
		p_Bs = p_As;
		return;
	}

	// Both non-empty
	void * PosA = p_As.HeadPos();
	void * PosB = p_Bs.HeadPos();

	while( PosA )
	{
		// Find PosB such that B>=A
		while( p_Bs.GetAt(PosB)<p_As.GetAt(PosA) && PosB )
			p_Bs.Next( PosB );

		// Found such B ?
		if( PosB )
		{
			// B>=A
			if( p_Bs.GetAt(PosB) == p_As.GetAt(PosA) )
			{
				// A=B ==> skip in A and B
				p_As.Next( PosA );
				p_Bs.Next( PosB );
			}
			else
			{
				// A<B ==> add all lesser values
				while( p_As.GetAt(PosA)<p_Bs.GetAt(PosB) && PosA )
				{
					p_Bs.AddBefore( PosB, p_As.GetAt(PosA) );
					p_As.Next( PosA );
				}
			}
		}
		else
		{
			// B>A ==> add all As at the end and finish
			while( PosA )
			{
				p_Bs.AddTail( p_As.GetAt(PosA) );
				p_As.Next( PosA );
			}
		}
	}
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
CSparseMatrix::CCell * CSparseMatrix::FindCellInRow( int p_I, int p_J, void * & p_NextCellInRow ) const
{
	// The row
	const CLst<CCell*> & RowI = m_pRows[p_I];

	// No cells in this row ?
	if( !RowI.Count() )
	{
		p_NextCellInRow = NULL; // new cell to be added at tail
		return NULL;
	}

	// Cell before head ?
	if( RowI.GetHead()->m_J > p_J )
	{
		p_NextCellInRow = RowI.HeadPos(); // new cell to be added before head
		return NULL;
	}

	// Cell after tail ?
	if( RowI.GetTail()->m_J < p_J )
	{
		p_NextCellInRow = NULL; // new cell to be added at tail
		return NULL;
	}

	// Search cell
	p_NextCellInRow = RowI.HeadPos();
	do
	{
		CCell * l_pCell = RowI.GetAt(p_NextCellInRow);
		int J = l_pCell->m_J;

		if( J == p_J )
			return l_pCell;
		else
		if( J > p_J )
			return NULL;

		RowI.Next(p_NextCellInRow);
	}
	while( p_NextCellInRow );

	// Error, should have found something
	LOGERR("[CSparseMatrix::FindCellInRow] : Row inconsistency !");
	return NULL;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
CSparseMatrix::CCell * CSparseMatrix::FindCellInCol( int p_I, int p_J, void * & p_NextCellInCol ) const
{
	// The col
	const CLst<CCell*> & ColJ = m_pCols[p_J];

	// No cells in this col ?
	if( !ColJ.Count() )
	{
		p_NextCellInCol = NULL; // new cell to be added at tail
		return NULL;
	}

	// Cell before head ?
	if( ColJ.GetHead()->m_I > p_I )
	{
		p_NextCellInCol = ColJ.HeadPos(); // new cell to be added before head
		return NULL;
	}

	// Cell after tail ?
	if( ColJ.GetTail()->m_I < p_I )
	{
		p_NextCellInCol = NULL; // new cell to be added at tail
		return NULL;
	}

	// Search cell
	p_NextCellInCol = ColJ.HeadPos();
	do 
	{
		CCell * l_pCell = ColJ.GetAt(p_NextCellInCol);
		int I = l_pCell->m_I;

		if( I == p_I )
			return l_pCell;
		else
		if( I > p_I )
			return NULL;

		ColJ.Next(p_NextCellInCol);
	}
	while( p_NextCellInCol );

	// Error, should have found something
	LOGERR("[CSparseMatrix::FindCellInCol] : Col inconsistency !");
	return NULL;
}


////////////////////////////////////////////////////////////////////////////////
//
// Debug
//
//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CSparseMatrix::IsEqual( const CSparseMatrix & p_Other, double tol/*=TOLERANCE*/ )
{
	if( Rows()!=p_Other.Rows()
	 || Cols()!=p_Other.Cols() )
	 return false;

	// Compare row to row
	for( int I=0 ; I<Rows() ; I++ )
	{
		const CLst<CCell*> & ARowI = m_pRows[I];
		const CLst<CCell*> & BRowI = p_Other.m_pRows[I];

		if( ARowI.Count() != BRowI.Count() )
			return false;

		void * PosA = ARowI.HeadPos();
		void * PosB = BRowI.HeadPos();

		while( PosA && PosB )
		{
			const CCell * pAij = ARowI.GetAt(PosA);
			const CCell * pBij = BRowI.GetAt(PosB);

			if( pAij->m_J!=pBij->m_J
			 || !IsZero(pAij->m_Val-pBij->m_Val,tol) )
				return false;

			ARowI.Next(PosA);
			BRowI.Next(PosB);
		}
	}

	return true;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
void CSparseMatrix::Log( CString p_Prefix/*=""*/ )
{
	if( !Rows() )
	{
		LOGMSG("%s [.] = empty matrix",p_Prefix);
	}
	else
	{
		for( int i=0 ; i<Rows() ; i++ )
		{
			CString l_Row;
			l_Row.Format("%s [%.2d] = [",p_Prefix,i);
			for( int j=0 ; j<Cols() ; j++ )
			{
				CString l_Elt;
				l_Elt.Format("\t%.16f",Elt(i,j));
				l_Row += l_Elt;
			}
			l_Row += "\t]";
			LOGMSG(l_Row);
		}
	}
	LOGMSG();
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
void CSparseMatrix::LogBin( CString p_Prefix/*=""*/ )
{
	if( !Rows() )
	{
		LOGMSG("%s [.] = empty matrix",p_Prefix);
	}
	else
	{
		for( int I=0 ; I<Rows() ; I++ )
		{
			const CLst<CCell*> & RowI = m_pRows[I];

			CString l_Row;
			l_Row.Format("%s [%.2d] = [ ",p_Prefix,I);

			void * PosJ = RowI.HeadPos();
			int J = 0;
			while( J < Cols() )
			{
				if( PosJ )
				{
					if( J < RowI.GetAt(PosJ)->m_J )
					{
						l_Row += ".";
						J++;
					}
					else
					{
						// Only possibility : J == RowI.GetAt(PosJ)->m_J
						l_Row += "X";
						J++;
						RowI.Next(PosJ);
					}
				}
				else
				{
					l_Row += ".";
					J++;
				}
			}
			l_Row += " ]";
			LOGMSG(l_Row);
		}
	}
	LOGMSG();
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
void CSparseMatrix::LogBinToRAWImage( CString p_FnamePrefix/*=""*/ )
{
	if( !Rows() )
	{
		LOGMSG("[CSparseMatrix::LogBinToRAWImage] : %s [.] = empty matrix - no file written",p_FnamePrefix);
	}
	else
	{
		CArray2<BYTE> Pic(Rows(),Cols());
		Pic.SetValue( 255 );

		for( int I=0 ; I<Rows() ; I++ )
		{
			const CLst<CCell*> & RowI = m_pRows[I];
			for( void * PosJ = RowI.HeadPos() ; PosJ ; RowI.Next(PosJ) )
				Pic[I][RowI.GetAt(PosJ)->m_J] = 0;
		}


#pragma message("----- LogBinToRAWImage : fwrite directement !!! pas de CArray2")


		// Save
		CString FName;
		FName.Format("%s_Mat_%dx%d.raw",p_FnamePrefix,Rows(),Cols());

		if( CGraphTools::SaveRaw(FName,Pic.GetBuffer(),Cols(),Rows(),false/*H flip*/) )
			LOGMSG("[CSparseMatrix::LogBinToRAWImage] : Writing matrix to file <%s>",FName);
		else
			LOGERR("[CSparseMatrix::LogBinToRAWImage] : Could not write to file <%s> !",FName);
	}
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
void CSparseMatrix::LogRows( CString p_Prefix/*=""*/ )
{
	if( !m_H )
	{
		LOGMSG("%s [.] = empty matrix",p_Prefix);
	}
	else
	{
		for( int i=0 ; i<m_H ; i++ )
		{
			CString l_Row;
			l_Row.Format("%s ROW[%.2d] = ",p_Prefix,i);
			for( void * Pos=m_pRows[i].HeadPos() ; Pos ; m_pRows[i].Next(Pos) )
			{
				CString l_Elt;
				l_Elt.Format( "{ (%d,%d) = %.9f } ", m_pRows[i].GetAt(Pos)->m_I,
													 m_pRows[i].GetAt(Pos)->m_J,
													 m_pRows[i].GetAt(Pos)->m_Val );
				l_Row += l_Elt;
			}
			LOGMSG(l_Row);
		}
	}
	LOGMSG();
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
void CSparseMatrix::LogRowLists( CString p_Prefix/*=""*/ )
{
	if( !m_H )
	{
		LOGMSG("%s [.] = empty matrix",p_Prefix);
	}
	else
	{
		for( int i=0 ; i<m_H ; i++ )
			LOGMSG("%s ROW[%.2d] = %s",p_Prefix,i,m_pRows[i].ToString());
	}
	LOGMSG();
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
void CSparseMatrix::LogCols( CString p_Prefix/*=""*/ )
{
	if( !m_W )
	{
		LOGMSG("%s [.] = empty matrix",p_Prefix);
	}
	else
	{
		for( int j=0 ; j<m_W ; j++ )
		{
			CString l_Col;
			l_Col.Format("%s COL[%.2d] = ",p_Prefix,j);
			for( void * Pos=m_pCols[j].HeadPos() ; Pos ; m_pCols[j].Next(Pos) )
			{
				CString l_Elt;
				l_Elt.Format( "{ (%d,%d) = %.9f } ", m_pCols[j].GetAt(Pos)->m_I,
													 m_pCols[j].GetAt(Pos)->m_J,
													 m_pCols[j].GetAt(Pos)->m_Val );
				l_Col += l_Elt;
			}
			LOGMSG(l_Col);
		}
	}
	LOGMSG();
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
void CSparseMatrix::LogColLists( CString p_Prefix/*=""*/ )
{
	if( !m_W )
	{
		LOGMSG("%s [.] = empty matrix",p_Prefix);
	}
	else
	{
		for( int j=0 ; j<m_W ; j++ )
			LOGMSG("%s COL[%.2d] = %s",p_Prefix,j,m_pCols[j].ToString());
	}
	LOGMSG();
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
void CSparseMatrix::NonNullCellStatPerRow( int & Max, int & Min, int & Avg, int & Tot )
{
	Max = 0;
	Min = Cols();
	Tot = 0;

	for( int I=0 ; I<Rows() ; I++ )
	{
		int Row = m_pRows[I].Count();

		if( Row > Max )
			Max = Row;

		if( Row < Min )
			Min = Row;

		Tot += Row;
	}

	Avg = Tot / Rows();
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
void CSparseMatrix::LogStats()
{
	int Max, Min, Avg, Tot;
	NonNullCellStatPerRow( Max, Min, Avg, Tot );

	LOGMSG("[CSparseMatrix::LogStats] : Mat is %d x %d",Rows(),Cols());
	LOGMSG("[CSparseMatrix::LogStats] : Max non null cells in row = %d",Max);
	LOGMSG("[CSparseMatrix::LogStats] : Min non null cells in row = %d",Min);
	LOGMSG("[CSparseMatrix::LogStats] : Avg non null in row = %d",Avg);
	LOGMSG("[CSparseMatrix::LogStats] : Tot non null in mat = %d",Tot);

	double PercentNN = (100.0*Tot)/(Rows()*Cols());
	LOGMSG("[CSparseMatrix::LogStats] : Occupation mat = %.5f %%",PercentNN);
}


//	CString Format =
//	"\n[CSparseMatrix::LogNonNullCellStatPerRow] :\n\
//	Mat is %d x %d\n\
//	Max non null in row = %d\n\
//	Min non null in row = %d\n\
//	Avg non null in row = %d\n\
//	Tot non null in mat = %d\n\
//	Occupation mat = %d %%\n\n";
//
//	CString Txt;
//	Txt.Format( Format, Rows(), Cols(), Max, Min, Avg, Tot, PercentNN );

