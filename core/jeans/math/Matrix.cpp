//#include "stdafx.h"
#include <float.h>
#include "Matrix.h"
#include "Vector.h"
#include "PolyMatrix.h"
//#include <Services\Log.h>
#include <ctime>
#include <fcntl.h>
//#include <sys/io.h>

#define LOGERR(...) printf(__VA_ARGS__)
#define LOGMSG(...) printf(__VA_ARGS__)

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
//CList<int,int> CMatrix::m_LocalRows;
//CList<int,int> CMatrix::m_LocalCols;
CLst<int> CMatrix::m_LocalRows;
CLst<int> CMatrix::m_LocalCols;

// What is zero and what is not ....
const double CMatrix::TOLERANCE = 1e-15;

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
CMatrix::CMatrix()
{
//	LOGMSG("CMatrix::CMatrix");

	m_H = m_W = 0;
	m_pMat = NULL;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
CMatrix::CMatrix( const CMatrix & p_M )
{
	//Added by clobs to compile
	m_H = m_W = 0;
        m_pMat = NULL;
	//next line commented by clobs
	//this->CMatrix::CMatrix(); // default constructor not called !
	
//	LOGMSG("CMatrix::CMatrix( const CMatrix & p_M )");

	*this = p_M;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
CMatrix::CMatrix( int p_H, int p_W, double p_00, .../*,01,02,..,10,11,12,..,20,21,22*/ )
{

	//Added by clobs to compile
	m_H = m_W = 0;
        m_pMat = NULL;
	//next line commented by clobs
	//this->CMatrix::CMatrix(); // default constructor not called !

//	LOGMSG("CMatrix::CMatrix( int p_H=%d, int p_W=%d, double p_00, .../*,01,02,..,10,11,12,..,20,21,22*/ )",p_H,p_W);

	// Init matrix
	if( !SetDims(p_H,p_W) )
	{
		LOGERR("[CMatrix::CMatrix] : Could not set dims (%d,%d) !",p_H,p_W);
		return;
	}

	Elt(0,0) = p_00;

	va_list l_List;
	va_start( l_List, p_00 );

	for( int i=0 ; i<p_H ; i++ )
	for( int j=(i?0:1) ; j<p_W ; j++ )
	{
		Elt(i,j) = va_arg( l_List, double );
	}

	va_end( l_List );
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
CMatrix::~CMatrix()
{
	Free();
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
void CMatrix::Free()
{
	if( m_pMat )
	{
		// Free
		for( int j=0 ; j<m_W ; j++ )
			delete[] m_pMat[j];

		delete[] m_pMat;
		m_pMat = NULL;
	}

	// Mark as freed
	m_H = m_W = 0;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CMatrix::SetDims( int p_H, int p_W )
{
//	LOGMSG("CMatrix::SetDims( int p_H=%d, int p_W=%d )",p_H,p_W);

	// Ok ?
	if( p_H<0 || p_W<0 )
	{
		LOGERR("[CMatrix::SetDims] : Invalid dims !");
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
//		LOGMSG("CMatrix::SetDims ==> alloc");

		// Alloc
		m_pMat = new double * [p_W];
		for( int j=0 ; j<p_W ; j++ )
			m_pMat[j] = new double [p_H];

		// Keep
		m_H = p_H;
		m_W = p_W;
	}

	return true;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
static double ERR_ELT = 666;
double & CMatrix::Elt( int p_I, int p_J )
{
#ifdef _DEBUG
	// Ok ?
	if( p_I>=m_H || p_I<0
	 || p_J>=m_W || p_J<0 )
	{
		LOGERR("[CMatrix::Elt] : Accessing invalid element (i=%d,j=%d) !",p_I,p_J);
		return ERR_ELT;
	}
#endif

	return m_pMat[p_J][p_I];
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
const double & CMatrix::Elt( int p_I, int p_J ) const
{
#ifdef _DEBUG
	// Ok ?
	if( p_I>=m_H || p_I<0
	 || p_J>=m_W || p_J<0 )
	{
		LOGERR("[CMatrix::Elt] : Accessing invalid element (i=%d,j=%d) !",p_I,p_J);
		return ERR_ELT;
	}
#endif

	return m_pMat[p_J][p_I];
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CMatrix::SubMatrixTo( int p_FirstRow, int p_LastRow, int p_FirstCol, int p_LastCol, CMatrix & p_To )
{
	// Ok ?
	if( p_FirstRow>p_LastRow
	 || p_FirstCol>p_LastCol
	 || p_FirstRow<0
	 || p_FirstCol<0
	 || p_LastRow>=m_H
	 || p_LastCol>=m_W )
	{
		LOGERR("[CMatrix::SubMatrixTo] : Invalid range !");
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

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CMatrix::SubMatrixTo( int p_FirstRow, int p_LastRow, int p_Col, CVector & p_To )
{
	// Ok ?
	if( p_FirstRow>p_LastRow
	 || p_FirstRow<0
	 || p_LastRow>=m_H
	 || p_Col<0
	 || p_Col>=m_W )
	{
		LOGERR("[CMatrix::SubMatrixTo] : Invalid range !");
		return false;
	}

	// Fill new matrix
	p_To.SetDim( p_LastRow-p_FirstRow+1 );
	for( int i=0 ; i<p_To.Rows() ; i++ )
	{
		p_To.Elt(i) = Elt( p_FirstRow+i, p_Col );
	}

	return true;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CMatrix::SubMatrixTo( int p_Col, CVector & p_To )
{
	return SubMatrixTo( 0, Rows()-1, p_Col, p_To );
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
const double * CMatrix::GetColBuffer( int p_J ) const
{
	if( p_J<0 || p_J>m_W )
	{
		LOGERR("[CMatrix::GetColBuffer] : Invalid col index (%d) !",p_J);
		return NULL;
	}

	return m_pMat[p_J];
}


////////////////////////////////////////////////////////////////////////////////
//
// Operations
//
//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
void CMatrix::LoadIdentity()
{
	for( int i=0 ; i<m_H ; i++ )
	for( int j=0 ; j<m_W ; j++ )
		Elt(i,j) = i==j ? 1 : 0 ;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
void CMatrix::LoadValue( double p_Value )
{
	for( int i=0 ; i<m_H ; i++ )
	for( int j=0 ; j<m_W ; j++ )
		Elt(i,j) = p_Value;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CMatrix::Mult( const CMatrix & p_A, CMatrix & p_Res ) const
{
	// Ok ?
	if( !Rows() || !Cols() || p_A.Rows()!=Cols() || !p_A.Cols() )
	{
		LOGERR("[CMatrix::Mult] : Unable to multiplicate !");
		return false;
	}

	// Dim
	p_Res.SetDims( Rows(), p_A.Cols() );

	for( int i=0 ; i<p_Res.Rows() ; i++ )
	for( int j=0 ; j<p_Res.Cols() ; j++ )
	{
		p_Res.Elt(i,j) = 0;

		for( int k=0 ; k<Cols() ; k++ )
			p_Res.Elt(i,j) += Elt(i,k) * p_A.Elt(k,j);
	}

	return true;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CMatrix::Mult( const CPolyMatrix & p_A, CPolyMatrix & p_Res ) const
{
	// Ok ?
	if( !Rows() || !Cols() || p_A.Rows()!=Cols() || !p_A.Cols() )
	{
		LOGERR("[CMatrix::Mult] : Unable to multiplicate !");
		return false;
	}

	// Dim
	p_Res.SetDims( Rows(), p_A.Cols() );

	for( int i=0 ; i<p_Res.Rows() ; i++ )
	for( int j=0 ; j<p_Res.Cols() ; j++ )
	{
		p_Res.Elt(i,j) = 0;

		for( int k=0 ; k<Cols() ; k++ )
			p_Res.Elt(i,j) = p_Res.Elt(i,j) + Elt(i,k)*p_A.Elt(k,j);
	}

	return true;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CMatrix::Mult( double p_A, CMatrix & p_Res ) const
{
	if( !p_Res.SetDims(Rows(),Cols()) )
	{
		LOGERR("[CMatrix::Mult] : Unable to multiplicate !");
		return false;
	}

	for( int i=0 ; i<Rows() ; i++ )
	for( int j=0 ; j<Cols() ; j++ )
	{
		p_Res.Elt(i,j) = p_A * Elt(i,j);
	}

	return true;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CMatrix::AddMult( double p_A, const CMatrix & p_B, CMatrix & p_Res ) const
{
	// Ok ?
	if( !Rows() || !Cols() || Rows()!=p_B.Rows() || Cols()!=p_B.Cols() )
	{
		LOGERR("[CMatrix::MultAdd] : Unable to add !");
		return false;
	}

	p_Res.SetDims( Rows(), Cols() );

	for( int i=0 ; i<Rows() ; i++ )
	for( int j=0 ; j<Cols() ; j++ )
	{
		p_Res.Elt(i,j) = Elt(i,j) + p_A * p_B.Elt(i,j);
	}

	return true;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CMatrix::Add( const CMatrix & p_A, CMatrix & p_Res ) const
{
	// Ok ?
	if( !Rows() || !Cols() || Rows()!=p_A.Rows() || Cols()!=p_A.Cols() )
	{
		LOGERR("[CMatrix::Add] : Unable to add !");
		return false;
	}

	// Dim
	p_Res.SetDims( Rows(), Cols() );

	for( int i=0 ; i<Rows() ; i++ )
	for( int j=0 ; j<Cols() ; j++ )
		p_Res.Elt(i,j) = Elt(i,j) + p_A.Elt(i,j);

	return true;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CMatrix::Sub( const CMatrix & p_A, CMatrix & p_Res ) const
{
	// Ok ?
	if( !Rows() || !Cols() || Rows()!=p_A.Rows() || Cols()!=p_A.Cols() )
	{
		LOGERR("[CMatrix::Sub] : Unable to substract !");
		return false;
	}

	// Dim
	p_Res.SetDims( Rows(), Cols() );

	for( int i=0 ; i<Rows() ; i++ )
	for( int j=0 ; j<Cols() ; j++ )
		p_Res.Elt(i,j) = Elt(i,j) - p_A.Elt(i,j);

	return true;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CMatrix::Pow( int p_Pow, CMatrix & p_Res ) const
{
	if( Cols() != Rows() )
	{
		LOGERR("[CMatrix::Pow] : Matrix not square !");
		return false;
	}

	CMatrix l_Tmp;
	if( !p_Res.SetDims(Rows(),Cols())
	 || !l_Tmp.SetDims(Rows(),Cols()) )
	{
		LOGERR("[CMatrix::Pow] : Unable to set matrices !");
		return false;
	}

	p_Res.LoadIdentity();
	
	while( p_Pow )
	{
		Mult(p_Res,l_Tmp);
		p_Res = l_Tmp;
		p_Pow--;
	}
	
	return true;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CMatrix::Transpose()
{
	if( Cols() != Rows() )
	{
		LOGERR("[CMatrix::Transpose] : Matrix not square !");
		return false;
	}

	for( int i=0 ; i<Rows() ; i++ )
	for( int j=0 ; j<i      ; j++ )
	{
		double l_Tmp = Elt(i,j);
		Elt(i,j) = Elt(j,i);
		Elt(j,i) = l_Tmp;
	}

	return true;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CMatrix::TransposeTo( CMatrix & p_Res ) const
{
	if( !p_Res.SetDims(Cols(),Rows()) )
	{
		LOGERR("[CMatrix::TransposeTo] : Dimension error !");
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
CMatrix & CMatrix::operator=( const CMatrix & p_In )
{
//	LOGMSG("CMatrix::operator=");

	if( SetDims(p_In.Rows(),p_In.Cols()) )
	{
		for( int i=0 ; i<Rows() ; i++ )
		for( int j=0 ; j<Cols() ; j++ )
			Elt(i,j) = p_In.Elt(i,j);
	}
	else
	{
		LOGERR("[CMatrix::operator=] : Unable to copy matrix !");
	}

	return *this;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
double CMatrix::MaxFabs() const
{
	double l_MaxFabs = -1;

	for( int i=0 ; i<m_H ; i++ )
	for( int j=0 ; j<m_W ; j++ )
	{
		double l_Abs = fabs(Elt(i,j));
		if( l_Abs > l_MaxFabs )
			l_MaxFabs = l_Abs;
	}

	return l_MaxFabs;
}


////////////////////////////////////////////////////////////////////////////////
//
// File operations
//
//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CMatrix::SaveBin( const string & pFname )
{
	/*string aux_pFname = pFname;
	// Open file for writing
	FILE * l_File = fopen( aux_pFname.c_str() , "w" );
	if( !l_File )
	{
		LOGERR("[CMatrix::SaveBin] : Could not create file <%s> !",aux_pFname.c_str());
		return false;
	}

	// Switch to binary
	_setmode( _fileno(l_File) , _O_BINARY );

	// Write header for matrix and dims
	if( fwrite("MAT",sizeof(char),3,l_File)!=3
	 || fwrite(&m_H,sizeof(int),1,l_File)!=1
	 || fwrite(&m_W,sizeof(int),1,l_File)!=1 )
	{
		LOGERR("[CMatrix::SaveBin] : Could not write header !");
		return false;
	}

	// Write mat elements
	for( int i=0 ; i<m_H ; i++ )
	for( int j=0 ; j<m_W ; j++ )
	{
		// Write cell
		if( fwrite(&m_pMat[j][i],sizeof(double),1,l_File)!=1 )
		{
			LOGERR("[CMatrix::SaveBin] : Could not write cell (%d,%d) !",i,j);
			return false;
		}
	}

	// Fini
	fclose(l_File);
	return true;*/
	return false;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CMatrix::LoadBin( const string & pFname )
{
	/*string aux_pFname = pFname;
	// Open file for writing
	FILE * l_File = fopen( aux_pFname.c_str() , "r" );
	if( !l_File )
	{
		LOGERR("[CMatrix::LoadBin] : Could not open file <%s> !",aux_pFname.c_str());
		return false;
	}

	// Switch to binary
	_setmode( _fileno(l_File) , _O_BINARY );

	// Read header for sparse matrix and dims
	char lHeader[4];
	lHeader[3] = 0;
	int lW, lH;
	if( fread(lHeader,sizeof(char),3,l_File)!=3
	 || strcmp(lHeader,"MAT")
	 || fread(&lH,sizeof(int),1,l_File)!=1
	 || fread(&lW,sizeof(int),1,l_File)!=1
	 || !SetDims(lH,lW) )
	{
		LOGERR("[CMatrix::LoadBin] : Could not init matrix !");
		return false;
	}

	// Read mat elements
	for( int i=0 ; i<m_H ; i++ )
	for( int j=0 ; j<m_W ; j++ )
	{
		// Read cell
		if( fread(&m_pMat[j][i],sizeof(double),1,l_File)!=1 )
		{
			LOGERR("[CMatrix::LoadBin] : Could not read cell (%d,%d) !",i,j);
			return false;
		}
	}

	// Fini
	fclose(l_File);
	return true;*/
	return false;
}


////////////////////////////////////////////////////////////////////////////////
//
// Permutations
//
//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
//bool CMatrix::LoadPermutation( const CContainer1<int> & p_Mapping )
//{
//	// Check dimensions
//	if( !SetDims(p_Mapping.Width(),p_Mapping.Width()) )
//	{
//		LOGERR("[CMatrix::LoadPermutation] : Dimensions error !");
//		return false;
//	}
//
//	LoadValue(0);
//
//	// Fill
//	for( int i=0 ; i<m_H ; i++ )
//	{
//		int j = p_Mapping[i];
//		if( j<0 || j>=m_W )
//		{
//			LOGERR("[CMatrix::LoadPermutation] : Mapping error (i=%d,j=%d) !",i,j);
//			return false;
//		}
//
//		Elt(i,j) = 1;
//	}
//
//	// Check
//	for( int j=0 ; j<m_W ; j++ )
//	{
//		int count = 0;
//		for( i=0 ; i<m_H ; i++ )
//		{
//			if( Elt(i,j) > 0.5 )
//				count++;
//		}
//
//		if( count != 1 )
//		{
//			LOGERR("[CMatrix::LoadPermutation] : Mapping error : col (j=%d) has %d 1s !",j,count);
//			return false;
//		}
//	}
//
//	return true;
//}

////////////////////////////////////////////////////////////////////////////////
//
// Rotations
//
//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CMatrix::LoadRotation( const CVector & pRoot, const CVector & pDir, double pDeg )
{
	// Check dims
	if( pRoot.Rows()!=3 || pDir.Rows()!=3 )
	{
		LOGERR("[CMatrix::LoadRotation] : Invalid dims !");
		return false;
	}

	// Normalize dir
	CVector Dir = pDir;
	if( !Dir.Normalize() )
	{
		LOGERR("[CMatrix::LoadRotation] : Invalid rotation axis !");
		return false;
	}

	// Deg to rad
	double Rad = pDeg * 3.14159265 / 180.0;

	// Scal mat
	CMatrix S;
	Dir.ExtrProd( Dir, S );

	// Cross mat
	CMatrix W( 3,3, 0.0, -Dir.Elt(2), Dir.Elt(1),
					Dir.Elt(2), 0.0 ,-Dir.Elt(0),
					-Dir.Elt(1), Dir.Elt(0), 0.0 );
	// Sin mat
	CMatrix sinW;
	W.Mult( sin(Rad), sinW );

	// Cos mat
	CMatrix cosWW;
	W.Mult( W, cosWW );
	cosWW.Mult( -cos(Rad), cosWW );

	// Total cos mat + sin mat
	CMatrix Sum;
	S.Add( cosWW, Sum );
	Sum.Add( sinW, Sum );

	// This = pure rotation
	SetDims( 4, 4 );
	for( int i=0 ; i<3 ; i++ )
	  for( int j=0 ; j<3 ; j++ )
	  {
		Elt(i,j) = Sum.Elt(i,j);
	  }
	
	for(int i=0 ; i<3 ; i++ )
	{
		Elt(i,3) = 0;
		Elt(3,i) = 0;
	}
	Elt(3,3) = 1;

	// Translation to / from origin
	CMatrix T, U;
	T.SetDims( 4, 4 );
	U.SetDims( 4, 4 );
	T.LoadIdentity(); 
	U.LoadIdentity();
	T.Elt(0,3) = pRoot.Elt(0);
	T.Elt(1,3) = pRoot.Elt(1);
	T.Elt(2,3) = pRoot.Elt(2);
	U.Elt(0,3) = -pRoot.Elt(0);
	U.Elt(1,3) = -pRoot.Elt(1);
	U.Elt(2,3) = -pRoot.Elt(2);

	// This = all together
	CMatrix RU;
	Mult( U, RU );
	T.Mult( RU, *this );

	return true;
}


////////////////////////////////////////////////////////////////////////////////
//
// Co-Facteurs
//
//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
double CMatrix::CF_Det( bool p_EmptyMat/*=false*/ )
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
int CMatrix::MaxZeroLocalRow()
{
	int l_MaxZeroCount = -1;
	int l_LocalRow = 0;
	int l_BestRow;

	void * i_RowPos;
	BrowseList( i_RowPos, m_LocalRows )
//	for( POSITION i_RowPos=m_LocalRows.HeadPos() ; i_RowPos ; )
	{
//		int l_GlobalRow = m_LocalRows.GetNext(i_RowPos);
		int l_GlobalRow = m_LocalRows.GetAt(i_RowPos);
		int l_ZeroCount = 0;

		void * i_ColPos;
//		for( POSITION i_ColPos=m_LocalCols.GetHeadPosition() ; i_ColPos ; )
		BrowseList( i_ColPos, m_LocalCols )
		{
//			int l_GlobalCol = m_LocalCols.GetNext(i_ColPos);
			int l_GlobalCol = m_LocalCols.GetAt(i_ColPos);

			if( fabs(Elt(l_GlobalRow,l_GlobalCol)) < TOLERANCE )
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
double CMatrix::CF_RecDet( bool p_EmptyMat/*=false*/ )
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
		double l_00 = Elt(m_LocalRows.GetHead(),m_LocalCols.GetHead());
		double l_11 = Elt(m_LocalRows.GetTail(),m_LocalCols.GetTail());
		double l_01 = Elt(m_LocalRows.GetHead(),m_LocalCols.GetTail());
		double l_10 = Elt(m_LocalRows.GetTail(),m_LocalCols.GetHead());

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
	double l_Det = 0;
	for( int i_LocalJ=0 ; i_LocalJ<LocalCols() ; i_LocalJ++ )
	{
		// Remove local col
		int l_GlobalCol = RemoveLocalCol(i_LocalJ);

		// Compute sub det only if element non null
		double l_Elt = Elt(l_GlobalRow,l_GlobalCol);
		if( fabs(l_Elt) >= TOLERANCE ) //!IsZero(l_Elt) )
			l_Det += ((l_LocalI+i_LocalJ)%2 ? -1 : +1) * l_Elt * CF_RecDet(p_EmptyMat);

		// Add global col for further computing
		AddGlobalCol( l_GlobalCol );
	}

	// Add global row further computing
	AddGlobalRow( l_GlobalRow );

	return l_Det;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
void CMatrix::InitLocalRowsCols()
{
	m_LocalRows.DelAll();
	m_LocalCols.DelAll();
	for( int i=0 ; i<m_H ; i++ )
	{
		m_LocalRows.AddTail(i);
		m_LocalCols.AddTail(i);
	}
}
int CMatrix::RemoveLocalRow( int p_LocalI )
{
	if( p_LocalI<0 || p_LocalI>=m_LocalRows.Count() )
	{
		LOGERR("[CMatrix::RemoveLocalRow] : Could not remove %d !",p_LocalI);
		return -1;
	}
	void * l_Pos = m_LocalRows.FindIdx(p_LocalI);
	int l_GlobalRow = m_LocalRows.GetAt( l_Pos );
	m_LocalRows.DelAt( l_Pos );
	return l_GlobalRow;
}
int CMatrix::RemoveLocalCol( int p_LocalJ )
{
	if( p_LocalJ<0 || p_LocalJ>=m_LocalCols.Count() )
	{
		LOGERR("[CMatrix::RemoveLocalCol] : Could not remove %d !",p_LocalJ);
		return -1;
	}
	void * l_Pos = m_LocalCols.FindIdx(p_LocalJ);
	int l_GlobalCol = m_LocalCols.GetAt( l_Pos );
	m_LocalCols.DelAt( l_Pos );
	return l_GlobalCol;
}
void CMatrix::AddGlobalRow( int p_GlobalI )
{
	void * i_Pos = m_LocalRows.HeadPos();
	while( i_Pos && m_LocalRows.GetAt(i_Pos)<p_GlobalI )
		m_LocalRows.Next(i_Pos);
	if( i_Pos )
		m_LocalRows.AddBefore( i_Pos, p_GlobalI );
	else
		m_LocalRows.AddTail(p_GlobalI);
}
void CMatrix::AddGlobalCol( int p_GlobalJ )
{
	void * i_Pos = m_LocalCols.HeadPos();
	while( i_Pos && m_LocalCols.GetAt(i_Pos)<p_GlobalJ )
		m_LocalCols.Next(i_Pos);
	if( i_Pos )
		m_LocalCols.AddBefore( i_Pos, p_GlobalJ );
	else
		m_LocalCols.AddTail(p_GlobalJ);
}
void CMatrix::LogLocalRows()
{
	/*
	string l_Log = "Local ROWS = [";
	void * i_Pos;
	BrowseList( i_Pos, m_LocalRows )
//	for( POSITION i_Pos=m_LocalRows.GetHeadPosition() ; i_Pos ; )
	{
		string l_Idx;
//		l_Idx.Format("\t%d",m_LocalRows.GetNext(i_Pos));
		l_Idx.Format("\t%d",m_LocalRows.GetAt(i_Pos));
		l_Log += l_Idx;
	}
	l_Log += "\t]";
	LOGMSG(l_Log.c_str());*/
}
void CMatrix::LogLocalCols()
{
	/*
	string l_Log = "Local COLS = [";
	void * i_Pos;
	BrowseList( i_Pos, m_LocalCols )
//	for( POSITION i_Pos=m_LocalCols.GetHeadPosition() ; i_Pos ; )
	{
		string l_Idx;
//		l_Idx.Format("\t%d",m_LocalCols.GetNext(i_Pos));
		l_Idx.Format("\t%d",m_LocalCols.GetAt(i_Pos));
		l_Log += l_Idx;
	}
	l_Log += "\t]";
	LOGMSG(l_Log.c_str());*/
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CMatrix::CF_InverseTo( CMatrix & p_Inv )
{
	// Ok ?
	if( !Rows() || Rows()!=Cols() )
	{
		LOGERR("[CMatrix::CF_InverseTo] : Unable to inverse !");
		return false;
	}

	// Inversible ?
	double l_Det = CF_Det();
	if( fabs(l_Det) < TOLERANCE )
	{
		LOGERR("[CMatrix::CF_InverseTo] : Matrix not inversible !");
		return false;
	}

	// Dims
	p_Inv.SetDims(Rows(),Cols());

	// Fill with transpose(co-factors)
	for( int i=0 ; i<Rows() ; i++ )
	for( int j=0 ; j<Cols() ; j++ )
	{
		// Remove
		RemoveLocalRow(i);
		RemoveLocalCol(j);

		// Compute co-factor and transpose
		p_Inv.Elt(j,i) = ((i+j)%2 ? -1 : +1) * CF_RecDet() / l_Det;

		// Add
		AddGlobalRow(i);
		AddGlobalCol(j);
	}

	return true;
}



////////////////////////////////////////////////////////////////////////////////
//
// LU
//
//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CMatrix::LU_ify( CMatrix & p_L, CMatrix & p_U )
{
	// Square ?
	if( Rows()!=Cols() || !p_L.SetDims(Cols(),Cols()) || !p_U.SetDims(Cols(),Cols()) )
	{
		LOGERR("[CMatrix::LU_ify] : Matrix not square !");
		return false;
	}

	// Reset
	p_L.LoadValue(0);
	p_U.LoadValue(0);

	int j;

	// Init first line U
	for( j=0 ; j<Cols() ; j++ )
		p_U.Elt(0,j) = Elt(0,j);

	// Init diagonal L
	for( j=0 ; j<Cols() ; j++ )
		p_L.Elt(j,j) = 1;

	// Fill columns(L) and lines(U)
	int i_ColRow=0;
	while( i_ColRow < Cols()-1 )
	{
		// Have solution ?
		double l_K = p_U.Elt(i_ColRow,i_ColRow);
		if( fabs(l_K) < TOLERANCE )
		{
			LOGERR("[CMatrix::LU_ify] : No solution !");
			return false;
		}

		// Fill col(L)
		for( int i=i_ColRow+1 ; i<Cols() ; i++ )
		{
			// Calc L(row=i, col=i_ColRow)
			double l_Sum = 0;
			for( int k=0 ; k<i_ColRow ; k++ )
				l_Sum += p_L.Elt(i,k) * p_U.Elt(k,i_ColRow);

			p_L.Elt(i,i_ColRow) = ( Elt(i,i_ColRow) - l_Sum ) / l_K;
		}

		// Next row for U
		i_ColRow++;

		// Fill row(U)
		for( int j=i_ColRow ; j<Cols() ; j++ )
		{
			// Calc U(row=i_ColRow, col=j)
			double l_Sum = 0;
			for( int k=0 ; k<i_ColRow ; k++ )
				l_Sum += p_L.Elt(i_ColRow,k) * p_U.Elt(k,j);

			p_U.Elt(i_ColRow,j) = Elt(i_ColRow,j) - l_Sum;
		}
	}

	return true;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CMatrix::LU_Det( double & p_Det )
{
	CMatrix L,U;
	if( !LU_ify(L,U) )
	{
		LOGERR("[CMatrix::LU_Det] : Unable to LU-ify !");
		return false;
	}

	p_Det = U.TriDet();

	return true;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CMatrix::LU_InverseTo( CMatrix & p_Inv )
{
	// Decomposition
	CMatrix L,U;
	if( !LU_ify(L,U) )
	{
		LOGERR("[CMatrix::LU_InverseTo] : Unable to LU-ify !");
		return false;
	}

	// Inverse each triangular mat
	CMatrix InvL, InvU;
	if( !L.L_InverseTo(InvL)
	 || !U.U_InverseTo(InvU) )
	{
		LOGERR("[CMatrix::LU_InverseTo] : Matrix not inversible !");
		return false;
	}

	// Put all together
	InvU.Mult( InvL, p_Inv );

	return true;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CMatrix::LU_Solve( CVector & p_X, const CVector & p_Y )
{
	// This is a square non-empty matrix ?
	if( !Rows() || Rows()!=Cols() )
	{
		LOGERR("[CMatrix::LU_Solve] : Empty or not square matrix !");
		return false;
	}

	// Y vector ok ?
	if( Cols() != p_Y.Rows() )
	{
		LOGERR("[CMatrix::LU_Solve] : Dimensions mismatch !");
		return false;
	}

	CMatrix L,U;
	if( !LU_ify(L,U) )
	{
		LOGERR("[CMatrix::LU_Solve] : Unable to LU-ify !");
		return false;
	}

	// Z <== Z / LZ=Y
	CVector Z;
	Z.SetDim( p_Y.Rows() );
	for( int i=0 ; i<p_Y.Rows() ; i++ )
	{
		Z.Elt(i) = p_Y.Elt(i);
		
		for( int j=i-1 ; j>=0 ; j-- )
			Z.Elt(i) -= L.Elt(i,j)*Z.Elt(j); 
	}

	// X <== X / UX=Z
	p_X.SetDim( p_Y.Rows() );
	for(int i=p_Y.Rows()-1 ; i>=0 ; i-- )
	{
		p_X.Elt(i) = Z.Elt(i) / U.Elt(i,i);

		for( int j=i+1 ; j<p_Y.Rows() ; j++ )
			p_X.Elt(i) -= U.Elt(i,j)*p_X.Elt(j)/U.Elt(i,i); 
	}

	return true;
}



////////////////////////////////////////////////////////////////////////////////
//
// Cholesky LLt : matrice sym def pos
//
//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CMatrix::LLt_ify( CMatrix & p_L )
{
	// Square ?
	if( Rows() != Cols() )
	{
		LOGERR("[CMatrix::LLt_ify] : Matrix not square !");
		return false;
	}

	// Ok ?
	if( !p_L.SetDims(Cols(),Cols()) )
	{
		LOGERR("[CMatrix::LLt_ify] : Dim error !");
		return false;
	}

	// Reset
	p_L.LoadValue(0);

	int i,j,k;

	// Fill col by col
	for( j=0 ; j<Cols() ; j++ )
	{
		// Ljj
		double Ljj_sum = Elt(j,j);
		for( i=0 ; i<j ; i++ )
			Ljj_sum -= p_L.Elt(j,i)*p_L.Elt(j,i);
		if( Ljj_sum <= 0 )
		{
			LOGERR("[CMatrix::LLt_ify] : Unable to LLt-ify !");
			return false;
		}
		p_L.Elt(j,j) = sqrt(Ljj_sum);

		// Fill rows below Ljj
		for( i=j+1 ; i<Cols() ; i++ )
		{
			double Lij_sum = Elt(i,j);
			for( k=0 ; k<j ; k++ )
				Lij_sum -= p_L.Elt(j,k)*p_L.Elt(i,k);

			p_L.Elt(i,j) = Lij_sum / p_L.Elt(j,j);
		}
	}

	return true;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CMatrix::LLt_Solve( const CMatrix & p_L, CVector & p_X, const CVector & p_Y )
{
	// L matrix ok ?
	if( !p_L.Rows() || p_L.Rows()!=p_L.Cols() )
	{
		LOGERR("[CMatrix::LLt_Solve] : Empty or not square L matrix !");
		return false;
	}

	// Y vector ok ?
	if( p_L.Rows() != p_Y.Rows() )
	{
		LOGERR("[CMatrix::LLt_Solve] : Dimensions mismatch !");
		return false;
	}

	int i,j;

	// Check L
	for( i=0 ; i<p_L.Rows() ; i++ )
	if( p_L.Elt(i,i) == 0 )
	{
		LOGERR("[CMatrix::LLt_Solve] : Unable to solve !");
		return false;
	}

	// Z <== Z / LZ=Y
	CVector Z;
	Z.SetDim( p_Y.Rows() );
	for( i=0 ; i<Z.Rows() ; i++ )
	{
		Z.Elt(i) = p_Y.Elt(i);
		
		for( j=0 ; j<i ; j++ )
			Z.Elt(i) -= p_L.Elt(i,j)*Z.Elt(j);

		Z.Elt(i) /= p_L.Elt(i,i);
	}

	// X <== X / LtX=Z
	p_X.SetDim( p_Y.Rows() );
	for( i=p_Y.Rows()-1 ; i>=0 ; i-- )
	{
		p_X.Elt(i) = Z.Elt(i);

		for( j=i+1 ; j<p_Y.Rows() ; j++ )
			p_X.Elt(i) -= p_L.Elt(j,i)*p_X.Elt(j);

		p_X.Elt(i) /= p_L.Elt(i,i);
	}

	return true;
}



////////////////////////////////////////////////////////////////////////////////
//
// Matrices triangulaires
//
//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
double CMatrix::TriDet()
{
	//!!! Assuming non-empty square matrix !!!

	double l_Det = 1;
	for( int i=0 ; i<Cols() ; i++ )
		l_Det *= Elt(i,i);

	return l_Det;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CMatrix::L_InverseTo( CMatrix & p_InvL )
{
	// Inversible ?
	if( fabs(TriDet()) < TOLERANCE )
	{
		LOGERR("[CMatrix::L_InverseTo] : Matrix not invertible !");
		return false;
	}

	if( !p_InvL.SetDims(Rows(),Cols()) )
	{
		LOGERR("[CMatrix::L_InverseTo] : Unable to set matrix !");
		return false;
	}

	// Fill-in inverse col after col
	for( int j=0 ; j<Cols() ; j++ )
	for( int i=0 ; i<Rows() ; i++ )
	{
		if( i < j )
		{
			p_InvL.Elt(i,j) = 0;
		}
		else if( i == j )
		{
			p_InvL.Elt(i,i) = 1 / Elt(i,i);
		}
		else
		{
			double l_Sum = 0;
			for( int k=j ; k<i ; k++ )
				l_Sum += Elt(i,k)*p_InvL.Elt(k,j);

			p_InvL.Elt(i,j) = -l_Sum / Elt(i,i);
		}
	}

	return true;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CMatrix::U_InverseTo( CMatrix & p_InvU )
{
	// Inversible ?
	if( fabs(TriDet()) < TOLERANCE )
	{
		LOGERR("[CMatrix::U_InverseTo] : Matrix not invertible !");
		return false;
	}

	if( !p_InvU.SetDims(Rows(),Cols()) )
	{
		LOGERR("[CMatrix::U_InverseTo] : Unable to set matrix !");
		return false;
	}

	// Fill-in inverse backwards col after col
	for( int j=Cols()-1 ; j>=0 ; j-- )
	for( int i=Rows()-1 ; i>=0 ; i-- )
	{
		if( i > j )
		{
			p_InvU.Elt(i,j) = 0;
		}
		else if( i == j )
		{
			p_InvU.Elt(i,i) = 1 / Elt(i,i);
		}
		else
		{
			double l_Sum = 0;
			for( int k=Rows()-1 ; k>i ; k-- )
				l_Sum += Elt(i,k)*p_InvU.Elt(k,j);

			p_InvU.Elt(i,j) = -l_Sum / Elt(i,i);
		}
	}

	return true;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CMatrix::SubsInAllRowsFor( int p_Var, CVector & p_F )
{
	// Check if matrix and vector are ok ?
	if( !Rows() || Rows()!=Cols() || Rows()!=p_F.Rows() )
	{
		LOGERR("[CMatrix::SubsInAllRowsFor] : Wrong dims !");
		return false;
	}

	// Check if variable ok
	if( p_Var<0 || p_Var>=Rows() )
	{
		LOGERR("[CMatrix::SubsInAllRowsFor] : Wrong variable !");
		return false;
	}

	// Divisor
	double lPivot = Elt( p_Var, p_Var );
	if( fabs(lPivot) < DBL_EPSILON )
	{
		LOGERR("[CMatrix::SubsInAllRowsFor] : Could not substitute for variable %d ! Null coef.",p_Var);
		return false;
	}

	// Substitute in all rows
	for( int i=0 ; i<Rows() ; i++ )
	{
		// Skip p_Var row
		if( i == p_Var )
			continue;

		// Change constant in vector
		p_F.Elt(i) = p_F.Elt(i) - p_F.Elt(p_Var)*Elt(i,p_Var)/lPivot;

		// Change coefs in matrix
		for( int j=0 ; j<Cols() ; j++ )
		{
			// Skip the col corresponding to p_Var (will be reset later)
			if( j == p_Var )
				continue;

			Elt(i,j) = Elt(i,j) - Elt(i,p_Var)*Elt(p_Var,j)/lPivot;
		}

		// Reset coef for p_Var
		Elt(i,p_Var) = 0;
	}

	return true;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CMatrix::KillRowCols( const CLst<int> & pRows, const CLst<int> & pCols, CMatrix & pToMat ) const
{
	// Check empty matrix
	if( !Rows() || !Cols() )
	{
		LOGERR("[CMatrix::KillRowCols] : Empty matrix !");
		return false;
	}

	// Check re-entrance
//#pragma message("----- AJOUTER CHECKS DE REENTRANCE PARTOUT ? (#ifdef _DEBUG)")
	if( &pToMat == this )
	{
		LOGERR("[CMatrix::KillRowCols] : Re-entering same matrix !");
		return false;
	}

	// Iterator
	void * iPos;

	// Check row idx ok
	for( iPos=pRows.HeadPos() ; iPos ; pRows.Next(iPos) )
	{
		int lIdx = pRows.GetAt( iPos );

		if( lIdx<0 || lIdx>=Rows() )
		{
			LOGERR("[CMatrix::KillRowCols] : Invalid row idx (%d) !",lIdx);
			return false;
		}
	}

	// Check col idx ok
	for( iPos=pCols.HeadPos() ; iPos ; pCols.Next(iPos) )
	{
		int lIdx = pCols.GetAt( iPos );

		if( lIdx<0 || lIdx>=Cols() )
		{
			LOGERR("[CMatrix::KillRowCols] : Invalid col idx (%d) !",lIdx);
			return false;
		}
	}

	// Reduced size
	int lNewRows = Rows();
	int lNewCols = Cols();

	// Build bool vectors
	static CVector lRowIn, lColIn;
	lRowIn.SetDim( Rows() );
	lColIn.SetDim( Cols() );
	lRowIn.LoadValue( 1 );
	lColIn.LoadValue( 1 );

	// Fill row bool vector
	for( iPos=pRows.HeadPos() ; iPos ; pRows.Next(iPos) )
	{
		int lIdx = pRows.GetAt( iPos );

		// In case of repeated idx
		if( lRowIn.Elt(lIdx) )
			lNewRows--;

		lRowIn.Elt(lIdx) = 0;
	}

	// Fill col bool vector
	for( iPos=pCols.HeadPos() ; iPos ; pCols.Next(iPos) )
	{
		int lIdx = pCols.GetAt( iPos );

		// In case of repeated idx
		if( lColIn.Elt(lIdx) )
			lNewCols--;

		lColIn.Elt(lIdx) = 0;
	}

	// Size matrix
	if( !pToMat.SetDims(lNewRows,lNewCols) )
	{
		LOGERR("[CMatrix::KillRowCols] : Unable to set mat dims !");
		return false;
	}

	// For all rows
	int lNewI = 0;
	for( int i=0 ; i<Rows() ; i++ )
	{
		// This row is in ?
		if( !lRowIn.Elt(i) )
			continue;

		// For all cols
		int lNewJ = 0;
		for( int j=0 ; j<Cols() ; j++ )
		{
			// This col is in ?
			if( !lColIn.Elt(j) )
				continue;

			// Copy element
			pToMat.Elt(lNewI,lNewJ) = Elt(i,j);

			// Next new col
			lNewJ++;
		}

		// Next new row
		lNewI++;
	}

	return true;
}


////////////////////////////////////////////////////////////////////////////////
//
// Debug
//
//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CMatrix::IsEqual( const CMatrix & p_Other, double tol/*=TOLERANCE*/ )
{
	if( Rows()!=p_Other.Rows()
	 || Cols()!=p_Other.Cols() )
	 return false;

	for( int i=0 ; i<Rows() ; i++ )
	for( int j=0 ; j<Cols() ; j++ )
	{
		if( fabs(Elt(i,j)-p_Other.Elt(i,j)) >= tol )
			return false;
	}

	return true;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CMatrix::IsIdentity( double tol/*=TOLERANCE*/ )
{
	if( !Rows() || Rows()!=Cols() )
	{
		LOGERR("[CMatrix::IsIdentity] : Matrix is empty or not square !");
		return false;
	}

	for( int i=0 ; i<Rows() ; i++ )
	for( int j=0 ; j<Cols() ; j++ )
	{
		if( fabs(Elt(i,j)-(i==j?1:0)) >= tol )
			return false;
	}

	return true;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CMatrix::IsNull( double tol/*=TOLERANCE*/ )
{
	if( !Rows() || !Cols() )
	{
		LOGERR("[CMatrix::IsNull] : Matrix is empty !");
		return false;
	}

	for( int i=0 ; i<Rows() ; i++ )
	for( int j=0 ; j<Cols() ; j++ )
	{
		if( fabs(Elt(i,j)) >= tol )
			return false;
	}

	return true;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
bool CMatrix::IsSymmetric( double tol/*=TOLERANCE*/ )
{
	if( !Rows() || Rows()!=Cols() )
	{
		LOGERR("[CMatrix::IsSymmetric] : Matrix is empty or not square !");
		return false;
	}

	for( int i=1 ; i<Rows() ; i++ )
	for( int j=0 ; j<i      ; j++ )
	{
		if( fabs(Elt(i,j)-Elt(j,i)) >= tol )
			return false;
	}

	return true;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
void CMatrix::LoadRandom( bool p_IntValues/*=true*/,double p_Center/*=0*/, double p_Amplitude/*=100*/ )
{
	srand( (unsigned)time( NULL ) );

	for( int i=0 ; i<m_H ; i++ )
	for( int j=0 ; j<m_W ; j++ )
	{
		double Rnd = p_Center + p_Amplitude*((double)rand()/(double)RAND_MAX - 0.5);

		if( p_IntValues )
		{
			Elt(i,j) = (int)Rnd;
		}
		else
		{
			Elt(i,j) = Rnd;
		}
	}
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
void CMatrix::LoadTridiagonal()
{
	if( m_H != m_W )
	{
		LOGMSG("[CMatrix::LoadTridiagonal] : Matrix not square !");
		return;
	}
	
	srand( (unsigned)time( NULL ) );

	LoadValue(0);

	for( int i=0 ; i<m_H ; i++ )
	{
		if( i-1 >= 0 )
			Elt(i,i-1) = 5;

		Elt(i,i) = 6;

		if( i+1 < m_W )
			Elt(i,i+1) = 5;
//
//		if( i-1 >= 0 )
//			Elt(i,i-1) = (int)( 20*(double)rand()/(double)RAND_MAX - 10 );
//
//		Elt(i,i) = (int)( 20*(double)rand()/(double)RAND_MAX - 10 );
//
//		if( i+1 < m_W )
//			Elt(i,i+1) = (int)( 20*(double)rand()/(double)RAND_MAX - 10 );
	}
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
void CMatrix::LoadRandomEmpty()
{
	srand( (unsigned)time( NULL ) );

	for( int i=0 ; i<m_H ; i++ )
	for( int j=0 ; j<m_W ; j++ )
	{
		if( (int)( 4*(double)rand()/(double)RAND_MAX ) == 0 )
			Elt(i,j) = (int)( 10*(double)rand()/(double)RAND_MAX - 5 );
		else
			Elt(i,j) = 0;
	}
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
void CMatrix::Log( string p_Prefix/*=""*/ ) const
{
	/*
	if( !m_H )
	{
		LOGMSG("%s [.] = empty matrix",p_Prefix.c_str());
	}
	else
	{
		for( int i=0 ; i<m_H ; i++ )
		{
			string l_Row;
			l_Row.Format("%s [%.2d] = [",p_Prefix,i);
			for( int j=0 ; j<m_W ; j++ )
			{
				string l_Elt;
				l_Elt.Format("\t%.16f",Elt(i,j));
				l_Row += l_Elt;
			}
			l_Row += "\t]";
			LOGMSG(l_Row.c_str());
		}
	}

	LOGMSG("\n");*/
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
void CMatrix::NonNullCellStatPerRow( int & Max, int & Min, int & Avg, int & Tot, double tol/*=TOLERANCE*/ )
{
	Max = 0;
	Min = Cols();
	Tot = 0;

	for( int i=0 ; i<Rows() ; i++ )
	{
		int Row = 0;

		for( int j=0 ; j<Cols() ; j++ )
			if( fabs(Elt(i,j)) >= tol )
				Row++;

		if( Row > Max )
			Max = Row;

		if( Row < Min )
			Min = Row;

		Tot += Row;
	}

	Avg = Tot / Rows();
}







