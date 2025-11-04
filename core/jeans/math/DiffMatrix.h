#ifndef __CDiffMatrix__
#define __CDiffMatrix__



#include <Storage/List.h>



class CMatrix;



//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
class CDiffMatrix
{
public:

	//----------------------------
	//----------------------------
	class CDiff
	{
	public:
		CDiff() : m_Nod(-1), m_Var(-1) {}
		CDiff( int pNod, int pVar ) : m_Nod(pNod), m_Var(pVar) {}
		
		int m_Nod;
		int m_Var;
	};


	//----------------------------
	//----------------------------
	class CProd
	{
	public:
		CProd() : m_Coef(1) {}
		CProd( const CProd & Prod ) : m_Coef(Prod.m_Coef), m_Prod(Prod.m_Prod) { }
		CProd( double pCoef, CDiff pDiff ) : m_Coef(pCoef) { m_Prod.AddTail(pDiff); }
		CProd & operator=( const CProd & pProd )
		{
			m_Coef = pProd.m_Coef;
			m_Prod = pProd.m_Prod;
			return *this;
		}
		void Mult( double pCoef ) { m_Coef *= pCoef; }
		void Mult( const CProd & pProd )
		{
			m_Coef *= pProd.m_Coef;
			m_Prod.AddTail( pProd.m_Prod );
		}
		CString ToString() const;

		double m_Coef;
		CLst<CDiff> m_Prod;
	};

	#define _dF_dU_(A,B)  (CDiffMatrix::CProd( 1, CDiffMatrix::CDiff(A,B)))
	#define _PROD_(K,A,B) (CDiffMatrix::CProd( K, CDiffMatrix::CDiff(A,B)))


	//----------------------------
	// Construction / destruction
	//----------------------------
	CDiffMatrix();
	virtual ~CDiffMatrix();


	//----------------------------
	// Sizing
	//----------------------------
	virtual bool SetDims( int p_H/*ROWS*/, int p_W/*COLS*/ );
	int Rows() const { return m_H; }
	int Cols() const { return m_W; }
	void Free();
	void LoadEmpty();
	void DeleteNulls();


	//----------------------------
	// Access
	//----------------------------
	CLst<CProd> & Elt( int p_I/*ROW*/, int p_J/*COL*/ );
	const CLst<CProd> & Elt( int p_I/*ROW*/, int p_J/*COL*/ ) const;
	void AddToElt( int p_I/*ROW*/, int p_J/*COL*/, const CProd & pProd ) { Elt(p_I,p_J).AddTail(pProd); }


	//----------------------------
	// Operations
	//----------------------------
	bool TransposeTo( CDiffMatrix & p_Res ) const;
	bool Mult( const CMatrix & p_A, CDiffMatrix & p_Res ) const;
	bool Mult( const CDiffMatrix & p_A, CDiffMatrix & p_Res ) const;


	//----------------------------
	// Debug
	//----------------------------
	void Log( CString p_Prefix="" ) const;


protected:

	// Data
	int m_H;
	int m_W;
	CLst<CProd> ** m_pMat;
};




#endif //__CDiffMatrix__
