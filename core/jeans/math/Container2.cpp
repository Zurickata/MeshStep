// Array\Container2.cpp

#include "Container2.h"
#include "ContainerTools.h"
//#include <Services\Log.h>

#define LOGMSG(...) printf(__VA_ARGS__)
#define LOGERR(...) printf(__VA_ARGS__)


// --------------
// public methods
// --------------

// constructors
// -----------
template <class Type> CContainer2<Type>::CContainer2(const int p_Height /* = 0 */, const int p_Width /* = 0 */)  
:	m_pData(NULL),
	m_Width(0),
	m_Height(0)
{	
	Alloc(p_Height, p_Width);
} 

template <class Type> CContainer2<Type>::CContainer2(const CSize& p_Size)
:	m_pData(NULL),
	m_Width(0),
	m_Height(0)
{
	Alloc(p_Size.cy, p_Size.cx);
} 

template <class Type> CContainer2<Type>::CContainer2(const Type* p_pSrc, const int p_Height, 
	const int p_Width)  
:	m_pData(NULL),
	m_Width(0),
	m_Height(0)
{	
	if(Alloc(p_Height, p_Width))
		CContainerTools<Type>::Copy(*m_pData, p_pSrc, p_Height * p_Width);
}

template <class Type> CContainer2<Type>::CContainer2(const CContainer2<Type>& p_Src)
:	m_pData(NULL),
	m_Width(0),
	m_Height(0)
{
  	if(Alloc(p_Src.m_Height, p_Src.m_Width))
		CContainerTools<Type>::Copy(*m_pData, *p_Src.m_pData, p_Src.GetNbElements());
}

template <class Type> CContainer2<Type>::CContainer2(const CContainer2<Type>& p_Src, 
	const int p_Height, const int p_Width)
:	m_pData(NULL),
	m_Width(0),
	m_Height(0)
{
  	if(Alloc(p_Height, p_Width))
	{	
		int l_mnW = min(m_Width, p_Src.m_Width);
		int l_mnH = min(m_Height, p_Src.m_Height);
		for(register int jj=0; jj < l_mnH; jj++)
			CContainerTools<Type>::Copy(&m_pData[jj][0], &p_Src[jj][0], l_mnW);
	}
}

template <class Type> CContainer2<Type>::CContainer2(const CContainer2<Type>& p_Src, 
	const CSize& p_Size)
:	m_pData(NULL),
	m_Width(0),
	m_Height(0)
{
  	if(Alloc(p_Size.cy, p_Size.cx))
	{	int l_mnW = min(m_Width, p_Src.m_Width);
		int l_mnH = min(m_Height, p_Src.m_Height);
		for(register int jj=0; jj < l_mnH; jj++)
			CContainerTools<Type>::Copy(&m_pData[jj][0], &p_Src[jj][0], l_mnW);
	}
}

// desctructor
// -----------
template <class Type> CContainer2<Type>::~CContainer2() 
{
	Free();
} 

// free memory
// -----------
template <class Type> void CContainer2<Type>::Free()
{
	if(m_pData != NULL)
	{	delete [] (Type*) *m_pData;
		delete [] (Type**) m_pData;
	}

	m_pData		= NULL;
	m_Width		= 0;
	m_Height	= 0;
}


// set the size of the container
// -----------------------------
template <class Type> bool CContainer2<Type>::SetSize(const int p_Height, const int p_Width)
{
  	if(!Alloc(p_Height, p_Width))
	{
		return false;	
	}
	return true;
}

template <class Type> bool	CContainer2<Type>::SetSize(const CSize& p_Size)
{
	return SetSize(p_Size.cy, p_Size.cx); 
}

// access to the size of the container
// -----------------------------------
template <class Type> CSize	CContainer2<Type>::GetSize() const
{
	return CSize(m_Width, m_Height); 
}

// size of the memory allocated to the container
// ----------------------------------------------
template <class Type> int CContainer2<Type>::Sizeof() const 
{ 
	 return GetNbElements()*sizeof(Type);
}


// setting values
// --------------
template <class Type> void	CContainer2<Type>::SetValue(const Type p_Val)
{
	CContainerTools<Type>::SetValue(GetBuffer(), GetNbElements(), p_Val); 
}

template <class Type> void CContainer2<Type>::SetValue(const Type p_Val, const int p_OffX, 
	const int p_DimX, const int p_OffY, const int p_DimY)
{
	if(p_OffX < 0)
		LOGERR("Offset index out of range");
	if(p_DimX < 0)
		LOGERR("size is negative");
	if((p_OffX+p_DimX) > m_Width)
		LOGERR("last index will be out of range");
	if(p_OffY < 0)
		LOGERR("Offset index out of range");
	if(p_OffY < 0)
		LOGERR("size is negative");
	if((p_OffY+p_DimY) > m_Height)
		LOGERR("last index will be out of range");

	for(register int jj=0; jj < p_DimY; jj++)
		CContainerTools<Type>::SetValue(&m_pData[jj+p_OffY][p_OffX], p_DimX, p_Val);
}

