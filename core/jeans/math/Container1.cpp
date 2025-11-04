// Array\Container1.cpp

//#include "stdafx.h"
#include "Container1.h"
#include "ContainerTools.h"


#define LOGMSG(...) printf(__VA_ARGS__)
#define LOGERR(...) printf(__VA_ARGS__)

//#include <Services\Log.h>

// --------------
// public methods
// --------------

// constructors
// -----------
template <class Type> CContainer1<Type>::CContainer1(const int p_Width /* = 0 */) 
:	m_pData(0), 
	m_Width(0)
{
	Alloc(p_Width);
} 

template <class Type> CContainer1<Type>::CContainer1(const Type* p_pSrc, const int p_Width)
:	m_pData(0), 
	m_Width(0)
{
	if(Alloc(p_Width))
		CContainerTools<Type>::Copy(GetBuffer(), p_pSrc, p_Width); 
}
		
template <class Type> CContainer1<Type>::CContainer1(const CContainer1<Type>& p_Src)
:	m_pData(0), 
	m_Width(0)
{
	if(Alloc(p_Src.m_Width))
		CContainerTools<Type>::Copy(GetBuffer(), p_Src.GetBuffer(), p_Src.m_Width); 
}

template <class Type> CContainer1<Type>::CContainer1(const CContainer1<Type>& p_Src, const int p_Width)
:	m_pData(0), 
	m_Width(0)
{
	if(Alloc(p_Width)) {	
		int l_Width = 0;
		//CContainerTools<Type>::Copy(GetBuffer(), p_Src.GetBuffer(), l_Width); 
	}
}


// desctructor
// -----------
template <class Type> CContainer1<Type>::~CContainer1() 
{
	Free();
} 

// free memory
// -----------
template <class Type> void CContainer1<Type>::Free()
{
	if(m_pData != 0)
		delete [] (Type*) m_pData;	
	m_pData		= 0;
	m_Width		= 0;
}

// set the size of the container
// -----------------------------
template <class Type> bool CContainer1<Type>::SetSize(const int p_Width)
{
	if(!Alloc(p_Width))
	{
		return false;
	}
	return true;
}

// size of the memory allocated to the container
// ----------------------------------------------
template <class Type> int CContainer1<Type>::Sizeof() const 
{ 
	return GetNbElements()*sizeof(Type); 
}

// value setting
// -------------
template <class Type> void	CContainer1<Type>::SetValue(const Type p_Val) 
{ 
	CContainerTools<Type>::SetValue(GetBuffer(), GetNbElements(), p_Val); 
}

template <class Type> void CContainer1<Type>::SetValue(const Type p_Val, const int p_OffX, 
	const int p_DimX)
{
	if(p_OffX < 0)
		LOGERR("Offset index out of range");
	if(p_DimX < 0)
		LOGERR("size is negative");
	if((p_OffX+p_DimX) > m_Width)
		LOGERR("Last index will be out of range");

	CContainerTools<Type>::SetValue(GetBuffer()+p_OffX, p_DimX, p_Val);
}
// DEBUT MODIF 01-009
// values setting from template CList<val, val> object
// ---------------------------------------------------
/*template <class Type> bool CContainer1<Type>::FromList(const CList<Type, Type> &p_List)
{
	if(!SetSize(p_List.GetCount()))
		return false;

	POSITION l_Pos = p_List.GetHeadPosition();
	for (int l_Loop=0; l_Loop<p_List.GetCount(); l_Loop++)
		m_pData[l_Loop] = p_List.GetNext(l_Pos);

	return true;
}*/

// values setting from template CList<val, ref> object
// ---------------------------------------------------
/*template <class Type> bool CContainer1<Type>::FromListRef(const CList<Type, Type&> &p_List)
{
	if(!SetSize(p_List.GetCount()))
		return false;

	POSITION l_Pos = p_List.GetHeadPosition();
	for (int l_Loop=0; l_Loop<p_List.GetCount(); l_Loop++)
		m_pData[l_Loop] = p_List.GetNext(l_Pos);

	return true;
}*/

// set a template CList<val, val> object with values of container's data
// ----------------------------------------------------------------------
/*template <class Type> void CContainer1<Type>::ToList(CList<Type, Type> &p_List)
{
	p_List.RemoveAll();
	for (int l_Loop = 0; l_Loop<GetSize(); l_Loop++)
		p_List.AddTail(m_pData[l_Loop]);
}*/

