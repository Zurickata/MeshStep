// Array\Container3.cpp

#include "Container3.h"
#include "ContainerTools.h"
//#include <Services\Log.h>

#define LOGMSG(...) printf(__VA_ARGS__)
#define LOGERR(...) printf(__VA_ARGS__)


// --------------
// public methods
// --------------

// constructors
// -----------
template <class Type> CContainer3<Type>::CContainer3(const int p_Depth /* = 0 */, const int p_Height /* = 0 */, 
	const int p_Width /* = 0 */)  
:	m_pData(NULL),
	m_Width(0),
	m_Height(0),
	m_Depth(0)
{	
	Alloc(p_Depth, p_Height, p_Width);
} 

template <class Type> CContainer3<Type>::CContainer3(const Type* p_pSrc, const int p_Depth, const int p_Height, 
	const int p_Width)  
:	m_pData(NULL),
	m_Width(0),
	m_Height(0),
	m_Depth(0)
{	
	if(Alloc(p_Depth, p_Height, p_Width))
  		CContainerTools<Type>::Copy(&m_pData[0][0][0], p_pSrc, GetNbElements());
}

template <class Type> CContainer3<Type>::CContainer3(const CContainer3<Type>& p_Src)
:	m_pData(NULL),
	m_Width(0),
	m_Height(0),
	m_Depth(0)
{
  	if(Alloc(p_Src.m_Depth, p_Src.m_Height, p_Src.m_Width))
		CContainerTools<Type>::Copy(&m_pData[0][0][0], &p_Src[0][0][0], GetNbElements());
}


// desctructor
// -----------
template <class Type> CContainer3<Type>::~CContainer3() 
{
	Free();
} 

// free memory
// -----------
template <class Type> void CContainer3<Type>::Free()
{
	if(m_pData != NULL)
	{	delete [] **m_pData;
		delete [] *m_pData;
		delete [] m_pData;
	}

	m_pData		= NULL;
	m_Width		= 0;
	m_Height	= 0;
	m_Depth		= 0;
}


// set the size of the container
// -----------------------------
template <class Type> bool CContainer3<Type>::SetSize(const int p_Depth, const int p_Height, const int p_Width)
{
  	if(!Alloc(p_Depth, p_Height, p_Width))
	{
		return false;	
	}	
	return true;

}

// size of the memory allocated to the container
// ----------------------------------------------
template <class Type> int CContainer3<Type>::Sizeof() const 
{ 
	 return GetNbElements()*sizeof(Type);
}


// setting values
// --------------
template <class Type> void	CContainer3<Type>::SetValue(const Type p_Val)
{
	CContainerTools<Type>::SetValue(GetBuffer(), GetNbElements(), p_Val); 
}

template <class Type> void CContainer3<Type>::SetValue(const Type p_Val, const int p_OffX, const int p_DimX,
				const int p_OffY, const int p_DimY, const int p_OffZ, const int p_DimZ)
{
	if(p_OffX < 0)
		LOGERR("Offset index out of range");
	if(p_DimX < 0)
		LOGERR("size is negative");
	if((p_OffX+p_DimX) > m_Width)
		LOGERR("last index will be out of range");
	if(p_OffY < 0)
		LOGERR("Offset index out of range");
	if(p_DimY < 0)
		LOGERR("size is negative");
	if((p_OffY+p_DimY) > m_Height)
		LOGERR("last index will be out of range");
	if(p_OffZ < 0)
		LOGERR("Offset index out of range");
	if(p_DimZ < 0)
		LOGERR("size is negative");
	if((p_OffZ+p_DimZ) > m_Depth)
		LOGERR("last index will be out of range");

	for(register int kk=0; kk < p_DimZ; kk++)
		for(register int jj=0; jj < p_DimY; jj++)
			CContainerTools<Type>::SetValue(&m_pData[kk+p_OffZ][jj+p_OffY][p_OffX], p_DimX, p_Val);
}

template <class Type> void CContainer3<Type>::GetSubArray(const CContainer3& p_Src, const int p_OffSrcX, const int p_DimSrcX, 
				const int p_OffSrcY, const int p_DimSrcY, const int p_OffSrcZ, 
				const int p_DimSrcZ, const int p_OffDestX /* = 0 */, const int p_OffDestY /* = 0 */, 
				const int p_OffDestZ /* = 0 */)
{
	if(!p_Src)
	{
		LOGMSG("Source container is null");
		return;
	}

	if((p_OffSrcX+p_DimSrcX) > p_Src.Width())
		LOGERR("Last width index of source container will be out of range");
	if((p_OffSrcY+p_DimSrcY) > p_Src.Height())
		LOGERR("Last width index of source container will be out of range");
	if((p_OffSrcZ+p_DimSrcZ) > p_Src.Depth())
		LOGERR("Last width index of source container will be out of range");

	if(SetSize(p_OffDestZ+p_DimSrcZ, p_OffDestY+p_DimSrcY, p_OffDestX+p_DimSrcX))
	{	int dim = p_DimSrcX;
		for(register int kk=0; kk < p_DimSrcZ; kk++)
			for(register int jj=0; jj < p_DimSrcY; jj++)
				CContainerTools<Type>::Copy(
					&m_pData[p_OffDestZ+kk][p_OffDestY+jj][p_OffDestX], 
					&p_Src[p_OffSrcZ+kk][p_OffSrcY+jj][p_OffSrcX], dim);
	}
	else
		LOGMSG("Destination container is null");
}