template <class Type> void CContainer2<Type>::GetSubArray(const CContainer2& p_Src,
	const int p_OffSrcX, const int p_DimSrcX, const int p_OffSrcY, const int p_DimSrcY, 
	const int p_OffDestX /* = 0 */, const int p_OffDestY /* = 0 */)
{
	if(!p_Src)
	{
		LOGMSG("Source container is null");
		return;
	}

	if((p_OffSrcX+p_DimSrcX) > p_Src.Width())
		LOGERR("Last width index of source container will be out of range");
	if((p_OffSrcY+p_DimSrcY) > p_Src.Height())
		LOGERR("Last height index of source container will be out of range");

	if(SetSize(p_OffDestY+p_DimSrcY, p_OffDestX+p_DimSrcX))
	{	int l_Dim = p_DimSrcX;
		for(register int jj=0; jj < p_DimSrcY; jj++)
			CContainerTools<Type>::Copy(&m_pData[p_OffDestY+jj][p_OffDestX], &p_Src[p_OffSrcY+jj][p_OffSrcX], l_Dim);
	}
	else
		LOGMSG("Destination container is null");
}

// search for a value
// ------------------
template <class Type> bool	CContainer2<Type>::IsFound(const Type p_Val) const 
{
	return CContainerTools<Type>::IsFound(GetBuffer(), GetNbElements(), p_Val); 
}	

// reverse bytes
// -------------
template <class Type> void	CContainer2<Type>::Swap()
{
	CContainerTools<Type>::ReverseBytes(GetBuffer(), GetNbElements());	
}


// operators
// ---------
template <class Type> bool	CContainer2<Type>::operator!() const
{
	return (m_pData == NULL); 
}

template <class Type> Type*& CContainer2<Type>::operator[](const int p_Ind) const 
{
	if(p_Ind >= 0 && p_Ind < m_Height)
		return m_pData[p_Ind]; 
	else
	{
		LOGERR("Index out of range");
		return m_pData[p_Ind]; 
	}
}
// DEBUT MODIF 01-009
template <class Type> Type& CContainer2<Type>::operator()(const int p_Height, const int p_Width) const 
{
	if ((p_Height>=0)&&(p_Height<m_Height)&&(p_Width>=0)&&(p_Width<m_Width))
		return m_pData[p_Height][p_Width];
	else
	{
		LOGERR("Index (%d,%d) is over maximum values (%d,%d)", p_Height, p_Width, m_Height-1, m_Width-1);
		return m_pData[0][0];
	}
}
// FIN MODIF 01-009


template <class Type> void CContainer2<Type>::operator=(const CContainer2<Type>& p_Src)
{
	if(SetSize(p_Src.m_Height, p_Src.m_Width))
		CContainerTools<Type>::Copy(GetBuffer(), p_Src.GetBuffer(), GetNbElements());
	else
	{
		if ((m_Width!=0)||(m_Height!=0))				// Accepte les containers de taille (0,0)
			LOGMSG("Destination container is null");
	}
}

template <class Type> void	CContainer2<Type>::operator=(const Type p_Val)
{
	SetValue(p_Val); 
}

template <class Type> bool CContainer2<Type>::operator==(const CContainer2<Type>& p_Src) const
{
	if(Sizeof() == p_Src.Sizeof())
		return CContainerTools<Type>::Compare(GetBuffer(), p_Src.GetBuffer(), GetNbElements());
	else
	{
		LOGMSG("Containers are not the same size");
		return false;
	}

}

template <class Type> bool 	CContainer2<Type>::operator!=(const CContainer2<Type>& p_Src) const
{
	return !(*this == p_Src); 
}



// -----------------
// Protected methods
// -----------------

// memory allocation
// -----------------
template <class Type> bool CContainer2<Type>::Alloc(const int p_Height, const int p_Width)
{
// DEBUT MODIF 01-009	
	if((p_Height <= 0) || (p_Width <= 0))
	{
		if((p_Height == 0) && (p_Width == 0))
		{
			Free();
			return true;
		}
		
		LOGMSG("Can't change container size from (%d,%d) to (%d,%d)", m_Height,m_Width, p_Height,p_Width);
		Free();
		return false;
	}

	Free();
	m_Height	= p_Height;
	m_Width		= p_Width;
// FIN MODIF 01-009	
	m_pData = new Type*[m_Height];
	if(!m_pData)
	{
		LOGERR("Allocation failed"); 
		return false;
	}
	if(m_pData != NULL)
	{	Type* l_d = new Type[m_Height*m_Width];
					
		if(l_d == NULL)
		{	delete [] m_pData;
			LOGERR("Allocation failed"); 
			m_pData = NULL;
		}
		else
			for(int ii=0; ii < m_Height; ii++, l_d+=m_Width)
				m_pData[ii] = l_d;
	}

	return m_pData != NULL;
}
