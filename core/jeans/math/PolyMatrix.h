#ifndef __CPolyMatrix__
#define __CPolyMatrix__



#include "List.h"
#include "Polynom.h"
#include <string>

using namespace std;


class CMatrix;



class CPolyMatrix
{
public:

	// Construction / destruction
	CPolyMatrix();
	~CPolyMatrix();

	// Sizing
	bool SetDims( int p_H/*ROWS*/, int p_W/*COLS*/ );
	int Rows() const { return m_H; }
	int Cols() const { return m_W; }
	void Free();

	// Access
	CPolynom & Elt( int p_I/*ROW*/, int p_J/*COL*/ );
	CPolynom Elt( int p_I/*ROW*/, int p_J/*COL*/ ) const;
	bool SubMatrixTo( int p_FirstRow, int p_LastRow, int p_FirstCol, int p_LastCol, CPolyMatrix & p_To );

	// Operations
	bool Mult( const CMatrix & p_A, CPolyMatrix & p_Res );
	bool Mult( const CPolyMatrix & p_A, CPolyMatrix & p_Res );
	bool TransposeTo( CPolyMatrix & p_Res );

	// Evaluation
	void EvalTo( double X, double Y, CMatrix & p_To ) const;
	void EvalTo( double X, double Y, double Z, CMatrix & p_To ) const;

	// Integration
	bool IntegralTo( int p_MaxDegX, int p_MaxDegY, int p_MaxDegZ, double * p_pSums, CMatrix & p_Res );

	// Debug
	void Log( string p_Prefix="" );

	// Co-Facteurs
	CPolynom CF_Det( bool p_EmptyMat=false );
	bool CF_InverseTo( CPolyMatrix & p_Cof, CPolynom & p_Det );


protected:

	// Data
	int m_H;
	int m_W;
	CPolynom ** m_pMat;

	// Co-Facteurs
	int MaxZeroLocalRow();
	CPolynom CF_RecDet( bool p_EmptyMat=false );
	void InitLocalRowsCols();
	static CLst<int> m_LocalRows;
	static CLst<int> m_LocalCols;
	int LocalCols() { return m_LocalCols.Count(); }
	int RemoveLocalRow( int p_LocalI );
	int RemoveLocalCol( int p_LocalJ );
	void AddGlobalRow( int p_GlobalI );
	void AddGlobalCol( int p_GlobalJ );
};



#endif //__CPolyMatrix__
