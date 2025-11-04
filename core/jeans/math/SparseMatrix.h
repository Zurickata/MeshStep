#ifndef __CSparseMatrix__
#define __CSparseMatrix__



#include <math.h>
#include <Storage/List.h>

class CMatrix;
class CVector;



class CSparseMatrix
{
public:

	//------------------------------------------------------------------------------
	class CCell
	{
	public:

		double m_Val;	// Cell value
		int m_RefCount;	// Reference counter for empty cell deletion

	protected:

		// Only the SparseMatrix can create and delete Cells
		CCell( int p_I, int p_J )
		{
			m_Val = 0;
			m_RefCount = 0;
			m_I = p_I; 
			m_J = p_J; 
			m_ColPos = NULL;
			m_RowPos = NULL;
		}
		~CCell() {}

		int m_I;
		int m_J;

		void * m_ColPos; // Position in col list
		void * m_RowPos; // Position in row list

		friend class CSparseMatrix;
	};
	//------------------------------------------------------------------------------

	// Construction / destruction
	CSparseMatrix();
	~CSparseMatrix();

	// Sizing
	bool SetDims( int p_H/*ROWS*/, int p_W/*COLS*/ );
	int Rows() const { return m_H; }
	int Cols() const { return m_W; }

	// Access
	double Elt( int p_I/*ROW*/, int p_J/*COL*/ ) const;
	CCell * PtrElt( int p_I/*ROW*/, int p_J/*COL*/ );

	// Operations
	void LoadEmpty();
	bool FromMatrix( const CMatrix & p_From, double tol=TOLERANCE );
	bool ToMatrix( CMatrix & p_To ) const;
	bool ColToVector( int p_J, CVector & p_To, int p_MatFirstRow=0 );
	bool Mult( const CVector & p_A, CVector & p_Res ) const;
	bool CompleteMult( const CVector & p_A, CVector & p_Res ) const;
	void RemoveCell( CCell * p_pCell );
	void RemoveCellKeepDiagonal( CCell * p_pCell );
	CSparseMatrix & operator=( const CSparseMatrix & p_In );

	// File operations
	bool SaveBin( const CString & pFname );
	bool LoadBin( const CString & pFname );

	// Cholesky
	bool LLt_ify( CSparseMatrix & p_L, int p_FirstRowCol=0 ) const;
	bool LLt_Update( CSparseMatrix & p_L, int p_SubmatFirstRowCol=0, int p_UpdateFromGlobalCol=0 ) const;
	static bool LLt_Solve( const CSparseMatrix & p_L, CVector & p_X, const CVector & p_Y, int p_YFirstRow=0 );

	// Gaussian elimination: makes all equations p_Var-independent (except row #p_Var)
//	bool SubsInAllRowsFor( int p_Var, CVector & p_F ); TO DO 

	// Debug
	bool IsEqual( const CSparseMatrix & p_Other, double tol=TOLERANCE );
	void Log( CString p_Prefix="" );
	void LogBin( CString p_Prefix="" );
	void LogBinToRAWImage( CString p_FnamePrefix="" );
	void LogRows( CString p_Prefix="" );
	void LogRowLists( CString p_Prefix="" );
	void LogCols( CString p_Prefix="" );
	void LogColLists( CString p_Prefix="" );
	void NonNullCellStatPerRow( int & Max, int & Min, int & Avg, int & Tot );
	void LogStats();

	// What is zero and what is not ....
	static const double TOLERANCE;

protected:
 
	// Liberation
	void Free();

	// Nullification
	static bool IsZero( double x, double tol=TOLERANCE ) { return fabs(x)<tol; }

	// Cell finding
	CCell * FindCellInRow( int p_I, int p_J, void * & p_NextCellInRow ) const;
	CCell * FindCellInCol( int p_I, int p_J, void * & p_NextCellInCol ) const;
	
	// Non null rows in col below row
	void NonNullRows( int p_InJ, int p_BelowI, CLst<int> & p_Is ) const;

	// List merging
	static void MergeLists( const CLst<int> & p_As, CLst<int> & p_Bs );

	// Data
	int m_H;
	int m_W;
	CLst<CCell*> * m_pRows;
	CLst<CCell*> * m_pCols;
};



#endif //__CSparseMatrix__