// search for a value
// ------------------
template <class Type> bool	CContainer3<Type>::IsFound(const Type p_Val) const 
{
	return CContainerTools<Type>::IsFound(GetBuffer(), GetNbElements(), p_Val); 
}	

// reverse bytes
// -------------
template <class Type> void	CContainer3<Type>::Swap()
{
	CContainerTools<Type>::ReverseBytes(GetBuffer(), GetNbElements());	
}


// operators
// ---------
template <class Type> bool	CContainer3<Type>::operator!() const
{
	return (m_pData == NULL); 
}

template <class Type> Type**& CContainer3<Type>::operator[](const int p_Ind) const 
{
	if(p_Ind >= 0 && p_Ind < m_Depth)
		return m_pData[p_Ind]; 
	else
	{
		LOGERR("Index out of range");
		return m_pData[p_Ind]; 
	}
}
// DEBUT MODIF 01-009
template <class Type> Type& CContainer3<Type>::operator()(const int p_Depth, const int p_Height, const int p_Width) const
{
	if ((p_Depth>=0)&&(p_Depth<m_Depth)&&
		(p_Height>=0)&&(p_Height<m_Height)&&
		(p_Width>=0)&&(p_Width<m_Width))
		return m_pData[p_Depth][p_Height][p_Width];
	else
	{
		LOGERR("Index (%d,%d,%d) is over maximum values (%d,%d,%d)", p_Depth,p_Height,p_Width, m_Depth-1,m_Height-1,m_Width-1);
		return m_pData[0][0][0];
	}
}
// FIN MODIF 01-009
template <class Type> void CContainer3<Type>::operator=(const CContainer3<Type>& p_Src)
{
	if(SetSize(p_Src.m_Depth, p_Src.m_Height, p_Src.m_Width))
		CContainerTools<Type>::Copy(GetBuffer(), p_Src.GetBuffer(), GetNbElements());
	else
	{
		if ((m_Depth!=0)||(m_Height!=0)||(m_Width!=0))		// Autorise les tableaux de taille (0,0,0)
			LOGMSG("Destination container is null");
	}
}

template <class Type> void	CContainer3<Type>::operator=(const Type p_Val)
{
	SetValue(p_Val); 
}

template <class Type> bool CContainer3<Type>::operator==(const CContainer3<Type>& p_Src) const
{
	if(Sizeof() == p_Src.Sizeof())
		return CContainerTools<Type>::Compare(GetBuffer(), p_Src.GetBuffer(), GetNbElements());
	else
	{
		LOGMSG("Containers are not the same size");
		return false;
	}
}

template <class Type> bool 	CContainer3<Type>::operator!=(const CContainer3<Type>& p_Src) const
{
	return !(*this == p_Src); 
}



// -----------------
// Protected methods
// -----------------

// memory allocation
// -----------------
template <class Type> bool CContainer3<Type>::Alloc(const int p_Depth, const int p_Height, const int p_Width)
{
// DEBUT MODIF 01-009
	if((p_Depth <= 0) || (p_Height <= 0) || (p_Width <= 0))
	{
		if((p_Depth == 0) && (p_Height == 0) && (p_Width == 0))
		{
			Free();
			return true;
		}
		LOGMSG("Can't change container size from (%d,%d,%d) to (%d,%d,%d)", m_Depth,m_Height,m_Width, p_Depth,p_Height,p_Width);
		Free();
		return false;
	}
		
	Free();
// FIN MODIF 01-009
	m_Depth		= p_Depth;
	m_Height	= p_Height;
	m_Width		= p_Width;

	m_pData = new Type**[m_Depth];
	if(!m_pData)
	{
		LOGERR("Allocation failed"); 
		return false;
	}
	if(m_pData != NULL)
	{	Type** mR = new Type*[m_Depth*p_Height];
		if(mR != NULL)
		{	Type* mD = new Type[m_Depth*p_Height*p_Width];
			
			if(mD != NULL)
			{
				for(int ii=0; ii < m_Depth; ii++, mR+=p_Height)
				{	m_pData[ii]	= mR;
					for(int jj=0; jj < p_Height; jj++, mD+=p_Width)
					{	mR[jj] = mD;
			}	}	}
			else
			{	delete [] mR;
				delete [] m_pData;
				LOGERR("Allocation failed"); 
				m_pData = NULL;
		}	}
		else
		{	delete [] m_pData;
			LOGERR("Allocation failed"); 
			m_pData = NULL;
	}	}


	return m_pData != NULL;
}
