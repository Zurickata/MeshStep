#ifndef __CLst__
#define __CLst__


#include <stdio.h>
#include <string.h>



template <class T> class CLst
{
public:

	// Construction/destruction
	CLst<T>() { m_pHead=m_pTail=NULL; m_Count=0; }
	CLst<T>( const CLst<T> & Other ) { m_pHead=m_pTail=NULL; m_Count=0; *this=Other; }
	~CLst<T>() { DelAll(); }

	// Iteration
	void * HeadPos() const { return m_pHead; }
	void * TailPos() const { return m_pTail; }
	void * NextPos( void * Ptr ) const { if( Ptr ) return ((CLstElt<T>*)Ptr)->m_pNext; else return NULL; }
	void * PrevPos( void * Ptr ) const { if( Ptr ) return ((CLstElt<T>*)Ptr)->m_pPrev; else return NULL; }
	void Next( void * & Ptr ) const { if( Ptr ) Ptr=((CLstElt<T>*)Ptr)->m_pNext; }
	void Prev( void * & Ptr ) const { if( Ptr ) Ptr=((CLstElt<T>*)Ptr)->m_pPrev; }

	// Access refs
	T & GetAt( void * Ptr );
	T & GetTail() { return GetAt(m_pTail); }
	T & GetHead() { return GetAt(m_pHead); }

	// Access const refs
	const T & GetAt( void * Ptr ) const;
	const T & GetTail() const { return GetAt(m_pTail); }
	const T & GetHead() const { return GetAt(m_pHead); }

	// Access pointers
	T * GetPtrAt( void * Ptr );
	T * GetPtrTail() { return m_pTail ? &(m_pTail->m_T) : 0 ; }
	T * GetPtrHead() { return m_pHead ? &(m_pHead->m_T) : 0 ; }

	// Access const pointers
	const T * GetPtrAt( void * Ptr ) const;

	// Search
	int Count() const { return m_Count; }
	void * FindIdx( int Idx );
	void ToArray( T * pArray );

	// Insertion
	void * AddBefore( void * Ptr, T p_T );
	void * AddAfter( void * Ptr, T p_T );
	void * AddHead( T p_T );
	void * AddTail( T p_T );
	void * AddTail( const CLst<T> & p_L );
	void * AddIntoIncrList( T p_T, bool p_Unique );
	void * AddIntoDecrList( T p_T, bool p_Unique );

	// Affectation
	CLst<T> & operator=( const CLst<T> & p_L );

	// Deletion
	void DelAll();
	void DelAt( void * Ptr );
	void DelHead() { DelAt(m_pHead); }
	void DelTail() { DelAt(m_pTail); }

	// Debug
	const char * ToString();

protected:

	//..............................................................................
	//..............................................................................
	template <class A> class CLstElt
	{
	public:
		CLstElt() { m_pNext = m_pPrev = NULL; }

		A m_T;

		CLstElt * m_pNext;
		CLstElt * m_pPrev;
	};
	//..............................................................................
	//..............................................................................

	int m_Count;
	CLstElt<T> * m_pHead;
	CLstElt<T> * m_pTail; 
};

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
template <class T> T & CLst<T>::GetAt( void * Ptr )
{
	static T t;
	return Ptr ? ((CLstElt<T>*)Ptr)->m_T : t ;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
template <class T> const T & CLst<T>::GetAt( void * Ptr ) const
{
	static T t;
	return Ptr ? ((CLstElt<T>*)Ptr)->m_T : t ;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
template <class T> T * CLst<T>::GetPtrAt( void * Ptr )
{
	return Ptr ? &((CLstElt<T>*)Ptr)->m_T : 0 ;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
template <class T> const T * CLst<T>::GetPtrAt( void * Ptr ) const
{
	return Ptr ? &((CLstElt<T>*)Ptr)->m_T : 0 ;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
template <class T> void * CLst<T>::FindIdx( int Idx )
{
	if( Idx < m_Count-1-Idx )
	{
		int I = 0;

		// From start
		for( void * Pos = m_pHead ; Pos ; Next(Pos) )
		{
			if( I == Idx )
				return Pos;

			I++;
		}
	}
	else
	{
		int I = m_Count-1;

		// From start
		for( void * Pos = m_pTail ; Pos ; Prev(Pos) )
		{
			if( I == Idx )
				return Pos;

			I--;
		}
	}

	return NULL;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
template <class T> void CLst<T>::ToArray( T * pArray )
{
	int i = 0;

	for( void * iT=m_pHead ; iT ; Next(iT) )
		pArray[i++] = GetAt(iT);
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
template <class T> void * CLst<T>::AddBefore( void * Ptr, T p_T )
{
	if( Ptr )
	{
		CLstElt<T> * l_pNew = new CLstElt<T>;
		l_pNew->m_T = p_T;

		l_pNew->m_pNext = (CLstElt<T>*)Ptr;
		l_pNew->m_pPrev = ((CLstElt<T>*)Ptr)->m_pPrev;

		l_pNew->m_pNext->m_pPrev = l_pNew;
		if( l_pNew->m_pPrev )
			l_pNew->m_pPrev->m_pNext = l_pNew;

		m_Count++;

		// New head ?
		if( !l_pNew->m_pPrev )
			m_pHead = l_pNew;

		return l_pNew;
	}
	else
		return 0;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
template <class T> void * CLst<T>::AddAfter( void * Ptr, T p_T )
{
	if( Ptr )
	{
		CLstElt<T> * l_pNew = new CLstElt<T>;
		l_pNew->m_T = p_T;

		l_pNew->m_pNext = ((CLstElt<T>*)Ptr)->m_pNext;
		l_pNew->m_pPrev = (CLstElt<T>*)Ptr;

		l_pNew->m_pPrev->m_pNext = l_pNew;
		if( l_pNew->m_pNext )
			l_pNew->m_pNext->m_pPrev = l_pNew;

		m_Count++;

		// New tail ?
		if( !l_pNew->m_pNext )
			m_pTail = l_pNew;

		return l_pNew;
	}
	else
		return 0;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
template <class T> void * CLst<T>::AddHead( T p_T )
{
	if( m_Count )
	{
		CLstElt<T> * l_pNew = new CLstElt<T>;
		l_pNew->m_T = p_T;

		l_pNew->m_pNext = m_pHead;
		m_pHead->m_pPrev = l_pNew;

		m_Count++;

		m_pHead = l_pNew;
	}
	else
	{
		m_pHead = m_pTail = new CLstElt<T>;
		m_pHead->m_T = p_T;
		m_Count = 1;
	}

	return m_pHead;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
template <class T> void * CLst<T>::AddTail( T p_T )
{
	if( m_Count )
	{
		CLstElt<T> * l_pNew = new CLstElt<T>;
		l_pNew->m_T = p_T;

		l_pNew->m_pPrev = m_pTail;
		m_pTail->m_pNext = l_pNew;

		m_Count++;

		m_pTail = l_pNew;
	}
	else
	{
		m_pHead = m_pTail = new CLstElt<T>;
		m_pHead->m_T = p_T;
		m_Count = 1;
	}

	return m_pTail;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
template <class T> void * CLst<T>::AddTail( const CLst<T> & p_L )
{
	for( void * Pos=p_L.HeadPos() ; Pos ; p_L.Next(Pos) )
		AddTail( p_L.GetAt(Pos) );

	return m_pTail;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
template <class T> void * CLst<T>::AddIntoIncrList( T p_T, bool p_Unique )
{
	void* iPos;
	// Find element higher or equal
	for(iPos=m_pHead ; iPos ; Next(iPos) )
	{
		if( GetAt(iPos) >= p_T )
			break;
	}

	if( !iPos )
	{
		// No higher element found : this one is the highest => tail
		return AddTail( p_T );
	}
	else if( GetAt(iPos) != p_T )
	{
		// The element found is not equal, hence greater => add before
		return AddBefore( iPos, p_T );
	}
	else
	{
		// The element found is equal to the one considered : duplicate or not
		if( p_Unique )
			return NULL;
		else
			return AddBefore( iPos, p_T );
	}
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
template <class T> void * CLst<T>::AddIntoDecrList( T p_T, bool p_Unique )
{
	void* iPos;
	// Find element smaller or equal
	for(iPos=m_pHead ; iPos ; Next(iPos) )
	{
		if( GetAt(iPos) <= p_T )
			break;
	}

	if( !iPos )
	{
		// No smaller element found : this one is the smallest => tail
		return AddTail( p_T );
	}
	else if( GetAt(iPos) != p_T )
	{
		// The element found is not equal, hence smaller => add before
		return AddBefore( iPos, p_T );
	}
	else
	{
		// The element found is equal to the one considered : duplicate or not
		if( p_Unique )
			return NULL;
		else
			return AddBefore( iPos, p_T );
	}
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
template <class T> CLst<T> & CLst<T>::operator=( const CLst<T> & p_L )
{
	DelAll();

	for( void * Pos=p_L.HeadPos() ; Pos ; p_L.Next(Pos) )
		AddTail( p_L.GetAt(Pos) );

	return *this;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
template <class T> void CLst<T>::DelAt( void * Ptr ) 
{
	if( Ptr )
	{
		CLstElt<T> * l_pTarget = (CLstElt<T>*)Ptr;

		if( l_pTarget->m_pPrev )
			l_pTarget->m_pPrev->m_pNext = l_pTarget->m_pNext;
		else
			m_pHead = l_pTarget->m_pNext;

		if( l_pTarget->m_pNext )
			l_pTarget->m_pNext->m_pPrev = l_pTarget->m_pPrev;
		else
			m_pTail = l_pTarget->m_pPrev;

		delete l_pTarget;

		m_Count--;
	}
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
template <class T> void CLst<T>::DelAll()
{
	CLstElt<T> * l_pTarget = m_pHead;
	while( l_pTarget )
	{
		CLstElt<T> * l_pNext = l_pTarget->m_pNext;
		delete l_pTarget;
		l_pTarget = l_pNext;
	}
	
	m_pHead = m_pTail = NULL;
	m_Count = 0;
}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
template <class T> const char * CLst<T>::ToString()
{
	static char Str[1024];
	char * c = Str;
	sprintf( c, "H->", 3);
	c += 3;
	void * Ptr = m_pHead;
	while( Ptr )
	{
		char elt[32];
		sprintf( elt, " %d->", GetAt(Ptr) );
		sprintf( c, elt );
		c += strlen(elt);
		Next(Ptr);
	}
	sprintf( c, " T" );
	return Str;
}

//------------------------------------------------------------------------------
// MACROS
//------------------------------------------------------------------------------
#define BrowseList( A, B ) for( A=(B).HeadPos() ; (A) ; (B).Next(A) )





#endif //__CLst__