// set a template CList<val, ref> object with values of container's data
// ----------------------------------------------------------------------
/*template <class Type> void CContainer1<Type>::ToListRef(CList<Type, Type&> &p_List)
{
	p_List.RemoveAll();
	for (int l_Loop = 0; l_Loop<GetSize(); l_Loop++)
		p_List.AddTail(m_pData[l_Loop]);
}*/
// FIN MODIF 01-009
// ----------------------------------------------------------------------
template <class Type> void CContainer1<Type>::GetSubArray(const CContainer1& p_Src,
	const int p_OffSrcX, const int p_DimSrcX, const int p_OffDestX /* = 0 */)
{
	if(!p_Src)
	{
		LOGMSG("Source container is null");
		return;
	}

	if((p_OffSrcX+p_DimSrcX) > p_Src.Width()){}
		LOGERR("Last index of source container will be out of range");

	if(SetSize(p_OffDestX+p_DimSrcX)) {

		CContainerTools<Type>::Copy(&m_pData[p_OffDestX], &p_Src.m_pData[p_OffSrcX], p_DimSrcX); 
	}
	else{}
		LOGMSG("Destination container is null");
}

//value information
// -----------------
template <class Type> bool CContainer1<Type>::IsFound(const Type val) const 
{ 
	return CContainerTools<Type>::IsFound(GetBuffer(), GetNbElements(), val); 
}	

//compatibility between machines (bytes order changing)
// ----------------------------------------------------
template <class Type> void CContainer1<Type>::ReverseBytes()	
{	
	CContainerTools<Type>::ReverseBytes(GetBuffer(), GetNbElements());	
}
	
// test validity of the container
// ------------------------------
template <class Type> bool CContainer1<Type>::operator!() const 
{ 
	return (m_pData == 0); 
} 

// index operator
// --------------
template <class Type> Type&	CContainer1<Type>::operator[](const int p_Ind) const
{
	if(p_Ind >= 0 && p_Ind < m_Width)
		return m_pData[p_Ind]; 
	else
	{
		LOGERR("Index out of range");
		return m_pData[p_Ind]; 
	}
}
// DEBUT MODIF 01-009
template <class Type> Type&	CContainer1<Type>::operator()(const int p_Ind) const
{
	if(p_Ind >= 0 && p_Ind < m_Width)
		return m_pData[p_Ind]; 
	else
	{
		LOGERR("Index %d is over maximum value %d", p_Ind, m_Width);
		return m_pData[p_Ind]; 
	}
}
// FIN MODIF 01-009

// operators
// ---------
template <class Type> void CContainer1<Type>::operator=(const CContainer1<Type>& p_Src)
{
	if(SetSize(p_Src.m_Width)) {
		CContainerTools<Type>::Copy(m_pData, p_Src.m_pData, p_Src.m_Width);
	}
	else
	{
		if (m_Width!=0)
			LOGMSG("Destination container is null");
	}
}

template <class Type> void CContainer1<Type>::operator=(const Type p_Val)  
{ 
	SetValue(p_Val); 
}


template <class Type> bool CContainer1<Type>::operator==(const CContainer1<Type>& p_Src) const
{
	if(Sizeof() == p_Src.Sizeof())
		return CContainerTools<Type>::Compare(GetBuffer(), p_Src.GetBuffer(), GetNbElements());
	else
	{
		LOGMSG("Containers are not the same size");
		return false;
	}
}

template <class Type> bool  CContainer1<Type>::operator!=(const CContainer1<Type>& p_Src) const 
{
	return !(*this == p_Src); 
}


// -----------------
// Protected methods
// -----------------

// memory allocation
// -----------------
template <class Type> bool CContainer1<Type>::Alloc(const int p_Width)
{
	if(p_Width != m_Width || !m_pData) {

// DEBUT MODIF 01-009
		if(p_Width <= 0)
		{	
			if (p_Width==0)
			{
				Free();
				return true;
			}
			LOGMSG("Can't change container size from %d to %d", m_Width, p_Width);
			Free();
			return false;
		}

		Free();
		m_Width		= p_Width;
// FIN MODIF 01-009
		m_pData = (Type*) new Type[m_Width];
		if(!m_pData)
		{
			LOGERR("Allocation failed, requested size %d", p_Width); 
			return false;
		}
	}	

	return true;
}
