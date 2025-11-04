#ifndef __CMatrix__
#define __CMatrix__



//#include <afxtempl.h>
#include <math.h>
#include "Container1.h"
#include "List.h"
#include <string>
#include <stdarg.h>
#include <cstdlib>

using namespace std;


class CVector;
class CPolyMatrix;
class CMatrix;


class CMatrix
{
public:

	// Construction / destruction
	CMatrix();
	CMatrix( const CMatrix & p_M );
	CMatrix( int p_H, int p_W, double p_00, .../*,01,02,..,10,11,12,..,20,21,22*/ );
	virtual ~CMatrix();

	// Sizing
	virtual bool SetDims( int p_H/*ROWS*/, int p_W/*COLS*/ );
	int Rows() const { return m_H; }
	int Cols() const { return m_W; }
	void Free();

	// Access
	double & Elt( int p_I/*ROW*/, int p_J/*COL*/ );
	const double & Elt( int p_I/*ROW*/, int p_J/*COL*/ ) const;
	bool SubMatrixTo( int p_FirstRow, int p_LastRow, int p_FirstCol, int p_LastCol, CMatrix & p_To );
	bool SubMatrixTo( int p_FirstRow, int p_LastRow, int p_Col, CVector & p_To );
	bool SubMatrixTo( int p_Col, CVector & p_To );
	const double * GetColBuffer( int p_J ) const;
	
	// Operations
	void LoadIdentity();
	void LoadValue( double p_Value );
	bool Mult( const CMatrix & p_A, CMatrix & p_Res ) const;
	bool Mult( const CPolyMatrix & p_A, CPolyMatrix & p_Res ) const;
	bool Mult( double p_A, CMatrix & p_Res ) const;							// accepts re-entrance
	bool AddMult( double p_A, const CMatrix & p_B, CMatrix & p_Res ) const;	// Res = this + A*B : accepts re-entrance
	bool Add( const CMatrix & p_A, CMatrix & p_Res ) const;					// accepts re-entrance
	bool Sub( const CMatrix & p_A, CMatrix & p_Res ) const;					// accepts re-entrance
	bool Pow( int p_Pow, CMatrix & p_Res ) const;
	bool Transpose();
	bool TransposeTo( CMatrix & p_Res ) const;
	CMatrix & operator=( const CMatrix & p_In );
	double MaxFabs() const;

	// File operations
	bool SaveBin( const string & pFname );
	bool LoadBin( const string & pFname );

	// Permutations
//	bool LoadPermutation( const CContainer1<int> & p_Mapping );

	// Rotations
	bool LoadRotation( const CVector & pRoot, const CVector & pDir, double pDeg );

	// Co-Facteurs
	double CF_Det( bool p_EmptyMat=false );
	bool CF_InverseTo( CMatrix & p_Inv );

	// Decomposition LU
	bool LU_ify( CMatrix & p_L, CMatrix & p_U );
	bool LU_Det( double & p_Det );
	bool LU_InverseTo( CMatrix & p_Inv );
	bool LU_Solve( CVector & p_X, const CVector & p_Y );

	// Cholesky LLt : matrice sym def pos
	bool LLt_ify( CMatrix & p_L );
	static bool LLt_Solve( const CMatrix & p_L, CVector & p_X, const CVector & p_Y );

	// Gaussian elimination: makes all equations p_Var-independent (except row #p_Var)
	bool SubsInAllRowsFor( int p_Var, CVector & p_F );

	// Produces a matrix with reduced dimension by deleting listed rows and cols
	bool KillRowCols( const CLst<int> & pRows, const CLst<int> & pCols, CMatrix & pToMat ) const;

	// Debug
	bool IsEqual( const CMatrix & p_Other, double tol=TOLERANCE );
	bool IsIdentity( double tol=TOLERANCE );
	bool IsNull( double tol=TOLERANCE );
	bool IsSymmetric( double tol=TOLERANCE );
	void LoadRandom( bool p_IntValues=true,double p_Center=0, double p_Amplitude=100 );
	void LoadTridiagonal();
	void LoadRandomEmpty();
	void Log( string p_Prefix="" ) const;
	void NonNullCellStatPerRow( int & Max, int & Min, int & Avg, int & Tot, double tol=TOLERANCE );

	// What is zero and what is not ....
	static const double TOLERANCE;


protected:

	// Co-Facteurs
	int MaxZeroLocalRow();
	double CF_RecDet( bool p_EmptyMat=false );
	void InitLocalRowsCols();
//	static CList<int,int> m_LocalRows;
//	static CList<int,int> m_LocalCols;
	static CLst<int> m_LocalRows;
	static CLst<int> m_LocalCols;
//	int LocalCols() { return m_LocalCols.GetCount(); }
	int LocalCols() { return m_LocalCols.Count(); }
	int RemoveLocalRow( int p_LocalI );
	int RemoveLocalCol( int p_LocalJ );
	void AddGlobalRow( int p_GlobalI );
	void AddGlobalCol( int p_GlobalJ );
	void LogLocalRows();
	void LogLocalCols();

	// Matrices triangulaires
	double TriDet();
	bool L_InverseTo( CMatrix & p_InvL );
	bool U_InverseTo( CMatrix & p_InvU );

	// Data
	int m_H;
	int m_W;
	double ** m_pMat;
};



#endif //__CMatrix__
