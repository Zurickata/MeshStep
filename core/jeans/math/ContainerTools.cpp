// Array\ContainerTools.cpp

#include "ContainerTools.h"

// value setting
// -------------
template <class Type> void CContainerTools<Type>::SetValue(Type* p_pData, const int p_DimData, const Type p_Val)
{
	 Type*	l_pData = p_pData;
	 int	l_Dim = p_DimData;

	while(l_Dim--)
		*l_pData++ = p_Val;
}

template <class Type> bool CContainerTools<Type>::IsFound(Type* p_pData, const int p_DimData, const Type p_Val)
{
	 Type*	l_pData = p_pData;
	 int	l_Dim = p_DimData;

	while(l_Dim--)
		if(memcmp(l_pData++, &p_Val, sizeof(Type)) == 0)
			return true;

	return false;
}

template <class Type> void CContainerTools<Type>::ReverseBytes(Type* p_pData, int p_DimData)
{
	 int	l_ii;
	int				l_sz = sizeof(Type)/2;
	char*	l_p1 = (char*)(p_pData);
	char*			l_p2;

	while(p_DimData--)
	{	for(l_ii=0, l_p2=l_p1+sizeof(Type)-1; l_ii < l_sz; l_ii++, l_p1++, l_p2--)
		{	char    l_val	= *l_p1;
  		 	*l_p1			= *l_p2;
  			*l_p2			= l_val;
		}

		l_p1 += l_sz;
		p_pData++;
	}
}

// comparison
// ----------
template <class Type> bool CContainerTools<Type>::Compare(Type* p_pData1, Type* p_pData2, const int p_DimData)
{
	 Type*	l_pData1 = p_pData1;
	 Type*	l_pData2 = p_pData2;
	 int	l_dim = p_DimData;

	while(l_dim--)
		if(memcmp(l_pData1++, l_pData2++, sizeof(Type)) != 0)
			return false;

	return true;
}


template <class Type> void CContainerTools<Type>::Copy(Type* p_pTo, const Type* p_pFrom, const int p_DimData)
{
	int	l_Idx = 0;
	while(l_Idx < p_DimData) {
		p_pTo[l_Idx] = p_pFrom[l_Idx];
		l_Idx++;
	}
}
